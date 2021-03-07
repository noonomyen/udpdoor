# -*- coding: utf-8 -*-

"""
            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2021 NooNomYen <noonomyenmail@gamil.com>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
"""

# User Datagram Protocol Door - Socket
# UDP Door Version 1.0 16112020
# Author : NooNomYen
# Github : https://github.com/noonomyen

import time
import sys
import datetime
import threading
import socket

if __name__ != "__main__":
    exit()

help_ = ("""UserDatagramProtocolDoor Version 1.0 16112020
[InputIP:Port] [OutputIP:PortStart-PortEnd] [ConnectIP:Port] [Timeout socket]
Use Ctrl+C to stop.""")

if len(sys.argv) != 5:
    print(help_)
    exit()

def check_ip(ip):
    ip = ip.split(".")
    if len(ip) != 4:
        return True;
    for i in range(4):
        ii = int(ip[i])
        if ii < 0 or ii > 255:
            return True;
    return False;

def check_port(port):
    if port > 65535 or port < 0:
        return True;
    return False;

try:
    er = 1
    argv = sys.argv[1].split(":")
    inip = argv[0]
    if check_ip(inip):
        exit()
    er = 2
    inport = int(argv[1])
    if check_port(inport):
        exit()
    er = 3
    argv = sys.argv[2].split(":")
    outip = argv[0]
    if check_ip(outip):
        exit()
    er = 4
    argv = argv[1].split("-")
    argv = [int(argv[0]), int(argv[1])]
    outport = []
    
    for i in range(argv[1] - argv[0] + 1):
        outport.append(argv[0] + i)
        if check_port(outport[-1]):
            exit()

    er = 5
    argv = sys.argv[3].split(":")
    cnip = argv[0]
    if check_ip(cnip):
        exit()
    er = 6
    cnport = int(argv[1])
    del argv
    if check_port(cnport):
        exit()
    er = 7
    tos = float(sys.argv[4])
    if tos <= 0:
        exit()
    er = 0
except:
    if er == 0:
        pass
    elif er == 1:
        print("Error : Input IP !")
        print(help_)
        exit()
    elif er == 2:
        print("Error : Input Port !")
        print(help_)
        exit()
    elif er == 3:
        print("Error : Output IP !")
        print(help_)
        exit()
    elif er == 4:
        print("Error : Output Port !")
        print(help_)
        exit()
    elif er == 5:
        print("Error : Connect To IP !")
        print(help_)
        exit()
    elif er == 6:
        print("Error : Connect To Port !")
        print(help_)
        exit()
    elif er == 7:
        print("Error : Set Timeout !")
        print(help_)
        exit()

def create_socket_output(outip, outport, tos):
    global socket_output
    try:
        for i in range(len(outport)):
            print("[" + getdate() + "] Start socket UDP Port : " + str(outport[i]))
            socket_output.append([socket.socket(socket.AF_INET, socket.SOCK_DGRAM), None, 0])
            socket_output[-1][0].bind((outip, outport[i]))
            socket_output[-1][0].settimeout(tos)
    except:
        close_socket_output()
        print("Error : Can't start socket UDP Port : " + str(outport[i]) + " !")
        enddate()
        exit()

def close_socket_output():
    global socket_output
    for i in range(len(socket_output)):
        socket_output[i][0].close()
        print("[" + getdate() + "] Close socket UDP Port : " + str(outport[i]) + " !")

def socket_input_work(cnip, cnport):
    global socket_input
    global socket_output
    global workload
    global insizepkps
    global incps
    global log
    global swover

    lensocket = len(socket_output)

    while workload:
        try:
            data, addr = socket_input.recvfrom(65535)
            for i in range(lensocket):
                if socket_output[i][1] == addr:
                    socket_output[i][0].sendto(data, (cnip, cnport))
                    insizepkps += sys.getsizeof(data)
                    incps += 1
                    break
                elif socket_output[i][1] == None:
                    socket_output[i][1] = addr
                    socket_output[i][0].sendto(date, (cnip, cnport))
                    log.append([0, addr])
                    break
                if (i+1) == lensocket and swover == 0:
                    swover = 1
                    log.append([4, addr])
        except socket.timeout:
            for i in range(lensocket):
                if socket_output[i][2] == 1:
                    log.append([2, socket_output[i][1]])
                    socket_output[i][1] = None
                    socket_output[i][2] = 0
        except:
            pass

