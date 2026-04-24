from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError
from cryptography.hazmat.primitives.asymmetric import x25519
import hashlib
from cryptography.hazmat.primitives import serialization
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


# =========================
# SIGNATURE KEYPAIR
# secp256k1
# =========================
def generate_signature_keys():
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.get_verifying_key()

    return {
        "private_key": sk.to_string().hex(),
        "public_key": vk.to_string().hex()
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
    Verify chữ ký secp256k1
    public_key: hex public key
    data: text gốc
    signature: hex signature
    """
    try:
        vk = VerifyingKey.from_string(
            bytes.fromhex(public_key),
            curve=SECP256k1
        )

        vk.verify(
            bytes.fromhex(signature),
            data.encode("utf-8"),
            hashfunc=hashlib.sha256
        )
        return True

    except BadSignatureError:
        return False
    except Exception:
        return False


def sign_data(private_key: str, data: str) -> str:
    """
    Ký dữ liệu bằng secp256k1
    return hex signature
    """
    sk = SigningKey.from_string(
        bytes.fromhex(private_key),
        curve=SECP256k1
    )

    signature = sk.sign(
        data.encode("utf-8"),
        hashfunc=hashlib.sha256
    )

    return signature.hex()


def encypt_data(public_key: str, data: str) -> str:
    """
    Mã hóa kiểu shared secret X25519
    Trả về: eph_public_hex:encrypted_hex
    """
    receiver_pub = x25519.X25519PublicKey.from_public_bytes(
        bytes.fromhex(public_key)
    )

    # ephemeral key
    eph_private = x25519.X25519PrivateKey.generate()
    eph_public = eph_private.public_key()

    # shared secret
    secret = eph_private.exchange(receiver_pub)

    # tạo key stream
    key = hashlib.sha256(secret).digest()

    raw = data.encode("utf-8")

    encrypted = bytes(
        raw[i] ^ key[i % len(key)]
        for i in range(len(raw))
    )

    eph_pub_hex = eph_public.public_bytes_raw().hex()

    return eph_pub_hex + ":" + encrypted.hex()


def decrypt_data(private_key: str, data: str) -> str:
    """
    Giải mã dữ liệu từ format eph_pub:encrypted
    """
    eph_pub_hex, encrypted_hex = data.split(":")

    my_private = x25519.X25519PrivateKey.from_private_bytes(
        bytes.fromhex(private_key)
    )

    sender_pub = x25519.X25519PublicKey.from_public_bytes(
        bytes.fromhex(eph_pub_hex)
    )

    secret = my_private.exchange(sender_pub)

    key = hashlib.sha256(secret).digest()

    encrypted = bytes.fromhex(encrypted_hex)

    decrypted = bytes(
        encrypted[i] ^ key[i % len(key)]
        for i in range(len(encrypted))
    )

    return decrypted.decode("utf-8")
