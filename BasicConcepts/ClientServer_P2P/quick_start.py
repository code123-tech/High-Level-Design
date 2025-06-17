#!/usr/bin/env python3
"""
Client-Server vs Peer-to-Peer Architecture Quick Start Guide

This script provides quick access to all architectural demonstrations and examples.
Choose from multiple options to explore different aspects of both architectures.

Usage:
    python quick_start.py
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Print a welcome banner"""
    print("\n" + "="*80)
    print("🏛️  CLIENT-SERVER vs PEER-TO-PEER ARCHITECTURE DEMO")
    print("="*80)
    print("Explore the fundamental network architectures through hands-on examples!")
    print("="*80)

def print_architecture_overview():
    """Print a quick overview of both architectures"""
    print("\n📚 QUICK OVERVIEW:")
    print("\n🏛️  CLIENT-SERVER ARCHITECTURE:")
    print("   • Centralized control with server managing all requests")
    print("   • Examples: Web browsers, email clients, banking apps")
    print("   • Best for: Security, compliance, centralized control")
    
    print("\n🌐 PEER-TO-PEER ARCHITECTURE:")
    print("   • Distributed network where peers communicate directly")
    print("   • Examples: BitTorrent, Bitcoin, file sharing networks")
    print("   • Best for: Scalability, cost reduction, censorship resistance")

def show_menu():
    """Display the main menu options"""
    print("\n🚀 WHAT WOULD YOU LIKE TO EXPLORE?")
    print("\n1. 🎯 Quick Demo - Side-by-side comparison")
    print("2. 🏛️  Client-Server Implementation")
    print("3. 🌐 Peer-to-Peer Implementation") 
    print("4. 🔄 Interactive Architecture Comparison")
    print("5. 📖 View Architecture Guide")
    print("6. 🗂️  Explore File Structure")
    print("7. ❓ Help & Documentation")
    print("8. 🚪 Exit")

def quick_demo():
    """Run a quick side-by-side demo"""
    print("\n🎯 QUICK ARCHITECTURE DEMONSTRATION")
    print("="*50)
    print("\nThis demo shows both architectures in action:")
    print("• Client-Server: Centralized file server")
    print("• Peer-to-Peer: Distributed file sharing")
    
    print("\n⚠️  SETUP REQUIRED:")
    print("To see both architectures working, you'll need to:")
    print("1. Open multiple terminal windows")
    print("2. Follow the step-by-step instructions")
    
    choice = input("\n📋 Ready to see the step-by-step guide? (y/n): ").lower()
    if choice == 'y':
        show_demo_instructions()

def show_demo_instructions():
    """Show detailed demo instructions"""
    print("\n" + "="*60)
    print("📋 STEP-BY-STEP DEMO INSTRUCTIONS")
    print("="*60)
    
    print("\n🏛️  CLIENT-SERVER DEMO:")
    print("   Terminal 1 (Server):")
    print("   → cd implementations/")
    print("   → python client_server_demo.py")
    print("   → Choose option 1 (Start Server)")
    
    print("   Terminal 2 (Client):")
    print("   → cd implementations/")
    print("   → python client_server_demo.py")
    print("   → Choose option 2 (Start Client)")
    print("   → Try commands: upload test.txt 'Hello World', list, download test.txt")
    
    print("\n🌐 PEER-TO-PEER DEMO:")
    print("   Terminal 1 (Peer Alice):")
    print("   → cd implementations/")
    print("   → python peer_to_peer_demo.py")
    print("   → Choose option 1, name: Alice, port: 9001, known peers: (empty)")
    
    print("   Terminal 2 (Peer Bob):")
    print("   → python peer_to_peer_demo.py")
    print("   → Choose option 1, name: Bob, port: 9002, known peers: 9001")
    
    print("   Terminal 3 (Peer Charlie):")
    print("   → python peer_to_peer_demo.py")
    print("   → Choose option 1, name: Charlie, port: 9003, known peers: 9001,9002")

def run_client_server():
    """Launch client-server demonstration"""
    print("\n🏛️  LAUNCHING CLIENT-SERVER DEMO")
    print("="*40)
    print("Starting the centralized file server demonstration...")
    
    impl_path = Path("implementations/client_server_demo.py")
    if impl_path.exists():
        try:
            subprocess.run([sys.executable, str(impl_path)], cwd="implementations")
        except KeyboardInterrupt:
            print("\n👋 Client-Server demo stopped.")
    else:
        print("❌ Error: client_server_demo.py not found in implementations/")
        print("   Make sure you're running this from the ClientServer_P2P directory")

