#!/usr/bin/env python3
import time
from gs_usb.gs_usb import GsUsb
from gs_usb.gs_usb_frame import GsUsbFrame
from gs_usb.constants import (
    CAN_EFF_FLAG,
    CAN_ERR_FLAG,
    CAN_RTR_FLAG,
)
import libusb_package
#innomaker usb2can device do not support the GS_USB_MODE_NO_ECHO_BACK mode
from gs_usb.gs_usb import (
    GS_CAN_MODE_LOOP_BACK,
    GS_CAN_MODE_NORMAL
)


def test_scan():
    devs = scan()
    assert len(devs)
    print(f"Discovered devices: {devs }")
    send_receive(devs[0])
    

def scan():
    r"""
    Retrieve the list of gs_usb devices handle
    :return: list of gs_usb devices handle
    """
    return [
        GsUsb(dev) for dev in libusb_package.find(find_all=True, custom_match = GsUsb.is_gs_usb_device)
    ]
    
def send_receive(device: GsUsb):
    """
    This code was copied from the usb2can.py example in the inno-maker/usb2can
    GitHub repository.
    """
    # Close before Start device in case the device was not properly stop last time
    # If do not stop the device, bitrate setting will be fail.
    device.stop() 

    # Configuration
    if not device.set_bitrate(1000000):
        print("Can not set bitrate for gs_usb")
        return
    
    # Start device, If you have only one device for test, pls use the loop-back mode,
    device.start(GS_CAN_MODE_LOOP_BACK)
    #device.start(GS_CAN_MODE_NORMAL)
    
    # Prepare frames
    data = b"\x12\x34\x56\x78\x9A\xBC\xDE\xF0"
    sff_frame = GsUsbFrame(can_id=0x7FF, data=data)
    sff_none_data_frame = GsUsbFrame(can_id=0x7FF)
    err_frame = GsUsbFrame(can_id=0x7FF | CAN_ERR_FLAG, data=data)
    eff_frame = GsUsbFrame(can_id=0x12345678 | CAN_EFF_FLAG, data=data)
    eff_none_data_frame = GsUsbFrame(can_id=0x12345678 | CAN_EFF_FLAG)
    rtr_frame = GsUsbFrame(can_id=0x7FF | CAN_RTR_FLAG)
    rtr_with_eid_frame = GsUsbFrame(can_id=0x12345678 | CAN_RTR_FLAG | CAN_EFF_FLAG)
    rtr_with_data_frame = GsUsbFrame(can_id=0x7FF | CAN_RTR_FLAG, data=data)
    frames = [
        sff_frame,
        sff_none_data_frame,
        err_frame,
        eff_frame,
        eff_none_data_frame,
        rtr_frame,
        rtr_with_eid_frame,
        rtr_with_data_frame,
    ]

    # Read all the time and send message in each second
    end_time, n = time.time() + 1, -1
    while n < 5:
        iframe = GsUsbFrame()
        if device.read(iframe, 1):
            # if you don't want to receive the error frame. filter out it.
            # otherwise you will receive a lot of error frame when your device do not connet to CAN-BUS
            if iframe.can_id & CAN_ERR_FLAG != CAN_ERR_FLAG:
                print("RX  {}".format(iframe))

        if time.time() - end_time >= 0:
            end_time = time.time() + 1
            n += 1
            n %= len(frames)

            if device.send(frames[n]):
                print("TX  {}".format(frames[n]))
    # Make sure the device is stopped before exit
    device.stop() 
