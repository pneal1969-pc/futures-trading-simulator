import streamlit as st
import pandas as pd
import random

# Streamlit app setup
st.title("Futures Trading Session Simulator with Max Drawdown")

# User inputs
starting_capital = st.number_input("Starting Capital ($)", min_value=100.0, value=5000.0, step=100.0)
win_percentage = st.slider("Win Percentage (%)", min_value=0, max_value=100, value=50)
amount_risked = st.number_input("Amount Risked per Trade ($)", min_value=1.0, value=100.0, step=10.0)
risk_reward_ratio = st.number_input("Risk/Reward Ratio", min_value=0.1, value=2.0, step=0.1)
number_of_trades = st.number_input("Number of Trades", min_value=1, value=30, step=1)
max_drawdown = st.number_input("Max Drawdown ($)", min_value=1.0, value=2500.0, step=100.0)

if st.button("Run Simulation"):
    # Initialize variables
    capital = starting_capital
    trades = []
    stopped = False

    # Tracking max capital and minimum allowed balance
    max_capital = starting_capital
    min_capital_balance = starting_capital - max_drawdown

    for trade_num in range(1, number_of_trades + 1):
        # Stop simulation if capital falls below the minimum allowed balance
        if capital < min_capital_balance:
            stopped = True
            st.warning("Trading session stopped: Capital balance fell below the minimum allowed balance.")
            break

        # Determine if the trade is a win or a loss
        win = random.random() < (win_percentage / 100)
        trade_result = amount_risked * risk_reward_ratio if win else -amount_risked
        capital += trade_result

        # Update max capital and recalculate min allowed balance
        if capital > max_capital:
            max_capital = capital
            min_capital_balance = max_capital - max_drawdown

        # Record trade details
        trades.append({
            "Trade Number": trade_num,
            "Result": "Win" if win else "Loss",
            "Change ($)": trade_result,
            "Running Capital ($)": capital,
            "Max Capital ($)": max_capital,
            "Min Capital Balance ($)": min_capital_balance
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
    st.write(f"Max Capital Reached: ${max_capital:.2f}")
    st.write(f"Final Min Allowed Balance: ${min_capital_balance:.2f}")
    
    # Plot capital progression
    if not results_df.empty:
        st.subheader("Capital Progression")
        st.line_chart(results_df["Running Capital ($)"])
