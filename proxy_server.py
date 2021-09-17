#!/usr/bin/env python3
import socket, time, sys
from multiprocessing import Process, Queue

def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('hostname could not be resolved, Exiting')
        sys.exit()
    print(f'Ip address of {host} is {remote_ip}')
    return remote_ip

def handle_request(conn, addr, extern_host, PORT):
    print("Connected by", addr)            
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
        print('connecting to google')
        remote_ip = get_remote_ip(extern_host)
        proxy_end.connect((remote_ip, PORT))
        
        send_full_data = conn.recv(BUFFER_SIZE)
        print(f"Sending recieved data {send_full_data} to google")
        
        proxy_end.shutdown(socket.SHUT_WR)
        
        data = proxy_end.recv(BUFFER_SIZE)
        conn.send(data)
        conn.close()

def main():
    HOST = "localhost"
    BUFFER_SIZE = 1024    
    extern_host = 'www.google.com'
    PORT = 8001
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #bind socket to address
        proxy_start.bind((HOST, PORT))
        #set to listening mode
        proxy_start.listen(1)        
        while True:
            conn, addr = proxy_start.accept()
            #now for the multiprocesssing...
            p = Process (target=handle_request, args=( conn, addr, extern_host, PORT))
            p.start()
            
            
if __name__ == "__main__":
    main()
