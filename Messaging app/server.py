#import necessary stuff
import socket
import threading
import tkinter as tk

root=tk.Tk()
root.geometry("600x600")
root.title("Messenger demo")
root.resizable(False,False)

top_frame=tk.Frame(root,width=600,height=100)
middle_frame=tk.Frame(root,width=600,height=400)
bottom_frame=tk.Frame(root,width=600,height=100)



HOST='127.0.0.1'
PORT=1234
LISTENER_LIMIT=5;
active_clients=[]

def listen_for_messages(client,username):
    while 1:
        response=client.recv(2048).decode('utf-8')
        if response!='':
            final_msg=username+"-"+response
            send_messages_to_all(final_msg);
        else:
            print(f"message from client {username} is empty")

def send_message_to_client(client,message):
    client.sendall(message.encode())

#function to send any new message to all the clients connected to server
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1],message)


# function to handle client
def client_handler(client):  
    while 1:
        username=client.recv(2048).decode('utf-8');
        if username!='':
            active_clients.append((username,client))
            msg="SERVER~"+f"{username} added to the chat"
            send_messages_to_all()
            break
        else:
            print("client username is empty")

    threading.Thread(target=listen_for_messages,args=(client,username,)).start()
 
def main():

    root.mainloop()  

    # AF_INET: we r using IPv4 addresses
    # SOCK_STREAM/; we r using tcp packets for communication
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        server.bind((HOST,PORT)) 
        print(f"running the server on {HOST} {PORT}")
    
    except:
        print("unable to bind to host {HOST} and port {PORT}")

    #set server limit
    server.listen(LISTENER_LIMIT)

    #this while loop will keep listening to client connections
    while 1:
        client,address=server.accept()
        print(f"successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler,args=(client,)).start()




if __name__ == '__main__':

    main()