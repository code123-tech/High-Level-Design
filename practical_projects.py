"""
Practical Network Protocol Projects
===================================
Real-world applications demonstrating TCP, UDP, and HTTP protocols
"""

import socket
import threading
import time
import json
import hashlib
import random

print("🚀 Practical Network Protocol Projects")
print("This file contains real-world examples of protocol implementations:")
print("1. Chat Application (TCP) - Reliable messaging")
print("2. Game Server (UDP) - Real-time gaming")  
print("3. Web API (HTTP) - REST services")
print("Run specific implementations from the other files!")

# Simple example functions for demonstration
def demonstrate_tcp_reliability():
    """Shows why TCP is good for reliable data transfer"""
    print("🛡️ TCP Example: Banking Transaction")
    print("- Connection established")
    print("- Data sent with acknowledgment")
    print("- Guaranteed delivery and order")
    print("- Perfect for: Email, file transfers, web browsing")

def demonstrate_udp_speed():
    """Shows why UDP is good for real-time applications"""  
    print("⚡ UDP Example: Video Streaming")
    print("- No connection setup needed")
    print("- Fast packet delivery")
    print("- Some packet loss acceptable")  
    print("- Perfect for: Gaming, live streams, video calls")

def demonstrate_http_structure():
    """Shows HTTP's request-response pattern"""
    print("🌐 HTTP Example: REST API")
    print("- Structured request/response")
    print("- Standard methods (GET, POST, etc.)")
    print("- Status codes and headers")
    print("- Perfect for: Web services, mobile apps, APIs")

