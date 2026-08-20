"""
Keiba API - メインアプリケーションおよびルーティング
FastAPIのインスタンス生成、各エンドポイントのルーティング、
およびリクエスト/レスポンスの制御を行います。
"""
from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from database import get_db
from models import AppUser
from schemas import LoginRequest, LoginSuccessResponse, ErrorResponse
from auth import verify_password, create_access_token

app = FastAPI(title="Keiba API")

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

    # API仕様書に沿って HttpOnly Cookie（セッションCookie）としてセット
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=False,  # ローカル開発環境(http)用。本番環境(https)ではTrueに設定
        samesite="lax",
        max_age=3600
    )

    return {"message": "ログインに成功しました。"}