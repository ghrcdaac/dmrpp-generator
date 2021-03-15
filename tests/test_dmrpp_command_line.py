import os
from unittest import TestCase
import json
from dmrpp_generator.dmrpp_command_line import DMRPPCommandLine
from unittest.mock import patch


class TestDMRPPCommandLine(TestCase):

    def test_1_local(self):
        """
        Testing local no env var
        :return:
        """
        dmrpp = DMRPPCommandLine(None)
        self.assertEqual('get_dmrpp -b', dmrpp.get_command())

    def test_2_local_m(self):
        """
        Testing local with env var true
        :return:
        """
        os.environ['CREATE_MISSING_CF'] = 'true'
        dmrpp = DMRPPCommandLine(None)
        self.assertEqual('get_dmrpp -M -b', dmrpp.get_command())

    def test_3_local_no_m(self):
        """
        Testing local with env var false
        :return:
        """
        os.environ['CREATE_MISSING_CF'] = 'false'
        dmrpp = DMRPPCommandLine(None)
        self.assertEqual('get_dmrpp -b', dmrpp.get_command())

    def test_4_cumulus_no_dmrpp_config(self):
        """
        Testing cumulus no config 1
        :return:
        """

        config = """
        {
            "config": {
                
            }
        }
        """
        dmrpp = DMRPPCommandLine(config)
        self.assertEqual('get_dmrpp -b', dmrpp.get_command())

    def test_5_cumulus_m(self):
        """
        Testing local with env var true
        :return:
        """
        config = """
        {
            "config": {
                "dmrpp": {
                    "create_missing_cf" : true    
                }
            }
        }
        """
        dmrpp = DMRPPCommandLine(config)
        self.assertEqual('get_dmrpp -M -b', dmrpp.get_command())

    def test_6_cumulus_m_false(self):
        """
        Testing local with env var false
        :return:
        """
        #del os.environ['CREATE_MISSING_CF']
        config = """
        {
            "config": {
                "dmrpp": {
                    "create_missing_cf" : false    
                }
            }
        }
        """
        dmrpp = DMRPPCommandLine(config)
        self.assertEqual('get_dmrpp -b', dmrpp.get_command())
    
    def test_7_cumulus_no_m(self):
        """
        Testing local with env var false
        :return:
        """
        config = """
        {
            "config": {
                "dmrpp": {
                }
            }
        }
        """
        dmrpp = DMRPPCommandLine(config)
        self.assertEqual('get_dmrpp -b', dmrpp.get_command())

