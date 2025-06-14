import socket
import threading
import time
import json
from urllib.parse import parse_qs

class SimpleHTTPServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Simple in-memory storage for demo
        self.data_store = {
            'users': [
                {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
                {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'}
            ],
            'messages': []
        }
    
    def start(self):
        """Start the HTTP server"""
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"🌐 HTTP Server running on http://{self.host}:{self.port}")
        print("📋 Available endpoints:")
        print("   GET  /                    - Home page")
        print("   GET  /api/users          - Get all users")
        print("   POST /api/users          - Create new user")
        print("   GET  /api/messages       - Get all messages")
        print("   POST /api/messages       - Send new message")
        
        while True:
            try:
                client_socket, address = self.socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_request, 
                    args=(client_socket, address)
                )
                client_thread.start()
                
            except KeyboardInterrupt:
                print("\n🛑 HTTP Server shutting down...")
                break
        
        self.socket.close()
    
    def handle_request(self, client_socket, address):
        """Handle HTTP requests"""
        try:
            # Receive HTTP request
            request_data = client_socket.recv(4096).decode('utf-8')
            if not request_data:
                return
            
            # Parse HTTP request
            lines = request_data.split('\r\n')
            request_line = lines[0]
            method, path, version = request_line.split(' ')
            
            print(f"📨 {method} {path} from {address}")
            
            # Find request body (for POST requests)
            body = ""
            if '\r\n\r\n' in request_data:
                body = request_data.split('\r\n\r\n')[1]
            
            # Route the request
            response = self.route_request(method, path, body)
            
            # Send HTTP response
            client_socket.send(response.encode('utf-8'))
            
        except Exception as e:
            print(f"❌ Error handling request: {e}")
            error_response = self.create_http_response(500, "Internal Server Error")
            client_socket.send(error_response.encode('utf-8'))
        finally:
            client_socket.close()
    
    def route_request(self, method, path, body):
        """Route HTTP requests to appropriate handlers"""
        if method == 'GET':
            if path == '/':
                return self.handle_home()
            elif path == '/api/users':
                return self.handle_get_users()
            elif path == '/api/messages':
                return self.handle_get_messages()
            else:
                return self.create_http_response(404, "Not Found")
        
        elif method == 'POST':
            if path == '/api/users':
                return self.handle_create_user(body)
            elif path == '/api/messages':
                return self.handle_create_message(body)
            else:
                return self.create_http_response(404, "Not Found")
        
        else:
            return self.create_http_response(405, "Method Not Allowed")
    
    def handle_home(self):
        """Handle home page request"""
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Simple HTTP Server Demo</title>
</head>
<body>
    <h1>HTTP Server Demo</h1>
    <p>This server demonstrates HTTP protocol implementation.</p>
    <h2>Available API Endpoints:</h2>
    <ul>
        <li>GET /api/users - Get all users</li>
        <li>POST /api/users - Create new user</li>
        <li>GET /api/messages - Get all messages</li>
        <li>POST /api/messages - Send new message</li>
    </ul>
</body>
</html>"""
        return self.create_http_response(200, html_content, 'text/html')
    
    def handle_get_users(self):
        """Handle GET /api/users"""
        return self.create_json_response(200, self.data_store['users'])
    
    def handle_create_user(self, body):
        """Handle POST /api/users"""
        try:
            user_data = json.loads(body)
            new_user = {
                'id': len(self.data_store['users']) + 1,
                'name': user_data.get('name', ''),
                'email': user_data.get('email', '')
            }
            self.data_store['users'].append(new_user)
            return self.create_json_response(201, new_user)
        except json.JSONDecodeError:
            return self.create_json_response(400, {'error': 'Invalid JSON'})
    
    def handle_get_messages(self):
        """Handle GET /api/messages"""
        return self.create_json_response(200, self.data_store['messages'])
    
    def handle_create_message(self, body):
        """Handle POST /api/messages"""
        try:
            message_data = json.loads(body)
            new_message = {
                'id': len(self.data_store['messages']) + 1,
                'message': message_data.get('message', ''),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            self.data_store['messages'].append(new_message)
            return self.create_json_response(201, new_message)
        except json.JSONDecodeError:
            return self.create_json_response(400, {'error': 'Invalid JSON'})
    
    def create_http_response(self, status_code, content, content_type='text/plain'):
        """Create HTTP response"""
        status_messages = {
            200: 'OK',
            201: 'Created',
            400: 'Bad Request',
            404: 'Not Found',
            405: 'Method Not Allowed',
            500: 'Internal Server Error'
        }
        
        status_message = status_messages.get(status_code, 'Unknown')
        
        response = f"HTTP/1.1 {status_code} {status_message}\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += f"Content-Length: {len(content)}\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += content
        
        return response
    
    def create_json_response(self, status_code, data):
        """Create JSON HTTP response"""
        json_content = json.dumps(data, indent=2)
        return self.create_http_response(status_code, json_content, 'application/json')

class SimpleHTTPClient:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
    
    def send_request(self, method, path, data=None):
        """Send HTTP request"""
        try:
            # Create socket and connect
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            
            # Create HTTP request
            request = f"{method} {path} HTTP/1.1\r\n"
            request += f"Host: {self.host}:{self.port}\r\n"
            request += "Connection: close\r\n"
            
            if data:
                json_data = json.dumps(data)
                request += "Content-Type: application/json\r\n"
                request += f"Content-Length: {len(json_data)}\r\n"
                request += "\r\n"
                request += json_data
            else:
                request += "\r\n"
            
            # Send request
            client_socket.send(request.encode('utf-8'))
            
            # Receive response
            response = client_socket.recv(4096).decode('utf-8')
            
            # Parse response
            headers, body = response.split('\r\n\r\n', 1)
            status_line = headers.split('\r\n')[0]
            
            print(f"📤 {method} {path}")
            print(f"📥 {status_line}")
            
            # Try to parse JSON response
            try:
                json_body = json.loads(body)
                print(f"📋 Response: {json.dumps(json_body, indent=2)}")
            except json.JSONDecodeError:
                print(f"📋 Response: {body[:200]}...")
            
            print("-" * 50)
            
            client_socket.close()
            return body
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def demo_requests(self):
        """Demonstrate various HTTP requests"""
        print("🌐 HTTP Client Demo")
        print("=" * 50)
        
        # GET users
        print("1. Getting all users...")
        self.send_request('GET', '/api/users')
        
        # POST new user
        print("2. Creating new user...")
        self.send_request('POST', '/api/users', {
            'name': 'Charlie',
            'email': 'charlie@example.com'
        })
        
        # GET users again
        print("3. Getting all users again...")
        self.send_request('GET', '/api/users')
        
        # POST message
        print("4. Sending a message...")
        self.send_request('POST', '/api/messages', {
            'message': 'Hello from HTTP client!'
        })
        
        # GET messages
        print("5. Getting all messages...")
        self.send_request('GET', '/api/messages')

def run_server():
    """Run HTTP server"""
    server = SimpleHTTPServer()
    server.start()

def run_client():
    """Run HTTP client demo"""
    time.sleep(1)  # Give server time to start
    client = SimpleHTTPClient()
    client.demo_requests()

if __name__ == "__main__":
    print("🌐 HTTP Implementation Demo")
    print("Choose mode:")
    print("1. HTTP Server")
    print("2. HTTP Client Demo")
    
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "1":
        run_server()
    elif choice == "2":
        run_client()
    else:
        print("Invalid choice!") 