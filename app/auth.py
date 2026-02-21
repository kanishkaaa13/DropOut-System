import mysql.connector
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext

# =========================
# Password hashing context
# =========================
pwd_context = CryptContext(
    schemes=["bcrypt"],   # you can add "argon2" later if you want
    deprecated="auto",
)

MAX_BCRYPT_LEN = 72  # bytes

def get_password_hash(password: str) -> str:
    """
    Hash password with bcrypt, trimming to 72 bytes to avoid bcrypt limit errors.
    """
    trimmed = password.encode("utf-8")[:MAX_BCRYPT_LEN].decode(
        "utf-8", errors="ignore"
    )
    return pwd_context.hash(trimmed)

def verify_password(plain: str, hashed: str) -> bool:
    """
    Verify plaintext password against stored hash, using same trimming.
    """
    trimmed = plain.encode("utf-8")[:MAX_BCRYPT_LEN].decode(
        "utf-8", errors="ignore"
    )
    return pwd_context.verify(trimmed, hashed)

# =========================
# JWT config
# =========================
SECRET_KEY = "CHANGE_THIS_IN_PRODUCTION"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# =========================
# MySQL connection helpers
# =========================
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,             # Standard MySQL port
        user="root",
        password="Karma@555",  # Updated to your confirmed password
        database="dropout_system",
    )

def get_user(email: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT email, hashed_password, role FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        return user
    finally:
        cursor.close()
        conn.close()

def create_user(email: str, password: str, role: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pw = get_password_hash(password)
    try:
        query = "INSERT INTO users (email, hashed_password, role) VALUES (%s, %s, %s)"
        cursor.execute(query, (email, hashed_pw, role))
        conn.commit()
        return {"email": email, "role": role}
    except mysql.connector.Error as err:
        # You can log this properly later
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        conn.close()
