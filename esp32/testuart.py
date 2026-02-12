from machine import UART, Pin
import time

__version__ = "1.0.2"

def readAll():
    # Initialize UART2 with default pins for ESP32 Dev Kit C V2
    # TX=GPIO17, RX=GPIO16
    uart2 = UART(2, baudrate=115200, tx=Pin(17), rx=Pin(16))
    uart2.init(115200, bits=8, parity=None, stop=1, timeout=1000)

    print("Reading from UART2 continuously... Press Ctrl+C to stop")

    try:
        while True:
            if uart2.any():
                data = uart2.read()
                if data:
                    print("Received:", data)
                    try:
                        print("Decoded:", data.decode('utf-8'))
                    except:
                        print("Raw bytes:", data)
            time.sleep(0.01)  # Small delay to prevent tight loop
    except KeyboardInterrupt:
        print("\nStopped reading from UART2")

def sendCommand(command):
    print(f"getVersion.py v{__version__}")
    # Initialize UART2 with default pins for ESP32 Dev Kit C V2
    # TX=GPIO17, RX=GPIO16
    uart2 = UART(2, baudrate=115200, tx=Pin(17), rx=Pin(16))
    uart2.init(115200, bits=8, parity=None, stop=1, timeout=1000)

    # Clear any existing data in buffer
    time.sleep(0.05)
    uart2.read()

    # Add CR LF to command and convert to bytes if needed
    if isinstance(command, str):
        command_bytes = (command + '\r\n').encode('utf-8')
    else:
        command_bytes = command + b'\r\n'

    print(f"Sending command: {command}")
    uart2.write(command_bytes)

    # Read all data until Control-Z (0x1A) or buffer is empty
    # Start reading immediately to prevent UART buffer overflow
    rxData = b''
    ctrl_z_found = False
    timeout_count = 0
    max_timeouts = 50  # Increased timeout attempts

    # Give a tiny delay for command to be sent
    time.sleep(0.02)

    while not ctrl_z_found and timeout_count < max_timeouts:
        if uart2.any():
            # Read all available data immediately to prevent buffer overflow
            chunk = uart2.read(uart2.any())
            if chunk:
                rxData += chunk
                # Check if Control-Z (0x1A) is in the accumulated data
                if b'\x1a' in rxData:
                    ctrl_z_found = True
                    break
            timeout_count = 0  # Reset timeout counter
        else:
            timeout_count += 1
        # Very short sleep to keep reading frequently
        time.sleep(0.02)

    if rxData:
        print("Received (raw):", rxData)
        # Decode and clean up response
        try:
            # Remove Control-Z and any trailing characters
            decoded = rxData.replace(b'\x1a', b'').decode('utf-8', errors='ignore')
            print("Decoded:", decoded)
            print("---")
        except:
            print("Raw bytes:", rxData)
    else:
        print("No response received - check TX connection!")

    return rxData

def getVersion():
    return sendCommand('GetVersion')

def playSound(sound_id=1):
    return sendCommand(f'PlaySound SoundID {sound_id}')
