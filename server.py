import socket
import threading
#import ssl

def run_client(socket_client, list_clients, usernames):
  username = socket_client.recv(1024).decode()
  usernames[socket_client] = username

  for client in list_clients:
    if client is not socket_client:
      client.sendall(f"\n[+] El usuario {username} ha entrado al chat\n".encode())

  while True:
    try:
      message = socket_client.recv(1024).decode()

      if message == "!users":
        socket_client.sendall(f"\nLista de usuarios disponibles: {', '.join(usernames.values())}\n".encode())
        continue

      if message:
        for client in list_clients:
          if client is not socket_client:
            client.sendall(f"{message}\n".encode())
    except:
      break

  socket_client.close()
  list_clients.remove(socket_client)
  del usernames[socket_client]

def start_server():

  list_clients = []
  usernames = {}

  HOST = 'localhost'
  PORT = 12346

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #TIME_WAIT
    socket_server.bind((HOST, PORT))
    #socket_server = ssl.wrap_socket(socket_server, keyfile="server-key.key", certfile="server-cert.pem", server_side=True)
    print(f"Servidor a la escucha en: HOST->{HOST} y PORT->{PORT}")  
    socket_server.listen()

    while True:
      socket_client, socket_client_info = socket_server.accept()
      print(f"Se ha conectado un nuevo cliente -> {socket_client_info}")
      list_clients.append(socket_client)
      new_thread = threading.Thread(target=run_client, args=(socket_client, list_clients, usernames))
      new_thread.daemon = True
      new_thread.start()


if __name__ == "__main__":
    start_server()