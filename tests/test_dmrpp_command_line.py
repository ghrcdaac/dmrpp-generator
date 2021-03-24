import os
from unittest import TestCase
import json

from dmrpp_generator.dmrpp_command_line import DMRPPCommandLine

class TestDMRPPCommandLine(TestCase):

    def test_1_local(self):
        """
        Testing local no env var
        :return:
        """
        dmrpp = DMRPPCommandLine()
        self.assertEqual('get_dmrpp -b foo -o bar.dmrpp bar', dmrpp.get_command(None, 'foo', 'bar'))

    def test_2_local_m(self):
        """
        Testing local with env var true
        :return:
        """
        os.environ['CREATE_MISSING_CF'] = 'true'
        dmrpp = DMRPPCommandLine()
        self.assertEqual('get_dmrpp -M -b foo -o bar.dmrpp bar', dmrpp.get_command(None, 'foo', 'bar'))

    def test_3_local_no_m(self):
        """
        Testing local with env var false
        :return:
        """
        os.environ['CREATE_MISSING_CF'] = 'false'
        dmrpp = DMRPPCommandLine()
        self.assertEqual('get_dmrpp -b foo -o bar.dmrpp bar', dmrpp.get_command(None, 'foo', 'bar'))

    def test_4_local_m(self):
        """
        Testing local with env var 1
        :return:
        """
        os.environ['CREATE_MISSING_CF'] = '1'
        dmrpp = DMRPPCommandLine()
        self.assertEqual('get_dmrpp -M -b foo -o bar.dmrpp bar', dmrpp.get_command(None, 'foo', 'bar'))

    def test_5_cumulus_no_meta_config(self):
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
        dmrpp = DMRPPCommandLine()
        self.assertEqual('get_dmrpp -b foo -o bar.dmrpp bar', dmrpp.get_command(config, 'foo', 'bar'))

    def test_6_cumulus_no_dmrpp_config(self):
        """
        Testing cumulus no config 1
        :return:
        """

        config = """
        {
            "config": {
                "meta": {
                }              
            }
        }
        """
        dmrpp = DMRPPCommandLine()
        self.assertEqual('get_dmrpp -b foo -o bar.dmrpp bar', dmrpp.get_command(config, 'foo', 'bar'))

    def test_7_cumulus_m(self):
        """
        Testing cumulus true
        :return:
        """
        config = """
        {
            "config": {
                "meta": {
                    "dmrpp": {
                        "create_missing_cf" : true    
                    }
                }
            }
        }
        """
        dmrpp = DMRPPCommandLine()
        self.assertEqual('get_dmrpp -M -b foo -o bar.dmrpp bar', dmrpp.get_command(config, 'foo', 'bar'))

    def test_8_cumulus_m_false(self):
        """
        Testing cumulus false
        :return:
        """
        config = """
        {
            "config": {
                "meta": {
                    "dmrpp": {
                        "create_missing_cf" : false    
                    }
                }
            }
        }
        """
        dmrpp = DMRPPCommandLine()
        self.assertEqual('get_dmrpp -b foo -o bar.dmrpp bar', dmrpp.get_command(config, 'foo', 'bar'))
    
    def test_9_cumulus_no_m(self):
        """
        Testing cumulus no explicit config
        :return:
        """
        config = """
        {
            "config": {
                "meta": {
                    "dmrpp": {
                    }
                }
            }
        }
        """
        dmrpp = DMRPPCommandLine()
        self.assertEqual('get_dmrpp -b foo -o bar.dmrpp bar', dmrpp.get_command(config, 'foo', 'bar'))

