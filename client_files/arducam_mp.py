from machine import Pin, SPI, I2C
import time
from OV2640_reg import *

# ---------------- Arducam Registers ----------------

ARDUCHIP_TRIG = 0x41
CAP_DONE_MASK = 0x08

FIFO_SIZE1 = 0x42
FIFO_SIZE2 = 0x43
FIFO_SIZE3 = 0x44
FIFO_BURST = 0x3C


class ArduCAM:

    def __init__(self):

        # ---------------- SPI ----------------
        self.cs = Pin(9, Pin.OUT)
        self.cs.value(1)

        self.spi = SPI(
            1,
            baudrate=4000000,
            polarity=0,
            phase=0,
            sck=Pin(12),
            mosi=Pin(10),
            miso=Pin(11)
        )

        # ---------------- I2C ----------------
        self.i2c = I2C(
            0,
            scl=Pin(14),
            sda=Pin(13),
            freq=100000
        )

        self.sensor_addr = 0x30

    # =================================================
    # SPI LOW LEVEL
    # =================================================

    def _cs_low(self):
        self.cs.value(0)

    def _cs_high(self):
        self.cs.value(1)

    def spi_write(self, addr, val):
        self._cs_low()
        self.spi.write(bytearray([addr | 0x80, val]))
        self._cs_high()

    def spi_read(self, addr):
        self._cs_low()
        self.spi.write(bytearray([addr & 0x7F]))
        data = self.spi.read(1)
        self._cs_high()
        return data[0]

    # =================================================
    # I2C SENSOR
    # =================================================

    def sensor_write(self, reg, val):
        self.i2c.writeto(self.sensor_addr, bytearray([reg, val]))

    def sensor_read(self, reg):
        self.i2c.writeto(self.sensor_addr, bytearray([reg]))
        data = self.i2c.readfrom(self.sensor_addr, 1)
        return data[0]

    def sensor_write_array(self, reg_list):
        for reg in reg_list:
            addr = reg[0]
            val = reg[1]
            if addr == 0xff and val == 0xff:
                break
            self.sensor_write(addr, val)
            time.sleep_ms(1)

    # =================================================
    # CAMERA INIT
    # =================================================

    def detect(self):
        self.sensor_write(0xFF, 0x01)
        id_high = self.sensor_read(0x0A)
        id_low  = self.sensor_read(0x0B)

        print("Camera ID:", hex(id_high), hex(id_low))

        if id_high == 0x26:
            print("OV2640 detected")
            return True
        else:
            print("Camera NOT detected")
            return False

    def init_ov2640(self):

        print("Initializing OV2640...")

        # Reset sensor
        self.sensor_write(0xff, 0x01)
        self.sensor_write(0x12, 0x80)
        time.sleep(0.1)

        # JPEG configuration sequence
        self.sensor_write_array(OV2640_JPEG_INIT)
        self.sensor_write_array(OV2640_YUV422)
        self.sensor_write_array(OV2640_JPEG)

        # Set resolution (fast + stable)
        self.sensor_write_array(OV2640_320x240_JPEG)

        print("OV2640 initialized.")

    # =================================================
    # FIFO CONTROL
    # =================================================

    def flush_fifo(self):
        self.spi_write(0x04, 0x01)

    def clear_fifo_flag(self):
        self.spi_write(0x04, 0x01)

    def start_capture(self):
        self.spi_write(0x04, 0x02)

    def capture_done(self):
        return self.spi_read(ARDUCHIP_TRIG) & CAP_DONE_MASK

    def read_fifo_length(self):
        len1 = self.spi_read(FIFO_SIZE1)
        len2 = self.spi_read(FIFO_SIZE2)
        len3 = self.spi_read(FIFO_SIZE3) & 0x7F
        return (len3 << 16) | (len2 << 8) | len1

    # =================================================
    # IMAGE READ
    # =================================================

    def read_image(self, filename="image.jpg"):

        length = self.read_fifo_length()
        print("Image length:", length)

        if length <= 0 or length > 2000000:
            print("Invalid image length")
            return False

        self._cs_low()

        # Send burst command
        self.spi.write(bytearray([FIFO_BURST]))

        with open(filename, "wb") as f:

            remaining = length
            chunk = 1024

            while remaining > 0:
                read_size = chunk if remaining > chunk else remaining
                data = self.spi.read(read_size)
                f.write(data)
                remaining -= read_size

        self._cs_high()
        self.clear_fifo_flag()

        print("Image saved as", filename)
        return True


