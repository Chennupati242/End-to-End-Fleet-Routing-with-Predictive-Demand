import pandas as pd
import numpy as np

# Create 10 delivery locations (Nodes)
locations = [f"Node_{i}" for i in range(1, 11)]
dates = pd.date_range(start="2024-01-01", periods=365)

data = []
for loc in locations:
    # Each location has a unique base demand level
    base_demand = np.random.randint(15, 60)
    for date in dates:
        # Add a "Weekend Rush" (demand goes up on Friday/Saturday)
        rush = 15 if date.dayofweek >= 4 else 0
        # Add some random "noise"
        noise = np.random.normal(0, 3)
        demand = max(0, int(base_demand + rush + noise))
        data.append([date, loc, demand])

df = pd.DataFrame(data, columns=['date', 'location', 'actual_demand'])
df.to_csv("historical_demand.csv", index=False)
print("Created historical_demand.csv!")