import socket
import time
import struct
import neopixel
from machine import Pin
from arducam_mp import ArduCAM
from wifi import connect



SSID = "your_wifi_name"
PASSWORD = "your_wifi_password"

SERVER_IP = "your_PC_IP"
PORT = 9001


#on my borad, the built-in RGB is on PIN#38. check yours
LED_PIN = 38 
np = neopixel.NeoPixel(Pin(LED_PIN), 1)

def led_idle():
    np[0] = (255, 0, 0)
    np.write()

def led_streaming():
    np[0] = (0, 255, 0)
    np.write()

def led_off():
    np[0] = (0, 0, 0)
    np.write()

led_idle()


# Connect WiFi

connect(SSID, PASSWORD)


# Connect to Server


sock = socket.socket()
sock.connect((SERVER_IP, PORT))

print("Connected to server.")


# Camera Init


cam = ArduCAM()

if not cam.detect():
    led_off()
    raise SystemExit

cam.init_ov2640()

streaming = False


# Main Loop


while True:

    try:
        print("Waiting for command...")
        cmd = sock.recv(1024).decode().strip()
        print("Command:", cmd)

        if cmd == "START":
            streaming = True
            led_streaming()

        elif cmd == "STOP":
            streaming = False
            led_idle()


        while streaming:

            # Capture
            cam.flush_fifo()
            cam.clear_fifo_flag()
            cam.start_capture()

            while not cam.capture_done():
                time.sleep(0.01)

            length = cam.read_fifo_length()

            if length <= 0 or length > 2000000:
                continue

            sock.sendall(struct.pack(">I", length))

            cam._cs_low()
            cam.spi.write(bytearray([0x3C]))

            remaining = length
            chunk = 512 

            while remaining > 0:
                read_size = chunk if remaining > chunk else remaining
                data = cam.spi.read(read_size)
                sock.sendall(data)
                remaining -= read_size

                time.sleep(0.002)

            cam._cs_high()
            cam.clear_fifo_flag()

            
            sock.settimeout(0.01)
            try:
                new_cmd = sock.recv(1024).decode().strip()
                if new_cmd == "STOP":
                    streaming = False
                    led_idle()
            except:
                pass

            sock.settimeout(None)

            time.sleep(0.1)

    except Exception as e:
        print("Connection lost:", e)
        break

sock.close()
led_off()
print("Client stopped.")
