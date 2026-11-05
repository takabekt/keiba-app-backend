"""
Keiba API - データベースモデル定義
SQLAlchemyを使用して、PostgreSQL(Neon)データベースの
テーブル構造をPythonクラスとして定義します。
"""

from sqlalchemy import Column, BigInteger, Date, String
from core.database import Base


class Horse(Base):
    """
    馬マスタテーブル (horse)
    競走馬の情報を管理するモデル
    """
    __tablename__ = "horse"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    sex_type = Column(String(1), nullable=False)
    birth_date = Column(Date, nullable=False)