import json
import os
import sys
import tempfile
from json import JSONDecodeError
from os import getenv
from time import sleep


def try_json_decode(key, required_type):
    print(f'getting os_var: {key}')
    os_var = getenv(key, str(required_type))
    print(os_var)
    try:
        os_var = json.loads(os_var)
        if type(os_var) is not type(required_type):
            raise ValueError(
                f'Incorrect JSON string format. Found {type(os_var).__name__} but a json {type(required_type).__name__}'
                f' is required.'
            )
    except JSONDecodeError:
        print(f'Environment variable {key} was not a valid json string.')
        print(f'Value: {os_var}')
        print('Required Format: \'{{"key": "value"}}\'')
        raise

    return os_var


def read_manifest(manifest):
    with open(manifest, 'r+') as manifest_file:
        manifest_lines = manifest_file.readlines()

    done = False
    while not done:
        dir_files = os.listdir()
        for line in manifest_lines:
            if line in dir_files:
                done = True
                continue
            else:
                done = False
                sleep(5)
                break




if __name__ == '__main__':
    read_manifest('temp.txt')
    # try_json_decode('PAYLOAD', {})
