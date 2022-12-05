import time

import numpy
from colr import color as font_color
from mss import mss
from yeelight import Bulb, discover_bulbs


class Main:
    def __init__(self):
        self.bulb = None
        self.rgb = [0, 0, 0, 0]
        self.running = True
        self.start()

    def start(self):
        try:
            self.bulb = Bulb(self.search_bulb_ipaddr())
            self.bulb.turn_on()
            self.bulb.start_music()
            while self.running:
                self.calculate_average()
                self.calculate_brightness()
                self.bulb.set_rgb(int(self.rgb[0]), int(self.rgb[1]), int(self.rgb[2]))
                self.bulb.set_brightness(int(self.rgb[3]))
                print(font_color("          ", back=self.rgb[:3]))
                time.sleep(0.25)
        finally:
            if self.bulb:
                self.bulb.stop_music()
            self.running = False

    def screenshot(self):
        with mss() as sct:
            image = sct.grab(sct.monitors[1])
            input_img = numpy.array(image)
            return input_img


    def calculate_average(self):
        image = self.screenshot()

        avg_color_per_row = numpy.average(image, axis=0)
        avg_color = numpy.average(avg_color_per_row, axis=0)
        output = [avg_color[0], avg_color[1], avg_color[2]]

        # hls = colorsys.rgb_to_hls(avg_color[0],avg_color[1],avg_color[2])
        # new_saturation = hls[1] * 1.25
        # output = list(colorsys.hls_to_rgb(hls[0],hls[1],hls[2]))

        self.rgb = output

    def calculate_brightness(self):
        brightness = (((0.2126 * self.rgb[0]) + (0.7152 * self.rgb[1]) + (0.0722 * self.rgb[2])) * 100) / 100
        self.rgb.append(brightness)

    def search_bulb_ipaddr(self):
        busqueda = discover_bulbs()
        if len(busqueda) <= 0:
            print("Couldn't find any bulb")
            exit()
        print(f"{len(busqueda)} bulbs found")
        ipaddr = busqueda[0]["ip"]
        print(f"Selected first: {ipaddr}")
        return ipaddr


if __name__ == "__main__":
    Main()
