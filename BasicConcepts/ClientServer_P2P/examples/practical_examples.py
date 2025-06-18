#!/usr/bin/env python3
"""
Practical Examples: Client-Server vs Peer-to-Peer Architectures

This file contains simplified examples of real-world systems that use
both Client-Server and Peer-to-Peer architectures, demonstrating when
and why to choose each approach.

Usage:
    python practical_examples.py
"""

import json
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Optional

# ============================================================================
# CLIENT-SERVER EXAMPLES
# ============================================================================

class BankingSystem:
    """
    Example: Banking System (Client-Server)
    
    Why Client-Server?
    - Security: Centralized control over all transactions
    - Compliance: Easier to meet regulatory requirements
    - Consistency: Single source of truth for account balances
    - Trust: Bank is the trusted authority
    """
    
    def __init__(self):
        self.accounts = {
            "alice": {"balance": 1000.0, "transactions": []},
            "bob": {"balance": 500.0, "transactions": []}
        }
        self.transaction_log = []
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Simulate user authentication"""
        # In real system, would check hashed passwords
        valid_users = {"alice": "password123", "bob": "secret456"}
        return valid_users.get(username) == password
    
    def get_balance(self, username: str) -> Optional[float]:
        """Get account balance (server authorizes request)"""
        if username in self.accounts:
            return self.accounts[username]["balance"]
        return None
    
    def transfer_money(self, from_user: str, to_user: str, amount: float) -> bool:
        """Transfer money between accounts (centralized validation)"""
        if (from_user in self.accounts and to_user in self.accounts and 
            self.accounts[from_user]["balance"] >= amount):
            
            # Atomic transaction - both operations must succeed
            self.accounts[from_user]["balance"] -= amount
            self.accounts[to_user]["balance"] += amount
            
            # Log transaction
            transaction = {
                "timestamp": datetime.now().isoformat(),
                "from": from_user,
                "to": to_user,
                "amount": amount,
                "type": "transfer"
            }
            
            self.transaction_log.append(transaction)
            self.accounts[from_user]["transactions"].append(transaction)
            self.accounts[to_user]["transactions"].append(transaction)
            
            return True
        return False

class WebServer:
    """
    Example: Web Server (Client-Server)
    
    Why Client-Server?
    - Content Control: Server manages what content is available
    - Caching: Efficient content delivery from central location
    - Security: Protected business logic and data
    - Updates: Easy to update content for all users
    """
    
    def __init__(self):
        self.pages = {
            "/": "<html><body><h1>Welcome to our website!</h1></body></html>",
            "/about": "<html><body><h1>About Us</h1><p>We are a company...</p></body></html>",
            "/products": "<html><body><h1>Our Products</h1><ul><li>Product 1</li></ul></body></html>"
        }
        self.user_sessions = {}
    
    def handle_request(self, path: str, user_id: str = None) -> Dict:
        """Handle HTTP request from client"""
        response = {
            "timestamp": datetime.now().isoformat(),
            "status": 200,
            "headers": {"Content-Type": "text/html"},
            "body": ""
        }
        
        if path in self.pages:
            response["body"] = self.pages[path]
            
            # Log user session
            if user_id:
                if user_id not in self.user_sessions:
                    self.user_sessions[user_id] = []
                self.user_sessions[user_id].append({
                    "timestamp": datetime.now().isoformat(),
                    "path": path,
                    "ip": "192.168.1.100"  # Simulated
                })
        else:
            response["status"] = 404
            response["body"] = "<html><body><h1>404 - Page Not Found</h1></body></html>"
        
        return response

# ============================================================================
# PEER-TO-PEER EXAMPLES
# ============================================================================

class BitTorrentPeer:
    """
    Example: BitTorrent-style File Sharing (Peer-to-Peer)
    
    Why Peer-to-Peer?
    - Scalability: More peers = better performance
    - Cost: No expensive central servers needed
    - Resilience: System works even if some peers leave
    - Bandwidth: Distributed across all participants
    """
    
    def __init__(self, peer_id: str):
        self.peer_id = peer_id
        self.files = {}  # files this peer has
        self.partial_files = {}  # files being downloaded
        self.known_peers = set()
        self.connections = {}
    
    def add_file(self, filename: str, content: str):
        """Add a file to share with the network"""
        file_hash = hashlib.md5(content.encode()).hexdigest()
        self.files[filename] = {
            "content": content,
            "hash": file_hash,
            "size": len(content),
            "pieces": self._split_into_pieces(content)
        }
    
    def _split_into_pieces(self, content: str, piece_size: int = 10) -> List[str]:
        """Split file into pieces for distributed sharing"""
        return [content[i:i+piece_size] for i in range(0, len(content), piece_size)]
    
    def discover_peers(self, tracker_response: List[str]):
        """Discover other peers from tracker (hybrid approach)"""
        self.known_peers.update(tracker_response)
    
    def request_file(self, filename: str) -> Optional[Dict]:
        """Request file from network of peers"""
        # In real BitTorrent, would request from multiple peers simultaneously
        for peer_id in self.known_peers:
            peer = self.connections.get(peer_id)
            if peer and filename in peer.files:
                return {
                    "filename": filename,
                    "peer_source": peer_id,
                    "file_info": peer.files[filename]
                }
        return None
    
    def share_file_list(self) -> List[str]:
        """Share list of available files with other peers"""
        return list(self.files.keys())

class BlockchainNetwork:
    """
    Example: Simple Blockchain (Peer-to-Peer)
    
    Why Peer-to-Peer?
    - Decentralization: No single point of control
    - Trust: Consensus mechanism ensures validity
    - Censorship Resistance: Difficult to shut down
    - Transparency: All transactions are public
    """
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.blockchain = [self._create_genesis_block()]
        self.pending_transactions = []
        self.connected_nodes = set()
        self.balances = {"genesis": 1000}  # Initial balance
    
    def _create_genesis_block(self) -> Dict:
        """Create the first block in the blockchain"""
        return {
            "index": 0,
            "timestamp": datetime.now().isoformat(),
            "transactions": [],
            "previous_hash": "0",
            "hash": self._calculate_hash(0, [], "0")
        }
    
    def _calculate_hash(self, index: int, transactions: List, previous_hash: str) -> str:
        """Calculate block hash"""
        block_string = f"{index}{transactions}{previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def add_transaction(self, from_addr: str, to_addr: str, amount: float) -> bool:
        """Add transaction to pending pool"""
        if self.balances.get(from_addr, 0) >= amount:
            transaction = {
                "from": from_addr,
                "to": to_addr,
                "amount": amount,
                "timestamp": datetime.now().isoformat()
            }
            self.pending_transactions.append(transaction)
            return True
        return False
    
    def mine_block(self) -> Dict:
        """Mine a new block (simplified proof of work)"""
        if not self.pending_transactions:
            return None
        
        previous_block = self.blockchain[-1]
        new_block = {
            "index": len(self.blockchain),
            "timestamp": datetime.now().isoformat(),
            "transactions": self.pending_transactions.copy(),
            "previous_hash": previous_block["hash"]
        }
        
        new_block["hash"] = self._calculate_hash(
            new_block["index"],
            new_block["transactions"],
            new_block["previous_hash"]
        )
        
        # Update balances
        for tx in self.pending_transactions:
            self.balances[tx["from"]] -= tx["amount"]
            self.balances[tx["to"]] = self.balances.get(tx["to"], 0) + tx["amount"]
        
        self.blockchain.append(new_block)
        self.pending_transactions = []
        
        return new_block
    
    def validate_chain(self) -> bool:
        """Validate the entire blockchain"""
        for i in range(1, len(self.blockchain)):
            current_block = self.blockchain[i]
            previous_block = self.blockchain[i-1]
            
            if current_block["previous_hash"] != previous_block["hash"]:
                return False
        
        return True

# ============================================================================
# DEMONSTRATION FUNCTIONS
# ============================================================================

def demo_banking_system():
    """Demonstrate banking system (Client-Server)"""
    print("\n🏦 BANKING SYSTEM DEMO (Client-Server)")
    print("="*50)
    
    bank = BankingSystem()
    
    print("Initial balances:")
    print(f"Alice: ${bank.get_balance('alice')}")
    print(f"Bob: ${bank.get_balance('bob')}")
    
    print("\n💸 Alice transfers $200 to Bob...")
    success = bank.transfer_money("alice", "bob", 200.0)
    print(f"Transfer successful: {success}")
    
    print("\nUpdated balances:")
    print(f"Alice: ${bank.get_balance('alice')}")
    print(f"Bob: ${bank.get_balance('bob')}")
    
    print(f"\nTransaction log entries: {len(bank.transaction_log)}")

def demo_web_server():
    """Demonstrate web server (Client-Server)"""
    print("\n🌐 WEB SERVER DEMO (Client-Server)")
    print("="*50)
    
    server = WebServer()
    
    # Simulate client requests
    requests = ["/", "/about", "/products", "/nonexistent"]
    
    for path in requests:
        response = server.handle_request(path, "user123")
        print(f"\nRequest: {path}")
        print(f"Status: {response['status']}")
        print(f"Content preview: {response['body'][:50]}...")

def demo_bittorrent():
    """Demonstrate BitTorrent-style sharing (P2P)"""
    print("\n📁 BITTORRENT DEMO (Peer-to-Peer)")
    print("="*50)
    
    # Create peers
    alice = BitTorrentPeer("alice")
    bob = BitTorrentPeer("bob")
    charlie = BitTorrentPeer("charlie")
    
    # Connect peers
    alice.known_peers.add("bob")
    alice.known_peers.add("charlie")
    alice.connections = {"bob": bob, "charlie": charlie}
    
    # Add files to peers
    alice.add_file("song.mp3", "This is a great song! " * 10)
    bob.add_file("movie.mp4", "Amazing movie content! " * 20)
    charlie.add_file("document.pdf", "Important document text! " * 15)
    
    print("Files available in network:")
    all_peers = [alice, bob, charlie]
    for peer in all_peers:
        print(f"{peer.peer_id}: {list(peer.files.keys())}")
    
    print(f"\n🔍 Alice searching for 'movie.mp4'...")
    result = alice.request_file("movie.mp4")
    if result:
        print(f"Found at peer: {result['peer_source']}")
        print(f"File size: {result['file_info']['size']} bytes")

def demo_blockchain():
    """Demonstrate blockchain network (P2P)"""
    print("\n⛓️  BLOCKCHAIN DEMO (Peer-to-Peer)")
    print("="*50)
    
    # Create blockchain nodes
    node1 = BlockchainNetwork("node1")
    
    print("Initial blockchain:")
    print(f"Blocks: {len(node1.blockchain)}")
    print(f"Genesis balance: {node1.balances}")
    
    # Add transactions
    print(f"\n💰 Adding transactions...")
    node1.balances["alice"] = 100  # Give Alice some coins
    node1.add_transaction("alice", "bob", 50)
    node1.add_transaction("genesis", "charlie", 200)
    
    print(f"Pending transactions: {len(node1.pending_transactions)}")
    
    # Mine block
    print(f"\n⛏️  Mining new block...")
    new_block = node1.mine_block()
    
    if new_block:
        print(f"Block mined! New blockchain length: {len(node1.blockchain)}")
        print(f"Updated balances: {node1.balances}")
        print(f"Chain valid: {node1.validate_chain()}")

def comparison_summary():
    """Show architecture comparison summary"""
    print("\n📊 ARCHITECTURE COMPARISON SUMMARY")
    print("="*50)
    
    print("\n🏛️  CLIENT-SERVER BEST FOR:")
    print("   ✅ Banking: Security, compliance, trust")
    print("   ✅ Web Services: Content control, caching")
    print("   ✅ Enterprise: Centralized management")
    
    print("\n🌐 PEER-TO-PEER BEST FOR:")
    print("   ✅ File Sharing: Distributed bandwidth")
    print("   ✅ Blockchain: Decentralized trust")
    print("   ✅ Gaming: Reduced server costs")
    
    print("\n🔄 HYBRID APPROACHES:")
    print("   🔗 BitTorrent: P2P + Central tracker")
    print("   🔗 Skype: P2P calls + Central directory")
    print("   🔗 CDNs: Central content + Edge distribution")

def main():
    """Main demonstration runner"""
    print("🎯 PRACTICAL ARCHITECTURE EXAMPLES")
    print("="*60)
    print("Real-world examples of Client-Server vs Peer-to-Peer systems")
    
    try:
        demo_banking_system()
        input("\n⏎ Press Enter to continue to Web Server demo...")
        
        demo_web_server()
        input("\n⏎ Press Enter to continue to BitTorrent demo...")
        
        demo_bittorrent()
        input("\n⏎ Press Enter to continue to Blockchain demo...")
        
        demo_blockchain()
        input("\n⏎ Press Enter to see comparison summary...")
        
        comparison_summary()
        
        print("\n🎓 CONCLUSION:")
        print("Choose your architecture based on your specific needs:")
        print("• Security & Control → Client-Server")
        print("• Scalability & Cost → Peer-to-Peer")
        print("• Best of Both → Hybrid Approach")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Thanks for exploring!")

if __name__ == "__main__":
    main() 