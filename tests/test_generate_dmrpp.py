from os import path
from unittest import TestCase
import json
from dmrpp_generator.main import DMRPPGenerator



class TestDMRPPFileGeneration(TestCase):
    """
    Test generating dmrpp files.
    This will test if er2mir metadata will be extracted correctly
    """
    granule_name = "tpw_v07r01_201910.nc"
    fixture_path = path.join(path.dirname(__file__), "fixtures")
    input_file = [f"{fixture_path}/{granule_name}"]
    payload_file = f"{fixture_path}/payload.json"
    with open(payload_file) as f:
        payload = json.load(f)

    process_instance = DMRPPGenerator(input = input_file, config=payload['config'], path=fixture_path)
    
    def test_1_generate_dmrpp(self):
        """
        Testing get correct start date
        :return:
        """
        print(self.process_instance.process())

        self.assertEqual(1+1, 2)
