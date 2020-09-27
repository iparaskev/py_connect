#from pidevices import HcSr04RPiGPIO
from commlib.transports.amqp import Publisher, ConnectionParameters
import time
import random


class Node():
    """Runing node."""

    def __init__(self):
        topic = "sonar_front.distance"
        conn_params = ConnectionParameters()
        conn_params.credentials.username = "testuser"
        conn_params.credentials.password = "testuser"
        conn_params.host = "r4a-platform.ddns.net"
        conn_params.port = 5782

        #self.dev = HcSr04RPiGPIO(echo=10, trigger=9,)

        self.publisher = Publisher(conn_params=conn_params,
                                   topic=topic)

    def run(self, freq=1):
        while True:
            #data = dev.read()
            data = random.randint(3, 20)
            data = {"distance": data}
            print(f"Fornt: {data}")
            self.publisher.publish(data)
            time.sleep(1/freq)


def main():
    node = Node()
    node.run()


if __name__ == "__main__":
    main()
