import asyncio
import struct
import time

from bleak import BleakScanner, BleakClient

SERVICE_UUID = "3ec837af-b0c6-4e7e-a8c5-4b31311d98cf"
CHAR_UUID = "945c4d90-825d-452f-820a-0d8b0cc74a12" 

# pico2w (2C:CF:67:E2:CC:8C)

SENSOR = None # here will be stored sensor BLE instance
CONNECTED = False # true if there is connected sensor in BLE callacks

def handle_notification(sender, data: bytearray):
    
   # rozbal 6 floatov (veľké endian, teda '>'), každý po 4 bajty
    floats = struct.unpack('>ffffff', data[:24])

    # rozbal posledný bajt ako unsigned char
    usb_connected = struct.unpack('B', data[24:25])[0]

    decoded = {
        'temperature': round(floats[0],2),
        'humidity': round(floats[1],2),
        'pressure': round(floats[2],2),
        'sea_level_pressure': round(floats[3],2),
        'battery_voltage': round(floats[4],2),
        'battery_percentage': round(floats[5],2),
        'is_usb_connected': bool(usb_connected)
    }

    print("   -     ")
    print(decoded)
    
def handle_disconnection(client :BleakClient):
    CONNECTED = False
   # client.disconnect()
    print("Connection lost")

async def scan():
    results = await BleakScanner.discover(return_adv=True)
    for device, adv_data in results.values():

        uuids = [uuid.lower() for uuid in adv_data.service_uuids or []]
        if SERVICE_UUID in uuids:
            print(f"Found sensor on: {device.name} ({device.address})")
            return device
        
    print("Scan found nothing")
    return None


async def connect(device):
    CONNECTED = False # reset connection flag state
    async with BleakClient(
        address_or_ble_device = device,
        disconnected_callback = handle_disconnection
        ) as client: # try to create connection

        print("Pripojené:", client.is_connected) #check if 
 
        print("Počúvam notifikácie...")
        await client.start_notify(CHAR_UUID, handle_notification)
        CONNECTED = True

        # run BLE loop
        while client.is_connected: # loop only while connected
            await asyncio.sleep(1)

while True:

    # if there is no conected sensor, try to find it using scanner
    if (CONNECTED is False):
        device = asyncio.run(scan()) # got sensor device
        if (device is not None):
            asyncio.run(connect(device)) # connect it
    print("Waiting for connections.")
    time.sleep(2) # wait 1s to try again