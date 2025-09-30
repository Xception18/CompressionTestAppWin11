import configparser
import logging
import ssl
import threading
import time

import psycopg2
import requests

# logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - [%(levelname)s] [%(threadName)s] (%(module)s:%(lineno)d) %(message)s",filename="aplikasiAlatUji.log")


class threadSinkData(threading.Thread):

    def __init__(self, threadID, name, delayNya):
        logging.info(
            "Inisialisasi Daemon Sinkronisasi database lokal dengan database ERP"
        )
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delayNya = delayNya

    def run(self):
        siklusUmum = 1
        while True:
            logging.debug("Memulai thread ThreadSinkron yang Ke- %s", str(siklusUmum))
            print(
                f"Memulai Thread  : {self.name}, Siklus Thread yang ke-{str(siklusUmum)}"
            )
            counterCekData = 1
            data = {}
            try:
                # Query Data Benda pada database lokal dengan kondisi field
                # sinkron = 'B'
                while not data:
                    logging.debug(
                        "Melakukan proses pemerikasaan data yg akan disinkronkan yang Ke- : %s",
                        str(counterCekData),
                    )
                    logging.debug(
                        "Memanggil method cekData(data) dengan data : %s", str(data)
                    )
                    print(f"Cek data ke-{str(counterCekData)}")
                    data = cekData()
                    logging.debug(
                        "Hasil query cekData(data) dengan data : %s", str(data)
                    )
                    if not data:  # and   counter < 3:
                        logging.warn("Tidak ada data yang harus disinkronkan")
                        print("Tidak ada data yang harus di sinkronkan")
                        print(
                            f"Sleep Cek Data ke-{str(counterCekData)} selama {str(self.delayNya)} detik."
                        )
                        counterCekData += 1
                        time.sleep(self.delayNya)
                    else:
                        logging.debug(
                            "Ada data yang harus di sinkronkan : %s ", str(data)
                        )
                        print("Ada data yang harus di sinkronkan", data)
                respon = 0
                counterPost = 1
                while respon != 200:  # and counter < 3:
                    print(
                        f"Percobaan yang ke-{str(counterPost)} untuk posting data ke webservice ERP"
                    )
                    logging.info(
                        "Memanggil method kirimDataPost(data) untuk mengirimkan data sinkronisasi ke database ERP dengan data : %s",
                        str(data),
                    )
                    responKode = kirimDataPost(data)
                    if responKode is not None:
                        respon = responKode.status_code
                    else:
                        respon = None
                    print(respon)
                    logging.debug(
                        "Respon server dari proses pengiriman server : %s", str(respon)
                    )
                    if respon != 200:
                        logging.warn("Respon belum OK")
                        logging.debug(
                            'Sleep Post Data yang ke-" %s, selama : %s detik',
                            str(counterPost),
                            str(self.delayNya),
                        )
                        print(" Data tidak berhasil dikirim ke Database ERP")
                        print(
                            f"Sleep Post Data yang ke-{str(counterPost)} selama {str(self.delayNya)}  detik"
                        )
                        counterPost += 1
                        time.sleep(self.delayNya)

                    else:
                        logging.debug(
                            "Respon OK, Data telah berhasil disinkronkan dengan ERP"
                        )
                        print(" Data telah berhasil di sinkronkan ke ERP")
                        print("Proses update database lokal")

                countCekDb = 1
                cekdb = data[7]
                print("cekdb Asal :", cekdb)
                while cekdb == "B":
                    print("cekDbLokal  = 'S'")
                    logging.info(
                        "Mengupdate database lokal yang ke - %s dengan status S pada kolom sinkron",
                        str(countCekDb),
                    )
                    print(" Proses update database lokal yang ke-", countCekDb)
                    sinkUpdateLokal(data[5], data[6])
                    print("cekdb = ", cekdb)
                    logging.debug(
                        "Update database lokal berhasil dilakukan untuk data benda uji dengan Nomer Docket : %s",
                        data[5],
                    )
                    print(
                        "Update database lokal berhasil dilakukan untuk data benda uji dengan Nomer Docket : %s",
                        data[5],
                    )
                    logging.info(
                        "Memanggil method cekSinkronLokal() untuk memeriksa data : %s",
                        str(data[4]),
                    )
                    cekdb = cekSinkronLokal(data[4])
                    logging.debug(
                        "Hasil query cekSinkronLokal() adalah :  %s", cekdb
                    )
                    print("cekdb hasil cekSinkronLokal() adalah :", cekdb)
                    countCekDb += 1
                    time.sleep(self.delayNya)
                                # counter += 1
            except Exception as e:
                logging.error("Error pada saat menjalan daemonSink.py : %s", str(e))
                print(e)

            time.sleep(self.delayNya)
            siklusUmum += 1


