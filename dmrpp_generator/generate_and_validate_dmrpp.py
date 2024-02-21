#! /usr/bin/python3
import argparse
import json
import subprocess
import os
import tempfile
from time import sleep

from dmrpp_generator import version


def check_docker_version(log_file_path):
    with open(log_file_path, "a+", encoding='utf-8') as output:
        dkr_comp_version = 'docker compose'
        cmd = f"{dkr_comp_version} version"
        subprocess.run(cmd, shell=True, check=False, stdout=output, stderr=output)
        output.seek(0)
        err_grab = output.readlines()[-1]
        if err_grab == f'/bin/sh: 1: {dkr_comp_version}: not found\n':
            dkr_comp_version = 'docker-compose'
    return dkr_comp_version


def run_docker_compose(payload, dmrpp_args, nc_hdf_path, port, dmrrpp_service, log_file_path):
    docker_compose = f'{os.path.dirname(os.path.realpath(__file__))}/docker-compose.yml'
    dkr_comp_version = check_docker_version(log_file_path)
    os.environ['DMRPP_VERSION'] = version.__version__
    with open(log_file_path, "r+", encoding='utf-8') as output:
        try:
            cmd = f"PAYLOAD='{payload}' " \
                  f"DMRPP_ARGS='{dmrpp_args}' " \
                  f"NC_FILES_PATH={nc_hdf_path} " \
                  f"PORT={port} " \
                  f"{dkr_comp_version} -f {docker_compose} up {dmrrpp_service}"
            print(cmd)
            compose_ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            for line in compose_ps.stdout:
                line = line.decode().strip()
                output.write(f'{line}\n')
                print(line)

        except KeyboardInterrupt:
            print('\nShutting down the Hyrax server. Please wait...')
            cmd = f" {dkr_comp_version} -f {docker_compose} down {dmrrpp_service}"
            subprocess.run(cmd, shell=True, check=False, stdout=output, stderr=output)


def main():
    print(f'dmrpp {version.__version__}\n')
    parser = argparse.ArgumentParser(
        description='Generate and validate DMRPP files. Any DMR++ commandline option can be provided in addition to'
                    ' the options listed below. To see what options are available check the documentation: '
                    'https://docs.opendap.org/index.php?title=DMR%2B%2B#Command_line_options'
    )
    parser.add_argument('-p', '--path', dest='nc_hdf_path', required=True,
                        help='Path to netCDF4 and HDF5 folder')
    parser.add_argument('-prt', '--port', dest='port', default="8080",
                        help='Port number to Hyrax local server')
    parser.add_argument('-pyld', '--payload', dest='payload', default=os.getenv('PAYLOAD', '{}'),
                        help='Payload to pass to the besd get_dmrpp call. '
                             'If not set, will check for PAYLOAD environment variable, or default to \'{}\''
                             'The value should be a json dictionary string \'{"key": "value"}\'')
    parser.add_argument('--validate', action='store_true',
                        help='Validate netCDF4 and HDF5 files against OPeNDAP local server. '
                             'This is the default behavior')
    parser.add_argument('--no-validate', dest='validate', action='store_false',
                        help='Do not validate netCDF4 and HDF5 files against OPeNDAP local server. '
                             'The default behavior is --validate.')
    parser.set_defaults(validate=True)

    args, unknown = parser.parse_known_args()
    unknown = json.dumps(unknown)
    nc_hdf_path, port, payload, validate = [getattr(args, ele) for ele in vars(args)]
    log_file_location = tempfile.mkstemp(prefix='dmrpp-generator-')[1]
    print(f'Log file: {log_file_location}')

    dmrrpp_service = 'dmrpp-generator'
    if validate:
        dmrrpp_service = ''
        visit_link_path_message = f'http://localhost:{port}/opendap (^C to kill the server)'
        message_visit_server = f'Results served at : {visit_link_path_message}'
        print(message_visit_server)
        sleep(2)

    run_docker_compose(payload, unknown, nc_hdf_path, port, dmrrpp_service, log_file_location)


if __name__ == "__main__":
    main()
