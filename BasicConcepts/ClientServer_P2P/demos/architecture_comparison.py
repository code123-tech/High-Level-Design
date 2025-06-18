"""
Client-Server vs P2P Architecture Comparison
==========================================
"""

def show_comparison():
    """Show detailed comparison"""
    print("🏛️ Client-Server vs 🌐 Peer-to-Peer")
    print("=" * 50)
    
    print(f"{'Aspect':<20} {'Client-Server':<25} {'P2P':<25}")
    print("-" * 70)
    print(f"{'Communication':<20} {'Client → Server':<25} {'Peer ↔ Peer':<25}")
    print(f"{'Control':<20} {'Centralized':<25} {'Distributed':<25}")
    print(f"{'Data Storage':<20} {'Central Server':<25} {'Distributed':<25}")
    print(f"{'Failure Risk':<20} {'Single Point':<25} {'Resilient':<25}")
    print(f"{'Scalability':<20} {'Server Bottleneck':<25} {'Natural Growth':<25}")
    print(f"{'Security':<20} {'Easier to Secure':<25} {'Complex Trust':<25}")
    print()

def show_examples():
    """Show real-world examples"""
    print("🌍 Real-World Examples")
    print("=" * 30)
    
    print("🏛️ Client-Server:")
    print("• 🌐 Web browsing (browser → web server)")
    print("• 📧 Email (client → mail server)")
    print("• 🏦 Banking (app → bank server)")
    print("• 🎮 Online games (game → game server)")
    print()
    
    print("🌐 Peer-to-Peer:")
    print("• 📥 BitTorrent (file sharing)")
    print("• 💰 Bitcoin (cryptocurrency)")
    print("• 📞 Skype calls (direct connection)")
    print("• 💬 Mesh messaging (device to device)")
    print()

def show_decision_guide():
    """Show when to use each"""
    print("🤔 When to Use Each Architecture")
    print("=" * 35)
    
    print("🏛️ Use Client-Server When:")
    print("• Security is critical")
    print("• Need centralized control")
    print("• Compliance requirements")
    print("• Consistent user experience needed")
    print()
    
    print("🌐 Use P2P When:")
    print("• Want to minimize costs")
    print("• Natural scaling is important")
    print("• Avoiding censorship")
    print("• Users can contribute resources")
    print()

def interactive_quiz():
    """Simple quiz"""
    print("🧠 Quick Quiz")
    print("=" * 15)
    
    scenarios = [
        ("🏦 Banking app", "Client-Server", "Security and compliance needed"),
        ("📁 File sharing", "P2P", "Distributed bandwidth benefits"),
        ("📧 Email system", "Client-Server", "Reliable routing needed")
    ]
    
    score = 0
    for i, (scenario, correct, reason) in enumerate(scenarios, 1):
        print(f"\n{i}. What's best for {scenario}?")
        print("1. Client-Server")
        print("2. P2P")
        
        try:
            choice = int(input("Your choice (1 or 2): "))
            answer = "Client-Server" if choice == 1 else "P2P"
            
            if answer == correct:
                print("✅ Correct!")
                score += 1
            else:
                print(f"❌ Best answer: {correct}")
            
            print(f"💡 Why: {reason}")
            
        except ValueError:
            print("❌ Invalid input")
    
    print(f"\n🎯 Score: {score}/{len(scenarios)}")

def main():
    """Main menu"""
    print("🏗️ Architecture Comparison Tool")
    print("=" * 35)
    
    while True:
        print("\nOptions:")
        print("1. 📊 Compare Architectures")
        print("2. 🌍 See Examples")
        print("3. 🤔 Decision Guide")
        print("4. 🧠 Take Quiz")
        print("5. 🚀 Run Demos")
        print("6. ❌ Exit")
        
        choice = input("Choice (1-6): ")
        
        if choice == "1":
            show_comparison()
        elif choice == "2":
            show_examples()
        elif choice == "3":
            show_decision_guide()
        elif choice == "4":
            interactive_quiz()
        elif choice == "5":
            print("\n🚀 Demo Files:")
            print("• python client_server_demo.py")
            print("• python peer_to_peer_demo.py")
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main() 