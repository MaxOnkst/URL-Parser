import os
import re
from OnkstAS1socket import TCPsocket
from OnkstAS1request import Request
from OnkstAS1parser import URLparser
from queue import Queue
import requests
import time


def main():

    #EVERYTHING COMMENTED IS FROM ASSIGNMENT 1
    #----------------------------------------------
    #host = input("Enter URL: ")

    #mysocket = TCPsocket()
    #mysocket.createSocket()

    #hostname, port, path, query = URLparser.parse(mysocket,host)
    #print("Parsing URL... host:",hostname, " port:", port, "request: ", query)


    #print("Doing DNS...")
    #time1 = time.time()*1000
    #ip = mysocket.getIP(hostname)
    #time2 = time.time()*1000
    #DNStime = round(time2-time1)
    #print("Done in", DNStime, "ms, found", ip)

    #print("Connecting on page...")
    #time3 = time.time()*1000
    #mysocket.connect(ip, port)
    #time4 = time.time()*1000
    #connectTime = round(time4-time3)
    #print("Done in", connectTime, "ms")

    #myrequest = Request()
    #msg = myrequest.headRequest(hostname)

    #print("Loading...")
    #time5 = time.time()*1000
    #mysocket.send(msg)
    #data, bytes = mysocket.receive()
    #time6 = time.time() * 1000
    #print("Done in", round(time6 - time5), " ms")
    #print("With", bytes, " bytes")



    #print("--------------------")
    #print(data.decode())
    #print("--------------------")

    #---------------------------------------------------------------------
    #ASSIGNMENT 2
    Q = Queue()
    ps = URLparser
    r = Request()
    ws = TCPsocket()

    seenHosts = set()
    seenHostsIP = set()
    try:
        with open("URL-input-100.txt") as file:
            file_size = os.path.getsize("URL-input-100.txt")
            for line in file:
                Q.put(line)
        print("file size: ", file_size, " bytes")
        file.close()
    except IOError:
        print('No such file')
        exit(1)

    count = 0
    while not Q.empty():
        ws.createSocket()
        url = Q.get()
        count += 1
        print("----------------------------------------")
        print(count)
        print("url: ", url)
        host, port, path, query = ps.parse(ws,url)
        newHost = host
        prevSize = len(seenHosts)
        seenHosts.add(newHost)
        if len(seenHosts) > prevSize:
            print("Checking host uniqueness... passed")
        else:
            print("Checking host uniqueness... failed")
            continue

        ip = ws.getIP(host)
        if ip is None:
            continue
        newHostIP = ip
        prevSizeIP = len(seenHostsIP)
        seenHostsIP.add(newHostIP)
        if len(seenHostsIP) > prevSizeIP:
            print("Checking IP uniqueness... passed")
        else:
            print("Checking IP uniqueness... failed")
            continue

        timeConnect = time.time()*1000
        ws.connect(ip, port)
        timeConnect2 = time.time()*1000
        if round(timeConnect2-timeConnect) >= 10000:
            continue
        print("Connecting on robots... done in ",round(timeConnect2-timeConnect), " ms")


        time1 = time.time()*1000
        msg = r.headRequest(host)
        ws.send(msg)
        try:
            data, bytes = ws.receive()
            info = data.decode()
            status = info[9:12]
            firstNum = info[9]
        except:
            continue
        time2 = time.time()*1000
        if round(time2-time1) > 9999: #if receive timeout
            print("Error: slow download")
            continue
        print("Loading... done in", round(time2-time1)," ms with", bytes, " bytes")
        print("Verifying header... status code", status)
        ws.close()
        ws.createSocket()
        if firstNum == "4":
            time3 = time.time()*1000
            ws.connect(ip, port)
            time4 = time.time()*1000
            print("*    Connecting on page... done in ", round(time4-time3), " ms")


            msg2 = r.getRequest(host, path, query)
            time5 = time.time()*1000
            ws.send(msg2)
            try:
                data2, bytes2 = ws.receive()
                time6 = time.time()*1000
                status2 = data2.decode()[9:12]
                print("     Loading... done in", round(time6-time5)," ms with", bytes, " bytes")
                print("     Verifying header... status code", status2)
            except:
                print("     Error connecting to page")
                continue
            time7 = time.time()*1000
            page = requests.get(url)
            text = page.text
            links = re.findall("href=[\"\'](.*?)[\"\']", text)
            time8 = time.time()*1000
            print("+    Parsing page... done in", round(time8-time7), " ms with", len(links), " links")
        ws.close()

if __name__ == '__main__':
    main()


