"""drawer.py"""

from PIL import Image, ImageDraw
from ..hw_devices.hw_connections import Spi2Spi


class Drawer():
    """Class for drawing a connection."""

    def __init__(self):
        self._img_dims = (600, 600)
        self._board_dims = (150, 400)
        self._per_dims = (150, 200)
        self._board_offset = (50, 100)
        self._board_per_dist = 200
        self._per_offset = (
            self._board_offset[0] + self._board_dims[0] + self._board_per_dist,
            self._board_offset[1] + (self._board_dims[1] - self._per_dims[1])/2
        )
        self._topic_center = self._per_offset[0] + self._per_dims[0]/2
        self._topic_margin = 10
        self._line_dist = 20

    def _draw_rect(self, offset, dims, text):
        self.draw.rectangle([offset, (offset[0]+dims[0], offset[1]+dims[1])],
                            width=1, outline="black")
        text_size = self.draw.textsize(text)
        self.draw.text((offset[0] + dims[0]/2 - text_size[0]/2,
                        offset[1] + dims[1]/2 - text_size[1]/2),
                       text,
                       fill="black")

    def _draw_line(self, start, end, y, text):
        self.draw.line([(start, y), (end, y)], width=1, fill="black")
        text_size = self.draw.textsize(text)
        center = (end - start)/2 + start
        self.draw.text((center - text_size[0]/2, y - 1 - text_size[1]),
                       text,
                       fill="black")

    def draw_connection(self, connection, save_path=None):
        self.img = Image.new("RGB", self._img_dims, color="white")
        self.draw = ImageDraw.Draw(self.img)

        # Draw board
        self._draw_rect(
            self._board_offset, self._board_dims, connection.board.name
        )

        # Draw peripheral
        self._draw_rect(
            self._per_offset, self._per_dims, connection.peripheral.name
        )

        # Draw topic
        topic_text = "topic: " + connection.com_endpoint.topic_name
        topic_size = self.draw.textsize(topic_text)
        self._draw_rect(
            (self._topic_center - topic_size[0]/2 - self._topic_margin/2, 15),
            (topic_size[0] + self._topic_margin, topic_size[1] + 7),
            topic_text
        )

        # Connect devices with pins
        # TODO: maybe an error will occure in pins order for hw_ints with more
        # than one pin.
        pins_text = self._get_conns(connection)
        start_y = self._per_offset[1] \
            + (self._per_dims[1] - (len(pins_text)-1)*self._line_dist)/2
        start = self._board_offset[0] + self._board_dims[0]
        end = start + self._board_per_dist
        for text in pins_text:
            self._draw_line(start, end, start_y, text)
            start_y += self._line_dist

        # Draw topic line
        self.draw.line([(self._topic_center, 15 + topic_size[1] + 7),
                        (self._topic_center, self._per_offset[1])],
                       width=1,
                       fill="red")

        # Save image
        if save_path:
            self.img.save(save_path)
        self.img.close()

    def _get_conns(self, connection):
        pins = []

        # Get names of power pins
        for power_con in connection.power_connections:
            b = self._get_power_pins(power_con.pin_1)
            p = self._get_power_pins(power_con.pin_2)
            pins.append(f"{b} -- {p}")

        # Get names of hw_int pins
        for hw_con in connection.hw_connections:
            pins += self._get_pin_names(hw_con)

        return pins

    def _get_pin_names(self, hw_con):
        if isinstance(hw_con, Spi2Spi):
            board_hw =\
                [hw_con.hwint_1.mosi.name, hw_con.hwint_1.miso.name,
                 hw_con.hwint_1.sclk.name, hw_con.hwint_1.ce[hw_con.ce_index].name]
            per_hw = [hw_con.hwint_2.mosi.name, hw_con.hwint_2.miso.name,
                      hw_con.hwint_2.sclk.name, hw_con.hwint_2.ce[0].name]
        else:
            board_hw = self._get_hwint_pins(hw_con.hwint_1)
            per_hw = self._get_hwint_pins(hw_con.hwint_2)

        return [f"{b} -- {p}" for b, p in zip(board_hw, per_hw)]

    def _get_hwint_pins(self, hw_int):
        pin_names = []
        for s in hw_int.eClass.eStructuralFeatures:
            if s.eClass.name == "EReference":
                pin_names.append(getattr(hw_int, s.name).name)
        return pin_names

    def _get_power_pins(self, power):
        return power.name
