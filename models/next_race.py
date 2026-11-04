"""
Keiba API - データベースモデル定義
SQLAlchemyを使用して、PostgreSQL(Neon)データベースの
テーブル構造をPythonクラスとして定義します。
"""

from sqlalchemy import (
    Column,
    BigInteger,
    String
)

from core.database import Base


class NextRace(Base):
    """
    次走情報テーブル (next_race)
    次のレース情報を管理するモデル
    """
    __tablename__ = "next_race"

    id = Column(BigInteger, primary_key=True)
    horse_id = Column(BigInteger, nullable=False)
    race_name = Column(String(50), nullable=True)