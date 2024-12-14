import streamlit as st
import pandas as pd
import random
import numpy as np

# Streamlit app setup
st.title("Futures Trading Session Simulator with Risk Optimization")

# User inputs
starting_capital = st.number_input("Starting Capital ($)", min_value=100.0, value=5000.0, step=100.0)
win_percentage = st.slider("Win Percentage (%)", min_value=0, max_value=100, value=50)
risk_reward_ratio = st.number_input("Risk/Reward Ratio", min_value=0.1, value=2.0, step=0.1)
max_drawdown = st.number_input("Max Drawdown ($)", min_value=1.0, value=2500.0, step=100.0)
capital_growth_goal = st.number_input("Capital Growth Goal ($)", min_value=100.0, value=8000.0, step=100.0)
trade_commission = st.number_input("Trade Commission ($)", min_value=0.0, value=5.0, step=0.5)
loop_simulations = st.number_input("Number of Simulations (for Loop Mode or Optimization)", min_value=1, value=500, step=1)

# Toggle between standard simulation and optimization
optimize_risk = st.checkbox("Optimize Risk Amount")

if st.button("Run Simulation"):
    def run_single_simulation(amount_risked):
        """Runs a single simulation with a specified risk amount."""
        capital = starting_capital
        max_capital = starting_capital
        min_capital_balance = starting_capital - max_drawdown
        trades = 0
        
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

        # Determine outcome
        outcome = "Target Achieved" if capital >= capital_growth_goal else "Max Drawdown Hit"
        return trades, outcome

    if optimize_risk:
        # Optimization mode
        st.subheader("Risk Optimization")
        
        # Range of risk amounts to test
        risk_values = np.linspace(1, starting_capital * 0.2, 50)  # Test risks from $1 to 20% of starting capital
        avg_trades_to_target = []
        avg_trades_to_drawdown = []

        for amount_risked in risk_values:
            total_trades_to_target = 0
            total_trades_to_drawdown = 0
            target_hits = 0
            drawdown_hits = 0

            for _ in range(loop_simulations):
                trades, outcome = run_single_simulation(amount_risked)
                if outcome == "Target Achieved":
                    total_trades_to_target += trades
                    target_hits += 1
                else:
                    total_trades_to_drawdown += trades
                    drawdown_hits += 1

            # Calculate average trades for this risk amount
            avg_to_target = total_trades_to_target / target_hits if target_hits > 0 else float('inf')
            avg_to_drawdown = total_trades_to_drawdown / drawdown_hits if drawdown_hits > 0 else float('inf')

            avg_trades_to_target.append(avg_to_target)
            avg_trades_to_drawdown.append(avg_to_drawdown)

        # Display results
        optimal_risk = risk_values[np.argmin(avg_trades_to_target)]
        st.write(f"Optimal Risk Amount: ${optimal_risk:.2f}")
        st.write(f"Average Trades to Target with Optimal Risk: {min(avg_trades_to_target):.2f} trades")

        # Plot results
        st.subheader("Risk vs. Average Trades")
        risk_df = pd.DataFrame({
            "Risk Amount ($)": risk_values,
            "Avg Trades to Target": avg_trades_to_target,
            "Avg Trades to Drawdown": avg_trades_to_drawdown
        })
        st.line_chart(risk_df.set_index("Risk Amount ($)"))
    else:
        # Standard simulation mode
        total_trades_to_target = 0
        total_trades_to_drawdown = 0
        target_hits = 0
        drawdown_hits = 0

        for _ in range(loop_simulations):
            trades, outcome = run_single_simulation(100)  # Default risk for standard simulation
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
