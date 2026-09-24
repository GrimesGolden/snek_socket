import socket
import sys # needed for exiting

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 12345  # The port used by the server
MAX_COUNT = 256 # Chars can't go over 256

def  menu(message):
    # Rotates through a menu of options, with choice to exit
    print("Main Menu")
    print("1. Encode a message")
    if (message is not None):
        print("2. Decode a message")
    print("3. Exit")

    while True:
        choice = input("Enter your choice (1-3): ")

        # If we want to encode a message, then first recieve one, and send it out.
        # With appropriate flag.
        if choice == "1":
            message = get_message()
            flag = False # Encoding
            return message, flag
        
        # If a message EXISTS TO DECODE...AND we also want to decode it, then do this...
        elif choice == "2" and message is not None: # We can only choose to decode if a message exists
            # return message (not needed)
            # There is no message required, we decode the stored message
            flag = True # Decoding
            return message, flag
        
        # Goodbye
        elif choice == "3":
            # Certainly a rude exit
            print("Exiting Program")
            sys.exit(0)
        
        # This is why the loop exists, outside of the main socket loop
        # It's solely an error checking loop
        else:
            print("Invalid entry. Please try again.")


def get_message():
    # This function exists to recieve a proper message under 256 chars
    # Empty input and non-ASCII characters are rejected.
    message = (input("Enter your message: "))

    if (len(message) > MAX_COUNT):
        message = "Hello, world!"
        print("Error: your message is larger than 256 chars.");
        print(f"Using default message: {message}")
        return message
    elif not message.strip():
        message = "Hello, world!"
        print("Error: no empty messages allowed");
        print(f"Using default message: {message}")
        return message
    elif not message.isascii():
        message = "Hello, world!"
        print("Error: only ASCII characters are allowed.");
        print(f"Using default message: {message}")
        return message
    else:
        print("Message accepted: ", message)
        return message



# Create a socket object, the with..as format just makes a clean open and exit
print("Welcome to Group Two's client!")

# Will continue to try to connect until it succeeds, or the user chooses to exit
while True:
    # Sets the socket to None so we can check if it was created if a connection error occurs
    s = None

    try:
        # IPv4 TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Attempts to connect the server's address and port
        s.connect((HOST, PORT))
        print("Connected to the server successfully")
        break

    except ConnectionRefusedError:
        # Usually occurs when the server isn't running
        print(f"Error: Unable to connect to the server at {HOST}:{PORT}.")
        print("Make sure the server is running.")

    except OSError as error:
        # Handles other OS-related errors, such as network issues or invalid addresses
        print(f"Network error: {error}")

    # Closes the unsuccessful socket if it was created, to free up resources
    if s is not None:
        s.close()

    # Enables the user to retry the connection or exit the program gracefully
    retry = input("Do you want to retry connecting? (y/n): ")
    if retry not in ("y", "Y"):
        print("Exiting program.")
        sys.exit(0)

# Closes the socket automatically when the client is done or exits this block
with s:
    # Stores the latest encoded message for decoding
    message = None
    # False means an encode request, True means a decode request
    decode = False
    
    while True:
        message, decode = menu(message)

        # Send all only works with bytes
        # We convert the decode flag into a single byte
        # 01 if decode is true 
        # 00 decode is false (encode operation on server side)
        decode_byte = b"\x01" if decode else b"\x00"

        # send all can only work with bytes
        # We turn it into bytes
        # Don't get confused by the encode() function (its unrelated to our encoding operation)

        # If it contains a char outside the ascii range it's going to cry
        # Someone might want to catch that. 
        outgoing_bytes = message.encode("ascii")    

        # This is the protocol
        # A packet contains the flag byte first, followed by the outgoing bytes
        my_lil_packet = decode_byte + outgoing_bytes

        # Send the message with s.sendall()
        s.sendall(my_lil_packet)

        # s.recv accepts the servers reply, and stores it in data. 
        response = s.recv(1024)
        # It's turning it back to ascii, not decoding it in context of the assignment
        # (Thats just the coincidental name of the function)
        response_text = response.decode("ascii")
        if response_text.startswith("Error:"):
            print(f"Server response: {response_text}")
            message = None
            continue

        # We already know what our choice was
        # So the server doesn't even need to send back a flag
        # Neat huh
        if decode:
            print(f"Decoded message: {response_text}")
        else:
            message = response_text
            print(f"Encoded message stored: {message}")