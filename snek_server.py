import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 12345  # Port to listen on (non-privileged ports are > 1023)
MAX_COUNT = 256 # Chars can't go over 256


# Arguments passed to socket are constants
# They specify the address family, and the socket type.
# AF_INET specifies IPv4, while SOCK_STREAM is TCP (more reiliable then UDP for our purpose)

welcome = "Welcome to Group Two's Server!"
print(welcome)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    # Bind() associates the socket with a network interface (host)
    # And a port number (we will use 12345 because it's easy)
    s.bind((HOST, PORT))
    # The values passed to .bind() depend on the address family
    # We are using IPv4 so it expects a (host, port) tuple

    # For host we are just using the standard loopback 127.0.0.1
    # I.E we are talking to ourselves

    # Listen() enables a server socket to accept connections
    # This turns it into a listening socket!
    # As a sidenote listen() actually has a backlog parameter, 
    # It specifies the number of unnacepted connections before refusing new ones
    # We don't care about it right now, we will use the default. 
    s.listen()
    print("Listening for connections...")


    # The accept method blocks execution
    # What I mean is, it sticks on this line and literally holds,
    # for an incoming connection.

    # When it connects, accept() returns a new socket object AND
    # addr = (host, port) = the address of the client. 
    # conn represents the socket itself, which IS the connection

    # Note: it is NOT the same as the listening socket
    # The server is using that to accept connection, but conn is used,
    # To communicate with the client!
    conn, addr = s.accept()


    with conn:
        print(
        f"Connection established successfully!\n"
        f"Client IP: {addr[0]} | Temporary port: {addr[1]}"
        )

        # This infinite loop (established with open connection socket)
        # Loops through all the blocking calls to conn.recv()
        while True:

            # conn.recv is how we read data, 
            # this method reads whatever the client sends us
            data = conn.recv(1024)

            if not data:
                break
            
            # Get the flag off the top (lil bit of encapsulation)
            flag = data[0]

            # The flag tells us whether to encode or decode
            # And this message is just for aesthetics
            if flag == 0:
                print("Encode request received")
            elif flag == 1:
                print("Decode request received")
            else:
                print("Error: invalid operation flag")
                continue
            
            # Use a slice, to remove the flag and store only the message itself
            message_slice = data[1:]

            # Turn it from bytes back into ascii text
            message = message_slice.decode("ascii")
            if len(message) > MAX_COUNT:
                error_message = "Error: Message cannot exceed 256 characters."
                print(error_message)
                conn.sendall(error_message.encode("ascii"))
                continue

            # But here the flag isn't for aesthetics
            # It very much tells us what operation to perform

            
            if flag == 0:  # Encode
                # ord() converts to an ascii number
                # then simply add or subtract one
                message = "".join(
                    chr(ord(character) + 1) for character in message
                )
            elif flag == 1:  # Decode
                message = "".join(
            chr(ord(character) - 1) for character in message
                )
            
            # Note message has been properly modified, turn it back into bytes
            outgoing_bytes = message.encode("ascii")

            # conn.sendall sends it back
            conn.sendall(outgoing_bytes)