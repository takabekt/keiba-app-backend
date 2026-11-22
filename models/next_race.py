"""
Keiba API - データベースモデル定義
SQLAlchemyを使用して、PostgreSQL(Neon)データベースの
テーブル構造をPythonクラスとして定義します。
"""

from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Numeric,
    SmallInteger,
    String,
)


from core.database import Base


class NextRace(Base):
    """
    次走情報テーブル（next_race）

    競走馬ごとの次走情報を管理するモデル。
    1頭につき1件の次走情報を保持する。
    """

    __tablename__ = "next_race"

    # ID
    id = Column(
        BigInteger,
        primary_key=True,
    )

    # 馬ID
    # 1頭につき次走情報は1件のみ保持
    horse_id = Column(
        BigInteger,
        ForeignKey("horse.id"),
        nullable=False,
        unique=True,
    )

    # レース名
    race_name = Column(
        String(50),
        nullable=True,
    )

    # 枠順
    bracket_number = Column(
        SmallInteger,
        nullable=True,
    )

    # 馬番
    horse_number = Column(
        SmallInteger,
        nullable=True,
    )

    # 斤量
    weight_carried = Column(
        Numeric(3, 1),
        nullable=True,
    )

    # 騎手ID
    jockey_id = Column(
        BigInteger,
        ForeignKey("jockey.id"),
        nullable=True,
    )