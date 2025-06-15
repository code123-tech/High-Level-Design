#!/usr/bin/env python3
"""
Quick Start Guide for Network Protocol Implementations
======================================================
Run this script to quickly test and understand TCP, UDP, and HTTP protocols
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def print_header():
    """Print welcome message"""
    print("🚀 Network Protocols - Quick Start Guide")
    print("=" * 50)
    print("This guide helps you quickly test all protocol implementations!")
    print()

def check_files():
    """Check if implementation files exist"""
    required_files = [
        'implementations/tcp_implementation.py',
        'implementations/udp_implementation.py', 
        'implementations/http_implementation.py',
        'demos/protocol_comparison_demo.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease make sure all implementation files are in their proper directories!")
        return False
    
    print("✅ All implementation files found!")
    return True

def show_protocol_summary():
    """Show summary of protocols"""
    print("\n📋 Protocol Summary:")
    print("-" * 30)
    
    protocols = {
        "TCP": {
            "emoji": "🛡️",
            "name": "Transmission Control Protocol",
            "key": "Reliable & Ordered",
            "use": "Banking, Email, File Downloads"
        },
        "UDP": {
            "emoji": "⚡", 
            "name": "User Datagram Protocol",
            "key": "Fast & Connectionless",
            "use": "Gaming, Streaming, Video Calls"
        },
        "HTTP": {
            "emoji": "🌐",
            "name": "Hypertext Transfer Protocol", 
            "key": "Structured Web Communication",
            "use": "Web APIs, Mobile Apps, REST Services"
        }
    }
    
    for proto, info in protocols.items():
        print(f"{info['emoji']} {proto} - {info['name']}")
        print(f"   Key: {info['key']}")
        print(f"   Use: {info['use']}")
        print()

def run_comparison_demo():
    """Run the protocol comparison demo"""
    print("🔄 Running Protocol Comparison Demo...")
    print("-" * 40)
    try:
        subprocess.run([sys.executable, 'demos/protocol_comparison_demo.py'], check=True)
    except subprocess.CalledProcessError:
        print("❌ Error running comparison demo")
    except KeyboardInterrupt:
        print("\n⏹️ Demo stopped by user")

def show_implementation_guide():
    """Show step-by-step implementation guide"""
    print("\n🛠️ Step-by-Step Implementation Guide:")
    print("=" * 45)
    
    implementations = [
        {
            "title": "1. TCP Implementation (Reliable Messaging)",
            "file": "implementations/tcp_implementation.py",
            "steps": [
                "Open 2 terminals in the NetworkProtocols directory",
                "Terminal 1: python implementations/tcp_implementation.py → Choose 1 (Server)",
                "Terminal 2: python implementations/tcp_implementation.py → Choose 2 (Client)",
                "Type messages - notice they all arrive in order!"
            ]
        },
        {
            "title": "2. UDP Implementation (Fast Streaming)",
            "file": "implementations/udp_implementation.py", 
            "steps": [
                "Open 2 terminals in the NetworkProtocols directory",
                "Terminal 1: python implementations/udp_implementation.py → Choose 1 (Server)",
                "Terminal 2: python implementations/udp_implementation.py → Choose 2 (Client)",
                "Type messages - some might get lost (this is normal!)"
            ]
        },
        {
            "title": "3. HTTP Implementation (Web Server)",
            "file": "implementations/http_implementation.py",
            "steps": [
                "Terminal 1: python implementations/http_implementation.py → Choose 1 (Server)",
                "Open browser: http://localhost:8080",
                "Try the REST API endpoints",
                "OR Terminal 2: python implementations/http_implementation.py → Choose 2 (Client Demo)"
            ]
        }
    ]
    
    for impl in implementations:
        print(f"\n{impl['title']}")
        print(f"File: {impl['file']}")
        print("Steps:")
        for i, step in enumerate(impl['steps'], 1):
            print(f"   {i}. {step}")
        print()

def show_practical_examples():
    """Show practical, real-world examples"""
    print("🎯 Real-World Examples:")
    print("-" * 25)
    
    examples = [
        {
            "protocol": "TCP",
            "emoji": "💳",
            "scenario": "Online Banking",
            "why": "Every transaction must be 100% accurate - no money can be lost!"
        },
        {
            "protocol": "UDP", 
            "emoji": "🎮",
            "scenario": "Online Gaming",
            "why": "Player position updates need to be fast - losing one frame is OK"
        },
        {
            "protocol": "HTTP",
            "emoji": "📱", 
            "scenario": "Mobile App API",
            "why": "Structured requests for user data, posts, notifications"
        }
    ]
    
    for example in examples:
        print(f"{example['emoji']} {example['protocol']}: {example['scenario']}")
        print(f"   Why: {example['why']}")
        print()

def main_menu():
    """Show main menu and handle user choice"""
    while True:
        print("\n🎯 What would you like to do?")
        print("1. 📊 Run Protocol Comparison Demo")
        print("2. 📖 Show Implementation Guide") 
        print("3. 🎯 Show Real-World Examples")
        print("4. 📋 Show Protocol Summary")
        print("5. 🌐 Open HTTP Server & Browser")
        print("6. ❌ Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            run_comparison_demo()
            
        elif choice == "2":
            show_implementation_guide()
            
        elif choice == "3":
            show_practical_examples()
            
        elif choice == "4":
            show_protocol_summary()
            
        elif choice == "5":
            print("🌐 Starting HTTP Server...")
            print("The server will start and your browser will open automatically!")
            print("Press Ctrl+C to stop the server when done.")
            try:
                # Start HTTP server in background
                import threading
                import time
                
                def start_http_server():
                    subprocess.run([sys.executable, 'implementations/http_implementation.py'])
                
                server_thread = threading.Thread(target=start_http_server)
                server_thread.daemon = True
                server_thread.start()
                
                # Wait a moment then open browser
                time.sleep(2)
                webbrowser.open('http://localhost:8080')
                
                input("Press Enter when done testing the HTTP server...")
                
            except Exception as e:
                print(f"❌ Error starting HTTP server: {e}")
                
        elif choice == "6":
            print("👋 Thanks for learning about network protocols!")
            print("Remember: TCP for reliability, UDP for speed, HTTP for web services!")
            break
            
        else:
            print("❌ Invalid choice! Please enter 1-6.")

def main():
    """Main function"""
    print_header()
    
    if not check_files():
        return
    
    print("\n💡 Quick Tips:")
    print("• TCP: Like registered mail - guaranteed delivery")
    print("• UDP: Like regular mail - fast but might get lost") 
    print("• HTTP: Like a structured conversation - request & response")
    
    main_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Happy coding!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please make sure all files are in the same directory.") 