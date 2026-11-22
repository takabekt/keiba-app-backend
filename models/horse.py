"""
Keiba API - データベースモデル定義
SQLAlchemyを使用して、PostgreSQL(Neon)データベースの
テーブル構造をPythonクラスとして定義します。
"""

from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    SmallInteger,
    String,
    Text,
)
from core.database import Base


class Horse(Base):
    """
    馬マスタテーブル (horse)
    競走馬の情報を管理するモデル
    """
    __tablename__ = "horse"

    # ID
    id = Column(
        BigInteger,
        primary_key=True,
    )

    # 馬名
    name = Column(
        String(20),
        nullable=False,
    )

    # 性別区分
    # 0: 牡 / 1: 牝 / 2: セン
    sex_type = Column(
        SmallInteger,
        nullable=False,
    )

    # 生年月日
    birth_date = Column(
        Date,
        nullable=False,
    )

    # 血統（父）
    sire = Column(
        String(20),
        nullable=True,
    )

    # 血統（母）
    dam = Column(
        String(20),
        nullable=True,
    )

    # 血統（母父）
    bms = Column(
        String(20),
        nullable=True,
    )

    # 脚質区分
    # 0: 逃げ / 1: 先行 / 2: 差し / 3: 追込
    running_style_type = Column(
        SmallInteger,
        nullable=False,
    )

    # 現役・引退区分
    # 0: 現役 / 1: 引退
    status_type = Column(
        SmallInteger,
        nullable=False,
    )

    # メモ
    memo = Column(
        Text,
        nullable=True,
    )