import echo_util
import threading
import compareAction
import time
HOST = echo_util.HOST
PORT = echo_util.PORT

def Diff(li1, li2):
    return (list(set(li1) - set(li2)))

def handle_client(sock, addr):
    """ Receive data from the client via sock and echo it back """
    while True:
        try:
            msg = echo_util.recv_msg(sock) # Blocks until received
            # complete message
            print('{}: {}'.format(addr, msg))
            array1 = compareAction.bigFunction(msg)
            time.sleep(60)
            array2 = compareAction.bigFunction(msg)
            print(Diff(array2,array1))
            echo_util.send_msg(sock, msg) # Blocks until sent
        except (ConnectionError, BrokenPipeError):
            print('Closed connection to {}'.format(addr))
            sock.close()
            break

listen_sock = echo_util.create_listen_socket(HOST, PORT)
addr = listen_sock.getsockname()
print('Listening on {}'.format(addr))
while True:
    client_sock, addr = listen_sock.accept()
    # Thread will run function handle_client() autonomously
        # and concurrently to this while loop
    thread = threading.Thread(target = handle_client, args = [client_sock, addr], daemon=True)
    thread.start()
    print('Connection from {}'.format(addr))
