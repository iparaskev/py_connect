from pidevices import HcSr04RPiGPIO
import time
from commlib.transports.amqp import Publisher, ConnectionParameters
import random


class Node():
    """Runing node."""

    def __init__(self):
        topic = "sonar_left.front"
        conn_params = ConnectionParameters()
        conn_params.credentials.username = "testuser"
        conn_params.credentials.password = "testuser"
        conn_params.host = "r4a-platform.ddns.net"
        conn_params.port = 5782

        self.dev = HcSr04RPiGPIO(echo=27, trigger=17,)

        self.publisher = Publisher(conn_params=conn_params,
                                   topic=topic)

    def run(self, freq=1):
        while True:
            data = self.dev.read()
            data = {"distance": data}
            self.publisher.publish(data)
            time.sleep(1/freq)


def main():
    node = Node()
    node.run()


if __name__ == "__main__":
    main()
