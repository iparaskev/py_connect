from pidevices import ButtonRPiGPIO
from commlib.transports.amqp import (
    Publisher, Subscriber, ConnectionParameters, AMQPConnection)
import time


class Node():
    """Runing node."""

    def __init__(self):
        topic = "button_stop"
        conn_params = ConnectionParameters()
        conn_params.credentials.username = "testuser"
        conn_params.credentials.password = "testuser"
        conn_params.host = "r4a-platform.ddns.net"
        conn_params.port = 5782

        self.dev = ButtonRPiGPIO(button=24,)

        self.publisher = Publisher(conn_params=conn_params,
                                   topic=topic)

    def run(self, freq=1):
        while True:
            #data = dev.read()
            data = 5
            data = {"button": data}
            self.publisher.publish(data)
            time.sleep(1/freq)


def main():
    node = Node()
    node.run()


if __name__ == "__main__":
    main()
