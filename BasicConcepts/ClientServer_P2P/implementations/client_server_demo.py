"""
Client-Server Architecture Implementation
========================================
Demonstrates the traditional client-server model where:
- Clients initiate requests
- Servers respond to requests
- Centralized control and data management
"""

import socket
import threading
import time
import json
import hashlib
from datetime import datetime

class SimpleFileServer:
    """File Server - Demonstrates centralized server control"""
    
    def __init__(self, host='localhost', port=8001):
        self.host = host
        self.port = port
        self.files = {}  # Server stores all files
        
    def start(self):
        """Start the file server"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        
        print(f"📁 File Server running on {self.host}:{self.port}")
        print("🔗 Waiting for clients...")
        
        try:
            while True:
                client_socket, address = server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.start()
        except KeyboardInterrupt:
            print("\n🛑 Server shutting down...")
        finally:
            server_socket.close()
    
    def handle_client(self, client_socket, address):
        """Handle client requests - Server processes all requests"""
        print(f"👤 Client connected from {address}")
        
        try:
            while True:
                request_data = client_socket.recv(4096).decode('utf-8')
                if not request_data:
                    break
                
                request = json.loads(request_data)
                response = self.process_request(request)
                
                response_json = json.dumps(response)
                client_socket.send(response_json.encode('utf-8'))
                
        except Exception as e:
            print(f"❌ Error with client {address}: {e}")
        finally:
            client_socket.close()
            print(f"👋 Client {address} disconnected")
    
    def process_request(self, request):
        """Server processes all requests centrally"""
        operation = request.get('operation')
        
        if operation == 'UPLOAD':
            filename = request.get('filename')
            content = request.get('content')
            self.files[filename] = content
            print(f"📤 Stored file: {filename}")
            return {'status': 'success', 'message': f'File {filename} uploaded'}
            
        elif operation == 'DOWNLOAD':
            filename = request.get('filename')
            if filename in self.files:
                print(f"📥 Serving file: {filename}")
                return {'status': 'success', 'content': self.files[filename]}
            else:
                return {'status': 'error', 'message': 'File not found'}
                
        elif operation == 'LIST':
            file_list = list(self.files.keys())
            return {'status': 'success', 'files': file_list}
            
        else:
            return {'status': 'error', 'message': 'Unknown operation'}

class SimpleFileClient:
    """File Client - Always initiates requests to server"""
    
    def __init__(self, host='localhost', port=8001):
        self.host = host
        self.port = port
    
    def connect_and_interact(self):
        """Client initiates connection and sends requests"""
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            
            print(f"🔗 Connected to server at {self.host}:{self.port}")
            print("Commands: upload <filename> <content>, download <filename>, list, quit")
            
            while True:
                command = input(">> ").strip().split()
                if not command:
                    continue
                
                if command[0] == 'quit':
                    break
                
                request = self.build_request(command)
                if request:
                    # Client sends request to server
                    client_socket.send(json.dumps(request).encode('utf-8'))
                    
                    # Client waits for server response
                    response_data = client_socket.recv(4096).decode('utf-8')
                    response = json.loads(response_data)
                    
                    self.display_response(response)
                
        except ConnectionRefusedError:
            print("❌ Could not connect to server")
        finally:
            client_socket.close()
    
    def build_request(self, command):
        """Build request for server"""
        if command[0] == 'upload' and len(command) >= 3:
            return {
                'operation': 'UPLOAD',
                'filename': command[1],
                'content': ' '.join(command[2:])
            }
        elif command[0] == 'download' and len(command) == 2:
            return {'operation': 'DOWNLOAD', 'filename': command[1]}
        elif command[0] == 'list':
            return {'operation': 'LIST'}
        else:
            print("❌ Invalid command")
            return None
    
    def display_response(self, response):
        """Display server response"""
        if response['status'] == 'success':
            if 'files' in response:
                print(f"📁 Files: {response['files']}")
            elif 'content' in response:
                print(f"📄 Content: {response['content']}")
            else:
                print(f"✅ {response['message']}")
        else:
            print(f"❌ {response['message']}")

def demonstrate_client_server():
    """Show Client-Server characteristics"""
    print("🏛️ Client-Server Architecture:")
    print("=" * 40)
    print("✅ Server has centralized control")
    print("✅ Clients always initiate requests")
    print("✅ Server processes all operations")
    print("✅ Single point of authority")
    print("✅ Examples: Web servers, databases, email servers")
    print()

def main():
    print("🏛️ Client-Server Architecture Demo")
    print("Choose mode:")
    print("1. Start Server")
    print("2. Start Client")
    print("3. Learn About Client-Server")
    
    choice = input("Enter choice (1-3): ")
    
    if choice == "1":
        server = SimpleFileServer()
        server.start()
    elif choice == "2":
        client = SimpleFileClient()
        client.connect_and_interact()
    elif choice == "3":
        demonstrate_client_server()
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main() 