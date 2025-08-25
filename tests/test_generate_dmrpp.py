import os
from unittest import TestCase
from unittest.mock import patch
import json
from dmrpp_generator.main import DMRPPGenerator

class StorageValues:
    """
    storage values
    """
    processing_output = None


class TestDMRPPFileGeneration(TestCase):
    """
    Test generating dmrpp files.
    """
    granule_id = "f16_ssmis_20231011v7"
    granule_name = "f16_ssmis_20231011v7.nc"
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures")
    input_file = {
        "granules": [
            {
                "granuleId": granule_id,
                "dataType": "rssmif16d",
                "sync_granule_duration": 3759,
                "files": [
                  {
                    "bucket": "fake-cumulus-protected",
                    "checksum": "aa5204f125ae83847b3b80fa2e571b00",
                    "checksumType": "md5",
                    "fileName": granule_name,
                    "key": f"fakepath/2020/001/{granule_name}",
                    "size": 18232098,
                    "type": "data",
                  },
                  {
                    "bucket": "fake-cumulus-public",
                    "fileName": f"{granule_name}.md5",
                    "key": "fakepath/2020/001/{granule_name}.md5",
                    "size": 98,
                    "type": "metadata",
                  },
                  {
                    "bucket": "fake-cumulus-public",
                    "fileName": f"{granule_name}.cmr.json",
                    "key": f"{granule_name}.cmr.json",
                    "size": 1381,
                    "type": "metadata",
                  }
                ],
                "version": "2019.0"
            }
        ]
    }

    payload_file = f"{fixture_path}/payload.json"
    with open(payload_file, encoding='UTF-8') as fle:
        payload = json.load(fle)
    payload_data = payload

    payload_rp_file = f"{fixture_path}/payload_requester_pay.json"
    with open(payload_rp_file, encoding='UTF-8') as fle:
        payload_rp = json.load(fle)
    payload_rp_data = payload_rp

    process_instance = DMRPPGenerator(input=input_file, config=payload_data['config'], path=fixture_path)
    process_instance.path = fixture_path

    @patch('dmrpp_generator.main.DMRPPGenerator.upload_file_to_s3',
       return_value={granule_id:f's3://{granule_name}.dmrpp'})
    @patch('cumulus_process.Process.fetch_all',
       return_value={'input_key': [os.path.join(os.path.dirname(__file__), f"fixtures/{granule_name}")]})
    @patch('os.remove', return_value=granule_name)
    @patch('cumulus_process.s3.download', return_value=f"{process_instance.path}/{granule_name}")
    def test_1_check_generate_dmrpp(self, mock_upload, mock_fetch, mock_remove, mock_download):
        """
        Testing get correct start date
        :return:
        """
        _ = mock_upload, mock_fetch, mock_remove, mock_download

        StorageValues.processing_output = self.process_instance.process()
        expected_file_path = f"{self.process_instance.path}/{self.granule_name}.dmrpp"
        self.assertEqual(os.path.exists(expected_file_path), 1)

    def test_2_check_output(self):
        """
        Test the putput schema of the processnig
        :return:
        """
        self.assertListEqual(['granules'], list(StorageValues.processing_output.keys()))

    def test_3_checkout_dmrpp_output(self):
        dmrpp_file = f"{self.granule_name}.dmrpp"
        dmrpp_exists = False
        for granules in StorageValues.processing_output.get('granules'):
            for file in granules.get('files'):
                if file["fileName"] == dmrpp_file:
                    dmrpp_exists = True
        self.assertEqual(True, dmrpp_exists)

    def test_4_s3_extra_requester_pay_default(self):
        extra_dict = self.process_instance._get_s3_extra()
        assert not bool(extra_dict)

    def test_5_s3_extra_requester_pay_enabled(self):
        with patch.dict(self.process_instance.dmrpp_meta,
                        self.payload_rp_data['config']['collection']['meta']['dmrpp'],
                        clear=True):
            extra_dict = self.process_instance._get_s3_extra()
            assert bool(extra_dict) and extra_dict['RequestPayer'] == 'requester'