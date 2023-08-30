#!/usr/bin/env python3
import sys
import json
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

Gst.init(sys.argv)

device_provider = Gst.DeviceProviderFactory.get_by_name("v4l2deviceprovider")
devices = device_provider.get_devices()

def getcapval(caps):
    return [cap['value'] for cap in caps]

retDevices = []

for device in devices:
    path = device.get_properties().get_string("device.path")
    name = device.get_properties().get_string("v4l2.device.card")
    caps = []

    if "mmal service" in name:
        caps = [
            {
                'value': "1920x1080",
                'text': "1920x1080",
                'height': 1080,
                'width': 1920,
                'format': 'raspivid',
            },
            {
                'value': "1640x922",
                'text': "1640x922",
                'height': 922,
                'width': 1640,
                'format': 'raspivid',
            },
            {
                'value': "1280x720",
                'text': "1280x720",
                'height': 720,
                'width': 1280,
                'format': 'raspivid',
            },
            {
                'value': "640x480",
                'text': "640x480",
                'height': 480,
                'width': 640,
                'format': 'raspivid',
            },
        ]
        name = "Raspberry Pi Camera (V2)"
            # path = "raspivid"
    elif "bcm2835-isp" in name:
        continue
    else:
        if "UVC Camera (" in name:
            vendorproduct = name.split("(")[1].split(")")[0]
            import subprocess
            process = subprocess.Popen(['lsusb', '-d', vendorproduct], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stderr == b'' and vendorproduct in stdout.decode("utf-8"):
                name = stdout.decode("utf-8").split(vendorproduct)[1].strip()
        capsGST = device.get_caps()

        for i in range(capsGST.get_size()):
            structure = capsGST.get_structure(i)
            if structure.get_name() in ['video/x-raw', 'video/x-h264', 'image/jpeg'] :
                width = structure.get_int('width').value
                height = structure.get_int('height').value

                if "{0}x{1}".format(width, height) not in getcapval(caps):
                    form = structure.get_name().split('/')[1]
                    caps.append({'value': "{0}x{1}".format(width, height), 'text': "{0}x{1} ({2})".format(width, height, form), 'height': int(height), 'width': int(width), 'format': structure.get_name()})

    retDevices.append({'value': path, 'value': path, 'text': name, 'caps': caps})


print(json.dumps(retDevices))