from json import JSONDecodeError
from os import listdir, getenv
from os.path import isfile, join, basename
import json
from re import match
import logging
from dmrpp_generator.main import DMRPPGenerator
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()


def try_json_decode(key, required_type):
    logger.info(f'getting os_var: {key}')
    os_var = getenv(key, required_type)
    try:
        os_var = json.loads(os_var)
        if type(os_var) is not type(required_type):
            raise ValueError(
                f'Incorrect JSON string format. Found {type(os_var).__name__} but a json {type(required_type).__name__}'
                f' is required.'
            )
    except JSONDecodeError:
        logger.info(f'Environment variable {key} was not a valid json string.')
        logger.info(f'Value: {os_var}')
        logger.info('Required Format: \'{{"key": "value"}}\'')
        raise

    return os_var


def main():
    meta = try_json_decode('PAYLOAD', {})
    args = try_json_decode('DMRPP_ARGS', [])
    workstation_path = getenv('MOUNT_VOL', '/usr/share/hyrax/')
    join_path = lambda x: join(workstation_path, x)
    input_files = [join_path(f) for f in listdir(workstation_path) if isfile(join_path(f))]
    dmrpp = DMRPPGenerator(input=input_files)
    dmrpp.path = workstation_path
    dmrpp.processing_regex = meta.get('dmrpp_regex', dmrpp.processing_regex)
    for input_file in input_files:
        if match(f"{dmrpp.processing_regex}$", basename(input_file)):
            out_files = dmrpp.dmrpp_generate(input_file, local=True, dmrpp_meta=meta, args=args)
            logger.info(f'Generated: {out_files}')


if __name__ == "__main__":
    main()
    pass
