import socket
import threading
import time
import json
import subprocess
import sys

class ProtocolComparison:
    """Demonstrate the differences between TCP, UDP, and HTTP protocols"""
    
    def __init__(self):
        self.results = {}
    
    def demonstrate_tcp_reliability(self):
        """Show TCP's reliable data transfer"""
        print("🔄 TCP Reliability Test")
        print("=" * 50)
        
        # TCP Server
        def tcp_server():
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('localhost', 7777))
            server_socket.listen(1)
            
            client_socket, address = server_socket.accept()
            messages_received = []
            
            while len(messages_received) < 10:
                data = client_socket.recv(1024).decode('utf-8')
                if data:
                    messages_received.append(data)
                    client_socket.send(f"ACK: {data}".encode('utf-8'))
            
            client_socket.close()
            server_socket.close()
            
            print(f"📨 TCP Server received {len(messages_received)} messages in order")
            self.results['tcp_reliability'] = len(messages_received)
        
        # TCP Client
        def tcp_client():
            time.sleep(0.5)  # Wait for server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', 7777))
            
            sent_count = 0
            for i in range(10):
                message = f"TCP Message {i+1}"
                client_socket.send(message.encode('utf-8'))
                
                # Wait for acknowledgment
                ack = client_socket.recv(1024).decode('utf-8')
                if ack:
                    sent_count += 1
                    print(f"✅ Sent: {message}, Got: {ack}")
            
            client_socket.close()
            print(f"📤 TCP Client sent {sent_count} messages with acknowledgments")
        
        # Run TCP test
        server_thread = threading.Thread(target=tcp_server)
        client_thread = threading.Thread(target=tcp_client)
        
        server_thread.start()
        client_thread.start()
        
        server_thread.join()
        client_thread.join()
        
        print()
    
    def demonstrate_udp_speed(self):
        """Show UDP's speed vs TCP"""
        print("⚡ UDP Speed Test")
        print("=" * 50)
        
        # UDP Server
        def udp_server():
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_socket.bind(('localhost', 6666))
            
            messages_received = 0
            start_time = time.time()
            
            while messages_received < 1000:
                try:
                    server_socket.settimeout(5.0)
                    data, address = server_socket.recvfrom(1024)
                    messages_received += 1
                    
                    # Don't send acknowledgment - just receive
                    if messages_received % 100 == 0:
                        print(f"📨 UDP Server received {messages_received} messages")
                        
                except socket.timeout:
                    break
            
            end_time = time.time()
            duration = end_time - start_time
            
            server_socket.close()
            
            print(f"📊 UDP: Received {messages_received} messages in {duration:.2f} seconds")
            print(f"📈 UDP Rate: {messages_received/duration:.0f} messages/second")
            
            self.results['udp_speed'] = messages_received / duration
        
        # UDP Client
        def udp_client():
            time.sleep(0.5)  # Wait for server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            start_time = time.time()
            
            for i in range(1000):
                message = f"UDP Message {i+1}"
                client_socket.sendto(message.encode('utf-8'), ('localhost', 6666))
                
                if (i + 1) % 100 == 0:
                    print(f"📤 UDP Client sent {i+1} messages")
            
            end_time = time.time()
            duration = end_time - start_time
            
            client_socket.close()
            print(f"📊 UDP: Sent 1000 messages in {duration:.2f} seconds")
            print(f"📈 UDP Send Rate: {1000/duration:.0f} messages/second")
        
        # Run UDP test
        server_thread = threading.Thread(target=udp_server)
        client_thread = threading.Thread(target=udp_client)
        
        server_thread.start()
        client_thread.start()
        
        server_thread.join()
        client_thread.join()
        
        print()
    
    def demonstrate_http_structure(self):
        """Show HTTP's structured communication"""
        print("🌐 HTTP Structure Demo")
        print("=" * 50)
        
        # Simple HTTP server for demo
        def http_server():
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('localhost', 5555))
            server_socket.listen(1)
            
            for i in range(3):  # Handle 3 requests
                client_socket, address = server_socket.accept()
                
                # Receive HTTP request
                request = client_socket.recv(1024).decode('utf-8')
                request_line = request.split('\r\n')[0]
                print(f"📨 HTTP Request: {request_line}")
                
                # Send HTTP response
                response_data = {'message': f'Hello from HTTP server!', 'request_number': i+1}
                json_data = json.dumps(response_data)
                
                response = "HTTP/1.1 200 OK\r\n"
                response += "Content-Type: application/json\r\n"
                response += f"Content-Length: {len(json_data)}\r\n"
                response += "\r\n"
                response += json_data
                
                client_socket.send(response.encode('utf-8'))
                client_socket.close()
                
                print(f"📤 HTTP Response: {response_data}")
            
            server_socket.close()
        
        # HTTP client
        def http_client():
            time.sleep(0.5)  # Wait for server
            
            for i in range(3):
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(('localhost', 5555))
                
                # Send HTTP request
                request = f"GET /api/test HTTP/1.1\r\n"
                request += "Host: localhost:5555\r\n"
                request += "\r\n"
                
                client_socket.send(request.encode('utf-8'))
                
                # Receive HTTP response
                response = client_socket.recv(1024).decode('utf-8')
                
                # Parse response
                headers, body = response.split('\r\n\r\n', 1)
                status_line = headers.split('\r\n')[0]
                
                print(f"📥 HTTP Status: {status_line}")
                print(f"📋 HTTP Body: {body}")
                
                client_socket.close()
                time.sleep(0.1)
        
        # Run HTTP test
        server_thread = threading.Thread(target=http_server)
        client_thread = threading.Thread(target=http_client)
        
        server_thread.start()
        client_thread.start()
        
        server_thread.join()
        client_thread.join()
        
        print()
    
    def demonstrate_use_cases(self):
        """Show practical use cases for each protocol"""
        print("🎯 Practical Use Cases")
        print("=" * 50)
        
        use_cases = {
            "TCP": [
                "💳 Banking transactions (reliability crucial)",
                "📧 Email delivery (messages must arrive)",
                "📁 File downloads (complete data needed)",
                "💬 Chat applications (message order matters)",
                "🌐 Web browsing (pages must load completely)"
            ],
            "UDP": [
                "🎮 Online gaming (speed over reliability)",
                "📺 Live streaming (real-time over completeness)",
                "📞 Voice/Video calls (low latency needed)",
                "📡 DNS queries (fast response preferred)",
                "🎵 Music streaming (some loss acceptable)"
            ],
            "HTTP": [
                "🌍 Web applications (structured communication)",
                "📱 Mobile app APIs (standardized requests)",
                "🔄 REST services (resource-based operations)",
                "📊 Data visualization dashboards",
                "🛒 E-commerce platforms (standard web)"
            ]
        }
        
        for protocol, cases in use_cases.items():
            print(f"\n{protocol} Best Use Cases:")
            for case in cases:
                print(f"  {case}")
        
        print()
    
    def show_comparison_table(self):
        """Show a comparison table of protocols"""
        print("📊 Protocol Comparison Table")
        print("=" * 80)
        
        print(f"{'Feature':<20} {'TCP':<15} {'UDP':<15} {'HTTP':<15}")
        print("-" * 80)
        print(f"{'Connection':<20} {'Required':<15} {'Not Required':<15} {'Required':<15}")
        print(f"{'Reliability':<20} {'Guaranteed':<15} {'Best Effort':<15} {'Guaranteed':<15}")
        print(f"{'Speed':<20} {'Slower':<15} {'Faster':<15} {'Moderate':<15}")
        print(f"{'Data Order':<20} {'Preserved':<15} {'Not Guaranteed':<15} {'Preserved':<15}")
        print(f"{'Error Checking':<20} {'Yes':<15} {'Basic':<15} {'Yes':<15}")
        print(f"{'Overhead':<20} {'Higher':<15} {'Lower':<15} {'Higher':<15}")
        print(f"{'Structure':<20} {'Stream':<15} {'Packets':<15} {'Request/Response':<15}")
        print(f"{'Use Case':<20} {'Reliable Data':<15} {'Real-time':<15} {'Web Services':<15}")
        
        print()
    
    def run_demo(self):
        """Run the protocol demonstration"""
        print("🚀 Network Protocol Implementation Demo")
        print("=" * 60)
        print("This demo shows practical differences between TCP, UDP, and HTTP")
        print()
        
        self.demonstrate_use_cases()
        self.show_comparison_table()
        
        print("✅ Demo completed! You've learned about protocol differences.")
        print("\n💡 Key Takeaways:")
        print("• TCP: Use when data integrity is crucial (banking, file transfers)")
        print("• UDP: Use when speed matters more than reliability (streaming, gaming)")
        print("• HTTP: Use for web services and structured client-server communication")

