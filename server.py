import socket
import threading

host = '192.168.56.107'
port = 8888

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((' ', port))

server.listen()

clients = []
nicknames = []

def boradcast(message):
  for client in clients:
    print(message)

def handle(client):
  while True:
    try:
      position = client.recv(1024)
      
    except:
      index = clients.index(client)
      clients.remove(client)
      client.close()
      nickname = nicknames[index]
      broadcast('{ } left.'.format(nickname).encode('ascii'))
      nicknames.remove(nickname)
      break
      
 def receive():
  while True:
    client, address = server.accept()
    print("Connected to { }".format(str(address)))
    
    client.send('NICK'.encode('ascii'))
    nickname = client.recv(1024).decode('ascii')
    nicknames.append(nickname)
    clients.append(client)
    
    print("Nickname joined: { }".format(nickname))
    broadcast("{ } joined the game!".format(nickname).encode('ascii'))
    client.send('Connected to server!'.encode('ascii'))
    
    thread = threading.Thread(target=handle, args=(client,))
    thread.start()
 
print("Server is listening...")
receive()
