import datetime
import logging
import time
from datetime import date

import wx
from serial.tools import list_ports

import ctrlAlat
import dbctrl
import webserv

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - [%(levelname)s] [%(threadName)s] (%(module)s:%(lineno)d) %(message)s",
    filename="aplikasiAlatUji.log",
)


class PanelBendaUji(wx.Panel):
    def __init__(self, parent):
        logging.info("Inisialisasi Aplikasi Pengendali Alat Penguji Tekanan")
        wx.Panel.__init__(self, parent)
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        self.panelPengujian = wx.Panel(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL
        )
        self.panelPengujian.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT)
        )

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        fgSizer4 = wx.FlexGridSizer(0, 2, 10, 10)
        fgSizer4.SetFlexibleDirection(wx.BOTH)
        fgSizer4.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # ID Alat
        # staticText Alat
        self.m_staticText8 = wx.StaticText(
            self.panelPengujian,
            wx.ID_ANY,
            "ID Alat",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText8.Wrap(-1)
        self.m_staticText8.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        fgSizer4.Add(self.m_staticText8, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.m_staticText8.Hide()
        # TextCtrl Alat
        self.txtIdAlat = wx.TextCtrl(
            self.panelPengujian,
            wx.ID_ANY,
            "4",
            wx.DefaultPosition,
            wx.Size(100, -1),
        )
        self.txtIdAlat.SetToolTipString("ID Alat Compression Test")
        fgSizer4.Add(self.txtIdAlat, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.txtIdAlat.Hide()

        # Tanggal Pengujian
        # staticText Tanggal Pengujian
        self.m_staticText201 = wx.StaticText(
            self.panelPengujian,
            wx.ID_ANY,
            "Tanggal Pengujian",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText201.Wrap(-1)
        self.m_staticText201.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        fgSizer4.Add(self.m_staticText201, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        # TextCtrl Tanggal Pengujian
        self.txtTglPengujian = wx.TextCtrl(
            self.panelPengujian,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(100, -1),
            wx.TE_READONLY,
        )
        self.txtTglPengujian.ChangeValue(str(date.today().strftime("%d/%m/%Y")))
        self.txtTglPengujian.SetToolTipString("Tanggal dilakukan pengujian")
        fgSizer4.Add(self.txtTglPengujian, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Rencana Tanggal Uji
        # staticText Tanggal Pengujian
        self.m_staticText501 = wx.StaticText(
            self.panelPengujian,
            wx.ID_ANY,
            "Rencana Tgl Pengujian",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText501.Wrap(-1)
        self.m_staticText501.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        fgSizer4.Add(self.m_staticText501, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        # TextCtrl Tanggal Pengujian
        self.txtRencanaTglUji = wx.TextCtrl(
            self.panelPengujian,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(100, -1),
            wx.TE_READONLY,
        )
        # self.txtRencanaTglUji.ChangeValue (str(date.today().strftime("%d/%m/%Y")))
        self.txtRencanaTglUji.SetToolTipString("Tanggal Rencana Pengujian")
        fgSizer4.Add(self.txtRencanaTglUji, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Tanggal Benda Uji
        # staticText Tanggal Benda Uji
        self.m_staticText17 = wx.StaticText(
            self.panelPengujian,
            wx.ID_ANY,
            "Tanggal Benda Uji",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText17.Wrap(-1)
        self.m_staticText17.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        fgSizer4.Add(self.m_staticText17, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        # TextCtrl Tanggal Benda Uji
        self.txtTglBendaUji = wx.TextCtrl(
            self.panelPengujian,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(100, -1),
            wx.TE_READONLY,
        )
        self.txtTglBendaUji.SetToolTipString("Tanggal pengambilan/pembuatan benda uji")
        fgSizer4.Add(self.txtTglBendaUji, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Umur Benda Uji
        # staticText Umur Benda Uji
        self.staTxtUmur = wx.StaticText(
            self.panelPengujian,
            wx.ID_ANY,
            "Umur Benda Uji",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.staTxtUmur.Wrap(-1)
        self.staTxtUmur.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        fgSizer4.Add(self.staTxtUmur, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        # TextCtrl Tanggal Benda Uji
        self.txtUmur = wx.TextCtrl(
            self.panelPengujian,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(100, -1),
            wx.TE_READONLY,
        )
        self.txtUmur.SetToolTipString(
            "Umur Benda Uji dalam Hari (Tanggal Pembuatan s/d Tanggal Pengujian"
        )
        fgSizer4.Add(self.txtUmur, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Nomor Docket
        # staticText Nomor Docket
        self.m_staticText10 = wx.StaticText(
            self.panelPengujian,
            wx.ID_ANY,
            "Nomor Docket",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText10.Wrap(-1)
        self.m_staticText10.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        fgSizer4.Add(self.m_staticText10, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        # TextCtrl Nomor Docket
        # self.txtNomorDocket = wx.TextCtrl( self.panelPengujian, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), wx.TE_PROCESS_ENTER )
        self.txtNomorDocket = wx.TextCtrl(
            self.panelPengujian,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(300, -1),
            wx.TE_PROCESS_ENTER,
        )
        self.txtNomorDocket.SetFocus()
        self.txtNomorDocket.SetToolTipString("Nomor Docket Benda Uji")
        fgSizer4.Add(self.txtNomorDocket, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # No Urut Benda Uji
        # # staticText No Urut Benda Uji
        self.m_staticText9 = wx.StaticText(
            self.panelPengujian,
            wx.ID_ANY,
            "No Urut Benda Uji",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText9.Wrap(-1)
        self.m_staticText9.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        fgSizer4.Add(self.m_staticText9, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        # TextCtrl No Urut Benda Uji
        # self.txtNoUrut = wx.TextCtrl( self.panelPengujian, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), wx.TE_READONLY  )
        self.txtNoUrut = wx.TextCtrl(
            self.panelPengujian,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(100, -1),
            wx.TE_PROCESS_ENTER,
        )
        self.txtNoUrut.SetToolTipString(
            "Nomer Urut Benda Uji untuk Nomer Docket yang bersangkutan"
        )
        fgSizer4.Add(self.txtNoUrut, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Tanggal Docket
        # staticText Tanggal Docket
        self.m_staticText181 = wx.StaticText(
            self.panelPengujian,
            wx.ID_ANY,
            "Tanggal Docket",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText181.Wrap(-1)
        self.m_staticText181.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        fgSizer4.Add(self.m_staticText181, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        # TextCtrl Tanggal Docket
        self.txtTglDocket = wx.TextCtrl(
            self.panelPengujian,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(100, -1),
            wx.TE_READONLY,
        )
        self.txtTglDocket.SetToolTipString("Tanggal pembuatan Docket")
        fgSizer4.Add(self.txtTglDocket, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Kode Benda Uji
        # staticText Kode Benda Uji
        self.m_staticText191 = wx.StaticText(
            self.panelPengujian,
            wx.ID_ANY,
            "Kode Benda Uji",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText191.Wrap(-1)
        self.m_staticText191.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        fgSizer4.Add(self.m_staticText191, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        # Text Control Kode Benda Uji
        self.txtKodeBendaUji = wx.TextCtrl(
            self.panelPengujian,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(300, -1),
            wx.TE_READONLY,
        )
        self.txtKodeBendaUji.SetToolTipString("Kode khusus benda uji")
        fgSizer4.Add(self.txtKodeBendaUji, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Jenis Benda Uji
        # staticText Jenis Benda uji
        self.stTxtJenisBendaUji = wx.StaticText(
            self.panelPengujian,
            wx.ID_ANY,
            "Jenis Benda Uji",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.stTxtJenisBendaUji.Wrap(-1)
        self.stTxtJenisBendaUji.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        fgSizer4.Add(self.stTxtJenisBendaUji, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        # TextCtrl Berat Benda Uji
        self.txtJenisBUJ = wx.TextCtrl(
            self.panelPengujian,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(300, -1),
            wx.TE_READONLY,
        )
        self.txtJenisBUJ.SetToolTipString("Jenis/Bentuk Benda Uji")
        fgSizer4.Add(self.txtJenisBUJ, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Pelanggan
        # staticText Pelanggan
        self.m_staticText12 = wx.StaticText(
            self.panelPengujian,
            wx.ID_ANY,
            "Pelanggan",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText12.Wrap(-1)
        self.m_staticText12.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        fgSizer4.Add(self.m_staticText12, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        # TextCtrl Pelanggan
        self.txtPelanggan = wx.TextCtrl(
            self.panelPengujian,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(300, -1),
            wx.TE_READONLY,
        )
        self.txtPelanggan.SetToolTipString("Pelanggan sample benda uji")
        fgSizer4.Add(self.txtPelanggan, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Proyek
        # staticText Proyek
        self.m_staticText13 = wx.StaticText(
            self.panelPengujian,
            wx.ID_ANY,
            "Proyek",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText13.Wrap(-1)
        self.m_staticText13.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        fgSizer4.Add(self.m_staticText13, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        # TextCtrl Proyek
        self.txtProyek = wx.TextCtrl(
            self.panelPengujian,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(300, -1),
            wx.TE_READONLY,
        )
        self.txtProyek.SetToolTipString("Proyek ")
        fgSizer4.Add(self.txtProyek, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # ID Benda Uji
        # TextCtrl ID Benda Uji
        self.txtIdBendaUji = wx.TextCtrl(
            self.panelPengujian,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(300, -1),
            wx.TE_READONLY,
        )
        self.txtIdBendaUji.SetToolTipString("Proyek ")
        self.txtIdBendaUji.Hide()

        bSizer2.Add(fgSizer4, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 10)

        fgSizer5 = wx.FlexGridSizer(0, 2, 10, 10)
        fgSizer5.SetFlexibleDirection(wx.BOTH)
        fgSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # Berat Benda Uji
        # staticText Berat Benda uji
        self.stTxtBerat = wx.StaticText(
            self.panelPengujian,
            wx.ID_ANY,
            "Berat (Kg)",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.stTxtBerat.Wrap(-1)
        self.stTxtBerat.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        fgSizer5.Add(
            self.stTxtBerat, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5
        )
        # TextCtrl Berat Benda Uji
        self.txtBerat = wx.TextCtrl(
            self.panelPengujian,
            wx.ID_ANY,
            "0",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_RIGHT,
        )
        self.txtBerat.SetToolTipString("Berat bersih benda uji")
        fgSizer5.Add(self.txtBerat, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Port Serial
        # staticText Port Serial
        self.m_staticText11 = wx.StaticText(
            self.panelPengujian,
            wx.ID_ANY,
            "Port Serial",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText11.Wrap(-1)
        self.m_staticText11.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        fgSizer5.Add(
            self.m_staticText11,
            0,
            wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
            5,
        )
        # Choicebox Port Serial
        chcPortChoices = [port[0] for port in list_ports.comports()]
        self.chcPort = wx.Choice(
            self.panelPengujian,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            chcPortChoices,
            0,
        )
        self.chcPort.SetToolTipString("Letak port serial dari alat")
        fgSizer5.Add(self.chcPort, 0, wx.ALL, 5)

        # Test Koneksi
        # Button Test Koneksi
        self.btnTest = wx.Button(
            self.panelPengujian,
            wx.ID_ANY,
            "Test Koneksi",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.btnTest.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        self.btnTest.SetToolTipString("Test sambungan kesiapan alat")
        self.btnTest.Enable(False)
        fgSizer5.Add(
            self.btnTest,
            0,
            wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL,
            5,
        )
        # TextCtrl Status Koneksi
        self.txtStatusKoneksi = wx.TextCtrl(
            self.panelPengujian,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(120, -1),
            wx.TE_READONLY,
        )
        self.txtStatusKoneksi.SetToolTipString("Status Koneksi Alat")
        fgSizer5.Add(self.txtStatusKoneksi, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Start
        # Button Start
        self.btnStart = wx.Button(
            self.panelPengujian,
            wx.ID_ANY,
            "Start",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.btnStart.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        self.btnStart.SetToolTipString("Jalankan proses oleh alat")
        self.btnStart.Enable(False)
        fgSizer5.Add(
            self.btnStart,
            0,
            wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL,
            5,
        )

        # # Button Stop
        self.btnStop = wx.Button(
            self.panelPengujian,
            wx.ID_ANY,
            "Stop",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.btnStop.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        self.btnStop.SetToolTipString("Hentikan proses pengujian")
        self.btnStop.Enable(True)
        fgSizer5.Add(
            self.btnStop,
            0,
            wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL,
            5,
        )

        # Nilain KN Hasil Pengujian
        # staticText Hasil Pengujian
        self.m_staticText18 = wx.StaticText(
            self.panelPengujian,
            wx.ID_ANY,
            "Beban (KN)",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText18.Wrap(-1)
        self.m_staticText18.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        fgSizer5.Add(
            self.m_staticText18,
            0,
            wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
            5,
        )

        # TextCtrl Nilai KN Hasil Pengujian dibuat readonly
        self.txtBeban = wx.TextCtrl(
            self.panelPengujian,
            wx.ID_ANY,
            "0",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_READONLY | wx.TE_RIGHT,
        )
        # self.txtBeban = wx.TextCtrl( self.panelPengujian, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_RIGHT, wx.TE_PROCESS_ENTER)

        # TextCtrl Nilai KN Hasil Pengujian dibuat tidak readonly
        # self.txtBeban = wx.TextCtrl( self.panelPengujian, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_RIGHT )

        self.txtBeban.SetToolTipString("Nilai KN hasil proses pengujian")
        fgSizer5.Add(self.txtBeban, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Kuat Tekan Pengujian MPa
        # staticText Hasil Pengujian
        self.stTxtMpa = wx.StaticText(
            self.panelPengujian,
            wx.ID_ANY,
            "Kuat Tekan - Fc(MPa)",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.stTxtMpa.Wrap(-1)
        self.stTxtMpa.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        fgSizer5.Add(
            self.stTxtMpa, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5
        )

        # TextCtrl Nilai MPa Hasil Pengujian Readonly
        self.txtMpa = wx.TextCtrl(
            self.panelPengujian,
            wx.ID_ANY,
            "0",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_READONLY | wx.TE_RIGHT,
        )

        # TextCtrl Nilai MPa Hasil Pengujian tidak Reaadonly
        # self.txtMpa = wx.TextCtrl( self.panelPengujian, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_RIGHT )

        self.txtMpa.SetToolTipString("Nilai Kuat Tekan/Lentur dalam MPa")
        fgSizer5.Add(self.txtMpa, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Kuat Tekan Pengujian Kg/Cm2
        # staticText Hasil Pengujian
        self.stTxtKuatTekan = wx.StaticText(
            self.panelPengujian,
            wx.ID_ANY,
            "Kuat Tekan - K(Kg/cm2)",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.stTxtKuatTekan.Wrap(-1)
        self.stTxtKuatTekan.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        fgSizer5.Add(self.stTxtKuatTekan, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        # TextCtrl Nilai Kg/Cm3 Hasil Pengujian readonlu
        self.txtKg = wx.TextCtrl(
            self.panelPengujian,
            wx.ID_ANY,
            "0",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_READONLY | wx.TE_RIGHT,
        )
        # self.txtKg= wx.TextCtrl( self.panelPengujian, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_RIGHT )

        # TextCtrl Nilai Kg/Cm3 Hasil Pengujian tidak readonly
        # self.txtKg= wx.TextCtrl( self.panelPengujian, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_RIGHT )

        self.txtKg.SetToolTipString("Nilai Kuat Tekan/Lentur dalam Kg/Cm3")
        fgSizer5.Add(self.txtKg, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Jenis/Tipe Retakan
        # staticText Jenis/Tipe Retakan
        self.m_staticText20 = wx.StaticText(
            self.panelPengujian,
            wx.ID_ANY,
            "Jenis Retakan",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText20.Wrap(-1)
        self.m_staticText20.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        fgSizer5.Add(
            self.m_staticText20,
            0,
            wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
            5,
        )
        # Choice Tipe Retakan
        chcTipeRetakChoices = ["", "A", "B", "C", "D", "E"]
        self.chcTipeRetak = wx.Choice(
            self.panelPengujian,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            chcTipeRetakChoices,
            0,
        )
        self.chcTipeRetak.SetSelection(0)
        self.chcTipeRetak.SetToolTipString("Tipe/Jenis retakan hasil pengujian")
        fgSizer5.Add(self.chcTipeRetak, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer2.Add(fgSizer5, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer5.Add(bSizer2, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 10)

        bSizer8 = wx.BoxSizer(wx.HORIZONTAL)

        # self.btnKeluar = wx.Button( self.panelPengujian, wx.ID_ANY, u"KELUAR", wx.DefaultPosition, wx.DefaultSize, 0 )
        # self.btnKeluar.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )

        # bSizer8.Add( self.btnKeluar, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        bSizer8.Add(wx.Size(0, 0), 1, wx.EXPAND, 5)

        self.btnBatal = wx.Button(
            self.panelPengujian,
            wx.ID_ANY,
            "BATAL",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.btnBatal.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        self.btnBatal.Enable(False)

        bSizer8.Add(self.btnBatal, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.btnBaru = wx.Button(
            self.panelPengujian,
            wx.ID_ANY,
            "BARU",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.btnBaru.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )

        bSizer8.Add(self.btnBaru, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.btnSimpan = wx.Button(
            self.panelPengujian,
            wx.ID_ANY,
            "SIMPAN",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.btnSimpan.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString)
        )
        self.btnSimpan.Enable(False)

        bSizer8.Add(self.btnSimpan, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer8.Add(wx.Size(0, 0), 1, wx.EXPAND, 5)

        bSizer5.Add(bSizer8, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.panelPengujian.SetSizer(bSizer5)
        self.panelPengujian.Layout()
        bSizer5.Fit(self.panelPengujian)
        bSizer1.Add(self.panelPengujian, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # self.txtTglBendaUji.Bind( wx.EVT_TEXT, self.umurBendaUji )
        self.txtNoUrut.Bind(wx.EVT_TEXT_ENTER, self.nomorDocket)
        # self.txtBeban.Bind (wx.EVT_TEXT_ENTER, self.konversiKN)
        self.txtNomorDocket.Bind(wx.EVT_TEXT_ENTER, self.nomorDocket)
        # Events Tombol pada saat ditekan
        self.btnTest.Bind(wx.EVT_BUTTON, self.testAlatMethod)
        self.btnStart.Bind(wx.EVT_BUTTON, self.startAlatMethod)
        self.btnStop.Bind(wx.EVT_BUTTON, self.stopAlatMethod)
        # self.btnKeluar.Bind( wx.EVT_BUTTON, self.keluarMethod)
        self.btnBatal.Bind(wx.EVT_BUTTON, self.batalMethod)
        self.btnBaru.Bind(wx.EVT_BUTTON, self.baruMethod)
        self.btnSimpan.Bind(wx.EVT_BUTTON, self.simpanMehod)

    # Posisi Button apabila pengetesan tidak diperbolehkan untuk dilakukan

    def validasiUncek(
        self,
    ):
        self.btnSimpan.Enable(False)
        self.btnBaru.Enable(False)
        self.btnBatal.Enable(True)
        self.btnStart.Enable(False)
        self.btnTest.Enable(False)
        self.btnStop.Enable(False)

    # mengakses webservice pada ERP untuk query benda uji berdasarkan Nomor Docket
    def nomorDocket(self, event):
        logging.info(
            "Event pengambilan data benda uji pada saat penekanan tombol Enter"
        )

        noDocket = str(self.txtNomorDocket.GetValue())
        noUrutnya = str(self.txtNoUrut.GetValue())
        # timeini = datetime.datetime.now()
        # hariini = str(timeini.strftime("%d/%m/%Y"))

        if (noDocket is "") | (noUrutnya is ""):
            pesanError = "Periksa Nomer docket dan Nomer Urut Benda Uji. Apakah sudah diisi dengan benar ?"
            logging.error(
                "Periksa Nomer docket dan Nomer Urut Benda Uji. Apakah sudah diisi dengan benar ?".format(
                    noDocket
                )
            )
            dlgDokNo = wx.MessageDialog(
                None,
                pesanError,
                "Error Nomer Docket dan Nomer Urut",
                wx.OK | wx.ICON_INFORMATION,
            )
            dlgDokNo.ShowModal()
            dlgDokNo.Destroy()

        else:
            try:
                logging.debug(
                    "Pemanggilan data benda uji dari webserv.queryBendaUji() No Docket : %s dan nomor urut : %s ",
                    noDocket,
                    noUrutnya,
                )
                nilaikn = ""
                dataBendaUji = webserv.queryBendaUji(noDocket, noUrutnya)
                print(
                    "Memanggil fungsi clsNbBendaUji.nomorDocket() --> webserv.queryBendaUji() adalah = ",
                    dataBendaUji,
                )
                logging.debug(
                    "Memanggil fungsi clsNbBendaUji.nomorDocket() = %s", dataBendaUji
                )

                if dataBendaUji is not None:
                    self.txtIdBendaUji.SetValue(str(dataBendaUji["bjdt_id"]))
                    self.txtRencanaTglUji.SetValue(dataBendaUji["tgl_rencana_test"])
                    self.txtTglBendaUji.SetValue(str(dataBendaUji["bjqc_tgl_buat"]))
                    tglBuat = str(dataBendaUji["bjqc_tgl_buat"])
                    txtUmur = self.umurBendaUji(tglBuat)
                    self.txtUmur.SetValue(str(txtUmur))
                    self.txtNomorDocket.SetValue(noDocket)
                    self.txtNoUrut.SetValue(noUrutnya)
                    self.txtTglDocket.SetValue(str(dataBendaUji["do_tgl"]))
                    self.txtKodeBendaUji.SetValue(str(dataBendaUji["bjqc_nomor"]))
                    self.txtJenisBUJ.SetValue(str(dataBendaUji["buj_nama"]))
                    self.txtPelanggan.SetValue(str(dataBendaUji["pelanggan_nama"]))
                    self.txtProyek.SetValue(str(dataBendaUji["pry_nama"]))
                    self.txtBerat.SetValue(str(dataBendaUji["bjdt_berat"]))

                    self.txtBeban.SetValue(str(dataBendaUji["bjdt_kuat_tekan"]))
                    self.txtMpa.SetValue(str(dataBendaUji["bjdt_beban_mpa"]))
                    self.txtKg.SetValue(str(dataBendaUji["bjdt_beban_kg"]))
                    # self.txtBeban.SetValue(dataBendaUji["bjdt_beban"])
                    # self.txtMpa.SetValue(dataBendaUji["bjdt_mpa"])
                    # self.txtKg.SetValue(dataBendaUji["bjdt_kuatTekan"])
                    # self.chcTipeRetak.SetSelection(dataBendaUji["bjdt_tipe_retak"])

                    nilaikn = dataBendaUji["bjdt_kuat_tekan"]
                    print(f"nilai KN = {str(nilaikn)}")
                    # print type(nilaikN)
                    if str(nilaikn) != "0.0":
                        self.btnSimpan.Enable(False)
                        self.btnBaru.Enable(False)
                        self.btnBatal.Enable(True)
                        self.btnStart.Enable(False)
                        self.btnTest.Enable(False)
                        self.btnStop.Enable(False)
                        # self.validasiUncek()
                        self.validasiUncek()
                        pesanValidasi = "Benda Uji ini pernah dilakukan pengetesan. Periksa Nomer Docket dan Nomer Urut"
                        dlgValNilai = wx.MessageDialog(
                            None,
                            pesanValidasi,
                            "Error Benda Uji",
                            wx.OK | wx.ICON_INFORMATION,
                        )
                        dlgValNilai.ShowModal()
                        dlgValNilai.Destroy()

                    tglRencana = str(dataBendaUji["tgl_rencana_test"])
                    tglrencanaTest = datetime.datetime.strptime(tglRencana, "%d/%m/%Y")
                    tglSekarang = datetime.datetime.strptime(
                        datetime.datetime.now().strftime("%d/%m/%Y"), "%d/%m/%Y"
                    )
                    selisihTest = tglSekarang - tglrencanaTest
                    if (
                        self.txtJenisBUJ.GetValue() == "Balok"
                        or dataBendaUji["buj_nama"] == "Beam"
                    ):
                        self.stTxtKuatTekan.SetLabel("Kuat Lentur - K(Kg/cm2)")
                        self.stTxtMpa.SetLabel("Kuat Lentur - Fc(MPa))")
                    else:
                        self.stTxtKuatTekan.SetLabel("Kuat Tekan - K(Kg/cm2)")
                        self.stTxtMpa.SetLabel("Kuat Tekan - Fc(MPa)")

                    # self.tampilkanQuery()

                    # if (selisihTest.days > 2) | (tglSekarang <
                    # tglrencanaTest) :
                    if tglSekarang < tglrencanaTest:
                        self.btnSimpan.Enable(False)
                        self.btnBaru.Enable(False)
                        self.btnBatal.Enable(True)
                        self.btnStart.Enable(False)
                        self.btnTest.Enable(False)
                        self.btnStop.Enable(False)
                        # self.validasiUncek()

                    # if (selisihTest.days > 2) | (tglSekarang <
                    # tglrencanaTest) :
                    if tglSekarang < tglrencanaTest:
                        self.validasiUncek()
                        pesanValidasi = "Benda uji tidak diperkenankan untuk dilakukan pengujian. Periksa umur benda uji dan Tanggal Rencana Test"
                        dlgValWaktu = wx.MessageDialog(
                            None,
                            pesanValidasi,
                            "Error Benda Uji",
                            wx.OK | wx.ICON_INFORMATION,
                        )
                        dlgValWaktu.ShowModal()
                        dlgValWaktu.Destroy()
                        # self.validasiUncek()

                else:
                    # self.btnSimpan.Enable(False)
                    # self.btnBaru.Enable(False)
                    # self.btnBatal.Enable(True)
                    # self.btnStart.Enable(False)
                    # self.btnTest.Enable(False)
                    # self.btnStop.Enable(False)
                    # self.validasiUncek()
                    self.txtRencanaTglUji.Clear()
                    self.txtTglBendaUji.Clear()
                    self.txtUmur.Clear()
                    self.txtNomorDocket.Clear()
                    self.txtTglDocket.Clear()
                    self.txtNoUrut.Clear()
                    self.txtKodeBendaUji.Clear()
                    self.txtJenisBUJ.Clear()
                    self.txtPelanggan.Clear()
                    self.txtProyek.Clear()
                    self.txtBerat.Clear()
                    # self.chcPort.Clear()
                    # self.txtStatusKoneksi.Clear()
                    self.txtBeban.Clear()
                    self.txtMpa.Clear()
                    self.txtKg.Clear()
                    self.chcTipeRetak.SetSelection(0)
                    self.txtNomorDocket.SetFocus()
                    self.txtIdBendaUji.Clear()
                    pesanError = 'Data Benda uji tidak tersedia. Atau jika sebelumnya ada pesan "Error Koneksi Webservice", laporkan pada bagian IT'
                    dlg = wx.MessageDialog(
                        None, pesanError, "Error Benda Uji", wx.OK | wx.ICON_INFORMATION
                    )
                    dlg.ShowModal()
                    dlg.Destroy()

            except Exception as e:
                print(e)
                logging.error(
                    "Error dalam pemanggilan method webserv.queryBendaUji() No Docket : %s dan nomor urut : %s ",
                    noDocket,
                    noUrutnya,
                )

    def tampilkanQuery(
        self,
        dataBendaUji,
        noDocket=None,
        noUrutnya=None,
    ):
        self.txtIdBendaUji.SetValue(str(dataBendaUji["bjdt_id"]))
        self.txtRencanaTglUji.SetValue(dataBendaUji["tgl_rencana_test"])
        self.txtTglBendaUji.SetValue(str(dataBendaUji["bjqc_tgl_buat"]))
        tglBuat = str(dataBendaUji["bjqc_tgl_buat"])
        txtUmur = self.umurBendaUji(tglBuat)
        self.txtUmur.SetValue(str(txtUmur))
        if noDocket is not None:
            self.txtNomorDocket.SetValue(str(noDocket))
        if noUrutnya is not None:
            self.txtNoUrut.SetValue(str(noUrutnya))
        self.txtTglDocket.SetValue(str(dataBendaUji["do_tgl"]))
        self.txtKodeBendaUji.SetValue(str(dataBendaUji["bjqc_nomor"]))
        self.txtJenisBUJ.SetValue(str(dataBendaUji["buj_nama"]))
        self.txtPelanggan.SetValue(str(dataBendaUji["pelanggan_nama"]))
        self.txtProyek.SetValue(str(dataBendaUji["pry_nama"]))
        self.txtBerat.SetValue(str(dataBendaUji["bjdt_berat"]))

        self.txtBeban.SetValue(str(dataBendaUji["bjdt_kuat_tekan"]))
        self.txtMpa.SetValue(str(dataBendaUji["bjdt_beban_mpa"]))
        self.txtKg.SetValue(str(dataBendaUji["bjdt_beban_kg"]))
        self.chcTipeRetak.SetSelection(dataBendaUji.get("tipe_retak", 0))

        tglRencana = str(dataBendaUji["tgl_rencana_test"])
        tglrencanaTest = datetime.datetime.strptime(tglRencana, "%d/%m/%Y")
        tglSekarang = datetime.datetime.strptime(
            datetime.datetime.now().strftime("%d/%m/%Y"), "%d/%m/%Y"
        )
        selisihTest = tglSekarang - tglrencanaTest
        if self.txtJenisBUJ.GetValue() == "Balok" or dataBendaUji["buj_nama"] == "Beam":
            self.stTxtKuatTekan.SetLabel("Kuat Lentur - K(Kg/cm2)")
            self.stTxtMpa.SetLabel("Kuat Lentur - Fc(MPa))")
        else:
            self.stTxtKuatTekan.SetLabel("Kuat Tekan - K(Kg/cm2)")
            self.stTxtMpa.SetLabel("Kuat Tekan - Fc(MPa)")

    # test koneksi dengan pengujian membuka port serial
    def testAlatMethod(self, event):
        self.indexPort = self.chcPort.GetSelection()
        self.port = self.chcPort.GetString(self.indexPort)
        if len(self.port) == 0:
            pesanError = "Alat tidak terdeteksi, periksa sambungan kabel !"
            dlg = wx.MessageDialog(
                None, pesanError, "Error Setting Alat", wx.OK | wx.ICON_INFORMATION
            )
            dlg.ShowModal()
            dlg.Destroy()
            self.txtStatusKoneksi.SetValue("Tdk tersambung !")
        else:
            statusBaru = ctrlAlat.koneksi(self.port)
            self.txtStatusKoneksi.SetValue(str(statusBaru))

    # def konversiKN( self, event ):
    # 	try:
    # 		knNya = self.txtBeban.GetValue()
    # 		jenisNya = self.txtJenisBUJ.GetValue()
    # 		nilaiMPA = knToMpa(knNya, jenisNya)
    # 		nilaiKGCM = knToKgCm(knNya, jenisNya)
    # 		self.txtMpa.SetValue(nilaiMPA)
    # 		self.txtKg.SetValue(nilaiKGCM)
    # 	except Exception as e:
    # 		print str(e)

    # memberikan perintah pada alat untuk memulai proses pengujian

    def startAlatMethod(self, event):
        try:
            self.indexPort = self.chcPort.GetSelection()
            self.port = self.chcPort.GetString(self.indexPort)
            if self.txtStatusKoneksi.Value == "Tersambung !":
                self.gen = ctrlAlat.nilaiTekan(self.port)
                def updateBeban():
                    try:
                        nilaiKN = next(self.gen)
                        self.txtBeban.SetValue(str(nilaiKN))
                        wx.CallLater(200, updateBeban)  # loop lagi tiap 200ms
                        jenis = self.txtJenisBUJ.GetValue()
                        mpaNya = knToMpa(nilaiKN, jenis)
                        kgNya = knToKgCm(nilaiKN, jenis)
                        self.txtMpa.SetValue(mpaNya)
                        self.txtKg.SetValue(kgNya)
                        print(mpaNya)
                        print(kgNya)
                    except StopIteration:
                        pass
                    except Exception as e:
                        wx.MessageBox(str(e), "Error Update", wx.OK | wx.ICON_ERROR)

            else:
                pesanError = "Alat belum tersambung, lakukan Test Koneksi"
                dlg = wx.MessageDialog(
                    None, pesanError, "Error Setting Alat", wx.OK | wx.ICON_INFORMATION
                )
                dlg.ShowModal()
                dlg.Destroy()

        except Exception as e:
            print(e)

    # memberikan perintah pada alat untuk menghentikan proses pengujian

    def stopAlatMethod(self, event):
        self.indexPort = self.chcPort.GetSelection()
        self.port = self.chcPort.GetString(self.indexPort)
        if self.txtStatusKoneksi.Value == "Tersambung !":
            ctrlAlat.stopBtn(self.port)
        else:
            pesanError = "Alat belum tersambung, lakukan Test Koneksi"
            dlg = wx.MessageDialog(
                None, pesanError, "Error Setting Alat", wx.OK | wx.ICON_INFORMATION
            )
            dlg.ShowModal()
            dlg.Destroy()

    # keluar dari aplikasi
    # def keluarMethod( self, event ):
    # 	# event.Skip()
    # 	wx.App().close()

    # membersihkan field isian yang biasanya dilakukan untuk membatalkan
    def batalMethod(self, event):
        self.btnSimpan.Enable(False)
        self.btnBaru.Enable(True)
        self.btnBatal.Enable(False)
        self.btnStart.Enable(False)
        self.btnTest.Enable(False)
        self.btnStop.Enable(False)
        self.txtRencanaTglUji.Clear()
        self.txtTglBendaUji.Clear()
        self.txtUmur.Clear()
        self.txtNomorDocket.Clear()
        self.txtTglDocket.Clear()
        self.txtNoUrut.Clear()
        self.txtKodeBendaUji.Clear()
        self.txtJenisBUJ.Clear()
        self.txtPelanggan.Clear()
        self.txtProyek.Clear()
        self.txtBerat.Clear()
        # self.chcPort.Clear()
        # self.txtStatusKoneksi.Clear()
        self.txtBeban.Clear()
        self.txtMpa.Clear()
        self.txtKg.Clear()
        self.chcTipeRetak.SetSelection(0)
        self.txtIdBendaUji.Clear()

    # membersihkan seluruh nilai isian pada form pengujian
    def baruMethod(self, event):
        self.txtRencanaTglUji.Clear()
        self.txtTglBendaUji.Clear()
        self.txtUmur.Clear()
        self.txtNomorDocket.Clear()
        self.txtTglDocket.Clear()
        self.txtNoUrut.Clear()
        self.txtKodeBendaUji.Clear()
        self.txtJenisBUJ.Clear()
        self.txtPelanggan.Clear()
        self.txtProyek.Clear()
        self.txtBerat.Clear()
        # self.chcPort.Clear()
        # self.txtStatusKoneksi.Clear()
        self.txtBeban.Clear()
        self.txtMpa.Clear()
        self.txtKg.Clear()
        self.chcTipeRetak.SetSelection(0)
        self.txtNomorDocket.SetFocus()
        self.txtIdBendaUji.Clear()

        self.btnSimpan.Enable(True)
        self.btnBaru.Enable(False)
        self.btnBatal.Enable(True)
        self.btnStart.Enable(True)
        self.btnTest.Enable(True)
        self.btnStop.Enable(True)

    # menyimpan pada database lokal
    def simpanMehod(self, event):
        # simpan item data pada tabel di database
        if (
            len(self.txtBeban.GetValue())
            and len(self.txtBerat.GetValue())
            and self.chcTipeRetak.GetSelection() != 0
        ):

            tglUjiAwal = str(self.txtTglPengujian.GetValue())
            tglUjiNya = time.strptime(tglUjiAwal, "%d/%m/%Y")
            param = [
                time.strftime("%Y-%m-%d", tglUjiNya),
                str(self.txtIdAlat.GetValue()),
                str(self.txtKodeBendaUji.GetValue()),
                str(self.txtNomorDocket.GetValue()),
                str(self.txtNoUrut.GetValue()),
                float(self.txtBeban.GetValue()),
                float(self.txtBerat.GetValue()),
            ]
            tipeRetak = ""  # Default value to avoid unbound error
            if self.chcTipeRetak.GetSelection() == 1:
                tipeRetak = "A"
            elif self.chcTipeRetak.GetSelection() == 2:
                tipeRetak = "B"
            elif self.chcTipeRetak.GetSelection() == 3:
                tipeRetak = "C"
            elif self.chcTipeRetak.GetSelection() == 4:
                tipeRetak = "D"
            elif self.chcTipeRetak.GetSelection() == 5:
                tipeRetak = "E"
            param.extend((str(tipeRetak), str(self.txtIdBendaUji.GetValue())))
            renUjiAwal = str(self.txtRencanaTglUji.GetValue())
            renUjiNya = time.strptime(renUjiAwal, "%d/%m/%Y")
            param.extend(
                (
                    time.strftime("%Y-%m-%d", renUjiNya),
                    str(self.txtJenisBUJ.GetValue()),
                    float(str(self.txtKg.GetValue()).replace(",", ".")),
                    float(self.txtMpa.GetValue()),
                    str(self.txtUmur.GetValue()),
                )
            )
            strTglBenda = str(self.txtTglBendaUji.GetValue())
            # print "strTglBenda = ", strTglBenda
            tglBenda = datetime.datetime.strptime(strTglBenda, "%d/%m/%Y").date()
            # print "tglBenda = ", tglBenda
            # print 'tglBenda.strftime("Y-m-d") = ',
            # tglBenda.strftime("%Y-%m-%d")
            param.append(tglBenda.strftime("%Y-%m-%d"))
            # print param
            dbctrl.simpan(param)

            self.btnBaru.Enable(True)
            self.btnBatal.Enable(False)
            self.btnSimpan.Enable(False)
            self.btnStart.Enable(False)
            self.btnTest.Enable(False)
            self.btnStop.Enable(False)

        else:
            pesanError = (
                "Item data isian belum lengkap, periksa kembali item data isian"
            )
            dlg = wx.MessageDialog(
                None, pesanError, "Error Data Isian", wx.OK | wx.ICON_INFORMATION
            )
            dlg.ShowModal()
            dlg.Destroy()

    # menghitung umur benda uji

    def umurBendaUji(self, tglBuat):
        tglSekarang = datetime.datetime.strptime(
            datetime.datetime.now().strftime("%d/%m/%Y"), "%d/%m/%Y"
        )
        tglBendaUji = datetime.datetime.strptime(tglBuat, "%d/%m/%Y")
        tglUmur = tglSekarang - tglBendaUji
        return tglUmur.days


def knToMpa(knNya, jenis):
    # print "knToMpa -> kN = ", knNya
    # print "knToMpa -> jenis = ", jenis
    Mpa = str(0.00)  # Default value to ensure Mpa is always bound
    # #~ print "Mpa sebelum --> Mpa = ", Mpa
    if "Silinder 15 x 30" in jenis:
        Mpa = str(round((float(knNya) * 1000) / 17671, 2))
        print("Mpa setelah --> Mpa = ", Mpa)
        print("Jenis tipe Silinder --> ", jenis)
    elif "Kubus" in jenis or "Balok" in jenis or "Beam" in jenis:
        Mpa = str(0.00)
        print("Mpa setelah --> Mpa = ", Mpa)
    elif "Silinder 10 x 20" in jenis:
        Mpa = str(round((float(knNya) * 1000) / 7850, 2))
        print("Mpa setelah --> Mpa = ", Mpa)
        print("Jenis tipe Silinder --> ", jenis)
    return Mpa


# Konversi nilai KN ke Kg/Cm3


def knToKgCm(knNya, jenis):
    print("knToMpa -> kN = ", knNya)
    print("knToMpa -> jenis = ", jenis)
    KgCm = str(0.00)  # Default value to ensure KgCm is always bound
    # ~ print "KgCm sebelum --> KgCm = ", KgCm
    if "Silinder 15 x 30" in jenis:
        KgCm = str(round((((float(knNya) * 101.971) / 176.71) / 0.83), 2))
        print("KgCm setelah --> KgCm = ", KgCm)
        print("Jenis tipe Silinder --> ", jenis)
    elif "Kubus" in jenis:
        KgCm = str(round(((float(knNya) * 101.971) / 225), 2))
        print("KgCm setelah --> KgCm = ", KgCm)
    elif "Balok" in jenis or "Beam" in jenis:
        KgCm = str(round(((float(knNya) * 45 * 101.971) / (15 ** 3)), 2))
        print("KgCm setelah --> KgCm = ", KgCm)
    elif "Silinder 10 x 20" in jenis:
        KgCm = str(round((((float(knNya) * 101.971) / 78.50) / 0.83), 2))
        print("KgCm setelah --> KgCm = ", KgCm)
        print("Jenis tipe Silinder --> ", jenis)
    return KgCm
