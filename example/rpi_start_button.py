#from pidevices import ButtonRPiGPIO
from commlib.transports.amqp import Publisher, ConnectionParameters
import time
import random


class Node():
    """Runing node."""

    def __init__(self):
        topic = "button_start"
        conn_params = ConnectionParameters()
        conn_params.credentials.username = "testuser"
        conn_params.credentials.password = "testuser"
        conn_params.host = "r4a-platform.ddns.net"
        conn_params.port = 5782

        #self.dev = ButtonRPiGPIO(button=23,)

        self.publisher = Publisher(conn_params=conn_params,
                                   topic=topic)

    def run(self, freq=1):
        t_s = time.time()
        while True:
            #data = dev.read()
            #data = random.randint(3, 20)
            data = 0
            if time.time() - t_s > 5 and time.time() - t_s < 6:
                data = 1
                print("Start")
            data = {"button": data}
            self.publisher.publish(data)
            time.sleep(1/freq)


def main():
    node = Node()
    node.run()


if __name__ == "__main__":
    main()
