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
    # Empty input is also rejected.
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
    else:
        print("Message accepted: ", message)
        return message



# Create a socket object, the with..as format just makes a clean open and exit
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Welcome to Group Two's client!")
    # Connect to the server =
    s.connect((HOST, PORT))
    print("Connected to the server succesfully")
    
    # The message starts out empty
    # decode is True if we want to decode a message, False for encode()
    message = None
    decode = False # Naturally we can only start by encoding, theres no message to decode.  
    
    # This is the really important logical loop
    # It could have been put inside a function huh
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

        # We already know what our choice was
        # So the server doesn't even need to send back a flag
        # Neat huh
        if decode:
            print(f"Decoded message: {response_text}")
        else:
            message = response_text
            print(f"Encoded message stored: {message}")