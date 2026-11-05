"""
Keiba API - 馬一覧取得APIルーティング

馬情報検索画面/レース回顧検索画面で利用する馬一覧取得APIを提供します。
馬名および次走レース名による部分一致検索を行い、
検索条件未指定時は全件取得します。

また、性別区分の変換および競馬年齢の算出を行い、
フロントエンド向けのレスポンスを生成します。
"""

from datetime import date
from fastapi import APIRouter, Query, Depends

from sqlalchemy.orm import Session
from sqlalchemy import or_

from core.database import get_db
from models.horse import Horse
from schemas import HorseResponse
from models.next_race import NextRace

# 性別区分変換マップ
SEX_TYPE_MAP = {
    0: "牡",
    1: "牝",
    2: "セン"
}

router = APIRouter(
    prefix="/api/horses",
    tags=["馬"]
)

def calculate_horse_age(
    birth_date: date
) -> int:
    """
    競馬年齢算出

    競走馬は毎年1月1日に加齢するため、
    現在年 - 生年で年齢を算出する。
    """
    return date.today().year - birth_date.year


@router.get(
    "",
    response_model=list[HorseResponse]
)
async def get_horses(
    keyword: str | None = Query(
        default=None,
        max_length=50,
        description="検索キーワード"
    ),
    db: Session = Depends(get_db)
):
    """
    馬一覧取得API

    検索条件が指定された場合は、
    馬名または次走レース名の部分一致検索を行う。

    検索条件未指定時は全件取得し、
    馬名順で返却する。
    """

    # 検索条件あり
    if keyword:
        horses = (
            db.query(Horse, NextRace)
            # 次走情報を外部結合
            .outerjoin(
                NextRace,
                Horse.id == NextRace.horse_id
            )
            # 馬名または次走レース名で部分一致検索
            .filter(
                or_(
                    Horse.name.contains(keyword),
                    NextRace.race_name.is_not(None) &
                    NextRace.race_name.contains(keyword)
                )
            )
            # 馬名順でソート
            .order_by(Horse.name)
            .all()
        )
    else:
        # 検索条件未指定時は全件取得
        horses = (
            db.query(Horse, NextRace)
            .outerjoin(
                NextRace,
                Horse.id == NextRace.horse_id
            )
            .order_by(Horse.name)
            .all()
        )

    result = []

    # APIレスポンス生成
    for horse, next_race in horses:
        result.append(
            HorseResponse(
                id=horse.id,
                horse_name=horse.name,
                gender=SEX_TYPE_MAP.get(
                    horse.sex_type,
                    ""
                ),
                age=calculate_horse_age(
                    horse.birth_date
                ),
                next_race_name=(
                    next_race.race_name
                    if next_race
                    else None
                )
            )
        )

    return result