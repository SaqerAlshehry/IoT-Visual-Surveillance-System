# IoT Visual Surveillance System

## Project Overview
[cite_start]This project implements a visual surveillance system using an ESP32-S3 microcontroller as an edge device and a PC-based application as the cloud server[cite: 30, 31]. [cite_start]The system captures live video frames from an OV2640 camera and streams them over WiFi to a server GUI using a custom TCP protocol[cite: 87, 90].

## Demo
https://drive.google.com/file/d/1aEGI9DnI6Eht0EoDvf7fnex1NTiRcLQ_/view?usp=sharing

## System Architecture
The system utilizes a Client-Server architecture divided into two layers:

### 1. Edge Layer (Client)
* [cite_start]**Hardware:** ESP32-S3 (running MicroPython) with an OV2640 camera module[cite: 26, 27].
* [cite_start]**Function:** Captures JPEG images and streams them to the server via a TCP socket connection[cite: 37, 95].
* **Status Indication:** Uses the built-in RGB LED to indicate state:
    * [cite_start]🔴 **Red:** Idle / Streaming Stopped[cite: 40, 125].
    * [cite_start]🟢 **Green:** Streaming Active[cite: 41, 126].

### 2. Cloud Layer (Server)
* [cite_start]**Hardware:** PC/Laptop running Python[cite: 28, 38].
* [cite_start]**Function:** Listens for incoming connections, sends control commands (`START`/`STOP`), and decodes/displays the video feed in a GUI[cite: 38, 41].

## Features
* [cite_start]**Remote Control:** A GUI interface allows the user to Start and Stop the video stream remotely[cite: 39].
* [cite_start]**Visual Feedback:** LED indicators on the hardware provide real-time status updates[cite: 40].
* [cite_start]**Reliable Transmission:** Uses TCP to ensure ordered delivery of image frames[cite: 106].

## Hardware Requirements
* [cite_start]ESP32-S3 (N8R8) or similar[cite: 26].
* [cite_start]OV2640 or OV5642 Arducam Camera Module[cite: 27].
* [cite_start]PC/Laptop for the server[cite: 28].

## Software Dependencies

### Edge Device (MicroPython)
* `socket`, `struct`, `time`
* [cite_start]`machine`, `network`, `neopixel` [cite: 129-135]

### Server (Python)
* `socket`, `struct`, `threading`, `io`
* `tkinter` (for GUI)
* [cite_start]`pillow` (for JPEG decoding) [cite: 136-142]

## Communication Protocol
[cite_start]The system uses a custom application-layer protocol over TCP[cite: 104]:

**1. Control Commands (Server to Client)**
* [cite_start]`START`: Triggers the ESP32 to begin capturing and sending frames[cite: 109].
* [cite_start]`STOP`: Triggers the ESP32 to halt transmission[cite: 110].

**2. Data Transmission (Client to Server)**
To ensure data integrity, every frame is sent in two parts:
1.  [cite_start]**Header:** A 4-byte integer representing the size of the image[cite: 115].
2.  [cite_start]**Payload:** The raw JPEG byte stream[cite: 116].

## Setup & Usage

### 1. Server Setup
1.  Ensure Python 3 is installed.
2.  Install required libraries (e.g., `Pillow`).
3.  Run the server script. [cite_start]It will listen on the specified port (default: 4444)[cite: 43].

### 2. Edge Device Setup
1.  [cite_start]Flash MicroPython onto the ESP32[cite: 160].
2.  [cite_start]Configure WiFi credentials and the Server IP in the script[cite: 162].
3.  Upload the client script to the board.

### 3. Operation
1.  Run the Server application first.
2.  [cite_start]Power on the ESP32; the LED should be **Red** (Idle)[cite: 40].
3.  Click the **Start** button on the GUI. [cite_start]The LED will turn **Green**, and video will appear[cite: 41].
4.  Click **Stop** to end the stream.