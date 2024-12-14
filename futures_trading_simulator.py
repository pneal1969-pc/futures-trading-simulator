import streamlit as st
import pandas as pd
import random

# Streamlit app setup
st.title("Futures Trading Session Simulator")

# User inputs
starting_capital = st.number_input("Starting Capital ($)", min_value=100.0, value=5000.0, step=100.0)
win_percentage = st.slider("Win Percentage (%)", min_value=0, max_value=100, value=50)
amount_risked = st.number_input("Amount Risked per Trade ($)", min_value=1.0, value=100.0, step=10.0)
risk_reward_ratio = st.number_input("Risk/Reward Ratio", min_value=0.1, value=2.0, step=0.1)
number_of_trades = st.number_input("Number of Trades", min_value=1, value=30, step=1)

if st.button("Run Simulation"):
    # Initialize variables
    capital = starting_capital
    trades = []
    stopped = False
    
    for trade_num in range(1, number_of_trades + 1):
        # Stop simulation if capital reaches $0 or less
        if capital <= 0:
            stopped = True
            st.warning("Trading session stopped: Capital balance reached $0.")
            break

        # Determine if the trade is a win or a loss
        win = random.random() < (win_percentage / 100)
        trade_result = amount_risked * risk_reward_ratio if win else -amount_risked
        capital += trade_result
        
        # Record trade details
        trades.append({
            "Trade Number": trade_num,
            "Result": "Win" if win else "Loss",
            "Change ($)": trade_result,
            "Running Capital ($)": max(capital, 0)  # Ensure capital doesn't show negative
        })

    # Convert to DataFrame for display
    results_df = pd.DataFrame(trades)

    # Display results
    st.subheader("Simulation Results")
    st.dataframe(results_df)

    # Display summary
    st.subheader("Summary")
    final_capital = trades[-1]["Running Capital ($)"] if trades else starting_capital
    st.write(f"Final Capital: ${final_capital:.2f}")
    st.write(f"Net Change: ${final_capital - starting_capital:.2f}")
    st.write(f"Trades Executed: {len(trades)}")
    
    # Plot capital progression
    if not results_df.empty:
        st.subheader("Capital Progression")
        st.line_chart(results_df["Running Capital ($)"])
