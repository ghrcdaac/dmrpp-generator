import ast
from os import listdir, getenv
from os.path import isfile, join, basename
import json
from re import match
import logging
from dmrpp_generator.main import DMRPPGenerator
logging.getLogger()

if __name__ == "__main__":
    payload = getenv('PAYLOAD', '{}')
    args = json.loads(getenv('DMRPP_ARGS', '[]'))
    meta = json.loads(payload)
    workstation_path = getenv('MOUNT_VOL', '/usr/share/hyrax/')
    join_path = lambda x: join(workstation_path, x)
    input_files = [join_path(f) for f in listdir(workstation_path) if isfile(join_path(f))]
    dmrpp = DMRPPGenerator(input=input_files)
    dmrpp.path = workstation_path
    dmrpp.processing_regex = meta.get('dmrpp_regex', dmrpp.processing_regex)
    for input_file in input_files:
        if match(f"{dmrpp.processing_regex}$", basename(input_file)):
            dmrpp.dmrpp_generate(input_file, local=True, dmrpp_meta=meta, args=args)

