"""
Keiba API - 馬情報Repository

馬情報、次走情報、騎手情報に関する
データベース取得処理を提供します。

RouterからDBアクセス処理を分離し、
データ取得処理を一元管理します。
"""

from sqlalchemy import or_
from sqlalchemy.orm import Session

from models.horse import Horse
from models.jockey import Jockey
from models.next_race import NextRace

def get_horses_with_next_race(
    db: Session,
    keyword: str | None = None,
) -> list[tuple[Horse, NextRace | None]]:
    """
    馬一覧および次走情報取得

    馬情報と次走情報を外部結合して取得する。
    検索キーワードが指定された場合は、
    馬名または次走レース名による部分一致検索を行う。

    Args:
        db: データベースセッション
        keyword: 検索キーワード

    Returns:
        馬情報と次走情報の組み合わせ一覧。
        次走情報がない場合、NextRaceはNone。
    """

    # 馬情報と次走情報を外部結合
    query = (
        db.query(Horse, NextRace)
        .outerjoin(
            NextRace,
            Horse.id == NextRace.horse_id,
        )
    )

    # 検索キーワードが指定された場合
    if keyword:
        query = query.filter(
            or_(
                Horse.name.contains(keyword),
                (
                    NextRace.race_name.is_not(None)
                    & NextRace.race_name.contains(keyword)
                ),
            )
        )

    # 馬名順で取得
    return (
        query
        .order_by(Horse.name)
        .all()
    )

def get_horse_by_id(
    db: Session,
    horse_id: int,
) -> Horse | None:
    """
    馬IDによる馬情報取得

    指定された馬IDに一致する馬情報を取得する。

    Args:
        db: データベースセッション
        horse_id: 取得対象の馬ID

    Returns:
        対象の馬情報。存在しない場合はNone。
    """

    return (
        db.query(Horse)
        .filter(Horse.id == horse_id)
        .first()
    )

def get_next_race_by_horse_id(
    db: Session,
    horse_id: int,
) -> NextRace | None:
    """
    馬IDによる次走情報取得

    指定された馬IDに一致する次走情報を取得する。

    Args:
        db: データベースセッション
        horse_id: 取得対象の馬ID

    Returns:
        対象馬の次走情報。存在しない場合はNone。
    """

    return (
        db.query(NextRace)
        .filter(NextRace.horse_id == horse_id)
        .first()
    )

def get_jockey_by_id(
    db: Session,
    jockey_id: int,
) -> Jockey | None:
    """
    騎手IDによる騎手情報取得

    指定された騎手IDに一致する騎手情報を取得する。

    Args:
        db: データベースセッション
        jockey_id: 取得対象の騎手ID

    Returns:
        対象の騎手情報。存在しない場合はNone。
    """

    return (
        db.query(Jockey)
        .filter(Jockey.id == jockey_id)
        .first()
    )