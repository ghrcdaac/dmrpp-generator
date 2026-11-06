"""Module for signal-based graceful shutdown."""

import json
import signal
import sys
import time
from types import FrameType

from .main import main


class GracefulKiller:
    """Class for graceful shutdown."""

    kill_now = False

    def __init__(self):
        """Initialize signals."""
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum: int, frame: FrameType | None) -> None:
        """Exit upon interrupt or terminate.
        :param signum: Received signal.
        :param frame: Interrupted stack frame object.
        """
        print("Exiting gracefully")
        self.kill_now = True


if __name__ == "__main__":
    print(f"DMR++ argv: {sys.argv}")
    if len(sys.argv) <= 1:
        killer = GracefulKiller()
        print("DMR++ Task is running...")
        while not killer.kill_now:
            time.sleep(1)
        print("Terminating")
    else:
        print("DMR++ calling function")
        print(f"argv: {type(sys.argv[1])}")
        print(f"argv: {sys.argv[1]}")
        main(json.loads(sys.argv[1]), {})
