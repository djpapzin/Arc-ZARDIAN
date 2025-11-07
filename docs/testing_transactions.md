# Testing Transactions on Arc Network

This guide explains how to test USDC transactions on the Arc Testnet.

## Prerequisites

1. **Arc Testnet Account**: You need a testnet account with USDC balance
2. **Private Key**: The private key for your testnet account (for testing only!)
3. **Recipient Address**: A valid Arc address to send USDC to

## Arc Network Configuration

Based on the [Arc Network documentation](https://docs.arc.network/arc/concepts/welcome-to-arc):

- **Network**: Arc Testnet
- **Chain ID**: 1243
- **RPC URL**: `https://rpc-testnet.archivenode.io/`
- **USDC Contract**: `0x3600000000000000000000000000000000000000`
- **Explorer**: https://explorer.arc.network

## Testing Methods

### Method 1: Using the Streamlit App

1. Start the Streamlit app:
   ```bash
   streamlit run src/arc_zardian/app.py
   ```

2. Navigate to the app in your browser (usually `http://localhost:8501`)

3. Enter a ZAR amount and find the best conversion path

4. In the "Send USDC on Arc Network" section:
   - Enter recipient's Arc address
   - Enter USDC amount to send
   - Enter your private key (⚠️ for testing only!)
   - Click "Send USDC on Arc"

5. View the transaction hash and check it on the [Arc Explorer](https://explorer.arc.network)

### Method 2: Using the Test Script

1. Run the test script:
   ```bash
   python test_transaction.py
   ```

2. The script will:
   - Test connection to Arc Testnet
   - Check sender balance
   - Check recipient balance (before and after)
   - Send the transaction
   - Display transaction hash

3. You can also set environment variables:
   ```bash
   export SENDER_PRIVATE_KEY=0x...
   export RECIPIENT_ADDRESS=0x...
   export AMOUNT=0.01
   python test_transaction.py
   ```

### Method 3: Using Python Interactively

```python
from src.arc_zardian.api.arc_client import send_usdc_on_arc, get_usdc_balance, init_web3

# Initialize connection
w3 = init_web3("https://rpc-testnet.archivenode.io/")

# Check balance
balance = get_usdc_balance(w3, "0xYourAddress")

# Send transaction
success, result = send_usdc_on_arc(
    sender_private_key="0xYourPrivateKey",
    recipient_address="0xRecipientAddress",
    amount=0.01  # USDC amount
)

if success:
    print(f"Transaction hash: {result}")
    print(f"View on explorer: https://explorer.arc.network/tx/{result}")
else:
    print(f"Error: {result}")
```

## Getting Testnet USDC

To get testnet USDC for testing:

1. Check the [Arc Faucet](https://docs.arc.network/arc/get-started/faucet) if available
2. Request testnet tokens from the Arc community
3. Use a test account provided by the hackathon organizers

## Important Security Notes

⚠️ **WARNING**: The current implementation requires entering private keys in the UI. This is **ONLY for hackathon/demo purposes**.

**NEVER**:
- Use real private keys in production
- Expose private keys in client-side code
- Commit private keys to version control

**For production**, use:
- Hardware wallets
- Wallet connectors (MetaMask, WalletConnect)
- Secure key management services
- Backend signing with secure key storage

## Troubleshooting

### Connection Issues

If you get connection errors:
1. Verify the RPC URL is correct: `https://rpc-testnet.archivenode.io/`
2. Check your internet connection
3. Verify the Arc testnet is operational

### Chain ID Mismatch

If you see "Connected to wrong network":
- Verify chain ID is 1243
- Check if you're using the correct RPC endpoint
- Ensure middleware is properly configured

### Insufficient Balance

If transaction fails due to insufficient balance:
1. Check your USDC balance using `get_usdc_balance()`
2. Ensure you have enough USDC for:
   - The transaction amount
   - Gas fees (paid in USDC on Arc)

### Transaction Fails

Common reasons:
- Invalid recipient address
- Insufficient gas
- Network congestion
- Invalid contract address

Check the error message for specific details.

## Verifying Transactions

After sending a transaction:

1. **Get Transaction Hash**: The function returns the transaction hash
2. **View on Explorer**: Visit `https://explorer.arc.network/tx/{tx_hash}`
3. **Check Balance**: Use `get_usdc_balance()` to verify the recipient received USDC
4. **Wait for Confirmation**: Arc has deterministic sub-second finality, so transactions should confirm quickly

## Example Transaction Flow

```python
# 1. Check sender balance
sender_balance = get_usdc_balance(w3, sender_address)
print(f"Sender has: {sender_balance} USDC")

# 2. Send transaction
success, tx_hash = send_usdc_on_arc(
    sender_private_key=private_key,
    recipient_address=recipient,
    amount=1.0
)

# 3. Verify transaction
if success:
    print(f"Sent! Hash: {tx_hash}")
    print(f"View: https://explorer.arc.network/tx/{tx_hash}")
    
    # Check recipient balance after a moment
    import time
    time.sleep(2)
    recipient_balance = get_usdc_balance(w3, recipient)
    print(f"Recipient now has: {recipient_balance} USDC")
```

## Next Steps

- [Arc Network Documentation](https://docs.arc.network/)
- [Arc Explorer](https://explorer.arc.network)
- [Deploy on Arc Quickstart](https://docs.arc.network/arc/get-started/deploy-on-arc)

