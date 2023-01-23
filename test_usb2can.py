#!/usr/bin/env python3
import logging
from pathlib import Path
from gs_usb.gs_usb import GsUsb
import libusb_package
import sys


def test_scan():
    devs = scan()
    assert len(devs)
    print(f"Discovered devices: {devs }")

def scan():
    r"""
    Retrieve the list of gs_usb devices handle
    :return: list of gs_usb devices handle
    """
    return [
        GsUsb(dev) for dev in libusb_package.find(find_all=True, custom_match = GsUsb.is_gs_usb_device)
    ]