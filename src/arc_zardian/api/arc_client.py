from web3 import Web3
from web3.middleware.proof_of_authority import ExtraDataToPOAMiddleware
from eth_account import Account
from typing import Tuple, Optional, Dict
import os
import json

# Arc Network Configuration
# Official Arc Testnet (Chain ID 5042002) - Circle's Economic OS
# Based on expert infrastructure analysis and official documentation

# Tiered RPC endpoint strategy for resilience:
# Tier 1: Official public endpoint (Circle-managed)
# Tier 2: Public mirror endpoint (community-maintained)
# Tier 3: IaaS endpoints (for production-grade testing - require API keys)
ARC_RPC_URLS = [
    "https://rpc.testnet.arc.network",  # Tier 1: Official Circle public endpoint
    "https://arc-testnet.drpc.org",  # Tier 2: Public mirror endpoint
    "https://rpc.blockdaemon.testnet.arc.network",  # Tier 3: IaaS (Blockdaemon)
    "https://rpc.drpc.testnet.arc.network",  # Tier 3: IaaS (dRPC)
    "https://rpc.quicknode.testnet.arc.network",  # Tier 3: IaaS (QuickNode)
]

ARC_RPC_URL = ARC_RPC_URLS[0]  # Default to official endpoint

# Arc Testnet Chain ID (Official)
# Chain ID 1243 was associated with legacy/decommissioned infrastructure
# Current active Arc Testnet uses Chain ID 5042002
CHAIN_ID = 5042002  # Official Arc Testnet Chain ID
ACCEPTED_CHAIN_IDS = [5042002]  # Only accept the official chain ID

# Connection Configuration
RPC_TIMEOUT = 30  # Minimum 30 seconds for BFT consensus engine and complex queries

def get_web3():
    """Initialize Web3 with the first working RPC endpoint"""
    for rpc_url in ARC_RPC_URLS:
        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url))
            # Test the connection
            if w3.is_connected():
                print(f"✅ Connected to {rpc_url}")
                return w3
        except Exception as e:
            print(f"❌ Failed to connect to {rpc_url}: {str(e)}")
    
    raise ConnectionError("Could not connect to any Arc RPC endpoint. Please check your internet connection or try again later.")

# Set the default RPC URL to the first working one
try:
    w3 = get_web3()
    ARC_RPC_URL = w3.provider.endpoint_uri
    print(f"Using RPC endpoint: {ARC_RPC_URL}")
except Exception as e:
    print(f"⚠️ Could not connect to any RPC endpoint: {e}")
    ARC_RPC_URL = ARC_RPC_URLS[0]  # Fallback to first URL

# USDC contract address on Arc Testnet (Chain ID 5042002)
# Official testnet USDC contract - USDC is also the native gas token on Arc
USDC_CONTRACT_ADDRESS = "0x3600000000000000000000000000000000000000"  # Official Arc Testnet USDC

# ABI for ERC20 tokens (standard for USDC)
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "success", "type": "bool"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    }
]

