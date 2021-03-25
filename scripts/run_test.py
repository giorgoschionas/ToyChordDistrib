import subprocess
import random
import sys
import csv
import time
import yaml

class Address:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

def insertTest(testFilename, addresses):
    start = time.time()
    with open(testFilename, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            randomAddress = random.choice(addresses)
            result = subprocess.run(["chordy", f"--ip={randomAddress.ip}", f'--port={randomAddress.port}', 'insert', f'-k={row[0]}', f'-v={row[1]}'])
    end = time.time()
    print(end - start)

def queryTest(testFilename, addresses):
    start = time.time()
    with open(testFilename, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            randomAddress = random.choice(addresses)
            result = subprocess.run(["chordy", f"--ip={randomAddress.ip}", f'--port={randomAddress.port}', 'query', f'-k={row[0]}'])
    end = time.time()
    print(end - start)

def requestsTest(testFilename, addresses):
    start = time.time()
    with open(testFilename, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            randomAddress = random.choice(addresses)
            if row[0] == 'insert':
                result = subprocess.run(["chordy", f"--ip={randomAddress.ip}", f'--port={randomAddress.port}', 'insert', f'-k={row[1]}', f'-v={row[2]}'])
            elif row[0] == 'query':
                result = subprocess.run(["chordy", f"--ip={randomAddress.ip}", f'--port={randomAddress.port}', 'query', f'-k={row[1]}'])
            else:
                print("ERROR: Unknown command")
                exit(0)
    end = time.time()
    print(end - start)

#--------------------------------------------------------------------------------------------------------------------------

def insertTestSimple(testFilename, addresses):
    start = time.time()
    with open(testFilename, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            randomAddress = random.choice(addresses)
            result = subprocess.run(["python3", "client_simple/simple_client.py", "insert", f"{randomAddress.ip}", f'{randomAddress.port}', f'{row[0]}', f'{row[1]}'])
    end = time.time()
    print(end - start)
    

def queryTestSimple(testFilename, addresses):
    start = time.time()
    with open(testFilename, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            randomAddress = random.choice(addresses)
            result = subprocess.run(["python3", "client_simple/simple_client.py", "query", f"{randomAddress.ip}", f'{randomAddress.port}', f'{row[0]}'])
    end = time.time()
    print(end - start)

def requestsTestSimple(testFilename, addresses):
    start = time.time()
    with open(testFilename, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            randomAddress = random.choice(addresses)
            if row[0] == 'insert':
                result = subprocess.run(["python3", "client_simple/simple_client.py", "insert", f"{randomAddress.ip}", f'{randomAddress.port}', f'{row[1]}', f'{row[2]}'])
            elif row[0] == 'query':
                result = subprocess.run(["python3", "client_simple/simple_client.py", "query", f"{randomAddress.ip}", f'{randomAddress.port}', f'{row[1]}'])
            else:
                print("ERROR: Unknown command")
                exit(0)
    end = time.time()
    print(end - start)

#--------------------------------------------------------------------------------------------------------------------------

def main(argv):
    if len(argv) < 3 or len(argv) > 4:
        print('Usage: run_test.py [test] [server-location] {client}')
        exit(0)

    test = argv[1]
    location = argv[2]
    
    # Select client
    # Default client is chordy
    client = 'chordy'
    if len(argv) == 4:
        if argv[3] == 'simple':
            client = 'simple'
        elif argv[3] == 'chordy':
            client = 'chordy'
        else:
            print('Unknown client')
            exit(0)

    config = config = yaml.safe_load(open("config.yaml"))

    # Load servers
    if location == 'local':
        serverList = config['local_servers']
    elif location == 'remote-private':
        serverList = config['remote_private_servers']
    elif location == 'remote-public':
        serverList =  config['remote_public_servers']
    else:
        print('Please choose one of: local, remote-private, remote-public')
        exit(0)

    addresses = list()
    for serverAddress in serverList:
        addresses.append(Address(serverAddress['ip'], serverAddress['port']))

    # Read test filename from configuration
    filename = config['test'][test]

    # Run test based on client
    if client == 'chordy':
        if test == 'insert':
            insertTest(filename, addresses)
        elif test == 'query':
            queryTest(filename, addresses)
        elif test == 'requests':
            requestsTest(filename, addresses)
        else:
            print('Unknown test')
            exit(0)
    elif client == 'simple':
        if test == 'insert':
            insertTestSimple(filename, addresses)
        elif test == 'query':
            queryTestSimple(filename, addresses)
        elif test == 'requests':
            requestsTestSimple(filename, addresses)
        else:
            print('Unknown test')
            exit(0)            
    else:
        print('Unknown client')
        exit(0)        

if __name__ == "__main__":
    main(sys.argv)

