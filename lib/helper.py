from cryptography.hazmat.primitives.asymmetric import (
    ed25519,
    x25519
)
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import os
from cryptography.hazmat.primitives import serialization
import hashlib
import json
import os
import dns.resolver
from dotenv import load_dotenv

load_dotenv()



# =========================
# JSON HELPERS
# =========================
def write_json(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("[OK] Saved:", file_path)

    except Exception as e:
        print("[WRITE ERROR]", e)


def read_json(file_path):
    if not os.path.exists(file_path):
        return None

    try:
        if os.path.getsize(file_path) == 0:
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception as e:
        print("[READ ERROR]", e)
        return None



def generate_signature_keys():
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    priv_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )

    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    return {
        "private_key": priv_bytes.hex(),
        "public_key": pub_bytes.hex()
    }


# =========================
# ENCRYPTION KEYPAIR
# X25519
# =========================
def generate_encryption_keys():
    private_key = x25519.X25519PrivateKey.generate()
    public_key = private_key.public_key()

    priv_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )

    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    return {
        "private_key": priv_bytes.hex(),
        "public_key": pub_bytes.hex()
    }

# =========================
# GENERATE FULL ACCOUNT
# =========================
def generate_account():
    sign_keys = generate_signature_keys()
    enc_keys = generate_encryption_keys()

    return {
        "signature": sign_keys,
        "encryption": enc_keys
    }

# =========================
# SESSION CHECKER
# =========================
def checking_keys_available():
    sign_priv = os.getenv("SIGNATURE_PRIVATE_KEY")
    sign_pub  = os.getenv("SIGNATURE_PUBLIC_KEY")

    enc_priv  = os.getenv("ENCRYPT_PRIVATE_KEY")
    enc_pub   = os.getenv("ENCRYPT_PUBLIC_KEY")

    # Nếu đã có key trong .env
    if all([sign_priv, sign_pub, enc_priv, enc_pub]):
        print("[OK] Existing account loaded from .env")

        data = {
            "signature": {
                "private_key": sign_priv,
                "public_key": sign_pub
            },
            "encryption": {
                "private_key": enc_priv,
                "public_key": enc_pub
            }
        }

        print(json.dumps(data, indent=4))
        return data

    # Nếu chưa có key
    print("No account found in .env")
    ans = input("Create new account? (Y/N): ")

    if ans.lower() == "y":
        data = generate_account()

        print("\n=== SIGNATURE KEYS ===")
        print("Private:", data["signature"]["private_key"])
        print("Public :", data["signature"]["public_key"])

        print("\n=== ENCRYPTION KEYS ===")
        print("Private:", data["encryption"]["private_key"])
        print("Public :", data["encryption"]["public_key"])

        # Lưu ra .env
        with open(".env", "w", encoding="utf-8") as f:
            f.write(f'SIGNATURE_PRIVATE_KEY={data["signature"]["private_key"]}\n')
            f.write(f'SIGNATURE_PUBLIC_KEY={data["signature"]["public_key"]}\n')
            f.write(f'ENCRYPT_PRIVATE_KEY={data["encryption"]["private_key"]}\n')
            f.write(f'ENCRYPT_PUBLIC_KEY={data["encryption"]["public_key"]}\n')

        print("\n[OK] Keys saved to .env")
        return data

    else:
        print("Manual import mode")

        sign_priv = input("Signature private key: ")
        sign_pub  = input("Signature public key : ")

        enc_priv  = input("Encrypt private key : ")
        enc_pub   = input("Encrypt public key  : ")

        with open(".env", "w", encoding="utf-8") as f:
            f.write(f"SIGNATURE_PRIVATE_KEY={sign_priv}\n")
            f.write(f"SIGNATURE_PUBLIC_KEY={sign_pub}\n")
            f.write(f"ENCRYPT_PRIVATE_KEY={enc_priv}\n")
            f.write(f"ENCRYPT_PUBLIC_KEY={enc_pub}\n")

        data = {
            "signature": {
                "private_key": sign_priv,
                "public_key": sign_pub
            },
            "encryption": {
                "private_key": enc_priv,
                "public_key": enc_pub
            }
        }

        print("\n[OK] Keys imported and saved to .env")
        return data
    
def get_first_peer(domain, dns_ip):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_ip]

    answers = resolver.resolve(domain, "A")
    return [r.to_text() for r in answers]


def sha256(string: str) -> str:
    return hashlib.sha256(string.encode("utf-8")).hexdigest()

def verify_signature(public_key: str, data: str, signature: str) -> bool:
    """
    Verify chữ ký Ed25519
    public_key: hex public key (32 bytes)
    data: text gốc
    signature: hex signature (64 bytes)
    """
    try:
        vk = ed25519.Ed25519PublicKey.from_public_bytes(
            bytes.fromhex(public_key)
        )

        vk.verify(
            bytes.fromhex(signature),
            data.encode("utf-8")
        )

        return True

    except Exception:
        return False


def sign_data(private_key: str, data: str) -> str:
    """
    Ký dữ liệu bằng Ed25519
    return hex signature
    """
    sk = ed25519.Ed25519PrivateKey.from_private_bytes(
        bytes.fromhex(private_key)
    )

    signature = sk.sign(
        data.encode("utf-8")
    )

    return signature.hex()


def encrypt_data(public_key: str, data: str) -> str:
    receiver_pub = x25519.X25519PublicKey.from_public_bytes(bytes.fromhex(public_key))

    eph_private = x25519.X25519PrivateKey.generate()
    eph_public = eph_private.public_key()

    secret = eph_private.exchange(receiver_pub)

    key = hashlib.sha256(secret).digest()

    nonce = os.urandom(12)

    cipher = ChaCha20Poly1305(key)

    encrypted = cipher.encrypt(nonce, data.encode(), None)

    eph_pub_hex = eph_public.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    ).hex()

    return eph_pub_hex + ":" + nonce.hex() + ":" + encrypted.hex()

def decrypt_data(private_key: str, data: str) -> str:
    eph_pub_hex, nonce_hex, encrypted_hex = data.split(":")

    my_private = x25519.X25519PrivateKey.from_private_bytes(bytes.fromhex(private_key))

    sender_pub = x25519.X25519PublicKey.from_public_bytes(bytes.fromhex(eph_pub_hex))

    secret = my_private.exchange(sender_pub)

    key = hashlib.sha256(secret).digest()

    cipher = ChaCha20Poly1305(key)

    decrypted = cipher.decrypt(
        bytes.fromhex(nonce_hex),
        bytes.fromhex(encrypted_hex),
        None
    )

    return decrypted.decode()
