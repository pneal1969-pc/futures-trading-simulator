import streamlit as st
import pandas as pd
import random

# Streamlit app setup
st.title("Futures Trading Session Simulator with Capital Growth, Looping, and Commissions")

# User inputs
starting_capital = st.number_input("Starting Capital ($)", min_value=100.0, value=5000.0, step=100.0)
win_percentage = st.slider("Win Percentage (%)", min_value=0, max_value=100, value=50)
amount_risked = st.number_input("Amount Risked per Trade ($)", min_value=1.0, value=100.0, step=10.0)
risk_reward_ratio = st.number_input("Risk/Reward Ratio", min_value=0.1, value=2.0, step=0.1)
max_drawdown = st.number_input("Max Drawdown ($)", min_value=1.0, value=2500.0, step=100.0)
capital_growth_goal = st.number_input("Capital Growth Goal ($)", min_value=100.0, value=8000.0, step=100.0)
trade_commission = st.number_input("Trade Commission ($)", min_value=0.0, value=5.0, step=0.5)
loop_simulations = st.number_input("Number of Simulations (for Loop Mode)", min_value=1, value=1, step=1)

# Run simulation button
if st.button("Run Simulation"):
    def run_single_simulation(return_detailed_data=False):
        """Runs a single simulation and returns the number of trades to hit target or max drawdown."""
        capital = starting_capital
        max_capital = starting_capital
        min_capital_balance = starting_capital - max_drawdown
        trades = 0
        trade_data = []  # For detailed output if needed
        
        while capital < capital_growth_goal and capital >= min_capital_balance:
            trades += 1
            # Determine win or loss
            win = random.random() < (win_percentage / 100)
            trade_result = amount_risked * risk_reward_ratio if win else -amount_risked
            trade_result -= trade_commission  # Subtract commission
            capital += trade_result

            # Update max capital and recalculate min allowed balance
            if capital > max_capital:
                max_capital = capital
                min_capital_balance = max_capital - max_drawdown

            # Record trade details
            if return_detailed_data:
                trade_data.append({
                    "Trade Number": trades,
                    "Result": "Win" if win else "Loss",
                    "Change ($)": trade_result,
                    "Running Capital ($)": capital,
                    "Max Capital ($)": max_capital,
                    "Min Capital Balance ($)": min_capital_balance
                })

        # Determine outcome
        outcome = "Target Achieved" if capital >= capital_growth_goal else "Max Drawdown Hit"
        return (trades, outcome, trade_data) if return_detailed_data else (trades, outcome)

    # If only one simulation is selected
    if loop_simulations == 1:
        trades, outcome, trade_data = run_single_simulation(return_detailed_data=True)
        st.subheader("Simulation Result")
        st.write(f"Outcome: {outcome}")
        st.write(f"Number of Trades: {trades}")

        # Display individual trades as a chart
        results_df = pd.DataFrame(trade_data)
        st.subheader("Trade Data")
        st.dataframe(results_df)
        st.subheader("Capital Progression")
        st.line_chart(results_df["Running Capital ($)"])
    else:
        # Run multiple simulations
        total_trades_to_target = 0
        total_trades_to_drawdown = 0
        target_hits = 0
        drawdown_hits = 0

        for _ in range(loop_simulations):
            trades, outcome = run_single_simulation()
            if outcome == "Target Achieved":
                total_trades_to_target += trades
                target_hits += 1
            else:
                total_trades_to_drawdown += trades
                drawdown_hits += 1

        # Calculate averages and win/loss percentage
        avg_trades_to_target = total_trades_to_target / target_hits if target_hits > 0 else 0
        avg_trades_to_drawdown = total_trades_to_drawdown / drawdown_hits if drawdown_hits > 0 else 0
        win_rate = (target_hits / loop_simulations) * 100 if loop_simulations > 0 else 0
        loss_rate = (drawdown_hits / loop_simulations) * 100 if loop_simulations > 0 else 0

        # Display summary
        st.subheader("Loop Simulation Summary")
        st.write(f"Total Simulations: {loop_simulations}")
        st.write(f"Target Achieved (Wins): {target_hits}")
        st.write(f"Max Drawdown Hit (Losses): {drawdown_hits}")
        st.write(f"Win Rate: {win_rate:.2f}%")
        st.write(f"Loss Rate: {loss_rate:.2f}%")
        st.write(f"Average Trades to Target: {avg_trades_to_target:.2f} trades")
        st.write(f"Average Trades to Max Drawdown: {avg_trades_to_drawdown:.2f} trades")
