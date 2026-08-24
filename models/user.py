"""
Keiba API - データベースモデル定義
SQLAlchemyを使用して、PostgreSQL(Neon)データベースの
テーブル構造をPythonクラスとして定義します。
"""
from sqlalchemy import Column, BigInteger, String, DateTime, func
from core.database import Base

class AppUser(Base):
    """
    ユーザーテーブル (app_user)
    ログイン認証およびユーザー情報を管理するモデル
    """
    __tablename__ = "app_user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(10), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)  # ハッシュ化パスワード
    name = Column(String(20), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())