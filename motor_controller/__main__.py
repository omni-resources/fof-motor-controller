"""Main module to control the fan motors in the fans of fury game."""

import time
import sys
import signal
import configparser
import logging

from gpiocrust import Header, PinMode

from .web_socket_handler import WebSocketHandler

cfg = configparser.ConfigParser()
cfg.read('config.ini')

logging.basicConfig(level=logging.DEBUG)

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    def sigterm_handler(signum, frame):
        logging.info('GAME: received sigterm')
        socket.server_socket.close()
        sys.exit()

    signal.signal(signal.SIGTERM, sigterm_handler)

    # Loop for REAL forever
    logging.debug('SOCKET: Connecting to websocket server...')
    while 1:
        try:
            with Header(mode=PinMode.BCM) as header:
                with WebSocketHandler(cfg) as socket:
                    socket.run()
        except KeyboardInterrupt:
            logging.info('GAME: received keyboard interrupt.')
            socket.server_socket.close()
            sys.exit()
        except:
            exception = sys.exc_info()[1]
            logging.error(exception)
            logging.error('SOCKET: Reconnecting...')
            time.sleep(20)

if __name__ == "__main__":
    main()