def init_web3(rpc_url: str, timeout: int = RPC_TIMEOUT) -> Web3:
    """Initialize Web3 connection to the Arc Testnet (Chain ID 5042002).
    
    This function implements the recommended configuration from Arc infrastructure
    documentation: 30+ second timeouts for BFT consensus engine and PoA middleware
    injection for Malachite EVM compatibility.
    
    Args:
        rpc_url: RPC URL to connect to
        timeout: Connection timeout in seconds (default: 30, minimum recommended)
        
    Returns:
        Web3: Initialized Web3 instance with PoA middleware injected
        
    Raises:
        ConnectionError: If connection fails
    """
    try:
        # Create provider with increased timeout (30+ seconds recommended for BFT)
        # This accounts for Malachite consensus engine complexity and network jitter
        provider = Web3.HTTPProvider(
            rpc_url,
            request_kwargs={'timeout': timeout}
        )
        w3 = Web3(provider)
        
        # Test connection by getting chain ID (more reliable than is_connected())
        # This validates both connectivity and network identity
        try:
            chain_id = w3.eth.chain_id
            # If we got here, connection works
        except Exception as e:
            raise ConnectionError(f"Could not connect to RPC endpoint {rpc_url}: {str(e)}")
        
        # Inject PoA middleware at layer 0 (innermost layer) for Malachite EVM compatibility
        # This prevents ExtraDataLengthError from non-standard block header formatting
        # Required for Arc's custom BFT consensus engine sitting atop EVM
        try:
            # Modern web3.py naming (v7+)
            w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        except (TypeError, AttributeError):
            try:
                # Fallback: instantiate middleware if needed
                w3.middleware_onion.inject(ExtraDataToPOAMiddleware(), layer=0)
            except Exception:
                # Middleware injection failed, but connection works - log and continue
                # Some endpoints may not require PoA middleware
                pass
        
        return w3
        
    except ConnectionError:
        raise  # Re-raise connection errors
    except Exception as e:
        raise ConnectionError(f"Error initializing Web3 connection to {rpc_url}: {str(e)}")

def get_usdc_balance(w3: Web3, address: str) -> float:
    """Get USDC balance for the given address.
    
    Args:
        w3: Web3 instance
        address: Ethereum address to check balance for
        
    Returns:
        float: USDC balance
    """
    try:
        # Create USDC contract instance
        usdc_contract = w3.eth.contract(
            address=Web3.to_checksum_address(USDC_CONTRACT_ADDRESS),
            abi=ERC20_ABI
        )
        # Get USDC balance (USDC has 6 decimals)
        usdc_balance_wei = usdc_contract.functions.balanceOf(address).call()
        usdc_balance = usdc_balance_wei / 10**6
        return usdc_balance
    except Exception as e:
        raise Exception(f"Failed to get USDC balance: {str(e)}")

def get_wallet_balance(address: str, rpc_url: str = None) -> Dict:
    """Get native token and USDC balance for the given address.
    
    Args:
        address: Ethereum address to check balance for
        rpc_url: Optional RPC URL (uses default if None)
        
    Returns:
        dict: Dictionary containing native_balance (in ETH) and usdc_balance
    """
    # Try multiple RPC endpoints if one fails
    rpc_urls_to_try = [rpc_url] if rpc_url else ARC_RPC_URLS
    
    last_error = None
    for current_rpc in rpc_urls_to_try:
        try:
            # Initialize Web3 with the current RPC URL (using configured timeout)
            w3 = init_web3(current_rpc)
            
            # Verify chain ID (must be official Arc Testnet: 5042002)
            chain_id = w3.eth.chain_id
            if chain_id not in ACCEPTED_CHAIN_IDS:
                last_error = f'Wrong chain ID for {current_rpc}: expected {ACCEPTED_CHAIN_IDS[0]} (Arc Testnet), got {chain_id}. This endpoint may be pointing to a different network.'
                continue
            
            # Connection successful, proceed with balance check
            # Get native balance (in wei) and convert to ETH
            native_balance_wei = w3.eth.get_balance(address)
            native_balance = w3.from_wei(native_balance_wei, 'ether')
            
            # Get USDC balance if contract address is set
            usdc_balance = 0.0
            if USDC_CONTRACT_ADDRESS and USDC_CONTRACT_ADDRESS != "0x0000000000000000000000000000000000000000":
                try:
                    # Create USDC contract instance
                    usdc_contract = w3.eth.contract(
                        address=Web3.to_checksum_address(USDC_CONTRACT_ADDRESS),
                        abi=ERC20_ABI
                    )
                    # Get USDC balance (USDC has 6 decimals)
                    usdc_balance_wei = usdc_contract.functions.balanceOf(address).call()
                    usdc_balance = usdc_balance_wei / 10**6
                except Exception as usdc_err:
                    return {
                        'status': 'partial',
                        'native_balance': float(native_balance),
                        'usdc_balance': 0.0,
                        'message': f'Successfully connected to network. USDC balance check failed: {str(usdc_err)}',
                        'chain_id': w3.eth.chain_id,
                        'rpc_url': current_rpc
                    }
            
            # Success - return balance info
            actual_chain_id = w3.eth.chain_id
            return {
                'status': 'success',
                'native_balance': float(native_balance),
                'usdc_balance': usdc_balance,
                'chain_id': actual_chain_id,
                'rpc_url': current_rpc,
                'message': f'Connected to Arc network (Chain ID: {actual_chain_id})' if actual_chain_id != CHAIN_ID else None
            }
            
        except Exception as e:
            last_error = f'Error with {current_rpc}: {str(e)}'
            continue  # Try next RPC endpoint
    
    # All RPC endpoints failed
    return {
        'status': 'error',
        'message': f'Could not connect to any RPC endpoint. Last error: {last_error}',
        'rpc_urls_tried': rpc_urls_to_try
    }