def socket_output_work(idw, a):
    global socket_input
    global socket_output
    global workload
    global outsizepkps
    global outcps
    global log

    while workload:
        try:
            data, addr = socket_output[idw][0].recvfrom(65535)
            if socket_output[idw][1] != None:
                socket_input.sendto(data, socket_output[idw][1])
                outsizepkps += sys.getsizeof(data)
                outcps += 1
                if socket_output[idw][2] == 1:
                    socket_output[idw][2] = 0
                    log.append([3, socket_output[idw][1]])
        except socket.timeout:
            if socket_output[idw][1] != None:
                socket_output[idw][2] = 1
                log.append([1, socket_output[idw][1]])
        except:
            pass

def getdate():
    return str(datetime.datetime.now()).split(".")[0].split(" ")[1];

def enddate():
    global worktime
    t = (time.time() -worktime)
    h = ""
    m = ""
    if t > 3600:
        h = t // 3600
        h = " " + str(int(h)) + " hour"
        t = t % 3600
    if t > 60:
        m = t // 60
        m = " " + str(int(m)) + " minute"
        t = t % 60
    t = " " + ("%.5f" % t)
    print("The system runs for" + h + m + t + " second.")

def show_action():
    global log
    global insizepkps
    global incps
    global outsizepkps
    global outcps
    global socket_output
    global swover
    lensocket = len(socket_output)
    is0 = 0
    ic0 = 0
    os0 = 0
    oc0 = 0
    swover = 0

    while True:
        is0 = insizepkps
        insizepkps = insizepkps - is0
        ic0 = incps
        incps = incps - ic0
        os0 = outsizepkps
        outsizepkps = outsizepkps - os0
        oc0 = outcps
        outcps = outcps - oc0
        on = 0
        for i in range(lensocket):
            if socket_output[i][1] != None:
                on += 1
        print("[" + getdate() + "] SIN[" + str(is0) + "] SOUT[" + str(os0) + "] CIN[" + str(ic0) + "] COUT[" + str(oc0) + "] USE[" + str(on) + "/" + str(lensocket) + "]")
        if len(log) == 0:
            time.sleep(1)
        else:
            t = time.time()
            while True:
                if log[0][0] == 0:
                    print("[" + getdate() + "] New IP connect " + str(log[0][1]))
                    del log[0]
                elif log[0][0] == 1:
                    print("[" + getdate() + "] Server timeout " + str(log[0][1]))
                    del log[0]
                elif log[0][0] == 2:
                    print("[" + getdate() + "] Close connect " + str(log[0][1]))
                    del log[0]
                elif log[0][0] == 3:
                    print("[" + getdate() + "] Come back online " + str(log[0][1]))
                    del log[0]
                elif log[0][0] == 4:
                    print("[" + getdate() + "] Connect beyond the limit " + str(log[0][1]) + " !!!")
                    del log[0]
                if time.time() -t >= 1 or len(log) == 0:
                    break

worktime = time.time()
datestart = str(datetime.datetime.now()).split(".")[0].split(" ")
print("START User Datagram Protocol Door " + datestart[1])

print("START SOCKET INPUT " + ("-" * 31))
try:
    print("[" + getdate() + "] Start socket UDP [" + str(inip) + ":"  + str(inport)  +  "]")
    socket_input = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_input.bind((inip, inport))
    socket_input.settimeout(tos)
except:
    socket_input.close()
    print("Error : Start socket Input !")
    enddate()
    exit()

print("START SOCKET OUTPUT " + ("-" * 30))
socket_output = []
create_socket_output(outip, outport, tos)

print("-" * 50)

workload = 1
log = []
insizepkps = 0
incps = 0
outsizepkps = 0
outcps = 0
swover = 0

print("[" + getdate() + "] Start thread socket input")
tsi = threading.Thread(target=socket_input_work, args=(cnip, cnport))
tsi.start()
print("-" * 50)
tso = []
for i in range(len(socket_output)):
    print("[" + getdate() + "] Start thread socket output [" + str(outip) + ":" + str(outport[i]) + "]")
    tso.append(threading.Thread(target=socket_output_work, args=(i, 0)))
    tso[-1].start()

print("-" * 50)
while True:
    try:
        show_action()
    except KeyboardInterrupt:
        k = input("Want to stop the system ? [Y/N] : ")
        if k == "Y" or k == "y" or k == "Yes" or k == "yes":
            break

print("-" * 50)
print("Is about to stop working after the time expires !")
workload = 0
socket_input.close()
tsi.join()
print("[" + getdate() + "] Stop thread and socket input !")
close_socket_output()
print("[" + getdate() + "] Stop thread socket input [" + str(inip) + ":" + str(inport) + "] !")
for i in range(len(socket_output)):
    tso[i].join()
    print("[" + getdate() + "] Stop thread socket output [" + str(outip) + ":" + str(outport[i]) + "] !")

print("-" * 50)
enddate()
print("-" * 50)

