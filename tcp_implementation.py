import socket
import threading
import time

class TCPServer:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def start(self):
        """Start the TCP server"""
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"🚀 TCP Server listening on {self.host}:{self.port}")
        
        while True:
            try:
                client_socket, address = self.socket.accept()
                print(f"📞 Connection from {address}")
                
                # Handle client in a separate thread
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client_socket, address)
                )
                client_thread.start()
                
            except KeyboardInterrupt:
                print("\n🛑 Server shutting down...")
                break
        
        self.socket.close()
    
    def handle_client(self, client_socket, address):
        """Handle individual client connections"""
        try:
            while True:
                # Receive data from client
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                print(f"📨 Received from {address}: {data}")
                
                # Echo back with timestamp (reliable delivery)
                response = f"Server received: {data} at {time.strftime('%H:%M:%S')}"
                client_socket.send(response.encode('utf-8'))
                
        except ConnectionResetError:
            print(f"🔌 Client {address} disconnected")
        finally:
            client_socket.close()
            print(f"👋 Closed connection with {address}")

class TCPClient:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
    
    def connect_and_chat(self):
        """Connect to TCP server and start chatting"""
        try:
            # Create TCP socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Connect to server (connection-oriented)
            client_socket.connect((self.host, self.port))
            print(f"🔗 Connected to TCP server at {self.host}:{self.port}")
            print("💬 Type messages (or 'quit' to exit):")
            
            while True:
                # Get user input
                message = input("You: ")
                if message.lower() == 'quit':
                    break
                
                # Send message (guaranteed delivery)
                client_socket.send(message.encode('utf-8'))
                
                # Receive response (guaranteed delivery)
                response = client_socket.recv(1024).decode('utf-8')
                print(f"Server: {response}")
                
        except ConnectionRefusedError:
            print("❌ Could not connect to server. Is it running?")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            client_socket.close()
            print("🔌 Disconnected from server")

def run_server():
    """Run TCP server in a separate function"""
    server = TCPServer()
    server.start()

def run_client():
    """Run TCP client in a separate function"""
    client = TCPClient()
    client.connect_and_chat()

if __name__ == "__main__":
    print("🌐 TCP Implementation Demo")
    print("Choose mode:")
    print("1. Run Server")
    print("2. Run Client")
    
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "1":
        run_server()
    elif choice == "2":
        run_client()
    else:
        print("Invalid choice!") 