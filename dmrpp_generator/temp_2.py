import json
import os
import subprocess
from time import sleep
import logging
# logging.basicConfig(
#     format='%(asctime)s %(levelname)-8s %(message)s',
#     level=logging.INFO,
#     datefmt='%Y-%m-%d %H:%M:%S'
# )
#
# logger = logging.getLogger('temp_2.py')
# logger.info('sleeping')
# sleep(3)
# logger.info('slept')
#
# out = subprocess.Popen(['echo', '"sleeping"', '&&', 'sleep', '1'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# logger.info('temp_2.py: post out')
# for line in out.stdout:
#     logger.info(f'temp_2.py: {line.decode().strip()}')


if __name__ == '__main__':
    # json_str = '{"test": true}'
    #
    # a = json.loads(json_str)
    os.environ['ENABLE_SUBPROCESS_LOGGING'] = str(False)
    res = os.getenv('ENABLE_SUBPROCESS_LOGGING', 'False').lower() == 'true'
    # res = bool("something")
    print(type(res))
    print(res)
