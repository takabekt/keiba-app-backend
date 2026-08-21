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
from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import AppUser

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
    # 有効期限（現在時刻 + 指定分）を設定
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # SECRET_KEY を使って署名・暗号化
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> AppUser:
    """
    Cookie(access_token)からJWTを取得・検証し、
    ログイン中のユーザー情報(AppUser)を取得する Dependency
    """
    # Cookie から access_token を取得
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "認証が必要です。ログインしてください。"}
        )

    # 先頭の "Bearer " を除去
    if token.startswith("Bearer "):
        token = token[7:]

    # JWT のデコードと検証
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"message": "無効なトークンです。"}
            )
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "トークンの有効期限が切れています。"}
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "無効なトークンです。"}
        )

    # DB からユーザーを取得
    user = db.query(AppUser).filter(AppUser.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "ユーザーが存在しません。"}
        )

    return user