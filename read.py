import subprocess
import random
import sys
import csv
import time


ips = ['[2001:648:2ffe:501:cc00:10ff:fead:aa9c]', '[2001:648:2ffe:501:cc00:10ff:fead:aa9c]',
'[2001:648:2ffe:501:cc00:12ff:fe98:a535]', '[2001:648:2ffe:501:cc00:12ff:fe98:a535]',
'[2001:648:2ffe:501:cc00:11ff:fe56:ca8d]', '[2001:648:2ffe:501:cc00:11ff:fe56:ca8d]',
'[2001:648:2ffe:501:cc00:10ff:fe2e:3b6c]', '[2001:648:2ffe:501:cc00:10ff:fe2e:3b6c]',
'[2001:648:2ffe:501:cc00:12ff:fe45:4cf9]', '[2001:648:2ffe:501:cc00:12ff:fe45:4cf9]']

ports = [1024,1025,1050,1025,1060,1025,1090,1100,1031,1036]

ips = ['localhost']
ports = [1024]

class Address:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

addrs = [Address(ip,port) for ip,port in zip(ips,ports)]

filename = sys.argv[1]

start = time.time()

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row,i in zip(csvreader, range(100)):
        rand_addr = random.choice(addrs)
        list_files = subprocess.run(["chordy", f"--ip={rand_addr.ip}", f'--port={rand_addr.port}', 'insert', f'-k={row[0]}', f'-v={row[1]}'])

end = time.time()
print(end - start)

