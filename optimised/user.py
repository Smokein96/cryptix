from cryptography.fernet import Fernet, InvalidToken
import sql_mod

class obj :

    def __init__(self,username,password,log_status):
        self.username = username
        self.password = password
        self.log_status = log_status
     
    def encrypt(self, up_file):
        try:
            file_key = Fernet.generate_key()
            f = Fernet(file_key)
            encrypted_content = f.encrypt(up_file.read())
            return(encrypted_content,file_key)
        except(Exception):
            raise Exception("Encryption Failed")
    
    def decrypt(self, dec_file, key):
        if key is None:
            raise ValueError("No key found for this file in your vault.")
    
        try:
            enc_key = key.encode()
            f = Fernet(enc_key)
            
            decrypted_data = f.decrypt(dec_file.read())
            return decrypted_data # Success! Returns bytes.
    
        except InvalidToken: #from fernet module
            raise RuntimeError("Decryption failed. Invalid key or corrupted data.")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")
                    
            
        
            

        