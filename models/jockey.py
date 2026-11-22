"""
Keiba API - 騎手マスタモデル

騎手マスタ(jockey)テーブルの
SQLAlchemyモデルを定義します。
"""

from sqlalchemy import Column, BigInteger, String
from core.database import Base


class Jockey(Base):
    """
    騎手マスタテーブル（jockey）

    騎手の基本情報を管理するモデル。
    """

    __tablename__ = "jockey"

    # ID
    id = Column(
        BigInteger,
        primary_key=True,
    )

    # 騎手名
    jockey_name = Column(
        String(20),
        nullable=False,
    )

    # 騎手名カナ
    jockey_name_kana = Column(
        String(20),
        nullable=False,
    )