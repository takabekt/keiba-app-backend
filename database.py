"""
Keiba API - データベース接続・セッション管理
SQLAlchemy を使用して PostgreSQL (Neon) データベースとの接続を確立し、
リクエストごとの DB セッション管理 (get_db) を行います。
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# .env ファイルから環境変数を読み込む
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL が .env に設定されていません。")

# SQLAlchemy エンジンの作成
engine = create_engine(DATABASE_URL)

# DBセッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORMモデル用のベースクラス
Base = declarative_base()

def get_db():
    """
    DBセッションを取得・管理するジェネレータ関数 (FastAPIのDependency用)
    リクエスト処理の開始時にセッションを開き、処理終了時に自動でクローズします。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()