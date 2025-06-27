import secrets

# Generate a 32-character secure token
secret_key = secrets.token_hex(16)

# Write it to a .env file
with open(".env", "w") as f:
    f.write(f"SECRET_KEY={secret_key}\n")

print(".env file created with secret key!")