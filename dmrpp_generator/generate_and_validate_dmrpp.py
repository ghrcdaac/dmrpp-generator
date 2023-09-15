#! /usr/bin/python3
import argparse
import json
import subprocess
import os
from multiprocessing import Process
import tempfile


def generate_docker_compose():
    _, dockercompose_file_location = tempfile.mkstemp(suffix=".yml")
    with open(dockercompose_file_location, 'w', encoding="utf-8") as dockercompose_file:
        dockercompose_file.write(
            """
version: '3'
services:
  dmrpp:
    image: mlh/dmrpp:latest
    environment:
      - PAYLOAD=${PAYLOAD}
      - DMRPP_ARGS=${DMRPP_ARGS}
    # Mount volume
    volumes:
      - ${NC_FILES_PATH:-/tmp}:/usr/share/hyrax

  hyrax:
    image: opendap/hyrax:snapshot
    ports:
    - "${PORT:-8080}:8080"
    volumes:
      - ${NC_FILES_PATH:-/tmp}:/usr/share/hyrax/
    working_dir: /usr/share/hyrax
    container_name: hyrax
            """
        )
    return dockercompose_file_location


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
    dockercompose_file_location = generate_docker_compose()
    dkr_comp_version = check_docker_version(log_file_path)

    with open(log_file_path, "a", encoding='utf-8') as output:
        try:
            cmd = f"PAYLOAD='{payload}' " \
                  f"DMRPP_ARGS='{dmrpp_args}' " \
                  f"NC_FILES_PATH={nc_hdf_path} " \
                  f"PORT={port} {dkr_comp_version} " \
                  f"-f {dockercompose_file_location} up {dmrrpp_service}"
            subprocess.run(
                cmd,
                shell=True, check=False, stdout=output,
                stderr=output)
        except KeyboardInterrupt:
            cmd = f" {dkr_comp_version} -f {dockercompose_file_location} down {dmrrpp_service}"
            subprocess.run(cmd, shell=True, check=False, stdout=output, stderr=output)
            os.remove(dockercompose_file_location)


def main():
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
                             'If not set, will check for PAYLOAD environment variable, or default to \'{}\'')
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

    if validate:
        dmrrpp_service = ''
        visit_link_path_message = f'http://localhost:{port}/opendap (^C to kill the server)'
        message_visit_server = f'Results served at : {visit_link_path_message}'
        print(message_visit_server)
    else:
        dmrrpp_service = 'dmrpp'

    try:
        docker_compose = Process(
            target=run_docker_compose,
            args=(payload, unknown, nc_hdf_path, port, dmrrpp_service, log_file_location)
        )
        docker_compose.start()
        docker_compose.join()
    except KeyboardInterrupt:
        print("\nShutting down the server...")


if __name__ == "__main__":
    main()