def cekData():
    try:
        config = configparser.RawConfigParser()
        fileConfig = "config.cnf"
        config.read(fileConfig)
        datab = config.get("data", "database")
        hosted = config.get("data", "host")
        login = config.get("data", "user")
        passed = config.get("data", "password")
        conn = f"dbname={datab} user={login} host={hosted} password={passed}"
        konekdb = psycopg2.connect(conn)
        konekdb.autocommit = True
        kursor = konekdb.cursor()
        # print kursor 	# For Debug Only
        SQL = """ SELECT tgluji, nilaikn, beratbenda, tiperetak, idbendauji, nodocket,  nourutbenda, sinkron, bebanmpa, kuattekan, umur FROM pengujian
		WHERE sinkron = 'B' ; """
        kursor.execute(SQL)
        daftar = kursor.fetchone()
        kursor.close()
        konekdb.close()
        # print daftar
        return daftar
    except Exception as e:
        logging.error(
            "Error pada saat memanggil method cekData() pada file daemonSink.py : %s",
            str(e),
        )
        # print str(e)


def cekSinkronLokal(bjdt_id):
    try:

        config = configparser.RawConfigParser()
        fileConfig = "config.cnf"
        config.read(fileConfig)
        datab = config.get("data", "database")
        hosted = config.get("data", "host")
        login = config.get("data", "user")
        passed = config.get("data", "password")
        conn = f"dbname={datab} user={login} host={hosted} password={passed}"
        konekdb = psycopg2.connect(conn)
        konekdb.autocommit = True
        kursor = konekdb.cursor()
        SQL = """ SELECT sinkron FROM pengujian
		WHERE idbendauji = %s ; """
        data = (bjdt_id,)
        kursor.execute(SQL, data)
        daftar = kursor.fetchone()
        kursor.close()
        konekdb.close()
        # print daftar
        return daftar
    except Exception as e:
        logging.error(
            "Error pada saat memanggil method cekSinkronLokal() pada file daemonSink.py : %s",
            str(e),
        )
        # print str(e)


def sinkUpdateLokal(nomer, urut):
    try:
        config = configparser.RawConfigParser()
        fileConfig = "config.cnf"
        config.read(fileConfig)
        datab = config.get("data", "database")
        hosted = config.get("data", "host")
        login = config.get("data", "user")
        passed = config.get("data", "password")
        conn = f"dbname={datab} user={login} host={hosted} password={passed}"
        konekdb = psycopg2.connect(conn)
        konekdb.autocommit = True
        kursor = konekdb.cursor()
        # Perintah update disini
        SQL = """ UPDATE pengujian SET sinkron = 'S'
			WHERE noDocket = %s AND noUrutBenda = %s; """
        data = (
            nomer,
            urut,
        )
        kursor.execute(SQL, data)
        kursor.close()
        konekdb.close()

    except Exception as e:
        logging.error(
            "Error pada saat memanggil method sinkUpdateLokal() pada file daemonSink.py : %s",
            str(e),
        )
        # print str(e)


# isSinkron = 'S'
# return isSinkron


def kirimDataPost(bendaUji):

    fileConfig = "config.cnf"
    config = configparser.RawConfigParser()
    config.read(fileConfig)
    urlKirim = config.get("webser", "webser_hasilUji")
    config.get("webser", "http_user")
    config.get("webser", "http_pass")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    # print "URL : ", urlKirim
    datanya = {"params": {}}
    datanya["params"]["bjdt_tgl_test"] = str(bendaUji[0])
    datanya["params"]["bjdt_beban"] = float(bendaUji[1])
    datanya["params"]["bjdt_berat"] = float(bendaUji[2])
    datanya["params"]["bjdt_tipe_retak"] = bendaUji[3]
    datanya["params"]["bjdt_id"] = int(bendaUji[4])
    datanya["params"]["bjdt_beban_mpa"] = float(bendaUji[8])
    datanya["params"]["bjdt_beban_kg"] = str(bendaUji[9])
    datanya["params"]["bjdt_umur"] = int(bendaUji[10])

    # print "Data Benda Uji yang akan di kirim ke Webservice ERP : ", nilai
    # data = urllib.urlencode(nilai)
    # print urlKirim
    # print "Data yang di Post  : ", datanya

    try:
        return requests.post(urlKirim, json=datanya)
    except requests.HTTPError as e:
        logging.error(
            "Server tidak dapat memenuhi permintaan proses. Kode Error : %s", e.response.status_code
        )
        # print 'Kode Error: ', e.code
        # print 'Server tidak dapat memenuhi permintaan proses'
    except requests.ConnectionError as e:
        logging.error("Gagal menyambungkan ke server. Error: %s", str(e))
        # print('Gagal menyambungkan ke server.')
        # print('Alasan : ', str(e))


fileConfig = "config.cnf"
config = configparser.RawConfigParser()
config.read(fileConfig)
tunda = config.get("webser", "delay")
# daemon = threadSinkData(1, "ThreadSinkron", float(tunda))
# daemon.start()
