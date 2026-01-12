import pytest
import os
import json
from dmrpp_generator.main import DMRPPGenerator

@pytest.fixture(scope='session')
def fixture_path():
    return os.path.join(os.path.dirname(__file__), 'fixtures')

@pytest.fixture(scope='session')
def granule_id():
    return 'ISS_LIS_BG_V3.0_20170702_000346_FIN'

@pytest.fixture(scope='module')
def config_data(fixture_path):
    with open(os.path.join(fixture_path, 'payload.json'), encoding='UTF-8') as fle:
        return json.load(fle)['config']


@pytest.fixture(scope='module')
def payload_rp_data():
    return {
        "requester_pay": True,
        "options": []
    }

@pytest.fixture
def process_factory(granule_id, config_data, fixture_path):
    def _make_instance(filename):
        input_file = {
            "granules": [
                {
                    "granuleId": granule_id,
                    "sync_granule_duration": 3759,
                    "files": [
                    {
                        "bucket": "fake-cumulus-protected",
                        "checksum": "aa5204f125ae83847b3b80fa2e571b00",
                        "checksumType": "md5",
                        "fileName": filename,
                        "key": f"fakepath/2020/001/{filename}",
                        "size": 18232098,
                        "type": "data",
                    },
                    {
                        "bucket": "fake-cumulus-public",
                        "fileName": f"{filename}.md5",
                        "key": f"fakepath/2020/001/{filename}.md5",
                        "size": 98,
                        "type": "metadata",
                    },
                    {
                        "bucket": "fake-cumulus-public",
                        "fileName": f"{filename}.cmr.json",
                        "key": f"{filename}.cmr.json",
                        "size": 1381,
                        "type": "metadata",
                    }
                    ],
                    "version": "2019.0"
                }
            ]
        }
        return DMRPPGenerator(input=input_file, config=config_data, path=fixture_path)
    
    return _make_instance

@pytest.fixture(scope='session')
def dmrpp_cli(fixture_path):
    return DMRPPGenerator(input=[], config={}, path=fixture_path)