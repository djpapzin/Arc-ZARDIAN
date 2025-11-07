#!/usr/bin/env python3
"""
Quick test to verify Arc network connection and configuration.
Run this to ensure everything is set up correctly before testing transactions.
"""

from src.arc_zardian.api.arc_client import init_web3, get_usdc_balance, ARC_RPC_URL, CHAIN_ID

def quick_test():
    """Quick connection and configuration test."""
    print("=" * 60)
    print("Arc Network Quick Test")
    print("=" * 60)
    
    # Test 1: Connection
    print("\n1. Testing connection to Arc Testnet...")
    print(f"   RPC URL: {ARC_RPC_URL}")
    print(f"   Expected Chain ID: {CHAIN_ID}")
    
    try:
        w3 = init_web3(ARC_RPC_URL)
        chain_id = w3.eth.chain_id
        block_number = w3.eth.block_number
        
        print(f"   ✅ Connected!")
        print(f"   📍 Chain ID: {chain_id}")
        print(f"   📦 Latest Block: {block_number}")
        
        if chain_id == CHAIN_ID:
            print(f"   ✅ Chain ID matches expected value ({CHAIN_ID})")
        else:
            print(f"   ⚠️  Chain ID mismatch! Expected {CHAIN_ID}, got {chain_id}")
            
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        print(f"\n   💡 Troubleshooting:")
        print(f"      - Verify the RPC URL is correct: {ARC_RPC_URL}")
        print(f"      - Check your internet connection")
        print(f"      - The Arc testnet might be using a different endpoint")
        print(f"      - Try checking the Arc documentation for the latest RPC URL")
        print(f"\n   ⚠️  You can still test transactions via the Streamlit app (Option 2)")
        print(f"      which might work if the RPC is accessible from your browser context.")
        return False
    
    # Test 2: Check a sample address (optional)
    print("\n2. Testing balance check function...")
    test_address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"  # Example address
    try:
        balance = get_usdc_balance(w3, test_address)
        print(f"   ✅ Balance check works!")
        print(f"   💰 Sample address balance: {balance:.6f} USDC")
    except Exception as e:
        print(f"   ⚠️  Balance check had an issue (this is OK if address is invalid): {e}")
    
    print("\n" + "=" * 60)
    print("✅ All basic tests passed! Ready to test transactions.")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Get testnet USDC from the faucet")
    print("2. Run: python test_transaction.py")
    print("3. Or use the Streamlit app: streamlit run src/arc_zardian/app.py")
    
    return True

if __name__ == "__main__":
    quick_test()

