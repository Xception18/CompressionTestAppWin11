import configparser
import logging
import os

import wx
import wx.adv

from clsGridBendaUji import GridBendaUji
from clsNbBendaUji import PanelBendaUji
from daemonSink import threadSinkData

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - [%(levelname)s] [%(threadName)s] (%(module)s:%(lineno)d) %(message)s",
    filename="aplikasiAlatUji.log",
)

wx.SizerFlags.DisableConsistencyChecks()


class MainFrame(wx.Frame):
    def __init__(self):
        logging.info("Inisialisasi Aplikasi Pengendali Alat Penguji Tekanan")

        # wx.Frame.__init__ ( self, None, id = wx.ID_ANY, title = u"COMPRESSION TEST CONTROL APPLICATION", pos = wx.DefaultPosition, size = wx.Size( 940,650 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
        wx.Frame.__init__(
            self,
            None,
            id=wx.ID_ANY,
            title="COMPRESSION TEST CONTROL APPLICATION",
            pos=wx.DefaultPosition,
            size=wx.Size(940, 650),
            style=wx.CAPTION
            | wx.MINIMIZE_BOX
            | wx.STAY_ON_TOP
            | wx.SYSTEM_MENU
            | wx.TAB_TRAVERSAL,
        )

        # Membuat sebuah panel dan sebuah Tab(Notebook)
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # mmembuat halaman bendaUji dan PanelGrid sebagai halaman pada
        # Tab(Notebook)
        page1 = PanelBendaUji(nb)
        page2 = GridBendaUji(nb)

        # menambahkan halaman pada Tab(Notebook) dan menampilkan judul Tab
        nb.AddPage(page1, "Pengujian")
        logging.debug("Menampilkan notebook Pengujian pada MainFrame")
        nb.AddPage(page2, "Daftar Pengujian")
        logging.debug("Menampilkan notebook Pengujian pada MainFrame")

        # memasukan Tab(Notebook) pada sizer sesuai dengan jenis pengaturan
        # layout yang ditentukan
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)


sudoPassword = "ariswara?!"
command = "chmod 666 /dev/ttyUSB0"

try:
    os.system(f"echo {sudoPassword}|sudo -S {command}")
except Exception:
    pass

if __name__ == "__main__":
    fileConfig = "config.cnf"
    config = configparser.RawConfigParser()
    config.read(fileConfig)
    tunda = config.get("webser", "delay")
    daemon = threadSinkData(1, "ThreadSinkron", float(tunda))
    daemon.start()
    logging.debug("Menampilkan MainFrame")
    app = wx.App()
    MainFrame().Show()

    app.MainLoop()
