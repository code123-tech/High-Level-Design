import socket
import threading
import time
import json
import subprocess
import sys
import os
from pathlib import Path

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
        
        # Show use cases first for context
        self.demonstrate_use_cases()
        self.show_comparison_table()
        
        print("🎯 Now let's see these protocols in action!")
        print("=" * 50)
        
        # Ask user what they want to see
        print("\nChoose which practical demonstration to run:")
        print("1. 🛡️  TCP Reliability Test (10 messages with acknowledgments)")
        print("2. ⚡ UDP Speed Test (1000 messages, fast delivery)")
        print("3. 🌐 HTTP Structure Demo (3 request-response cycles)")
        print("4. 🚀 Run All Demonstrations (TCP → UDP → HTTP)")
        print("5. 📋 Skip practical demos (theory only)")
        
        demo_choice = input("\nEnter your choice (1-5): ").strip()
        
        if demo_choice == "1":
            print("\n" + "="*60)
            self.demonstrate_tcp_reliability()
            
        elif demo_choice == "2":
            print("\n" + "="*60)
            self.demonstrate_udp_speed()
            
        elif demo_choice == "3":
            print("\n" + "="*60)
            self.demonstrate_http_structure()
            
        elif demo_choice == "4":
            print("\n🚀 Running All Protocol Demonstrations...")
            print("This will take about 30 seconds to complete all tests.")
            
            input("Press Enter to start TCP Reliability Test...")
            print("\n" + "="*60)
            self.demonstrate_tcp_reliability()
            
            input("Press Enter to start UDP Speed Test...")
            print("\n" + "="*60)
            self.demonstrate_udp_speed()
            
            input("Press Enter to start HTTP Structure Demo...")
            print("\n" + "="*60)
            self.demonstrate_http_structure()
            
            # Show final results comparison
            print("\n📊 Final Results Summary:")
            print("=" * 50)
            if 'tcp_reliability' in self.results:
                print(f"🛡️  TCP: {self.results['tcp_reliability']} messages delivered reliably")
            if 'udp_speed' in self.results:
                print(f"⚡ UDP: {self.results['udp_speed']:.0f} messages/second speed")
            print("🌐 HTTP: 3 structured request-response cycles completed")
            
        elif demo_choice == "5":
            print("\n📋 Skipping practical demonstrations.")
            
        else:
            print("\n❌ Invalid choice! Skipping practical demonstrations.")
        
        print("\n✅ Demo completed! You've learned about protocol differences.")
        print("\n💡 Key Takeaways:")
        print("• TCP: Use when data integrity is crucial (banking, file transfers)")
        print("• UDP: Use when speed matters more than reliability (streaming, gaming)")
        print("• HTTP: Use for web services and structured client-server communication")
        
        if demo_choice in ["1", "2", "3", "4"]:
            print("\n🎯 What you just saw:")
            if demo_choice in ["1", "4"]:
                print("• TCP: Every message was acknowledged and delivered in order")
            if demo_choice in ["2", "4"]:
                print("• UDP: Messages sent rapidly without waiting for acknowledgments")
            if demo_choice in ["3", "4"]:
                print("• HTTP: Structured requests with proper headers and JSON responses")

def run_implementation(impl_type):
    """Helper function to run implementations"""
    impl_path = Path("../implementations")
    
    if impl_type == "tcp":
        file_path = impl_path / "tcp_implementation.py"
    elif impl_type == "udp":
        file_path = impl_path / "udp_implementation.py"
    elif impl_type == "http":
        file_path = impl_path / "http_implementation.py"
    else:
        print("❌ Invalid implementation type")
        return
    
    if file_path.exists():
        print(f"🚀 Launching {file_path.name}...")
        try:
            subprocess.run([sys.executable, str(file_path)])
        except KeyboardInterrupt:
            print(f"\n⏹️ {file_path.name} stopped by user")
        except Exception as e:
            print(f"❌ Error running {file_path.name}: {e}")
    else:
        print(f"❌ File not found: {file_path}")
        print("💡 Make sure you're running from the demos directory")