class ChatApplication:
    """TCP-based chat application demonstrating reliable messaging"""
    
    def __init__(self):
        self.clients = {}
        self.chat_history = []
    
    def run_server(self, host='localhost', port=9001):
        """Run chat server"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)
        
        print(f"💬 Chat Server running on {host}:{port}")
        print("🔗 Waiting for clients to connect...")
        
        try:
            while True:
                client_socket, address = server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.start()
        except KeyboardInterrupt:
            print("\n🛑 Chat server shutting down...")
        finally:
            server_socket.close()
    
    def handle_client(self, client_socket, address):
        """Handle individual chat clients"""
        username = None
        try:
            # Get username
            client_socket.send("Enter username: ".encode('utf-8'))
            username = client_socket.recv(1024).decode('utf-8').strip()
            
            self.clients[username] = client_socket
            print(f"👤 {username} joined from {address}")
            
            # Send chat history
            for message in self.chat_history[-10:]:  # Last 10 messages
                client_socket.send(f"[History] {message}\n".encode('utf-8'))
            
            # Broadcast join message
            join_message = f"🎉 {username} joined the chat!"
            self.broadcast_message(join_message, exclude=username)
            
            # Handle messages
            while True:
                message = client_socket.recv(1024).decode('utf-8').strip()
                if not message:
                    break
                
                if message == '/quit':
                    break
                
                full_message = f"{username}: {message}"
                self.chat_history.append(full_message)
                
                print(f"💬 {full_message}")
                self.broadcast_message(full_message, exclude=username)
                
        except ConnectionResetError:
            pass
        finally:
            if username:
                self.clients.pop(username, None)
                leave_message = f"👋 {username} left the chat"
                print(leave_message)
                self.broadcast_message(leave_message, exclude=username)
            client_socket.close()
    
    def broadcast_message(self, message, exclude=None):
        """Broadcast message to all connected clients"""
        for username, client_socket in list(self.clients.items()):
            if username != exclude:
                try:
                    client_socket.send(f"{message}\n".encode('utf-8'))
                except:
                    self.clients.pop(username, None)
    
    def run_client(self, host='localhost', port=9001):
        """Run chat client"""
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            
            # Get username prompt
            prompt = client_socket.recv(1024).decode('utf-8')
            print(prompt, end='')
            username = input()
            client_socket.send(username.encode('utf-8'))
            
            print(f"💬 Connected to chat as {username}")
            print("Type messages (or '/quit' to exit):")
            print("-" * 40)
            
            # Start receiving thread
            receive_thread = threading.Thread(
                target=self.receive_messages,
                args=(client_socket,)
            )
            receive_thread.daemon = True
            receive_thread.start()
            
            # Send messages
            while True:
                message = input()
                if message == '/quit':
                    break
                client_socket.send(message.encode('utf-8'))
            
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            client_socket.close()
    
    def receive_messages(self, client_socket):
        """Receive messages from server"""
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(message, end='')
                else:
                    break
            except:
                break

class GameServer:
    """UDP-based game server demonstrating real-time communication"""
    
    def __init__(self):
        self.players = {}
        self.game_state = {
            'ball_x': 50,
            'ball_y': 50,
            'ball_dx': 2,
            'ball_dy': 2
        }
    
    def run_server(self, host='localhost', port=9002):
        """Run game server"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((host, port))
        
        print(f"🎮 Game Server running on {host}:{port}")
        print("🏓 Starting Pong-like game simulation...")
        
        # Start game loop
        game_thread = threading.Thread(target=self.game_loop)
        game_thread.daemon = True
        game_thread.start()
        
        try:
            while True:
                data, address = server_socket.recvfrom(1024)
                message = json.loads(data.decode('utf-8'))
                
                if message['type'] == 'join':
                    player_id = f"player_{len(self.players)}"
                    self.players[address] = {
                        'id': player_id,
                        'x': random.randint(10, 90),
                        'y': random.randint(10, 90),
                        'last_seen': time.time()
                    }
                    print(f"🎮 {player_id} joined from {address}")
                    
                    # Send welcome message
                    response = {
                        'type': 'welcome',
                        'player_id': player_id,
                        'game_state': self.game_state
                    }
                    server_socket.sendto(
                        json.dumps(response).encode('utf-8'),
                        address
                    )
                
                elif message['type'] == 'move' and address in self.players:
                    # Update player position
                    self.players[address]['x'] = message['x']
                    self.players[address]['y'] = message['y']
                    self.players[address]['last_seen'] = time.time()
                
        except KeyboardInterrupt:
            print("\n🛑 Game server shutting down...")
        finally:
            server_socket.close()
    
    def game_loop(self):
        """Main game simulation loop"""
        while True:
            # Update ball position
            self.game_state['ball_x'] += self.game_state['ball_dx']
            self.game_state['ball_y'] += self.game_state['ball_dy']
            
            # Bounce off walls
            if self.game_state['ball_x'] <= 0 or self.game_state['ball_x'] >= 100:
                self.game_state['ball_dx'] *= -1
            if self.game_state['ball_y'] <= 0 or self.game_state['ball_y'] >= 100:
                self.game_state['ball_dy'] *= -1
            
            # Remove inactive players
            current_time = time.time()
            inactive_players = [
                addr for addr, player in self.players.items()
                if current_time - player['last_seen'] > 10
            ]
            for addr in inactive_players:
                print(f"👋 {self.players[addr]['id']} disconnected")
                del self.players[addr]
            
            # Broadcast game state to all players
            self.broadcast_game_state()
            
            time.sleep(1/30)  # 30 FPS
    
    def broadcast_game_state(self):
        """Send game state to all players"""
        if not self.players:
            return
        
        state_message = {
            'type': 'game_state',
            'ball': {
                'x': self.game_state['ball_x'],
                'y': self.game_state['ball_y']
            },
            'players': [
                {
                    'id': player['id'],
                    'x': player['x'],
                    'y': player['y']
                }
                for player in self.players.values()
            ]
        }
        
        message_data = json.dumps(state_message).encode('utf-8')
        
        # Send to all players (UDP doesn't guarantee delivery)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for address in self.players.keys():
            try:
                sock.sendto(message_data, address)
            except:
                pass
        sock.close()
    
    def run_client(self, host='localhost', port=9002):
        """Run game client"""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Join game
        join_message = {'type': 'join'}
        client_socket.sendto(
            json.dumps(join_message).encode('utf-8'),
            (host, port)
        )
        
        print("🎮 Joined game! Use WASD to move, Q to quit")
        
        # Receive welcome message
        try:
            data, address = client_socket.recvfrom(1024)
            welcome = json.loads(data.decode('utf-8'))
            player_id = welcome['player_id']
            print(f"🎯 You are {player_id}")
            
            # Start receiving game state
            receive_thread = threading.Thread(
                target=self.receive_game_state,
                args=(client_socket,)
            )
            receive_thread.daemon = True
            receive_thread.start()
            
            # Simple movement simulation
            x, y = 50, 50
            print("Game started! (This is a simple simulation)")
            
            for i in range(100):  # Simulate 100 moves
                # Simulate random movement
                direction = random.choice(['w', 'a', 's', 'd'])
                if direction == 'w' and y > 5:
                    y -= 5
                elif direction == 's' and y < 95:
                    y += 5
                elif direction == 'a' and x > 5:
                    x -= 5
                elif direction == 'd' and x < 95:
                    x += 5
                
                # Send position update
                move_message = {'type': 'move', 'x': x, 'y': y}
                client_socket.sendto(
                    json.dumps(move_message).encode('utf-8'),
                    (host, port)
                )
                
                time.sleep(0.5)
            
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            client_socket.close()
    
    def receive_game_state(self, client_socket):
        """Receive game state updates"""
        while True:
            try:
                client_socket.settimeout(2.0)
                data, address = client_socket.recvfrom(1024)
                state = json.loads(data.decode('utf-8'))
                
                if state['type'] == 'game_state':
                    ball = state['ball']
                    players_count = len(state['players'])
                    print(f"🏓 Ball: ({ball['x']:.1f}, {ball['y']:.1f}) | Players: {players_count}")
                
            except socket.timeout:
                continue
            except:
                break

