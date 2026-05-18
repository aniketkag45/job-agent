from app.auth.security import hash_password, verify_password, create_access_token

password = "mypassword123"
hashed_password = hash_password(password)
print(f"Hashed password: {hashed_password}")
print("\nPawword Match:")
print(verify_password("mypassword123", hashed_password))  # Should return True
token = create_access_token({"sub": "aniket"})
print(f"\nGenerated JWT Token: {token}")

