import yfinance as yf
import numpy as np
import pandas as pd


df = yf.download('AAPL', start='2019-01-01', end='2024-01-01')
df.columns = df.columns.droplevel(1)

# print(df.head())
# print(df.shape)

df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
df['Daily_Return'] = df['Close'].pct_change()
df['MA7'] = df['Close'].rolling(window=7).mean()
df['MA21'] = df['Close'].rolling(window=21).mean()
df['Volume_Change'] = df['Volume'].pct_change()
# RSI
delta = df['Close'].diff()
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = -delta.where(delta < 0, 0).rolling(14).mean()
df['RSI'] = 100 - (100 / (1 + gain / loss))

# MACD
exp12 = df['Close'].ewm(span=12).mean()
exp26 = df['Close'].ewm(span=26).mean()
df['MACD'] = exp12 - exp26

# Bollinger Bands
df['BB_middle'] = df['Close'].rolling(20).mean()
df['BB_upper'] = df['BB_middle'] + 2 * df['Close'].rolling(20).std()
df['BB_lower'] = df['BB_middle'] - 2 * df['Close'].rolling(20).std()
df['BB_width'] = df['BB_upper'] - df['BB_lower']

df = df.dropna()

#print(df['Target'].value_counts())

# featueres that would help understand the stock price movement
features = ['Open', 'High', 'Low', 'Volume', 'Daily_Return',
            'MA7', 'MA21', 'Volume_Change', 'RSI', 'MACD', 'BB_width']

X = df[features]
y = df['Target']

#print(X.shape)
#print(y.shape)


split_index = int(0.8 * len(df))
X_train, X_test = X[:split_index], X[split_index:]
y_train, y_test = y[:split_index], y[split_index:]

print(f"Train size: {len(X_train)}")
print(f"Test size: {len(X_test)}")

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

scalar = StandardScaler()
X_train_scaled = scalar.fit_transform(X_train)
X_test_scaled = scalar.transform(X_test)

#start training the model
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.ensemble import GradientBoostingClassifier

model = LogisticRegression()
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")


xgb_model = GradientBoostingClassifier()
xgb_model.fit(X_train_scaled, y_train)
y_pred_xgb = xgb_model.predict(X_test_scaled)
accuracy_xgb = accuracy_score(y_test, y_pred_xgb)
print(f"XGBoost Accuracy: {accuracy_xgb:.2f}")

from sklearn.metrics import classification_report

print("\nLogistic Regression:")
print(classification_report(y_test, y_pred))

print("XGBoost:")
print(classification_report(y_test, y_pred_xgb))
