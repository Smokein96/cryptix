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

# NEW PAGE
else:
    st.title("CRYPTIX")
    st.sidebar.title(f"WELCOME, {st.session_state.user.username}")
    if st.sidebar.button("Logout"):
        st.session_state.user.log_status = False
        st.session_state.user = None
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["🔒 Encrypt", "🔓 Decrypt", "📜 My Files"])

    # ENCRYPT
    with tab1:
        st.subheader("Encrypt New File")
        up_file = st.file_uploader("Upload file", key="enc_uploader")

        col1,col2 = st.columns(2)

        if col1.button("Encrypt & Store Key") and up_file:
            try :
                (encrypted_content,file_key) = st.session_state.user.encrypt(up_file)

                sql_mod.save_file(st.session_state.user.username, up_file.name, file_key.decode())
                st.success(f"Key for {up_file.name} saved to your vault!")
                col2.download_button(f"Download {up_file.name}.encrypted", encrypted_content, f"{up_file.name}.encrypted")
                st.code(file_key.decode(), language="plaintext")

            except (Exception) as error:
                st.error(str(error))
    
    #DECRYPT
    with tab2:
        st.subheader("Decrypt File")
        dec_file = st.file_uploader("Upload .encrypted file", key="dec_uploader")

        if dec_file:
            original_name = dec_file.name.replace(".encrypted", "")
            col1, col2 = st.columns(2)

            tab1, tab2 = col1.tabs(["Stored Key", "Manual Key"])

            # STORED KEY
            with tab1:

                st.write("Use key from your vault:")
                if st.button("Decrypt with Stored Key"):
                    try:

                        dec_file.seek(0)  # Reset file pointer
                        key = sql_mod.get_key(st.session_state.user.username, original_name)
                        decrypted_data = st.session_state.user.decrypt(dec_file, key)
                        st.success("File decrypted successfully!")
                        st.download_button(f"Download {original_name}", decrypted_data, f"{original_name}", key="stored_key_dl") # need key id to seperate the 2 download buttons
                    except (ValueError, RuntimeError, Exception) as error:
                        st.error(str(error))

            # MANUAL KEY
            with tab2:
                st.write("Use a manual key:")
                manual_key = st.text_input("Enter Key")
                if st.button("Decrypt with Manual Key"):
                    if manual_key:
                        try:

                            dec_file.seek(0)
                            decrypted_data = st.session_state.user.decrypt(dec_file, manual_key)
                            st.success("File decrypted successfully!")
                            st.download_button(f"Download {original_name}", decrypted_data, f"{original_name}", key="manual_key_dl")
                        
                        except (ValueError, RuntimeError, Exception) as error:
                            st.error(str(error))
                    else:
                        st.warning("Please enter a manual key.")
            
    with tab3:
        st.subheader("Your Secured Files")
        file = sql_mod.get_files(st.session_state.user.username)
        if file:
            for filename in file:
                st.write(f"{filename[2]}")
        else:
            st.info("No files registered yet.")
                
            
            

    
