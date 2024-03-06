import os
import subprocess
import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger('temp.py')
cmd = 'python'
target = '/home/michael/dmrpp-generator/dmrpp_generator/temp_2.py'

logger.info(os.getcwd())
out = subprocess.Popen([cmd, target], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
logger.info('temp.py post out')
for line in out.stdout:
    logger.info(f'temp.py: {line.decode().strip()}')
