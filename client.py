#import ssl
import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText

def send_message(client_socket, usuario, text_widget, entry_widget):
  message = entry_widget.get()
  client_socket.sendall(f"{usuario} > {message}".encode())

  entry_widget.delete(0, END)
  text_widget.configure(state='normal')
  text_widget.insert(END, f"{usuario} > {message}\n")
  text_widget.configure(state='disabled')

def recv_message(client_socket, text_widget):
  while True:
    try:
      message = client_socket.recv(1024).decode()
      if message:
        text_widget.configure(state='normal')
        text_widget.insert(END, message)
        text_widget.configure(state='disabled') 

    except:
      break

def list_users_request(client_socket):
  client_socket.sendall("!users".encode())

def exit_connection(client_socket, usuario, window):
  client_socket.sendall(f"El usuario {usuario} ha abandonado el chat.".encode())
  client_socket.close()
  window.quit()
  window.destroy()

def start_client():

  server_host = 'localhost'
  server_port = 12346

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    try:
      #client_socket = ssl.wrap_socket(client_socket)
      client_socket.connect((server_host, server_port))
    except Exception:
      print("No se pudo establecer la conexion con el servidor")
    else:
      usuario = input("Digite su nombre de usuario: ")
      client_socket.sendall(usuario.encode())

      window = Tk()
      window.title("Chat")

      text_widget = ScrolledText(window, state='disabled')
      text_widget.pack(padx=5, pady=5)

      frame_widget = Frame(window)
      frame_widget.pack(padx=5, pady=5, fill=BOTH, expand=1)

      entry_widget = Entry(frame_widget)
      entry_widget.bind("<Return>", lambda _: send_message(client_socket, usuario, text_widget, entry_widget))
      entry_widget.pack(padx=5, pady=5, fill=BOTH, expand=1)

      button_widget = Button(frame_widget, text="Enviar", command= lambda: send_message(client_socket, usuario, text_widget, entry_widget))
      button_widget.pack(side=RIGHT, padx=5)

      users_widget = Button(window, text="Listar Usuarios", command= lambda: list_users_request(client_socket))
      users_widget.pack(padx=5, pady=5)

      exit_widget = Button(window, text="Salir", command= lambda: exit_connection(client_socket, usuario, window))
      exit_widget.pack(padx=5, pady=5)

      new_thread = threading.Thread(target=recv_message, args=(client_socket, text_widget))
      new_thread.daemon = True
      new_thread.start()

      window.mainloop()


if __name__ == "__main__":
    start_client()