def run_peer_to_peer():
    """Launch peer-to-peer demonstration"""
    print("\n🌐 LAUNCHING PEER-TO-PEER DEMO")
    print("="*40)
    print("Starting the distributed peer-to-peer network demonstration...")
    
    impl_path = Path("implementations/peer_to_peer_demo.py")
    if impl_path.exists():
        try:
            subprocess.run([sys.executable, str(impl_path)], cwd="implementations")
        except KeyboardInterrupt:
            print("\n👋 Peer-to-Peer demo stopped.")
    else:
        print("❌ Error: peer_to_peer_demo.py not found in implementations/")
        print("   Make sure you're running this from the ClientServer_P2P directory")

def run_comparison():
    """Launch interactive comparison tool"""
    print("\n🔄 LAUNCHING INTERACTIVE COMPARISON")
    print("="*45)
    print("Starting the architecture comparison tool...")
    
    demo_path = Path("demos/architecture_comparison.py")
    if demo_path.exists():
        try:
            subprocess.run([sys.executable, str(demo_path)], cwd="demos")
        except KeyboardInterrupt:
            print("\n👋 Comparison tool stopped.")
    else:
        print("❌ Error: architecture_comparison.py not found in demos/")
        print("   Make sure you're running this from the ClientServer_P2P directory")

def view_guide():
    """Display the architecture guide"""
    print("\n📖 ARCHITECTURE GUIDE")
    print("="*30)
    
    readme_path = Path("README.md")
    if readme_path.exists():
        print("Opening README.md with comprehensive architecture guide...")
        try:
            # Try to open with default system viewer
            if sys.platform.startswith('win'):
                os.startfile(readme_path)
            elif sys.platform.startswith('darwin'):
                subprocess.run(['open', str(readme_path)])
            else:
                subprocess.run(['xdg-open', str(readme_path)])
        except:
            print("📄 Displaying first section of the guide:")
            with open(readme_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:50]  # Show first 50 lines
                print(''.join(lines))
                print("\n... (See README.md for the complete guide)")
    else:
        print("❌ Error: README.md not found")

def explore_structure():
    """Show the file structure"""
    print("\n🗂️  PROJECT STRUCTURE")
    print("="*30)
    print("""
ClientServer_P2P/
├── README.md                    # Comprehensive architecture guide
├── quick_start.py              # This quick start script
├── implementations/            # Core architecture implementations
│   ├── client_server_demo.py   # Centralized file server demo
│   └── peer_to_peer_demo.py    # Distributed P2P network demo
├── examples/                   # Real-world usage examples
└── demos/                     # Interactive demonstrations
    └── architecture_comparison.py  # Architecture comparison tool
    """)
    
    print("\n📁 Available files:")
    for root, dirs, files in os.walk('.'):
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if file.endswith(('.py', '.md')):
                print(f"{subindent}{file}")

def show_help():
    """Display help information"""
    print("\n❓ HELP & DOCUMENTATION")
    print("="*35)
    print("""
🎯 PURPOSE:
This toolkit helps you understand Client-Server vs Peer-to-Peer architectures
through hands-on demonstrations and interactive examples.

🚀 GETTING STARTED:
1. Start with the Quick Demo (option 1) for an overview
2. Try individual implementations (options 2-3)
3. Use the comparison tool (option 4) to understand trade-offs
4. Read the full guide (option 5) for comprehensive theory

🔧 REQUIREMENTS:
- Python 3.6 or higher
- Standard library only (no external dependencies)
- Multiple terminal windows for full demos

📚 LEARNING PATH:
1. Understand the theory (README.md)
2. Run Client-Server demo to see centralized architecture
3. Run P2P demo to see distributed architecture  
4. Compare both using the interactive tool
5. Experiment with modifications

🆘 TROUBLESHOOTING:
- Make sure you're in the ClientServer_P2P directory
- Check that Python 3.6+ is installed
- For network demos, ensure ports 8000-9003 are available
- Use Ctrl+C to stop running demos
    """)

def main():
    """Main program loop"""
    print_banner()
    print_architecture_overview()
    
    while True:
        show_menu()
        
        try:
            choice = input("\n🔢 Enter your choice (1-8): ").strip()
            
            if choice == '1':
                quick_demo()
            elif choice == '2':
                run_client_server()
            elif choice == '3':
                run_peer_to_peer()
            elif choice == '4':
                run_comparison()
            elif choice == '5':
                view_guide()
            elif choice == '6':
                explore_structure()
            elif choice == '7':
                show_help()
            elif choice == '8':
                print("\n👋 Thanks for exploring Client-Server vs P2P architectures!")
                print("🎓 Keep building amazing distributed systems!")
                break
            else:
                print("❌ Invalid choice. Please enter a number from 1-8.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for exploring network architectures!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            continue
        
        input("\n⏎ Press Enter to continue...")

if __name__ == "__main__":
    main() 