import getpass
import json
import os
import re
import subprocess
import tempfile
from time import sleep


def print_log(log):
    print(log)

def processes():
    p1 = subprocess.Popen(
        f'python {os.path.dirname(os.path.realpath(__file__))}/temp_1.py process_1 3', stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, shell=True
    )

    p2 = subprocess.Popen(
        f'python {os.path.dirname(os.path.realpath(__file__))}/temp_1.py process_2 8', stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, shell=True
    )
    processes = [p1, p2]

    while True:
        for process in processes:
            line = process.stdout.readline()
            if not line:
                break
            print(line)





if __name__ == '__main__':
    pass
    # res1 = os.stat('/home/michael/dmrpp-generator/setup.py')
    # sleep(1)
    # res2 = os.stat('/home/michael/dmrpp-generator/setup.py')
    # file_list = os.listdir()
    # file_list.sort()
    # manifest = tempfile.mkstemp(prefix='manifest-', suffix='.in', dir=tempfile.gettempdir(), text=True)
    # print(manifest[-1])



    # temp_dir = tempfile.TemporaryDirectory(prefix='dmrpp-generator-')
    # print(temp_dir.name)
    # temp = "{}"
    # temp = json.loads(temp)
    # print(type(temp))
    # processes()
    # staging_dir = f'{tempfile.gettempdir()}/dmrpp_staging'
    # if os.path.isdir(staging_dir):
    #     os.rmdir(staging_dir)
    # temp_dir = os.mkdir(staging_dir)
    # print(os.path.isdir(staging_dir))
    # res = subprocess.check_output(['conda', 'env', 'list'])
    # # print(res.decode().split('\n'))
    # for line in res.decode().split('\n'):
    #     if line.startswith('#'):
    #         continue
    #     g = re.search('\w+', line)
    #     if g:
    #         g = g.group()
    #     else:
    #         continue
    #     if g == 'base':
    #         continue
    #     res = subprocess.check_output(['conda', 'env', 'remove', '--name', g])
    #     print(res.decode())
