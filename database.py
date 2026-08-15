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

# DBセッションを取得する依存関数（API等で使用）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()