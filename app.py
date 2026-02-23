import streamlit as st
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt

st.set_page_config(page_title="InsiderSentinel AI - Dark Mode", layout="centered")

# Dark hacker style
st.markdown("""
<style>
body {background-color: #0e1117;}
h1, h2, h3, h4 {color: #00ff99;}
</style>
""", unsafe_allow_html=True)

model = joblib.load("insider_model.pkl")

st.title("🛡 InsiderSentinel AI")
st.subheader("Dark Hacker Edition - Insider Threat Detection")

st.markdown("---")

mode = st.radio("Select Mode:", ["Single User Analysis", "Upload CSV Analysis"])

if mode == "Single User Analysis":

    login_hour = st.slider("Login Hour", 0, 23, 10)
    files_accessed = st.slider("Files Accessed", 0, 100, 8)
    data_downloaded = st.slider("Data Downloaded (MB)", 0, 1000, 50)
    failed_logins = st.slider("Failed Login Attempts", 0, 20, 1)

    input_data = np.array([[login_hour, files_accessed, data_downloaded, failed_logins]])

    if st.button("Analyze Activity"):

        prediction = model.predict(input_data)
        anomaly_score = model.decision_function(input_data)
        risk_percentage = round((1 - anomaly_score[0]) * 100, 2)

        st.markdown("### 🔍 Threat Analysis")

        if risk_percentage < 30:
            st.success(f"🟢 Low Risk - {risk_percentage}%")
        elif risk_percentage < 70:
            st.warning(f"🟡 Medium Risk - {risk_percentage}%")
        else:
            st.error(f"🔴 High Risk - {risk_percentage}%")

        reasons = []
        if login_hour < 6 or login_hour > 20:
            reasons.append("Unusual login time")
        if data_downloaded > 200:
            reasons.append("High data download volume")
        if failed_logins > 3:
            reasons.append("Multiple failed login attempts")

        if reasons:
            st.write("⚠ Possible Causes:")
            for r in reasons:
                st.write("-", r)

        features = ["Login Hour", "Files Accessed", "Data Downloaded", "Failed Logins"]
        values = [login_hour, files_accessed, data_downloaded, failed_logins]

        fig = plt.figure()
        plt.bar(features, values)
        plt.xticks(rotation=45)
        plt.title("User Activity Overview")
        st.pyplot(fig)

else:

    uploaded_file = st.file_uploader("Upload Employee Activity CSV")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        predictions = model.predict(df)

        df["Anomaly"] = predictions
        total = len(df)
        anomalies = len(df[df["Anomaly"] == -1])

        st.markdown("### 📊 Organization Threat Summary")
        st.write(f"Total Records: {total}")
        st.write(f"Anomalies Detected: {anomalies}")

        fig2 = plt.figure()
        plt.bar(["Normal", "Anomaly"], [total - anomalies, anomalies])
        plt.title("Anomaly Distribution")
        st.pyplot(fig2)
