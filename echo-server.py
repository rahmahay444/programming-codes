# echo-server.py



# first of all import the socket library 
import socket			 

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		

# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests 
# coming from other computers on the network 
s.bind((HOST, PORT))
s.listen()

	 
print ("socket binded to %s" %(PORT)) 

print ("socket is listening....")		 

# a forever loop until we interrupt it or 
# an error occurs 
while True: 

    # Establish connection with client. 
    con, addr = s.accept()	 
    print ('Got connection from', addr )

    # send a thank you message to the client. encoding to send byte type. 
    con.send(b"Thank you for connecting...sent by server")

    #receive data from client and print it
    data = con.recv(1024) 
    print(f"Received {data!r}")

    # Close the connection with the client 
    con.close()

    # Breaking once connection closed
    break


# Use "netstat -an" command to show the service at cmd...