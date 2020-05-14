# -*- coding=utf-8 -*-
import os
import socket


def get_ip():
    name = socket.getfqdn(socket.gethostname())
    name = name.strip(".localdomain") if name.endswith(".localdomain") else name
    myaddr = socket.gethostbyname(name)
    return myaddr


def get_port():
    port = None
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(base_dir + "\weiqi\config.js", 'r') as config:
        lines = config.readlines()
    for line in lines:
        if "port:" in line:
            port = line.split(":")[1].strip()
    return port
