import streamlit as st
from typing import Dict
import asyncio
import os

from arc_zardian.core.optimizer import ConversionOptimizer, Exchange
from arc_zardian.core.models import ConversionPath, ConversionResult
from arc_zardian.api.arc_client import send_usdc_on_arc

# Set page config
st.set_page_config(
    page_title="Arc ZARDIAN - Optimal ZAR to USDC Converter",
    page_icon="💱",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .metric-box {
        background-color: #f0f2f6;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .best-option {
        border: 2px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.title("💱 Arc ZARDIAN")
st.markdown("### Find the best exchange rate for converting ZAR to USDC")
st.markdown("Compare rates across multiple exchanges to get the most USDC for your ZAR.")

# Input section
st.markdown("---")
col1, col2 = st.columns([2, 1])
with col1:
    zar_amount = st.number_input(
        "Enter ZAR Amount",
        min_value=0.01,
        value=1000.0,
        step=100.0,
        format="%.2f"
    )

# Convert button
if st.button("🚀 Find Best Conversion"):
    if zar_amount <= 0:
        st.error("Please enter a positive amount")
    else:
        with st.spinner("Finding the best conversion path..."):
            try:
                # Create optimizer and find best path
                optimizer = ConversionOptimizer()
                result = asyncio.run(optimizer.find_best_path(zar_amount))
                
                # Display results
                st.markdown("---")
                st.markdown("## 🎯 Best Conversion Option")
                
                # Best option metrics
                best = result.optimal_path
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Exchange", best.exchange.value)
                with col2:
                    st.metric("USDC Received", f"{best.usdc_received:,.2f}")
                with col3:
                    st.metric("Rate", f"R{best.rate:,.4f}/USDC")
                
                # Details in an expander
                with st.expander("📊 View Detailed Breakdown", expanded=True):
                    st.markdown("### Transaction Details")
                    st.write(f"- **ZAR Amount:** R{zar_amount:,.2f}")
                    st.write(f"- **Exchange Fee:** R{best.fee:,.2f}")
                    st.write(f"- **Effective Rate:** R{best.rate:,.4f} per USDC")
                    
                    # Show alternative options if available
                    if result.alternative_paths:
                        st.markdown("### Alternative Options")
                        alt_data = []
                        for path in result.alternative_paths:
                            alt_data.append({
                                "Exchange": path.exchange.value,
                                "USDC Received": f"{path.usdc_received:,.2f}",
                                "Rate (R/USDC)": f"{path.rate:,.4f}",
                                "Fee (ZAR)": f"{path.fee:,.2f}"
                            })
                        
                        if alt_data:
                            st.table(alt_data)
                
                # Disclaimer
                st.markdown("---")
                st.info(
                    "💡 *Rates and fees are subject to change. "
                    "Actual conversion may vary based on market conditions and exchange policies.*"
                )
                
                # Store the best conversion result in session state for payment section
                st.session_state.last_conversion = {
                    'usdc_amount': best.usdc_received,
                    'zar_amount': zar_amount
                }
                
            except Exception as e:
                st.error(f"An error occurred while processing your request: {str(e)}")
                st.error("Please try again later or check your internet connection.")
                
                # Log the error for debugging
                st.exception("Error details:")

# ============================================================================
# PAYMENT SECTION - Send USDC on Arc Blockchain
# ============================================================================
st.markdown("---")
st.markdown("## 💳 Send USDC on Arc Blockchain")
st.markdown("Transfer your acquired USDC to another address on the Arc network.")

# Create two columns for payment inputs
payment_col1, payment_col2 = st.columns(2)

with payment_col1:
    recipient_address = st.text_input(
        "Recipient's Arc Address",
        placeholder="0x...",
        help="Enter the recipient's Ethereum-compatible address on Arc network"
    )

with payment_col2:
    # Get the last conversion amount if available, otherwise default to 0
    default_usdc = 0.0
    if hasattr(st.session_state, 'last_conversion'):
        default_usdc = st.session_state.last_conversion.get('usdc_amount', 0.0)
    
    usdc_amount = st.number_input(
        "USDC Amount to Send",
        min_value=0.01,
        value=default_usdc if default_usdc > 0 else 1.0,
        step=0.01,
        format="%.2f",
        help="Amount of USDC to transfer to the recipient"
    )

# Payment button
if st.button("🚀 Send Payment on Arc", key="send_payment_button"):
    # Validate inputs
    if not recipient_address:
        st.error("❌ Please enter a recipient address")
    elif not recipient_address.startswith("0x") or len(recipient_address) != 42:
        st.error("❌ Invalid Arc address format. Must be 42 characters starting with '0x'")
    elif usdc_amount <= 0:
        st.error("❌ Please enter a positive USDC amount")
    else:
        with st.spinner("Processing payment on Arc network..."):
            try:
                # WARNING: For hackathon demo purposes only. Do not use in production.
                # This is a hardcoded demo private key - NEVER use in production!
                sender_private_key = os.getenv(
                    "ARC_DEMO_PRIVATE_KEY",
                    "0x1234567890123456789012345678901234567890123456789012345678901234"
                )
                
                # Send USDC on Arc
                success, tx_hash_or_error = send_usdc_on_arc(
                    sender_private_key=sender_private_key,
                    recipient_address=recipient_address,
                    amount=usdc_amount
                )
                
                if success:
                    # Display success message with block explorer link
                    st.success(f"✅ Payment sent successfully!")
                    st.markdown(
                        f"**Transaction Hash:** `{tx_hash_or_error}`\n\n"
                        f"[View on Arc Block Explorer](https://testnet.arcscan.io/tx/{tx_hash_or_error})"
                    )
                    st.balloons()
                else:
                    # Display error message
                    st.error(f"❌ Payment failed: {tx_hash_or_error}")
                    
            except Exception as e:
                st.error(f"❌ An error occurred while processing the payment: {str(e)}")
                st.exception("Error details:")

# Payment section disclaimer
st.markdown("---")
st.warning(
    "⚠️ **Demo Notice:** This payment feature uses a hardcoded demo private key for hackathon purposes. "
    "**Never use this in production.** Always use secure key management for real transactions."
)

# Add some spacing at the bottom
st.markdown("---")
st.markdown(
    "*Built with ❤️ for efficient crypto conversions. "
    "[Report issues](https://github.com/yourusername/arc-zardian/issues)*"
)
