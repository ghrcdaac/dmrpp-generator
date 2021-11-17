import os
from unittest import TestCase

from dmrpp_generator.main import DMRPPGenerator

class TestDMRPPCommandLine(TestCase):

    dmrpp = DMRPPGenerator(input=[], config={})
    def test_1_local(self):
        """
        Testing local no env var
        :return:
        """
        self.assertEqual('get_dmrpp -b foo -o bar.dmrpp bar', self.dmrpp.get_dmrpp_command({}, 'foo', 'bar'))

    def test_2_local_m(self):
        """
        Testing local with env var true
        :return:
        """

        meta = {'options': [{'flag': '-M'}]}
        self.assertEqual('get_dmrpp -M -b foo -o bar.dmrpp bar', self.dmrpp.get_dmrpp_command(dmrpp_meta=meta,
                                                                                              input_path='foo',
                                                                                              output_filename='bar'))

    def test_3_local_no_m(self):
        """
        Testing local with env var false
        :return:
        """
        meta = {'options': []}
        self.assertEqual('get_dmrpp -b foo -o bar.dmrpp bar', self.dmrpp.get_dmrpp_command(meta, 'foo', 'bar'))

    def test_4_local_m(self):
        """
        Testing local with env var 1
        :return:
        """
        meta = {'options': [{'flag': '-M'}]}
        self.assertEqual('get_dmrpp -M -b foo -o bar.dmrpp bar', self.dmrpp.get_dmrpp_command(meta, 'foo', 'bar'))

    def test_5_cumulus_no_meta_config(self):
        """
        Testing cumulus no config 1
        :return:
        """

        self.assertEqual('get_dmrpp -b foo -o bar.dmrpp bar', self.dmrpp.get_dmrpp_command({}, 'foo', 'bar'))


    def test_6_cumulus_m(self):
        """
        Testing cumulus true
        :return:
        """
        dmrpp_meta = {'options': [{'flag': '-M'}]}
        self.assertEqual('get_dmrpp -M -b foo -o bar.dmrpp bar', self.dmrpp.get_dmrpp_command(dmrpp_meta, 'foo', 'bar'))


    def test_7_cumulus_adding_wrongval(self):
        """
        Testing dmrpp ignoring wrong value
        :return:
        """
        dmrpp_meta = {
            "create_missing_cf": "foobar"
        }
        self.assertEqual('get_dmrpp -b foo -o bar.dmrpp bar', self.dmrpp.get_dmrpp_command(dmrpp_meta, 'foo', 'bar'))
