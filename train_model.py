import pandas as pd
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error

# Load the data we just made
df = pd.read_csv("historical_demand.csv")

# FEATURE ENGINEERING (This makes you look like a pro)
# We tell the model: "Look at what demand was 1 day ago and 7 days ago"
df['lag_1'] = df.groupby('location')['actual_demand'].shift(1)
df['lag_7'] = df.groupby('location')['actual_demand'].shift(7)
df = df.dropna() # Remove rows where we don't have lag data

#Split data (Train on most, test on the last 30 days)
train = df.iloc[:-300] 
test = df.iloc[-300:]

X_train = train[['lag_1', 'lag_7']]
y_train = train['actual_demand']
X_test = test[['lag_1', 'lag_7']]
y_test = test['actual_demand']

# Training the LightGBM Model
model = lgb.LGBMRegressor(verbosity=-1)
model.fit(X_train, y_train)

# Predicting  and Saving 
test['predicted_demand'] = model.predict(X_test).astype(int)
test.to_csv("predictions.csv", index=False)

print(f"Training Complete! Error Margin: {mean_absolute_error(y_test, test['predicted_demand']):.2f} units")
print("Predictions saved to predictions.csv")