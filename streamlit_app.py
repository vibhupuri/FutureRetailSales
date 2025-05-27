import streamlit as st
import numpy as np
import joblib
from xgboost import XGBRegressor

# Load trained model
model = joblib.load("xgb_model.pkl")

st.title("🛍️ Sales Forecasting App")
st.subheader("Predict next month’s item count from past sales")

st.write("Input lag features and additional data:")

lag_1 = st.number_input("Item Count Lag 1 (1 month ago)", min_value=0.0, max_value=100.0, value=5.0)
lag_2 = st.number_input("Item Count Lag 2 (2 months ago)", min_value=0.0, max_value=100.0, value=3.0)
lag_3 = st.number_input("Item Count Lag 3 (3 months ago)", min_value=0.0, max_value=100.0, value=2.0)
item_avg = st.number_input("Item Average Sales", min_value=0.0, max_value=100.0, value=4.0)
shop_avg = st.number_input("Shop Average Sales", min_value=0.0, max_value=100.0, value=6.0)
month = st.selectbox("Month", options=list(range(12)), index=0)

if st.button("Predict"):
    input_data = np.array([[lag_1, lag_2, lag_3, item_avg, shop_avg, month]])
    prediction = model.predict(input_data)
    st.success(f"📦 Forecasted Item Count: {prediction[0]:.2f}")
