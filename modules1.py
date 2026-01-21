import streamlit as st
from cryptography.fernet import Fernet
import os

# --- TITLE ---
st.title("🔐 My Simple File Vault")
st.write("A secure way to encrypt your local files.")

# --- STEP 1: KEY GENERATION ---
# In a real app, you'd save this key. For this simple version, we generate one.
if 'key' not in st.session_state:
    st.session_state.key = Fernet.generate_key()
fernet = Fernet(st.session_state.key)

# --- STEP 2: FILE UPLOAD ---
uploaded_file = st.file_uploader("Choose a file to encrypt")

if uploaded_file is not None:
    # Read the file data
    file_data = uploaded_file.read()
    
    # --- STEP 3: ENCRYPT BUTTON ---
    if st.button("Encrypt"):
        encrypted_data = fernet.encrypt(file_data)
        
        # Give the user the encrypted file back
        st.download_button(
            label="Download Encrypted File",
            data=encrypted_data,
            file_name=uploaded_file.name + ".encrypted"
        )
        st.success("File encrypted successfully! Even if someone opens this, it will look like gibberish.")

# --- STEP 4: DECRYPT SECTION ---
st.divider()
st.subheader("🔓 Decrypt a File")
dec_file = st.file_uploader("Upload an .encrypted file")

if dec_file is not None:
    enc_data = dec_file.read()
    if st.button("Decrypt"):
        try:
            original_data = fernet.decrypt(enc_data)
            st.download_button(label="Download Original File", data=original_data, file_name="restored_file.jpg")
            st.success("File restored!")
        except:
            st.error("Decryption failed. Wrong key or corrupted file.")