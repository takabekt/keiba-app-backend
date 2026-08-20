"""
Keiba API - リクエスト / レスポンス スキーマ定義
Pydanticモデルを使用して、APIに入力されるデータのバリデーションおよび
レスポンス出力のデータ構造を定義します。
"""
from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    """ログインリクエスト"""
    code: str = Field(..., max_length=10, description="ユーザーコード")
    password: str = Field(..., description="パスワード")

class LoginSuccessResponse(BaseModel):
    """ログイン成功レスポンス"""
    message: str = "ログインに成功しました。"

class ErrorDetail(BaseModel):
    """エラー詳細情報"""
    message: str

class ErrorResponse(BaseModel):
    """共通エラーレスポンス (401等)"""
    detail: ErrorDetail