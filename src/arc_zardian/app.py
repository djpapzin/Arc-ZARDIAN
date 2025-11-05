import streamlit as st
from typing import Dict
import asyncio

from arc_zardian.core.optimizer import ConversionOptimizer, Exchange
from arc_zardian.core.models import ConversionPath, ConversionResult

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
                
            except Exception as e:
                st.error(f"An error occurred while processing your request: {str(e)}")
                st.error("Please try again later or check your internet connection.")
                
                # Log the error for debugging
                st.exception("Error details:")

# Add some spacing at the bottom
st.markdown("---")
st.markdown(
    "*Built with ❤️ for efficient crypto conversions. "
    "[Report issues](https://github.com/yourusername/arc-zardian/issues)*"
)
