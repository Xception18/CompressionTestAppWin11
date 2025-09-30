import base64
import configparser
import json
import logging
import ssl
import urllib
import urllib.request

import wx
import psycopg2
import psycopg2.extras

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - [%(levelname)s] [%(threadName)s] (%(module)s:%(lineno)d) %(message)s",
    filename="aplikasiAlatUji.log",
)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fileConfig = "config.cnf"
config = configparser.RawConfigParser()
config.read(fileConfig)
webSerBendaUji = config.get("webser", "webser_bendaUji")
username = config.get("webser", "http_user")
password = config.get("webser", "http_pass")
# username = "paktomy"
# password = "S3l4m4tS3j4ht3r4"


def queryBendaUji(noDocket, nourut):
    logging.info(
        "Memulai proses query Benda Uji dari server ERP dengan Nomer Docket : %s dengan Nomer Urut = %s",
        noDocket,
        nourut,
    )
    bendaUji = webSerBendaUji + noDocket + "&no_urut=" + str(nourut)
    print(" URL encodenya adalah =  ", bendaUji)
    try:

        logging.debug("Koneksi ke webservice untuk parameter : %s", bendaUji)
        request = urllib.request.Request(bendaUji)
        base64string = (
            base64.encodebytes(f"{username}:{password}".encode("utf-8"))
            .decode("utf-8")
            .replace("\n", "")
        )
        request.add_header("Authorization", f"Basic {base64string}")
        respUrl = urllib.request.urlopen(request, context=ctx)
        jsonBendaUji = json.load(respUrl)
        logging.debug("HTTP Respond : %s", str(respUrl.getcode()))
        return jsonBendaUji
    except Exception as e:
        pesanError = str(e)
        logging.error(
            "Error dalam proses koneksi webservice dengan pesan error : %s", e
        )
        dlg = wx.MessageDialog(
            None, pesanError, "Error Koneksi Webservice", wx.OK | wx.ICON_INFORMATION
        )
        dlg.ShowModal()
        dlg.Destroy()


def cekBjdtId(doket):
    try:
        logging.info("Mulai mengeksekusi method cekBjdtId() pada file webserv.py")

        # ceknomerurut = []
        datab = config.get("database", "dbname")
        login = config.get("database", "user")
        hosted = config.get("database", "host")
        passed = config.get("database", "password")
        conn = f"dbname={datab} user={login} host={hosted} password={passed}"
        konekdb = psycopg2.connect(conn)
        konekdb.autocommit = True
        kursor = konekdb.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        data = (doket,)
        SQL = """ SELECT idbendauji FROM pengujian
                WHERE noDocket = %s ; """
        kursor.execute(SQL, data)

        bjdtid = kursor.fetchall()
        logging.debug("Data Benda uji hasil method cekBjdtId() : %s", str(bjdtid))
        # print bjdtid
        return bjdtid
            # return nomer
            # print no
            # return no

    except Exception as e:
        logging.error(
            "Error pada saat menjalankan method cekBjdtId() pda file webserv.py", str(e)
        )
        # pesanError = str(e)
        # print e
        # dlg = wx.MessageDialog(None, pesanError, "Error Koneksi Database", wx.OK | wx.ICON_INFORMATION)
        # dlg.ShowModal()
        # dlg.Destroy()
