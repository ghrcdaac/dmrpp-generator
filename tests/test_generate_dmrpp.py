import pytest
import os

class TestDMRPPFileGeneration:
    
    def test_generate_dmrpp_success(self, mocker, process_factory, granule_id):
        """
        Combined logic of original test_1, test_2, and test_3.
        Tests successful generation and output schema.
        """
        # Create DMRPP generator instance with for .nc file
        granule_name = f"{granule_id}.nc"
        process_instance = process_factory(granule_name)

        # Mocks
        mocker.patch('dmrpp_generator.main.DMRPPGenerator.upload_file_to_s3',
                     return_value={granule_id: f's3://{granule_name}.dmrpp'})
        mocker.patch('cumulus_process.Process.fetch_all',
                     return_value={'input_key': [os.path.join(process_instance.path, granule_name)]})
        mocker.patch('os.remove', return_value=granule_name)
        mocker.patch('cumulus_process.s3.download', return_value=f'{process_instance.path}/{granule_name}')

        # Process granule
        output = process_instance.process()

        # Check file existence
        expected_file_path = f'{process_instance.path}/{granule_name}.dmrpp'
        assert os.path.exists(expected_file_path) == 1

        # Check output schema
        assert list(output.keys()) == ['granules']

        # Check DMRPP file existence in output
        dmrpp_file = f'{granule_name}.dmrpp'
        dmrpp_exists = any(
            file['fileName'] == dmrpp_file 
            for granule in output.get('granules', []) 
            for file in granule.get('files', [])
        )
        assert dmrpp_exists is True

    def test_fail_on_no_matching_regex(self, mocker, process_factory, granule_id):
        """
        Original test_6: Specifically tests the regex failure using an .hdf extension.
        """
        # Create DMRPP generator instance with for .hdf file
        hdf_name = f"{granule_id}.hdf"
        process_instance = process_factory(hdf_name)

        # Mocks
        mocker.patch('dmrpp_generator.main.DMRPPGenerator.upload_file_to_s3',
                     return_value={granule_id: f's3://{hdf_name}.dmrpp'})
        mocker.patch('cumulus_process.Process.fetch_all',
                     return_value={'input_key': [os.path.join(process_instance.path, hdf_name)]})
        mocker.patch('os.remove', return_value=hdf_name)
        mocker.patch('cumulus_process.s3.download', return_value=f'{process_instance.path}/{hdf_name}')

        # Check regex failure
        with pytest.raises(Exception) as exception_test:
            process_instance.process()
        
        assert str(exception_test.value) == f"File '{hdf_name}_mvs.h5' does not match any file regex defined within the collection definition."

    def test_s3_extra_requester_pay_default(self, process_factory, granule_id):
        process_instance = process_factory(f'{granule_id}.nc')
        extra_dict = process_instance._get_s3_extra()
        assert not bool(extra_dict)

    def test_s3_extra_requester_pay_enabled(self, mocker, process_factory, granule_id, payload_rp_data):
        process_instance = process_factory(f'{granule_id}.nc')
        mocker.patch.dict(process_instance.dmrpp_meta,
                          payload_rp_data,
                          clear=True)
        extra_dict = process_instance._get_s3_extra()
        assert bool(extra_dict) and extra_dict['RequestPayer'] == 'requester'