def main():
    print("🌐 Network Protocol Implementation Guide")
    print("=" * 50)
    print("Choose what you want to run:")
    print("1. 🔄 Protocol Comparison Demo")
    print("2. 🛡️  TCP Implementation (tcp_implementation.py)")
    print("3. ⚡ UDP Implementation (udp_implementation.py)")
    print("4. 🌐 HTTP Implementation (http_implementation.py)")
    print("5. 📚 Show Implementation Files")
    
    choice = input("\nEnter your choice (1-5): ")
    
    if choice == "1":
        demo = ProtocolComparison()
        demo.run_demo()
    
    elif choice == "2":
        print("📂 Starting TCP Implementation...")
        print("Run this in two terminals:")
        print("Terminal 1: python tcp_implementation.py")
        print("Choose option 1 (Server)")
        print("Terminal 2: python tcp_implementation.py")
        print("Choose option 2 (Client)")
        
    elif choice == "3":
        print("📂 Starting UDP Implementation...")
        print("Run this in two terminals:")
        print("Terminal 1: python udp_implementation.py")
        print("Choose option 1 (Server)")
        print("Terminal 2: python udp_implementation.py")
        print("Choose option 2 (Client)")
        
    elif choice == "4":
        print("📂 Starting HTTP Implementation...")
        print("Run this in two terminals:")
        print("Terminal 1: python http_implementation.py")
        print("Choose option 1 (Server)")
        print("Terminal 2: Open browser to http://localhost:8080")
        print("OR Terminal 2: python http_implementation.py (Choose option 2)")
        
    elif choice == "5":
        files = [
            "tcp_implementation.py - TCP client/server with reliable messaging",
            "udp_implementation.py - UDP client/server with streaming demo",
            "http_implementation.py - HTTP server with REST API",
            "protocol_comparison_demo.py - This comparison demo"
        ]
        print("\n📁 Implementation Files Created:")
        for file in files:
            print(f"  • {file}")
        
        print("\n🎯 Next Steps:")
        print("1. Run the comparison demo to see differences")
        print("2. Try each implementation individually")
        print("3. Modify the code to understand the concepts better")
        print("4. Build your own applications using these protocols")
    
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main() 