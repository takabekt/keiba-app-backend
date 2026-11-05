"""
Keiba API - 騎手マスタモデル

騎手マスタ(jockey)テーブルの
SQLAlchemyモデルを定義します。
"""

from sqlalchemy import Column, BigInteger, String
from core.database import Base


class Jockey(Base):
    """
    騎手マスタテーブル(jockey)
    """

    __tablename__ = "jockey"

    id = Column(BigInteger, primary_key=True)
    jockey_name = Column(String(20), nullable=False)
    jockey_name_kana = Column(String(20), nullable=False)