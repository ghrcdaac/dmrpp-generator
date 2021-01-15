import os
from unittest import TestCase
import json
from dmrpp_generator.main import DMRPPGenerator
from unittest.mock import patch

class StorageValues:
    processing_output = None


class TestDMRPPFileGeneration(TestCase):
    """
    Test generating dmrpp files.
    """
    granule_name = "tpw_v07r01_201910.nc"
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures")
    input_file = [f"{fixture_path}/{granule_name}"]
    payload_file = f"{fixture_path}/payload.json"
    with open(payload_file) as f:
        payload = json.load(f)

    process_instance = DMRPPGenerator(input = input_file, config=payload['config'], path=fixture_path)

    @patch('cumulus_process.Process.upload_output_files',
       return_value=[f's3://{granule_name}',
                     f's3://{granule_name}.dmrpp'])
    @patch('cumulus_process.Process.fetch_all',
       return_value={'input_key': [os.path.join(os.path.dirname(__file__), f"fixtures/{granule_name}")]})
    @patch('os.remove', return_value=granule_name)
    def test_1_check_generate_dmrpp(self, mock_upload, mock_fetch, mock_remove):
        """
        Testing get correct start date
        :return:
        """
        StorageValues.processing_output = self.process_instance.process()
        expected_file_path = f"{self.process_instance.path}/{self.granule_name}.dmrpp"
        self.assertEqual(os.path.exists(expected_file_path), 1)

    def test_2_check_output(self):
        """
        Test the putput schema of the processing
        :return:
        """
        print(StorageValues.processing_output)
        self.assertListEqual(['granules', 'input'], list(StorageValues.processing_output.keys()))
