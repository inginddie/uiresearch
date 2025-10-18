"""
Genera una clave secreta segura para JWT.
Uso: python generate_secret.py
"""
import secrets

def generate_jwt_secret():
    """Genera una clave secreta segura para JWT."""
    secret = secrets.token_urlsafe(32)
    return secret

if __name__ == "__main__":
    secret = generate_jwt_secret()
    
    print("\n" + "="*60)
    print("🔐 JWT SECRET KEY GENERATOR")
    print("="*60)
    print("\nGenerated JWT Secret Key:")
    print(f"\n{secret}\n")
    print("="*60)
    print("\nCopy this value and add it to your Railway variables:")
    print(f"\nJWT_SECRET_KEY={secret}")
    print("\n" + "="*60)
    print("\n⚠️  IMPORTANT: Keep this secret safe!")
    print("   - Never commit it to Git")
    print("   - Never share it publicly")
    print("   - Use different keys for dev/prod")
    print("\n" + "="*60 + "\n")
