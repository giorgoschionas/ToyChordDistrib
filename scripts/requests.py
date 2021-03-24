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

ips = [
'192.168.0.5', '192.168.0.5', 
'192.168.0.1', '192.168.0.1',
'192.168.0.3', '192.168.0.3',
'192.168.0.4', '192.168.0.4',
'192.168.0.6', '192.168.0.6'
]

ports = [1024,1025,1026,1027,1028,1029,1030,1031,1032,1033]

class Address:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

addresses = [Address(ip,port) for ip, port in zip(ips,ports)]

filename = sys.argv[1]

start = time.time()
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rand_addr = random.choice(addresses)
        if row[0] == 'insert':
            list_files = subprocess.run(["chordy", f"--ip={rand_addr.ip}", f'--port={rand_addr.port}', 'insert', f'-k={row[1]}', f'-v={row[2]}'])
        elif row[0] == 'query':
            list_files = subprocess.run(["chordy", f"--ip={rand_addr.ip}", f'--port={rand_addr.port}', 'query', f'-k={row[1]}'])
        else:
            print("ERROR: Unknown command")
            exit(0)
end = time.time()
print(end - start)
