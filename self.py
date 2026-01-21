import streamlit as st
import json
import os
from cryptography.fernet import Fernet

db_file = "test_vault.json"

def load_data():
    if not os.path.exists(db_file):
        return {}
    with open (db_file,"r") as f :
        return json.load(f)
    
def save_data(data):
    with open (db_file, "w") as f :
        json.dump(data,f,indent=4)
    
if "logged_in" not in st.session_state :
    st.session_state.logged_in = False
    st.session_state.username = None

if not st.session_state.logged_in : #if not logged in then exe
    st.title("CRYPTIC")
    st.subheader("Login in to your account")
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1,col2 = st.columns(2)
    if col1.button("LOGIN"):
        data = load_data()
        if user in data and data[user]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = user
            st.rerun()
        else:
            st.error("Invalid Username or Password")

    if col2.button("REGISTER"):
        data = load_data()
        if user in data :
            st.warning("User Already Exists")
        elif user and password:
            data[user] = {"password":password, "files":{}}
            save_data(data)
            st.success("New User CREATED")

else :
    st.title("CRYPTIC")
    st.sidebar.title(f"WELCOME, {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["🔒 Encrypt", "🔓 Decrypt", "📜 My Files"])

    all_data = load_data()
    user_files = all_data[st.session_state.username]["files"]

    with tab1:
        st.subheader("Encrypt New File")
        up_file = st.file_uploader("Upload file")
        if up_file and st.button("Encrypt & Store Key"): #if file uploaded and button pressed
            
            file_key = Fernet.generate_key() #key
            f = Fernet(file_key) #initializing object, anything that passes through f will be encrypted
            encrypted_content = f.encrypt(up_file.read()) #up_file.read() reads the raw data of the uploaded file

            user_files[up_file.name] = file_key.decode() #decode turns key from bytes to text
            save_data(all_data)
            
            st.download_button(f"Download {up_file.name}.encrypted", encrypted_content, f"{up_file.name}.encrypted")
            st.success(f"Key for {up_file.name} saved to your vault!")   
    
    with tab2:
        st.subheader("Decrypt File")
        dec_file = st.file_uploader("Upload .encrypted file")
        
        if dec_file:
            original_name = dec_file.name.replace(".encrypted", "")

            if original_name in user_files:
                if st.button("Decrypt with Stored Key"):
                    stored_key = user_files[original_name].encode()
                    f = Fernet(stored_key)

                    try:
                        decrypted_data = f.decrypt(dec_file.read())
                        st.download_button(
                            label="Download Original",
                            data=decrypted_data,
                            file_name=original_name
                        )
                    except Exception:
                        st.error("Decryption failed. Data may be corrupted.")
            else:
                st.error("No key found for this file in your vault.")


    with tab3:
        st.subheader("Your Secured Files")
        if user_files:
            for filename in user_files.keys():  
                st.write(f"{filename}")
        else:
            st.info("No files registered yet.")
        