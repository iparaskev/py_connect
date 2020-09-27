from pidevices import DfrobotMotorController
import time

from commlib.transports.amqp import Subscriber, ConnectionParameters


class Node():
    """Runing node."""

    def __init__(self):
        topic = "motor_controller"
        conn_params = ConnectionParameters()
        conn_params.credentials.username = "testuser"
        conn_params.credentials.password = "testuser"
        conn_params.host = "r4a-platform.ddns.net"
        conn_params.port = 5782

        self.dev = DfrobotMotorController(M1=23, M2=24, E1=12, E2=13,)

        self.subscriber = Subscriber(conn_params=conn_params,
                                     topic=topic,
                                     on_message=self.callback)
        self.subscriber.run()

    def run(self, freq=1):
        while True:
            time.sleep(1/freq)

    def callback(self, msg, meta):
        try:
            self.dev.write(**msg)
            print(msg)
        except TypeError:
            print(
                "Unexpected argument. The proper msg is {\"speed_1\": int, \"speed_2\": int, \"RPM\": bool}")


def main():
    node = Node()
    node.run()


if __name__ == "__main__":
    main()
