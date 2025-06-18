"""
Peer-to-Peer Architecture Demo
=============================
Shows how all peers can send and receive requests
"""

import socket
import threading
import json
import random
import time

class SimplePeer:
    """P2P Peer - Both client and server"""
    
    def __init__(self, peer_name, port, known_peers=[]):
        self.peer_name = peer_name
        self.port = port
        self.known_peers = set(known_peers)
        self.files = {}
        self.running = True
    
    def start(self):
        """Start peer (both server and client)"""
        print(f"🤝 Starting peer '{self.peer_name}' on port {self.port}")
        
        # Start server thread
        server_thread = threading.Thread(target=self.listen_for_peers)
        server_thread.daemon = True
        server_thread.start()
        
        # Discover other peers
        self.discover_peers()
        
        # Start interactive mode
        self.interactive_mode()
    
    def listen_for_peers(self):
        """Listen for requests from other peers"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('localhost', self.port))
        server_socket.listen(5)
        
        while self.running:
            try:
                client_socket, address = server_socket.accept()
                threading.Thread(
                    target=self.handle_peer,
                    args=(client_socket, address)
                ).start()
            except:
                break
        
        server_socket.close()
    
    def handle_peer(self, client_socket, address):
        """Handle requests from other peers"""
        try:
            request_data = client_socket.recv(4096).decode('utf-8')
            request = json.loads(request_data)
            
            response = self.process_request(request)
            client_socket.send(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            client_socket.close()
    
    def process_request(self, request):
        """Process peer requests"""
        operation = request.get('operation')
        
        if operation == 'SEARCH':
            filename = request.get('filename')
            if filename in self.files:
                print(f"📋 {self.peer_name} has file: {filename}")
                return {'status': 'found', 'peer': self.peer_name}
            else:
                return {'status': 'not_found'}
        
        elif operation == 'DOWNLOAD':
            filename = request.get('filename')
            if filename in self.files:
                print(f"📤 {self.peer_name} sending: {filename}")
                return {
                    'status': 'success',
                    'content': self.files[filename],
                    'peer': self.peer_name
                }
            else:
                return {'status': 'error', 'message': 'File not found'}
        
        elif operation == 'MESSAGE':
            message = request.get('message')
            sender = request.get('sender')
            print(f"💬 Message from {sender}: {message}")
            return {'status': 'received'}
        
        else:
            return {'status': 'error', 'message': 'Unknown operation'}
    
    def send_to_peer(self, peer_port, request):
        """Send request to another peer"""
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', peer_port))
            
            client_socket.send(json.dumps(request).encode('utf-8'))
            response_data = client_socket.recv(4096).decode('utf-8')
            response = json.loads(response_data)
            
            client_socket.close()
            return response
        except:
            return None
    
    def search_file(self, filename):
        """Search for file among all peers"""
        print(f"🔍 Searching for '{filename}' in P2P network...")
        
        for peer_port in self.known_peers:
            response = self.send_to_peer(peer_port, {
                'operation': 'SEARCH',
                'filename': filename
            })
            
            if response and response.get('status') == 'found':
                peer_name = response.get('peer')
                print(f"✅ Found '{filename}' on {peer_name}")
                return peer_port
        
        print(f"❌ File '{filename}' not found")
        return None
    
    def download_file(self, filename, peer_port):
        """Download file from specific peer"""
        response = self.send_to_peer(peer_port, {
            'operation': 'DOWNLOAD',
            'filename': filename
        })
        
        if response and response.get('status') == 'success':
            content = response.get('content')
            self.files[filename] = content
            print(f"📥 Downloaded '{filename}' successfully")
            return True
        else:
            print(f"❌ Failed to download '{filename}'")
            return False
    
    def broadcast_message(self, message):
        """Send message to all known peers"""
        for peer_port in self.known_peers:
            self.send_to_peer(peer_port, {
                'operation': 'MESSAGE',
                'message': message,
                'sender': self.peer_name
            })
    
    def discover_peers(self):
        """Discover other peers"""
        if self.known_peers:
            print(f"🤝 Connected to peers: {list(self.known_peers)}")
        else:
            print("🔍 No known peers")
    
    def interactive_mode(self):
        """Interactive command interface"""
        print(f"\n🎯 {self.peer_name} ready!")
        print("Commands: share <file> <content>, search <file>, download <file>, message <text>, peers, quit")
        
        while self.running:
            try:
                command = input(f"{self.peer_name}> ").strip().split()
                if not command:
                    continue
                
                if command[0] == 'quit':
                    self.running = False
                    break
                
                elif command[0] == 'share' and len(command) >= 3:
                    filename = command[1]
                    content = ' '.join(command[2:])
                    self.files[filename] = content
                    print(f"📤 Sharing '{filename}'")
                
                elif command[0] == 'search' and len(command) == 2:
                    filename = command[1]
                    self.search_file(filename)
                
                elif command[0] == 'download' and len(command) == 2:
                    filename = command[1]
                    peer_port = self.search_file(filename)
                    if peer_port:
                        self.download_file(filename, peer_port)
                
                elif command[0] == 'message' and len(command) >= 2:
                    message = ' '.join(command[1:])
                    self.broadcast_message(message)
                    print(f"📢 Broadcasted: {message}")
                
                elif command[0] == 'peers':
                    print(f"🤝 Known peers: {list(self.known_peers)}")
                    print(f"📁 My files: {list(self.files.keys())}")
                
                else:
                    print("❌ Invalid command")
                    
            except KeyboardInterrupt:
                self.running = False
                break

def demonstrate_p2p():
    """Show P2P characteristics"""
    print("🌐 Peer-to-Peer Architecture:")
    print("=" * 40)
    print("✅ All peers can send AND receive")
    print("✅ No central server needed")
    print("✅ Distributed data sharing")
    print("✅ Each peer = client + server")
    print("✅ Examples: BitTorrent, file sharing")
    print()

def main():
    print("🌐 P2P Architecture Demo")
    print("1. Start P2P Peer")
    print("2. Learn About P2P")
    
    choice = input("Choice (1-2): ")
    
    if choice == "1":
        name = input("Peer name: ").strip() or f"Peer{random.randint(1,99)}"
        port = int(input("Port (9001-9005): ") or "9001")
        
        peers_input = input("Known peers (comma-separated ports): ").strip()
        known_peers = []
        if peers_input:
            known_peers = [int(p.strip()) for p in peers_input.split(',')]
        
        peer = SimplePeer(name, port, known_peers)
        peer.start()
    
    elif choice == "2":
        demonstrate_p2p()
    
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main() 