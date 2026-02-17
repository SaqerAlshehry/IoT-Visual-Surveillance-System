# IoT Visual Surveillance System

## Project Overview
This project implements a visual surveillance system using an ESP32-S3 microcontroller as an edge device and a PC-based application as the cloud server. The system captures live video frames from an OV2640 camera and streams them over WiFi to a server GUI using a custom TCP protocol.

## Demo
https://drive.google.com/file/d/1aEGI9DnI6Eht0EoDvf7fnex1NTiRcLQ_/view?usp=sharing

## System Architecture
The system utilizes a Client-Server architecture divided into two layers:

### 1. Edge Layer (Client)
* **Hardware:** ESP32-S3 (running MicroPython) with an OV2640 camera module.
* **Function:** Captures JPEG images and streams them to the server via a TCP socket connection.
* **Status Indication:** Uses the built-in RGB LED to indicate state:
    * 🔴 **Red:** Idle / Streaming Stopped.
    * 🟢 **Green:** Streaming Active.

### 2. Cloud Layer (Server)
* **Hardware:** PC/Laptop running Python.
* **Function:** Listens for incoming connections, sends control commands (`START`/`STOP`), and decodes/displays the video feed in a GUI.

## Features
* **Remote Control:** A GUI interface allows the user to Start and Stop the video stream remotely.
* **Visual Feedback:** LED indicators on the hardware provide real-time status updates.
* **Reliable Transmission:** Uses TCP to ensure ordered delivery of image frames.

## Hardware Requirements
* ESP32-S3 (N8R8) or similar.
* OV2640 or OV5642 Arducam Camera Module.
* PC/Laptop for the server.

## Software Dependencies

### Edge Device (MicroPython)
* `socket`, `struct`, `time`
* `machine`, `network`, `neopixel` 

### Server (Python)
* `socket`, `struct`, `threading`, `io`
* `tkinter` (for GUI)
* `pillow` (for JPEG decoding) 

## Communication Protocol
The system uses a custom application-layer protocol over TCP:

**1. Control Commands (Server to Client)**
* `START`: Triggers the ESP32 to begin capturing and sending frames.
* `STOP`: Triggers the ESP32 to halt transmission.

**2. Data Transmission (Client to Server)**
To ensure data integrity, every frame is sent in two parts:
1.  **Header:** A 4-byte integer representing the size of the image.
2.  **Payload:** The raw JPEG byte stream.

## Setup & Usage

### 1. Server Setup
1.  Ensure Python 3 is installed.
2.  Install required libraries (e.g., `Pillow`).
3.  Run the server script. It will listen on the specified port 9001.

### 2. Edge Device Setup
1.  Flash MicroPython onto the ESP32.
2.  Configure WiFi credentials and the Server IP in the script.
3.  Upload the client script to the board.

### 3. Operation
1.  Run the Server application first.
2.  Power on the ESP32; the LED should be **Red** (Idle).
3.  Click the **Start** button on the GUI. The LED will turn **Green**, and video will appear.
4.  Click **Stop** to stop the stream.
