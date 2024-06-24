import os
import signal
import sys
import time
from json import JSONDecodeError
from os import listdir, getenv
from os.path import isfile, join, basename
import json
from re import search
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


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        print('Exiting gracefully')
        self.kill_now = True


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
        if search(f"{dmrpp.processing_regex}", basename(input_file)):
            out_files = dmrpp.dmrpp_generate(input_file, local=True, dmrpp_meta=meta, args=args)
            logger.info(f'Generated: {out_files}')


def handler(event, context):
    # print(f'EVENT: {event}')
    collection = event.get('config').get('collection')
    meta = collection.get('meta', {})
    args = []
    workstation_path = getenv('/efs_test/rssmif17d3d__7', '/usr/share/hyrax/')
    # join_path = lambda x: join(workstation_path, x)
    # input_files = [join_path(f) for f in listdir(workstation_path) if isfile(join_path(f))]

    input_files = []
    local_store = os.getenv('EBS_MNT')
    c_id = f'{collection.get("name")}__{collection.get("version")}'
    collection_store = f'{local_store}/{c_id}'

    with open(f'{collection_store}/{c_id}.json', 'r') as output:
        contents = json.load(output)
        print(f'Granule Count: {len(contents.get("granules"))}')
        granules = {'granules': contents.get('granules')}

    for granule in granules.get('granules'):
        for file in granule.get('files'):
            input_files.append(f'{local_store}/{file.get("name")}')

    print(f'input_files: {input_files}')
    dmrpp = DMRPPGenerator(input=input_files)
    dmrpp.path = local_store
    dmrpp.processing_regex = meta.get('dmrpp_regex', dmrpp.processing_regex)
    for input_file in input_files:
        if search(f"{dmrpp.processing_regex}", basename(input_file)):
            out_files = dmrpp.dmrpp_generate(input_file, local=True, dmrpp_meta=meta, args=args)
            logger.info(f'Generated: {out_files}')
        else:
            logger.info(f'{dmrpp.processing_regex} did not match {input_file}')
    return 0


if __name__ == "__main__":
    print(f'GDG argv: {sys.argv}')
    if len(sys.argv) <= 1:
        killer = GracefulKiller()
        print('GDG Task is running...')
        while not killer.kill_now:
            time.sleep(1)
        print('terminating')
    else:
        print('GDG calling function')
        print(f'argv: {type(sys.argv[1])}')
        print(f'argv: {sys.argv[1]}')
        ret = handler(json.loads(sys.argv[1]), {})

    # main()
    pass
