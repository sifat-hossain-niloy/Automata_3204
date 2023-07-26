import socket
import threading
import rsa

# Name :  Md. Sifat Hossain
# Roll : 17
#creating a one time public and private key for each client
public_key,private_key = rsa.newkeys(1024)

#partner's public key to encrypt the message before sending to the partner
partner_public_key = None

type = input("Create a room (1) or Join a Chat (2)\n")

if type  == "1" : 
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # TCP Connection
    server.bind(("192.168.0.110",5001))
    server.listen()

    client,_ = server.accept()

    #interchanging each other's public key
    # server first sends it's public key
    client.send(public_key.save_pkcs1("PEM"))
    partner_public_key = rsa.PublicKey.load_pkcs1(client.recv(1024))

elif  type == "2":
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(("192.168.0.110",5001))

    #client first receives the partners public key
    partner_public_key = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))

else : 
    exit()


def send_message(c):
    while True:
        message = input("")
        #encrypting the message using partners public key
        c.send(rsa.encrypt(message.encode(),partner_public_key))
        print("You: ", message)

def receive_message(c):
    while True:
        #decrypting the message received from the partner
        print("Friend: ", rsa.decrypt(c.recv(1024),private_key).decode())

threading.Thread(target=send_message,args=(client,)).start()

threading.Thread(target=receive_message,args=(client,)).start()

