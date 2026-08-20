"""
Keiba API - 認証・暗号化ユーティリティ
パスワードの暗号化/照合(bcrypt)および
JWT(JSON Web Token)の生成・検証ロジックを管理します。
"""
import os
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from dotenv import load_dotenv

load_dotenv()

# .env から設定読み込み
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key_change_me")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """平文パスワードとDBのハッシュ値を検証"""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

def create_access_token(data: dict) -> str:
    """JWTアクセストークンを発行"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt