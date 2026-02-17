import socket
import struct
import threading
import tkinter as tk
from PIL import Image, ImageTk
import io

HOST = "0.0.0.0"
PORT = 9001

class CameraServer:

    def __init__(self, root):
        self.root = root
        self.root.title("Camera Viewer - Saqer Alshehri")

        self.label = tk.Label(root)
        self.label.pack()

        self.start_button = tk.Button(root, text="Start", command=self.start_stream)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_stream)
        self.stop_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((HOST, PORT))
        self.server.listen(1)

        print("Waiting for ESP32 connection...")
        self.conn, self.addr = self.server.accept()
        print("Connected:", self.addr)

        self.streaming = False

    def start_stream(self):
        if not self.streaming:
            self.streaming = True
            self.conn.sendall(b"START")
            threading.Thread(target=self.receive_stream, daemon=True).start()

    def stop_stream(self):
        if self.streaming:
            self.streaming = False
            self.conn.sendall(b"STOP")


    def receive_stream(self):
        try:
            while self.streaming:

                #receive size
                raw_size = b""
                while len(raw_size) < 4:
                    packet = self.conn.recv(4 - len(raw_size))
                    if not packet:
                        return
                    raw_size += packet
                size = struct.unpack(">I", raw_size)[0]

                #receive image
                data = b""
                while len(data) < size:
                    packet = self.conn.recv(min(4096, size - len(data)))
                    if not packet:
                        return
                    data += packet
                image = Image.open(io.BytesIO(data))
                image = image.resize((320, 240))

                photo = ImageTk.PhotoImage(image)

                self.label.config(image=photo)
                self.label.image = photo

        except Exception as e:
            print("Stream error:", e)



root = tk.Tk()
app = CameraServer(root)
root.mainloop()
