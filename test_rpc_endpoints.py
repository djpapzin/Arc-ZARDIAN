#!/usr/bin/env python3
"""
Test script to check which RPC endpoints are working and their chain IDs.
This helps diagnose connection issues.
"""

from web3 import Web3
from src.arc_zardian.api.arc_client import ARC_RPC_URLS, CHAIN_ID

def test_endpoints():
    """Test all RPC endpoints and show their status."""
    print("=" * 70)
    print("Arc Network RPC Endpoint Test")
    print("=" * 70)
    print(f"Expected Chain ID: {CHAIN_ID}")
    print(f"Testing {len(ARC_RPC_URLS)} endpoints...\n")
    
    working_endpoints = []
    failed_endpoints = []
    
    for rpc_url in ARC_RPC_URLS:
        print(f"Testing: {rpc_url}")
        try:
            provider = Web3.HTTPProvider(
                rpc_url,
                request_kwargs={'timeout': 10}
            )
            w3 = Web3(provider)
            
            # Try to get chain ID
            try:
                chain_id = w3.eth.chain_id
                block_number = w3.eth.block_number
                
                status = "✅ WORKING"
                if chain_id == CHAIN_ID:
                    status += " (CORRECT CHAIN ID)"
                    working_endpoints.append((rpc_url, chain_id, block_number))
                else:
                    status += f" (WRONG CHAIN ID: {chain_id})"
                    failed_endpoints.append((rpc_url, f"Wrong chain ID: {chain_id}"))
                
                print(f"  {status}")
                print(f"  Chain ID: {chain_id}")
                print(f"  Block Number: {block_number}")
                
            except Exception as e:
                print(f"  ❌ Connected but failed to get chain ID: {str(e)}")
                failed_endpoints.append((rpc_url, str(e)))
                
        except Exception as e:
            print(f"  ❌ Connection failed: {str(e)}")
            failed_endpoints.append((rpc_url, str(e)))
        
        print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    if working_endpoints:
        print(f"\n✅ {len(working_endpoints)} working endpoint(s) with correct chain ID:")
        for url, chain_id, block in working_endpoints:
            print(f"   - {url} (Chain ID: {chain_id}, Block: {block})")
    else:
        print("\n❌ No working endpoints found with correct chain ID!")
    
    if failed_endpoints:
        print(f"\n⚠️  {len(failed_endpoints)} endpoint(s) failed:")
        for url, error in failed_endpoints:
            print(f"   - {url}")
            print(f"     Error: {error}")
    
    print("\n" + "=" * 70)
    
    if not working_endpoints:
        print("\n💡 SUGGESTIONS:")
        print("   1. Check if the Arc testnet chain ID has changed")
        print("   2. Verify the RPC endpoints are correct")
        print("   3. Check your internet connection")
        print("   4. Try accessing the endpoints directly in a browser")
        print("   5. Check if there's a firewall blocking connections")

if __name__ == "__main__":
    test_endpoints()

