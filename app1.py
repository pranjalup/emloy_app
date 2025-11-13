import streamlit as st
from pymongo import MongoClient

# -----------------------------
# 🎯 PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="User & Admin Login System",
    layout="centered",
)

# -----------------------------
# 🧩 CONNECT TO MONGODB
# -----------------------------
# Mongo credentials are securely stored in Streamlit Cloud → Settings → Secrets
mongo_uri = st.secrets["mongo"]["uri"]
db_name = st.secrets["mongo"]["db_name"]

client = MongoClient(mongo_uri)
db = client[db_name]

users_collection = db["users"]
admins_collection = db["admins"]

# -----------------------------
# ⚙️ FUNCTIONS
# -----------------------------
def create_admin(username, password):
    """Create admin if username not already exists"""
    if admins_collection.find_one({"username": username}):
        return False
    admins_collection.insert_one({"username": username, "password": password})
    return True

def create_user(username, password, user_id):
    """Create user if username not already exists"""
    if users_collection.find_one({"username": username}):
        return False
    users_collection.insert_one({"username": username, "password": password, "user_id": user_id})
    return True

def validate_admin(username, password):
    """Validate admin credentials"""
    return admins_collection.find_one({"username": username, "password": password})

def validate_user(username, password):
    """Validate user credentials"""
    return users_collection.find_one({"username": username, "password": password})

# -----------------------------
# 🏠 APP LAYOUT
# -----------------------------
st.title("🔐 Login Portal")

menu = st.sidebar.radio("Choose Login Type", ["Admin Login", "User Login"])

# -----------------------------
# 👨‍💼 ADMIN LOGIN PAGE
# -----------------------------
if menu == "Admin Login":
    st.subheader("👨‍💼 Admin Login")

    admin_user = st.text_input("Admin Username")
    admin_pass = st.text_input("Admin Password", type="password")

    if st.button("Login as Admin"):
        if validate_admin(admin_user, admin_pass):
            st.success("✅ Admin login successful")

            # Section: Create new users
            st.subheader("➕ Create New User")

            new_user_id = st.text_input("User ID")
            new_user_name = st.text_input("New Username")
            new_user_pass = st.text_input("New Password", type="password")

            if st.button("Create User"):
                if create_user(new_user_name, new_user_pass, new_user_id):
                    st.success("🎉 User created successfully!")
                else:
                    st.warning("⚠️ Username already exists.")
        else:
            st.error("❌ Invalid admin credentials")

# -----------------------------
# 👤 USER LOGIN PAGE
# -----------------------------
elif menu == "User Login":
    st.subheader("👤 User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login as User"):
        if validate_user(username, password):
            st.success(f"✅ Welcome, {username}!")
            st.write("Access granted to user dashboard.")
        else:
            st.error("❌ Invalid username or password")
