import streamlit as st
import json
import os
from cryptography.fernet import Fernet

# --- CONFIG & DATABASE ---
DB_FILE = "vault.json"

def load_data():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- APP LOGIC ---
st.set_page_config(page_title="Secure Cloud Vault", page_icon="🔐")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    
# --- LOGIN UI ---
if not st.session_state.logged_in:
    with st.container():
        st.header("🔑 Login to Your Vault")
        user = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns(2)
        if col1.button("Login"):
            data = load_data()
            # Simple check (In a real app, use password hashing like 'bcrypt')
            if user in data and data[user]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = user
                st.rerun()
            else:
                st.error("Invalid username or password")
        
        if col2.button("Register New Account"):
            data = load_data()
            if user in data:
                st.warning("User already exists!")
            elif user and password:
                data[user] = {"password": password, "files": {}}
                save_data(data)
                st.success("Registered! You can now login.")

# --- MAIN VAULT UI ---
else:
    st.sidebar.title(f"Welcome, {st.session_state.username}!")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["🔒 Encrypt", "🔓 Decrypt", "📜 My Files"])

    # Load data for the current user
    all_data = load_data()
    user_files = all_data[st.session_state.username]["files"]

    with tab1:
        st.subheader("Encrypt New File")
        up_file = st.file_uploader("Upload file")
        if up_file and st.button("Encrypt & Store Key"):
            # Generate unique key for this file
            file_key = Fernet.generate_key()
            f = Fernet(file_key)
            encrypted_content = f.encrypt(up_file.read())
            
            # Save key info to JSON
            user_files[up_file.name] = file_key.decode()
            save_data(all_data)
            
            st.download_button(f"Download {up_file.name}.encrypted", encrypted_content, f"{up_file.name}.encrypted")
            st.success(f"Key for {up_file.name} saved to your vault!")

    with tab2:
        st.subheader("Decrypt File")
        dec_file = st.file_uploader("Upload .encrypted file")
        if dec_file:
            # Look for the original name in our JSON "brain"
            original_name = dec_file.name.replace(".encrypted", "")
            
            if original_name in user_files:
                if st.button("Decrypt with Stored Key"):
                    stored_key = user_files[original_name].encode()
                    f = Fernet(stored_key)
                    try:
                        decrypted_data = f.decrypt(dec_file.read())
                        st.download_button("Download Original", decrypted_data, original_name)
                    except:
                        st.error("Decryption failed. Data may be corrupted.")
            else:
                st.error("No key found for this file in your vault.")

    with tab3:
        st.subheader("Your Secured Files")
        if user_files:
            for filename in user_files.keys():
                st.write(f"📄 {filename}")
        else:
            st.info("No files registered yet.")