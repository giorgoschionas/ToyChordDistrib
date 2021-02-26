import socket
import chord 

def main():
    local_ip = socket.gethostbyname(socket.gethostname())
    chordy = chord.Chord(10, local_ip, 1024)
    # TODO: start server

if __name__ == '__main__':
    main()