class WebAPI:
    """HTTP-based REST API demonstrating web services"""
    
    def __init__(self):
        self.todos = [
            {'id': 1, 'task': 'Learn TCP', 'completed': True},
            {'id': 2, 'task': 'Learn UDP', 'completed': True},
            {'id': 3, 'task': 'Learn HTTP', 'completed': False}
        ]
    
    def run_server(self, host='localhost', port=9003):
        """Run web API server"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)
        
        print(f"🌐 Web API Server running on http://{host}:{port}")
        print("📋 Available endpoints:")
        print("   GET  /api/todos     - Get all todos")
        print("   POST /api/todos     - Create new todo")
        print("   GET  /api/todos/:id - Get specific todo")
        
        try:
            while True:
                client_socket, address = server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_request,
                    args=(client_socket, address)
                )
                client_thread.start()
        except KeyboardInterrupt:
            print("\n🛑 Web API server shutting down...")
        finally:
            server_socket.close()
    
    def handle_request(self, client_socket, address):
        """Handle HTTP requests"""
        try:
            request_data = client_socket.recv(4096).decode('utf-8')
            if not request_data:
                return
            
            lines = request_data.split('\r\n')
            request_line = lines[0]
            method, path, version = request_line.split(' ')
            
            print(f"📨 {method} {path} from {address}")
            
            # Get request body
            body = ""
            if '\r\n\r\n' in request_data:
                body = request_data.split('\r\n\r\n')[1]
            
            # Route request
            if method == 'GET' and path == '/api/todos':
                response = self.get_todos()
            elif method == 'POST' and path == '/api/todos':
                response = self.create_todo(body)
            elif method == 'GET' and path.startswith('/api/todos/'):
                todo_id = int(path.split('/')[-1])
                response = self.get_todo(todo_id)
            else:
                response = self.create_response(404, {'error': 'Not found'})
            
            client_socket.send(response.encode('utf-8'))
            
        except Exception as e:
            print(f"❌ Error: {e}")
            error_response = self.create_response(500, {'error': 'Internal server error'})
            client_socket.send(error_response.encode('utf-8'))
        finally:
            client_socket.close()
    
    def get_todos(self):
        """Get all todos"""
        return self.create_response(200, self.todos)
    
    def create_todo(self, body):
        """Create new todo"""
        try:
            data = json.loads(body)
            new_todo = {
                'id': len(self.todos) + 1,
                'task': data.get('task', ''),
                'completed': False
            }
            self.todos.append(new_todo)
            return self.create_response(201, new_todo)
        except json.JSONDecodeError:
            return self.create_response(400, {'error': 'Invalid JSON'})
    
    def get_todo(self, todo_id):
        """Get specific todo"""
        todo = next((t for t in self.todos if t['id'] == todo_id), None)
        if todo:
            return self.create_response(200, todo)
        else:
            return self.create_response(404, {'error': 'Todo not found'})
    
    def create_response(self, status_code, data):
        """Create HTTP response"""
        status_messages = {
            200: 'OK',
            201: 'Created',
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        }
        
        json_data = json.dumps(data, indent=2)
        
        response = f"HTTP/1.1 {status_code} {status_messages[status_code]}\r\n"
        response += "Content-Type: application/json\r\n"
        response += "Access-Control-Allow-Origin: *\r\n"
        response += f"Content-Length: {len(json_data)}\r\n"
        response += "\r\n"
        response += json_data
        
        return response

def main():
    print("🚀 Practical Network Protocol Projects")
    print("=" * 50)
    print("Choose a project to run:")
    print("1. 💬 Chat Application (TCP)")
    print("2. 🎮 Game Server (UDP)")
    print("3. 🌐 Web API (HTTP)")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == "1":
        print("\n💬 TCP Chat Application")
        print("Choose mode:")
        print("1. Server")
        print("2. Client")
        
        mode = input("Enter mode (1 or 2): ")
        chat = ChatApplication()
        
        if mode == "1":
            chat.run_server()
        elif mode == "2":
            chat.run_client()
    
    elif choice == "2":
        print("\n🎮 UDP Game Server")
        print("Choose mode:")
        print("1. Server")
        print("2. Client")
        
        mode = input("Enter mode (1 or 2): ")
        game = GameServer()
        
        if mode == "1":
            game.run_server()
        elif mode == "2":
            game.run_client()
    
    elif choice == "3":
        print("\n🌐 HTTP Web API")
        api = WebAPI()
        api.run_server()
    
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    demonstrate_tcp_reliability()
    print()
    demonstrate_udp_speed()
    print()
    demonstrate_http_structure()
    main() 