def send_usdc_on_arc(
    sender_private_key: str,
    recipient_address: str,
    amount: float,
    arc_rpc_url: str = None
) -> Tuple[bool, Optional[str]]:
    """Send USDC on the Arc network.
    
    Args:
        sender_private_key: Private key of the sender (for demo purposes only)
        recipient_address: Recipient's Arc address
        amount: Amount of USDC to send
        arc_rpc_url: Optional Arc network RPC URL (uses fallback list if None)
        
    Returns:
        Tuple[bool, Optional[str]]: (success, transaction_hash_or_error_message)
    """
    # Try multiple RPC endpoints if one fails
    rpc_urls_to_try = [arc_rpc_url] if arc_rpc_url else ARC_RPC_URLS
    
    last_error = None
    for current_rpc in rpc_urls_to_try:
        try:
            # Initialize Web3 (connection already tested in init_web3)
            w3 = init_web3(current_rpc)
            
            # Validate chain ID (must be official Arc Testnet: 5042002)
            chain_id = w3.eth.chain_id
            if chain_id not in ACCEPTED_CHAIN_IDS:
                last_error = f"Wrong chain ID for {current_rpc}: expected {ACCEPTED_CHAIN_IDS[0]} (Arc Testnet), got {chain_id}. This endpoint may be pointing to a different network."
                continue
            
            # Get sender address from private key
            account = Account.from_key(sender_private_key)
            sender_address = account.address
            
            # Validate recipient address
            if not w3.is_address(recipient_address):
                return False, "Invalid recipient address"
                
            # Initialize USDC contract
            usdc_contract = w3.eth.contract(
                address=USDC_CONTRACT_ADDRESS,
                abi=ERC20_ABI
            )
            
            # Get token decimals
            decimals = usdc_contract.functions.decimals().call()
            amount_in_wei = int(amount * (10 ** decimals))
            
            # Build transaction
            nonce = w3.eth.get_transaction_count(sender_address)
            
            # Build the transfer function call
            transfer_func = usdc_contract.functions.transfer(
                recipient_address,
                amount_in_wei
            )
            
            # Estimate gas
            gas_estimate = transfer_func.estimate_gas({
                'from': sender_address,
                'nonce': nonce,
            })
            
            # Build and sign the transaction
            txn = transfer_func.build_transaction({
                'chainId': w3.eth.chain_id,
                'gas': gas_estimate,
                'gasPrice': w3.eth.gas_price,
                'nonce': nonce,
            })
            
            signed_txn = w3.eth.account.sign_transaction(txn, private_key=sender_private_key)
            
            # Send the transaction
            tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            # Wait for transaction receipt (optional, can be removed for faster response)
            # receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return True, tx_hash.hex()
            
        except Exception as e:
            last_error = f"Error with {current_rpc}: {str(e)}"
            continue  # Try next RPC endpoint
    
    # All RPC endpoints failed
    return False, f"Could not connect to any RPC endpoint. Last error: {last_error}"
