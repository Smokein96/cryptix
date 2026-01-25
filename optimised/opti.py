from user import obj
import streamlit as st
import sql_mod
from cryptography.fernet import Fernet

# Initialize db only once
sql_mod.check_db()

if "user" not in st.session_state: # get user var to stay after rerun
    st.session_state.user = None


if st.session_state.user is None or st.session_state.user.log_status is False: #if user = none or
    st.title("CRYPTIX")
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    st.session_state.user = obj(username, password, False) # create obj

    col1, col2 = st.columns(2)

    if col1.button("Login") and st.session_state.user.username and st.session_state.user.password:
        if sql_mod.check_login(st.session_state.user.username, st.session_state.user.password): # runs if values ex
            st.session_state.user.log_status = True
            st.rerun() # rerun to move to next page
        else:
            st.error("Invalid Username or Password")

    if col2.button("Register") and st.session_state.user.username and st.session_state.user.password:
        
        if not sql_mod.check_exist(st.session_state.user.username):
            sql_mod.register_user(st.session_state.user.username, st.session_state.user.password)
            st.success("New User CREATED")
        else:
            st.warning("User Already Exists")

else:
    st.title("CRYPTIX")
    st.sidebar.title(f"WELCOME, {st.session_state.user.username}")
    if st.sidebar.button("Logout"):
        st.session_state.user.log_status = False
        st.session_state.user = None
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["🔒 Encrypt", "🔓 Decrypt", "📜 My Files"])

    with tab1:
        st.subheader("Encrypt New File")
        up_file = st.file_uploader("Upload file", key="enc_uploader")

        col1,col2 = st.columns(2)

        if col1.button("Encrypt & Store Key") and up_file:

            file_key = Fernet.generate_key()
            f = Fernet(file_key)
            encrypted_content = f.encrypt(up_file.read())

            sql_mod.save_file(st.session_state.user.username, up_file.name, file_key.decode())
            st.success(f"Key for {up_file.name} saved to your vault!")
            col2.download_button(f"Download {up_file.name}.encrypted", encrypted_content, f"{up_file.name}.encrypted")

    
    with tab2:
        st.subheader("Decrypt File")
        dec_file = st.file_uploader("Upload .encrypted file")
        col1,col2 = st.columns(2)

        if col1.button("Decrypt with Stored Key") and dec_file:
            original_name = dec_file.name.replace(".encrypted", "")
            
            key = sql_mod.get_key(st.session_state.user.username, original_name)
            
            if key is not None:
                enc_key = key.encode()
                f = Fernet(enc_key)

                try:
                    decrypted_data = f.decrypt(dec_file.read())
                    st.success("Succesfully Decrypted")
                    col2.download_button(label="Download Original",data=decrypted_data,file_name=original_name
                    )
                except Exception:
                    st.error("Decryption failed. Data may be corrupted.")
            else:
                st.error("No key found for this file in your vault.")

    with tab3:
        st.subheader("Your Secured Files")
        file = sql_mod.get_files(st.session_state.user.username)
        if file:
            for filename in file:
                st.write(f"{filename[2]}")
        else:
            st.info("No files registered yet.")
                
            
            

    
