#!/usr/bin/env python3
"""
Test script for sending a USDC transaction on Arc Testnet.
This script helps test the transaction functionality independently.

Usage:
    python test_transaction.py
    
Note: You'll need:
1. A testnet account with USDC balance
2. The private key for that account (for testing only!)
3. A recipient address to send USDC to
"""

import os
from src.arc_zardian.api.arc_client import (
    send_usdc_on_arc,
    get_usdc_balance,
    init_web3,
    ARC_RPC_URL,
    CHAIN_ID
)

def test_connection():
    """Test connection to Arc network."""
    print("🔗 Testing connection to Arc Testnet...")
    try:
        w3 = init_web3(ARC_RPC_URL)
        chain_id = w3.eth.chain_id
        latest_block = w3.eth.block_number
        
        print(f"✅ Connected to Arc Testnet!")
        print(f"   Chain ID: {chain_id}")
        print(f"   Expected: {CHAIN_ID}")
        print(f"   Latest Block: {latest_block}")
        
        if chain_id != CHAIN_ID:
            print(f"⚠️  Warning: Chain ID mismatch! Expected {CHAIN_ID}, got {chain_id}")
        else:
            print(f"✅ Chain ID matches!")
            
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def check_balance(address: str):
    """Check USDC balance for an address."""
    print(f"\n💰 Checking USDC balance for {address}...")
    try:
        w3 = init_web3(ARC_RPC_URL)
        balance = get_usdc_balance(w3, address)
        print(f"✅ Balance: {balance:.6f} USDC")
        return balance
    except Exception as e:
        print(f"❌ Failed to check balance: {e}")
        return None

def test_transaction(
    sender_private_key: str,
    recipient_address: str,
    amount: float
):
    """Test sending a USDC transaction."""
    print(f"\n🚀 Testing USDC transaction...")
    print(f"   Amount: {amount} USDC")
    print(f"   Recipient: {recipient_address}")
    
    # Check sender balance first
    from eth_account import Account
    sender_account = Account.from_key(sender_private_key)
    sender_address = sender_account.address
    print(f"   Sender: {sender_address}")
    
    sender_balance = check_balance(sender_address)
    if sender_balance is None:
        print("❌ Cannot proceed without checking sender balance")
        return False
    
    if sender_balance < amount:
        print(f"❌ Insufficient balance! Have {sender_balance:.6f} USDC, need {amount}")
        return False
    
    print(f"✅ Sufficient balance available")
    
    # Send transaction
    try:
        success, result = send_usdc_on_arc(
            sender_private_key=sender_private_key,
            recipient_address=recipient_address,
            amount=amount
        )
        
        if success:
            print(f"✅ Transaction sent successfully!")
            print(f"   Transaction Hash: {result}")
            print(f"   View on Explorer: https://explorer.arc.network/tx/{result}")
            
            # Check recipient balance after transaction
            print(f"\n⏳ Waiting a moment before checking recipient balance...")
            import time
            time.sleep(5)  # Wait a bit for transaction to be processed
            
            recipient_balance = check_balance(recipient_address)
            return True
        else:
            print(f"❌ Transaction failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending transaction: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("=" * 60)
    print("Arc Network USDC Transaction Test")
    print("=" * 60)
    
    # Test connection
    if not test_connection():
        print("\n❌ Cannot proceed without network connection")
        return
    
    # Get test parameters from environment or user input
    print("\n" + "=" * 60)
    print("Transaction Parameters")
    print("=" * 60)
    
    # Get sender private key
    sender_key = os.getenv("SENDER_PRIVATE_KEY")
    if not sender_key:
        print("\n⚠️  SENDER_PRIVATE_KEY not found in environment variables")
        print("   You can set it with: export SENDER_PRIVATE_KEY=0x...")
        sender_key = input("\nEnter sender private key (0x...): ").strip()
    
    if not sender_key or not sender_key.startswith("0x"):
        print("❌ Invalid private key format")
        return
    
    # Get recipient address
    recipient = os.getenv("RECIPIENT_ADDRESS")
    if not recipient:
        recipient = input("\nEnter recipient address (0x...): ").strip()
    
    if not recipient or not recipient.startswith("0x"):
        print("❌ Invalid recipient address format")
        return
    
    # Get amount
    amount_str = os.getenv("AMOUNT", "0.01")
    try:
        amount = float(amount_str)
    except ValueError:
        amount = 0.01
        print(f"⚠️  Invalid amount, using default: {amount} USDC")
    
    print(f"\n📋 Transaction Summary:")
    print(f"   Amount: {amount} USDC")
    print(f"   Recipient: {recipient}")
    
    # Confirm before sending
    confirm = input("\n⚠️  Confirm sending transaction? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("❌ Transaction cancelled")
        return
    
    # Execute test
    test_transaction(sender_key, recipient, amount)
    
    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()

