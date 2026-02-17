import network
import time

def connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)

    # to kill the wifi session
    wlan.active(False)
    time.sleep(1)

    wlan.active(True)
    wlan.disconnect()
    time.sleep(1)

    print("Connecting to WiFi...")
    wlan.connect(ssid, password)

    timeout = 15
    while timeout > 0:
        if wlan.isconnected():
            break
        print("Waiting for connection...")
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print("Connected!")
        print("IP:", wlan.ifconfig()[0])
        return wlan.ifconfig()[0]
    else:
        raise RuntimeError("WiFi connection failed")
