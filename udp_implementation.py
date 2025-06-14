import socket
import threading
import time
import random

class UDPServer:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket
    
    def start(self):
        """Start the UDP server"""
        self.socket.bind((self.host, self.port))
        print(f"🚀 UDP Server listening on {self.host}:{self.port}")
        print("📡 Waiting for UDP packets...")
        
        while True:
            try:
                # Receive data (no connection needed)
                data, client_address = self.socket.recvfrom(1024)
                message = data.decode('utf-8')
                
                print(f"📨 UDP packet from {client_address}: {message}")
                
                # Simulate some packet loss (10% chance)
                if random.random() < 0.1:
                    print(f"📦 Simulating packet loss - not responding to {client_address}")
                    continue
                
                # Send response (no connection needed)
                response = f"UDP Server got: {message} at {time.strftime('%H:%M:%S')}"
                self.socket.sendto(response.encode('utf-8'), client_address)
                
            except KeyboardInterrupt:
                print("\n🛑 UDP Server shutting down...")
                break
        
        self.socket.close()

class UDPClient:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket
    
    def send_messages(self):
        """Send UDP messages (connectionless)"""
        print(f"📡 UDP Client ready to send to {self.host}:{self.port}")
        print("💬 Type messages (or 'quit' to exit):")
        print("⚠️ Note: Some messages might get lost (UDP doesn't guarantee delivery)")
        
        try:
            while True:
                message = input("You: ")
                if message.lower() == 'quit':
                    break
                
                # Send UDP packet (no connection needed)
                self.socket.sendto(message.encode('utf-8'), (self.host, self.port))
                
                # Try to receive response (with timeout)
                self.socket.settimeout(2.0)  # 2 second timeout
                try:
                    response, server_address = self.socket.recvfrom(1024)
                    print(f"Server: {response.decode('utf-8')}")
                except socket.timeout:
                    print("⏰ No response from server (packet might be lost)")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            self.socket.close()
            print("🔌 UDP Client closed")

class StreamingSimulator:
    """Simulate live streaming using UDP"""
    
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
    
    def start_streaming_server(self):
        """Simulate a streaming server"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((self.host, self.port))
        
        print(f"🎥 Streaming Server started on {self.host}:{self.port}")
        print("📺 Broadcasting video frames...")
        
        frame_number = 0
        
        try:
            while True:
                # Wait for client to join
                try:
                    server_socket.settimeout(1.0)
                    data, client_address = server_socket.recvfrom(1024)
                    if data.decode('utf-8') == 'START_STREAM':
                        print(f"📺 Client {client_address} joined the stream")
                        
                        # Start streaming frames
                        for i in range(100):  # Send 100 frames
                            frame_number += 1
                            frame_data = f"📹 Frame #{frame_number} - Video content at {time.strftime('%H:%M:%S.%f')[:-3]}"
                            
                            server_socket.sendto(frame_data.encode('utf-8'), client_address)
                            time.sleep(0.033)  # ~30 FPS
                            
                except socket.timeout:
                    continue
                
        except KeyboardInterrupt:
            print("\n🛑 Streaming server stopped")
        finally:
            server_socket.close()
    
    def start_streaming_client(self):
        """Simulate a streaming client"""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        print(f"📺 Connecting to stream at {self.host}:{self.port}")
        
        try:
            # Request to join stream
            client_socket.sendto('START_STREAM'.encode('utf-8'), (self.host, self.port))
            
            frames_received = 0
            frames_lost = 0
            
            client_socket.settimeout(0.1)  # Short timeout for real-time streaming
            
            while frames_received < 100:
                try:
                    data, server_address = client_socket.recvfrom(1024)
                    frame_data = data.decode('utf-8')
                    frames_received += 1
                    
                    # Only print every 10th frame to avoid spam
                    if frames_received % 10 == 0:
                        print(f"📺 {frame_data}")
                        print(f"📊 Received: {frames_received}, Lost: {frames_lost}")
                    
                except socket.timeout:
                    frames_lost += 1
                    continue
            
            print(f"\n📊 Stream completed!")
            print(f"📈 Total frames received: {frames_received}")
            print(f"📉 Total frames lost: {frames_lost}")
            print(f"📋 Success rate: {(frames_received/(frames_received + frames_lost))*100:.1f}%")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            client_socket.close()

def run_udp_server():
    """Run UDP server"""
    server = UDPServer()
    server.start()

def run_udp_client():
    """Run UDP client"""
    client = UDPClient()
    client.send_messages()

def run_streaming_demo():
    """Run streaming demonstration"""
    print("🎥 UDP Streaming Demo")
    print("Choose mode:")
    print("1. Streaming Server")
    print("2. Streaming Client")
    
    choice = input("Enter choice (1 or 2): ")
    simulator = StreamingSimulator()
    
    if choice == "1":
        simulator.start_streaming_server()
    elif choice == "2":
        simulator.start_streaming_client()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    print("🌐 UDP Implementation Demo")
    print("Choose mode:")
    print("1. UDP Server (Basic)")
    print("2. UDP Client (Basic)")
    print("3. Streaming Demo")
    
    choice = input("Enter choice (1, 2, or 3): ")
    
    if choice == "1":
        run_udp_server()
    elif choice == "2":
        run_udp_client()
    elif choice == "3":
        run_streaming_demo()
    else:
        print("Invalid choice!") 