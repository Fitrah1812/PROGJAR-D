import random
import json
import logging
import threading
import sys
import socket
import xmltodict
import ssl
import os
import datetime

server_address = ('172.16.16.101', 20000)

def make_socket(destination_address='localhost',port=12000):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination_address, port)
        logging.warning(f"connecting to {server_address}")
        sock.connect(server_address)
        return sock
    except Exception as ee:
        logging.warning(f"error {str(ee)}")

def make_secure_socket(destination_address='localhost',port=10000):
    try:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.verify_mode=ssl.CERT_OPTIONAL
        context.load_verify_locations(os.getcwd() + '/domain.crt')

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination_address, port)
        # logging.warning(f"connecting to {server_address}")
        sock.connect(server_address)
        secure_socket = context.wrap_socket(sock,server_hostname=destination_address)
        # logging.warning(secure_socket.getpeercert())
        return secure_socket
    except Exception as ee:
        logging.warning(f"error {str(ee)}")

def deserialisasi(s):
    # logging.warning(f"deserialisasi {s.strip()}")
    return json.loads(s)
    

def send_command(command_str,is_secure=False):
    alamat_server = server_address[0]
    port_server = server_address[1]
#    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# gunakan fungsi diatas
    if is_secure:
        sock = make_secure_socket(alamat_server,port_server)
    else:
        sock = make_socket(alamat_server,port_server)

    # logging.warning(f"connecting to {server_address}")
    try:
        # logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received="" #empty string
        while True:
            #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                #data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
        hasil = deserialisasi(data_received)
        # logging.warning("data received from server:")
        return hasil
    except Exception as ee:
        # logging.warning(f"error during data receiving {str(ee)}")
        return False


def getdatapemain(nomor=0,is_secure=False):
    cmd=f"getdatapemain {nomor}\r\n\r\n"
    hasil = send_command(cmd,is_secure=is_secure)
    if hasil:
        print("Detail Pemain");
        print(f"nomor : {hasil['nomor']}, nama : {hasil['nama']},  posisi : {hasil['posisi']} ")
    else:
        print(f"gagal mendapatkan data pemain nomor {nomor}")
    # return hasil

def getDataPemainRequest(request_data, is_secure=False):
    for i in range(request_data):
        getdatapemain(random.randint(1,10), is_secure);

def cek_serialisasi(a):
    #print(a)
    #serialized = str(dicttoxml.dicttoxml(a))
    serialized =  json.dumps(a)
    logging.warning("serialized data")
    logging.warning(serialized)
    return serialized

def test_thread(sum_thread=1, is_secure=False,request_awal=1):
    texec = dict()
    check_time = datetime.datetime.now()
    #start
    for i in range(sum_thread):
        texec[i] = threading.Thread(target=getDataPemainRequest,args=(request_awal, is_secure))
        texec[i].start()

    #join
    for i in range(sum_thread):
        texec[i].join()

    after_check_time = datetime.datetime.now()
    sum_time = after_check_time-check_time

    print(
        f"Jumlah Thread {sum_thread}, Jumlah Request {request_awal}, Jumlah Response {sum_thread*request_awal} dan Waktu {sum_time} ms")

def lihatversi(is_secure=False):
    cmd=f"versi \r\n\r\n"
    hasil = send_command(cmd,is_secure=is_secure)
    return hasil

if __name__=='__main__':
    a = 1
    b = 5
    c = 10
    d = 20

    test_thread(c,True,1)