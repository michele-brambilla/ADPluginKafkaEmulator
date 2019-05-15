"""
Signal handler to allow to stop the program with SIGINT or SIGTERM (systemd).
"""

import signal

from loggersim import log


class SignalHandler(object):
    _handled_shutdown = None
    do_shutdown = None

    def __init__(self):
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGHUP, self.handle_signal)

    def handle_shutdown(self, ):
        if self._handled_shutdown:
            log.warning('already handled_shutdown')
            return
        self.do_shutdown = True
        self._handled_shutdown = True

    def handle_signal(self, signum, frame):
        log.info('handle_signal: {}'.format(signum))
        self.handle_shutdown()
        if signum == signal.SIGINT:
            log.warning('Simulation did not shut down cleanly.')
