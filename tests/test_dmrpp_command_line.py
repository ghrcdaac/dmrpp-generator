import os
from unittest import TestCase

from dmrpp_generator.main import DMRPPGenerator

class TestDMRPPCommandGeneration(TestCase):
    """
    test DMRPP comand line
    """
    test_fixtures_dir = '/home/worker/build/tests/fixtures/'

    def setUp(self):
        fixture_path = os.path.join(os.path.dirname(__file__), "fixtures")
        self.dmrpp = DMRPPGenerator(input=[], config={}, path=fixture_path)
        return super().setUp()

    def test_1_hdf4(self):
        """
        Testing command generation for hdf4 files
        """
        file_full_path = f'{self.test_fixtures_dir}test_file.hdf4'
        self.assertEqual(
            f'gen_dmrpp_side_car -i {file_full_path} -U -H',
            self.dmrpp.get_dmrpp_command(dmrpp_meta={}, file_full_path=file_full_path)
        )

    def test_2_hdf5(self):
        """
        Testing command generation for hdf5 files
        """
        file_full_path = f'{self.test_fixtures_dir}test_file.hdf5'
        self.assertEqual(
            f'gen_dmrpp_side_car -i {file_full_path} -U',
            self.dmrpp.get_dmrpp_command(dmrpp_meta={}, file_full_path=file_full_path)
        )

    def test_3_matlab_hdf5(self):
        """
        Testing command generation for matlab files
        """
        file_full_path = f'{self.test_fixtures_dir}test_file.matlab.hdf5'
        self.assertEqual(
            f'gen_dmrpp_side_car -i {file_full_path} -U',
            self.dmrpp.get_dmrpp_command(dmrpp_meta={}, file_full_path=file_full_path)
        )

    def test_4_option(self):
        """
        Testing command generation with options
        """
        file_full_path = f'{self.test_fixtures_dir}test_file.matlab.hdf5'
        test_meta = {
            'options': [
                {
                    'flag': '-c'
                }
            ]

        }
        self.assertEqual(
            f'gen_dmrpp_side_car -i {file_full_path} -U -c',
            self.dmrpp.get_dmrpp_command(dmrpp_meta=test_meta, file_full_path=file_full_path)
        )