def main():
    print("🌐 Network Protocol Implementation Guide")
    print("=" * 50)
    print("Choose what you want to run:")
    print("1. 🔄 Protocol Comparison Demo")
    print("2. 🛡️  TCP Implementation")
    print("3. ⚡ UDP Implementation") 
    print("4. 🌐 HTTP Implementation")
    print("5. 📚 Show Implementation Files")
    print("6. 🚀 Launch Quick Start Guide")
    
    choice = input("\nEnter your choice (1-6): ")
    
    if choice == "1":
        demo = ProtocolComparison()
        demo.run_demo()
    
    elif choice == "2":
        print("📂 TCP Implementation Options:")
        print("a) 🚀 Launch TCP implementation directly")
        print("b) 📋 Show manual instructions")
        
        sub_choice = input("Choose (a/b): ").lower()
        
        if sub_choice == "a":
            run_implementation("tcp")
        else:
            print("\n📂 Manual TCP Implementation Instructions:")
            print("Run this in two terminals from the NetworkProtocols directory:")
            print("Terminal 1: python implementations/tcp_implementation.py")
            print("Choose option 1 (Server)")
            print("Terminal 2: python implementations/tcp_implementation.py")
            print("Choose option 2 (Client)")
            print("\n💡 Or navigate to implementations folder:")
            print("cd ../implementations && python tcp_implementation.py")
        
    elif choice == "3":
        print("📂 UDP Implementation Options:")
        print("a) 🚀 Launch UDP implementation directly")
        print("b) 📋 Show manual instructions")
        
        sub_choice = input("Choose (a/b): ").lower()
        
        if sub_choice == "a":
            run_implementation("udp")
        else:
            print("\n📂 Manual UDP Implementation Instructions:")
            print("Run this in two terminals from the NetworkProtocols directory:")
            print("Terminal 1: python implementations/udp_implementation.py")
            print("Choose option 1 (Server)")
            print("Terminal 2: python implementations/udp_implementation.py")
            print("Choose option 2 (Client)")
            print("\n💡 Or navigate to implementations folder:")
            print("cd ../implementations && python udp_implementation.py")
        
    elif choice == "4":
        print("📂 HTTP Implementation Options:")
        print("a) 🚀 Launch HTTP implementation directly")
        print("b) 📋 Show manual instructions")
        
        sub_choice = input("Choose (a/b): ").lower()
        
        if sub_choice == "a":
            run_implementation("http")
        else:
            print("\n📂 Manual HTTP Implementation Instructions:")
            print("Run this from the NetworkProtocols directory:")
            print("Terminal 1: python implementations/http_implementation.py")
            print("Choose option 1 (Server)")
            print("Terminal 2: Open browser to http://localhost:8080")
            print("OR Terminal 2: python implementations/http_implementation.py (Choose option 2)")
            print("\n💡 Or navigate to implementations folder:")
            print("cd ../implementations && python http_implementation.py")
        
    elif choice == "5":
        files = [
            "../implementations/tcp_implementation.py - TCP client/server with reliable messaging",
            "../implementations/udp_implementation.py - UDP client/server with streaming demo",
            "../implementations/http_implementation.py - HTTP server with REST API",
            "protocol_comparison_demo.py - This comparison demo"
        ]
        print("\n📁 Implementation Files Available:")
        for file in files:
            print(f"  • {file}")
        
        print("\n🎯 Next Steps:")
        print("1. Run the comparison demo to see differences")
        print("2. Try each implementation individually")
        print("3. Navigate to NetworkProtocols directory for easier access:")
        print("   cd .. (to go back to NetworkProtocols folder)")
        print("4. Use quick_start.py for guided experience:")
        print("   python quick_start.py")
        print("5. Modify the code to understand the concepts better")
    
    elif choice == "6":
        quick_start_path = Path("../quick_start.py")
        if quick_start_path.exists():
            print("🚀 Launching Quick Start Guide...")
            try:
                subprocess.run([sys.executable, str(quick_start_path)])
            except KeyboardInterrupt:
                print("\n⏹️ Quick Start Guide stopped by user")
            except Exception as e:
                print(f"❌ Error running Quick Start Guide: {e}")
        else:
            print("❌ Quick Start Guide not found")
            print("💡 Navigate to NetworkProtocols directory and run: python quick_start.py")
    
    else:
        print("❌ Invalid choice! Please enter 1-6.")

if __name__ == "__main__":
    main() 