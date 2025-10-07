import configparser
import logging
import os
from binascii import unhexlify

import serial
import wx
from serial.tools import list_ports

logging.basicConfig(
    level=logging.CRITICAL,
    format="%(asctime)s - [%(levelname)s] [%(threadName)s] (%(module)s:%(lineno)d) %(message)s",
    filename="aplikasiAlatUji.log",
)

portname = []
portname = [port[0] for port in list_ports.comports()]

fileConfig = "config.cnf"

config = configparser.RawConfigParser()
config.read(fileConfig)

baud = int(config.get("alatUji", "baudrate"))
data = int(config.get("alatUji", "bytesize"))


bersih = config.get("perintah", "bersih")
start = config.get("perintah", "start")
stop = config.get("perintah", "stop")


def bersihMemory(port):
    logging.info(
        "Proses pembersihan memory data pengujian terakhir pada alat compression test.".format(
            port
        )
    )
    try:
        ser = serial.Serial(port, baud, data)
        if ser.is_open:
            perintah = config.get("perintah", "bersih")
            decPerintah = unhexlify(str(perintah))
            ser.write(decPerintah)
            ser.close()
            logging.debug("Pembersihan memory data pengujian terakhir".format(port))
    except Exception as e:
        pesanError = str(e)
        logging.error(
            "Error pada saat pembersihan memory terakhir data pengujian".format(e)
        )
        dlg = wx.MessageDialog(
            None, pesanError, "Error Setting Alat", wx.OK | wx.ICON_INFORMATION
        )
        dlg.ShowModal()
        dlg.Destroy()


def koneksi(port):
    try:
        ser = serial.Serial(port, baud, data)
        if ser.is_open:
            ser.close()
            return "Tersambung !"
    except Exception as e:
        pesanError = str(e)
        dlg = wx.MessageDialog(
            None, pesanError, "Error Setting Alat", wx.OK | wx.ICON_INFORMATION
        )
        dlg.ShowModal()
        dlg.Destroy()


def nilaiTekan(port):
    try:
        ser = serial.Serial(port, baud, data)
        if ser.is_open:
            print(ser)
            nilaiKN = ""
            while True:
                if datanya := ser.readline():
                    data_str = datanya.decode("utf-8", errors="ignore").strip()
                    if "ovalue" in data_str.lower():
                        nilaiKN = data_str.split()[1]
                        yield nilaiKN #Fungsi Looping nilaiKN
    except Exception as e:
        pesanError = str(e)
        dlg = wx.MessageDialog(
            None, pesanError, "Error Setting Alat", wx.OK | wx.ICON_INFORMATION
        )
        dlg.ShowModal()
        dlg.Destroy()


def stopBtn(port):
    try:
        ser = serial.Serial(port, baud, data)
        if ser.is_open:
            perintah = config.get("perintah", "stop")
            decPerintah = unhexlify(str(perintah))
            ser.write(decPerintah)
            ser.close()
    except Exception as e:
        pesanError = str(e)
        dlg = wx.MessageDialog(
            None, pesanError, "Error Setting Alat", wx.OK | wx.ICON_INFORMATION
        )
        dlg.ShowModal()
        dlg.Destroy()
