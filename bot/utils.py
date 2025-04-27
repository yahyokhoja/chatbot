from cryptography.fernet import Fernet

# Храни ключ в .env или settings (для простоты — здесь)
FERNET_KEY = Fernet.generate_key()
fernet = Fernet(FERNET_KEY)

def encrypt_data(data):
    return fernet.encrypt(data.encode())

def decrypt_data(token):
    return fernet.decrypt(token).decode()
