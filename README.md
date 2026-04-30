# End-to-End Fleet Routing with Predictive Demand

This project demonstrates a sophisticated decision-support system that combines **Machine Learning** and **Mathematical Optimization**. It predicts delivery demand for various city nodes and then calculates the most efficient vehicle routes to satisfy that demand.

## Key Features
- **Predictive Modeling:** Uses LightGBM to forecast package volume based on historical trends and "lag" features.
- **Route Optimization:** Formulates a Vehicle Routing Problem (VRP) using Google OR-Tools to minimize fleet mileage.
- **Constraint Programming:** Handles real-world constraints like vehicle capacity and mandatory node visits.

## The Architecture
1. **Data Generation:** Simulated 1 year of historical demand data for 10 delivery locations.
2. **Demand Forecasting:** A Gradient Boosting (LightGBM) model trained on historical lags to predict next-day volume.
3. **Operational Solver:** An optimization engine that assigns 3 trucks to 10 nodes based on AI-predicted volume.

## Tech Stack
- **Language:** Python 3.10
- **ML Library:** LightGBM, Scikit-learn
- **Optimization:** Google OR-Tools (CP-SAT Solver)
- **Environment:** Conda / Miniforge (optimized for Mac Apple Silicon)

##  Results
- **Prediction Accuracy:** The model achieved a Mean Absolute Error (MAE) of ~2.9 units.
- **Efficiency:** The solver successfully distributed load across a 3-vehicle fleet, ensuring 100% delivery fulfillment with optimized mileage.

## How to Run
1. **Clone the repo:**
   git clone [https://github.com/Chennupati242/fleet-routing-project.git]
   cd fleet-routing-project
2.**Setup Environment:**
  conda activate fleet_routing
  pip install -r requirements.txt
3. **Run Pipeline:**
   python app.py     # Generates data and trains AI
   python solver.py  # Runs the optimization

