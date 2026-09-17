# snek_socket
A basic client-server model using a socket, implemented in python

For this assignment you are to implement both a TCP server and a TCP client piece of software. You may use any high level language that provides built in networking support.

# Our version uses TCP in python
 

The server is to accept a connection from a client and receive a text message of no more than 256 characters. It will convert the message to an encoded message as detailed next. Your server will convert each character by replacing it with the next character in the ASCII sequence. For example the message: “Hello World” would become “Ifmmp!Xpsme”

 # It does that

You must also write a client that will connect to the server using the same port and then pass a message to the server. The server will respond with the message converted to the encoded string. The client will then display the converted message to the monitor.

 # It does that

For those of you looking for an extra challenge, you may pass a flag to the server so that it may either encode or decode a message. This task is entirely optional, but should not add much complexity to the server.

# We did that, but it did add complexity
 

Both programs need to perform a reasonable amount of error checking, be well documented, and include a set of user instructions. Upon an error, issue an appropriate error message and then continue.

# It doesn't do that, it needs to do that. 
 

Please feel free to choose any programming language, on any operating system.

# We chose Python on Mac Tahoe: 26.5.2 (25F84)
