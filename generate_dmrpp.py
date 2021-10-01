from os import listdir, getenv
from os.path import isfile, join, basename
from dmrpp_generator.main import DMRPPGenerator
from re import match
import logging
import json
logging.getLogger()
if __name__ == "__main__":
    payload = getenv('PAYLOAD', '{}')
    meta = json.loads(payload)
    workstation_path  = getenv('MOUNT_VOL', '/usr/share/hyrax/')
    join_path = lambda x: join(workstation_path, x)
    input_files = [join_path(f) for f in listdir(workstation_path) if isfile(join_path(f))]
    dmrpp = DMRPPGenerator(input=input_files)
    dmrpp.path = workstation_path
    [dmrpp.dmrpp_generate(input_file, local=True, dmrpp_meta=meta) for input_file in input_files if match(f"{dmrpp.processing_regex}$",
                                                                                         basename(input_file))]
