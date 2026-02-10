def test_hdf4(fixture_path, dmrpp_cli):
    """
    Testing command generation for hdf4 files
    """
    file_full_path = f'{fixture_path}/test_file.hdf4'
    assert dmrpp_cli.get_dmrpp_command(dmrpp_meta={}, file_full_path=file_full_path) == f'gen_dmrpp_side_car -i {file_full_path} -U -H'

def test_hdf5(fixture_path, dmrpp_cli):
    """
    Testing command generation for hdf5 files
    """
    file_full_path = f'{fixture_path}/test_file.hdf5'
    assert dmrpp_cli.get_dmrpp_command(dmrpp_meta={}, file_full_path=file_full_path) == f'gen_dmrpp_side_car -i {file_full_path} -U'

def test_matlab_hdf5(fixture_path, dmrpp_cli):
    """
    Testing command generation for matlab files
    """
    file_full_path = f'{fixture_path}/test_file.matlab.hdf5'
    assert dmrpp_cli.get_dmrpp_command(dmrpp_meta={}, file_full_path=file_full_path) == f'gen_dmrpp_side_car -i {file_full_path} -U'

def test_option(fixture_path, dmrpp_cli):
    """
    Testing command generation with options
    """
    file_full_path = f'{fixture_path}/test_file.matlab.hdf5'
    test_meta = {
        'options': [
            {
                'flag': '-c'
            }
        ]
    }
    assert dmrpp_cli.get_dmrpp_command(dmrpp_meta=test_meta, file_full_path=file_full_path) == f'gen_dmrpp_side_car -i {file_full_path} -U -c'
