"""
Keiba API - メインアプリケーションおよびルーティング
FastAPIのインスタンス生成、各エンドポイントのルーティング、
およびリクエスト/レスポンスの制御を行います。
"""
import os

from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import AppUser
from schemas import AuthCheckResponse, LoginRequest, LoginSuccessResponse, ErrorResponse
from core.auth import verify_password, create_access_token, get_current_user

app = FastAPI(title="Keiba API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://keiba-app-frontend.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"],
)

# 環境変数から環境種別（development / production）を取得（デフォルトは dev）
IS_PRODUCTION = os.getenv("ENV", "development") == "production"

@app.post(
    "/api/auth/login",
    response_model=LoginSuccessResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"}
    },
    tags=["認証"]
)
def login(
    request_data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    # code によるユーザーレコード取得
    user = db.query(AppUser).filter(AppUser.code == request_data.code).first()

    # ユーザーが存在しない、または bcrypt によるパスワード照合失敗時
    # 失敗時は 401 Unauthorized の共通エラーレスポンスを返却
    if not user or not verify_password(request_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "ユーザーコードまたはパスワードが正しくありません。"}
        )

    # PyJWTを利用したアクセストークン生成
    access_token = create_access_token(data={"sub": user.code, "user_id": user.id})

    # HttpOnly Cookie（セッションCookie）としてセット
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=IS_PRODUCTION,  # 本番環境のみ True になる
        samesite="lax",
        max_age=3600
    )

    return {"message": "ログインに成功しました。"}

# JWT認証処理確認用API
@app.get(
    "/api/auth/me",
    response_model=AuthCheckResponse,
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Unauthorized",
        }
    },
    tags=["認証"],
    dependencies=[Depends(get_current_user)],
)
def get_me():
    """
    Cookie内のJWTが有効か確認するAPI。
    認証成功時は認証結果を返し、
    認証失敗時は401を返す。
    """
    return {
        "authenticated": True
    }