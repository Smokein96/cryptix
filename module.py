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