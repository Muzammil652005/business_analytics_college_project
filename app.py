import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.linear_model import LinearRegression

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Business Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ================= USER STORAGE =================
USER_FILE = "users.csv"

# Create users.csv safely (prevents EmptyDataError)
if not os.path.exists(USER_FILE) or os.stat(USER_FILE).st_size == 0:
    pd.DataFrame(columns=["username", "password"]).to_csv(USER_FILE, index=False)

# ================= SESSION STATE =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

# ================= AUTH FUNCTIONS =================
def register_user(username, password):
    username = username.strip()
    password = password.strip()

    if username == "" or password == "":
        return "empty"

    users = pd.read_csv(USER_FILE)

    if username in users["username"].astype(str).values:
        return "exists"

    users.loc[len(users)] = [username, password]
    users.to_csv(USER_FILE, index=False)
    return "success"


def login_user(username, password):
    username = username.strip()
    password = password.strip()

    users = pd.read_csv(USER_FILE)

    match = users[
        (users["username"].astype(str) == username) &
        (users["password"].astype(str) == password)
    ]

    return not match.empty

# ================= SIDEBAR NAVIGATION =================
st.sidebar.title("📂 Navigation")

if not st.session_state.logged_in:
    page = st.sidebar.radio("Go to", ["Login", "Register"])
else:
    page = st.sidebar.radio("Go to", ["Dashboard", "Logout"])

# ================= REGISTER PAGE =================
if page == "Register":
    st.title("📝 Create Account")

    reg_user = st.text_input("Username")
    reg_pass = st.text_input("Password", type="password")

    if st.button("Register"):
        result = register_user(reg_user, reg_pass)

        if result == "success":
            st.success("✅ Registration successful. Please login.")
        elif result == "exists":
            st.error("❌ Username already exists")
        elif result == "empty":
            st.warning("⚠ Username and password are required")

# ================= LOGIN PAGE =================
elif page == "Login":
    st.title("🔐 Login")

    login_user_name = st.text_input("Username")
    login_password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(login_user_name, login_password):
            st.session_state.logged_in = True
            st.session_state.username = login_user_name
            st.success("Login successful")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# ================= DASHBOARD =================
elif page == "Dashboard":
    st.title("📊 Data-Driven Business Insights")
    st.subheader(f"Welcome, {st.session_state.username}")

    # Load dataset
    df = pd.read_csv("data/business_data.csv")

    # KPI Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Average Sales", f"{df['Sales'].mean():.2f}")
    c2.metric("Maximum Sales", df["Sales"].max())
    c3.metric("Total Customers", df["Customers"].sum())

    # Dataset preview
    st.header("📄 Dataset Preview")
    st.dataframe(df, use_container_width=True)

    # Correlation heatmap
    st.header("🔥 Correlation Heatmap")
    fig, ax = plt.subplots()
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    # Prediction section
    st.header("🤖 Sales Prediction")

    ad = st.slider("Advertising Spend", 5, 50, 20)
    cust = st.slider("Customers", 50, 210, 100)
    disc = st.slider("Discount (%)", 2, 20, 8)

    X = df[["Advertising", "Customers", "Discount"]]
    y = df["Sales"]

    model = LinearRegression()
    model.fit(X, y)

    prediction = model.predict([[ad, cust, disc]])[0]
    st.success(f"💰 Predicted Sales Value: ₹ {prediction:.2f}")

# ================= LOGOUT =================
elif page == "Logout":
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()

# ================= FOOTER =================
st.markdown("""
---
<center>
<b>Academic Business Analytics Project</b><br>
Python • Streamlit • Machine Learning
</center>
""", unsafe_allow_html=True)
