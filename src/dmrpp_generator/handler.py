import json
import signal
import sys
import time

from dmrpp_generator.main import main


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        print('Exiting gracefully')
        self.kill_now = True


if __name__ == "__main__":
    print(f'DMR++ argv: {sys.argv}')
    if len(sys.argv) <= 1:
        killer = GracefulKiller()
        print('DMR++ Task is running...')
        while not killer.kill_now:
            time.sleep(1)
        print('terminating')
    else:
        print('DMR++ calling function')
        print(f'argv: {type(sys.argv[1])}')
        print(f'argv: {sys.argv[1]}')
        main(json.loads(sys.argv[1]), {})
