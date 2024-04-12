import usb.core
import usb.util
import time

class HIDKeyboard:
    KEYBOARD_REPORT_DESC = bytes([
        0x05, 0x01,  # Usage Page (Generic Desktop)
        0x09, 0x06,  # Usage (Keyboard)
        0xA1, 0x01,  # Collection (Application)
        0x05, 0x07,  # Usage Page (Keyboard/Keypad)
        0x19, 0xE0,  # Usage Minimum (0xE0)
        0x29, 0xE7,  # Usage Maximum (0xE7)
        0x15, 0x00,  # Logical Minimum (0)
        0x25, 0x01,  # Logical Maximum (1)
        0x75, 0x01,  # Report Size (1)
        0x95, 0x08,  # Report Count (8)
        0x81, 0x02,  # Input (Data, Variable, Absolute)
        0x95, 0x01,  # Report Count (1)
        0x75, 0x08,  # Report Size (8)
        0x81, 0x01,  # Input (Constant) reserved byte(1)
        0x95, 0x05,  # Report Count (5)
        0x75, 0x01,  # Report Size (1)
        0x05, 0x08,  # Usage Page (LEDs)
        0x19, 0x01,  # Usage Minimum (Num Lock)
        0x29, 0x05,  # Usage Maximum (Kana)
        0x91, 0x02,  # Output (Data, Variable, Absolute)
        0x95, 0x01,  # Report Count (1)
        0x75, 0x03,  # Report Size (3)
        0x91, 0x01,  # Output (Constant) reserved byte(1)
        0x95, 0x06,  # Report Count (6)
        0x75, 0x08,  # Report Size (8)
        0x15, 0x00,  # Logical Minimum (0)
        0x25, 0x65,  # Logical Maximum (101)
        0x05, 0x07,  # Usage Page (Keyboard/Keypad)
        0x19, 0x00,  # Usage Minimum (0)
        0x29, 0x65,  # Usage Maximum (101)
        0x81, 0x00,  # Input (Data, Array) Key arrays(6 bytes)
        0xC0,        # End Collection
    ])

    def __init__(self, vendor_id=0x1d6b, product_id=0x0104):
        self.dev = usb.core.find(idVendor=0x1d6b, idProduct=0x0104)
        if self.dev is None:
            raise ValueError('Device not found')

        self.dev.set_configuration()

        cfg = self.dev.get_active_configuration()
        intf = cfg[(0, 0)]

        self.ep = usb.util.find_descriptor(
            intf,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)

        if self.ep is None:
            raise ValueError('Endpoint not found')

    def send_report(self, report):
        self.ep.write(report)
        time.sleep(0.1)

    def send_keystroke(self, keycode):
        report = bytearray([0, 0, keycode, 0, 0, 0, 0, 0])
        self.send_report(report)
        report[2] = 0  # Release the key
        self.send_report(report)

    def cameraShutter(self):
        self.send_keystroke(0x10)  # Camera shutter key code (0x28), Volume up (0x10)
        