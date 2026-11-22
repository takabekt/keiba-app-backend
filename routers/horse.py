"""
Keiba API - 馬情報APIルーティング

馬情報検索画面で利用する馬一覧取得APIと、
指定された馬IDから馬基本情報・次走情報を取得する
馬詳細取得APIを提供します。

馬一覧取得APIでは、馬名および次走レース名による
部分一致検索を行います。

馬詳細取得APIでは、馬情報・次走情報・騎手情報を取得し、
フロントエンド向けのレスポンスを生成します。
"""

from datetime import date
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)

from sqlalchemy.orm import Session

from core.database import get_db
from schemas import (
    HorseDetailResponse,
    HorseResponse,
    NextRaceDetailResponse,
)
from repositories.horse_repository import (
    get_horse_by_id,
    get_horses_with_next_race,
    get_jockey_by_id,
    get_next_race_by_horse_id,
)

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

    # 馬一覧および次走情報を取得
    horses = get_horses_with_next_race(
        db,
        keyword,
    )

    result = []

    # 馬一覧取得APIレスポンス生成
    for horse, next_race in horses:
        result.append(
            HorseResponse(
                # 馬ID
                id=horse.id,

                # 馬名
                horse_name=horse.name,

                # 性別区分を表示名へ変換
                gender=SEX_TYPE_MAP.get(
                    horse.sex_type,
                    ""
                ),

                # 生年月日から競馬年齢を算出
                age=calculate_horse_age(
                    horse.birth_date
                ),

                # 次走レース名
                # 次走情報が存在しない場合はNone
                next_race_name=(
                    next_race.race_name
                    if next_race
                    else None
                )
            )
        )

    return result


@router.get(
    "/{horse_id}",
    response_model=HorseDetailResponse,
)
async def get_horse_detail(
    horse_id: int,
    db: Session = Depends(get_db),
):
    """
    馬詳細取得API

    指定された馬IDをもとに、
    馬情報を取得する。
    """

    # 馬IDによる馬情報取得
    horse = get_horse_by_id(
        db,
        horse_id,
    )

    # 対象馬が存在しない場合
    if horse is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定された馬情報が存在しません。",
        )

    # 馬IDによる次走情報取得
    next_race = get_next_race_by_horse_id(
        db,
        horse_id,
    )

    # 騎手情報
    jockey = None

    # 次走情報と騎手IDが存在する場合
    if (
        next_race is not None
        and next_race.jockey_id is not None
    ):
        jockey = get_jockey_by_id(
            db,
            next_race.jockey_id,
        )

    # 次走情報レスポンス
    next_race_response = None

    # 次走情報が存在する場合
    if next_race is not None:
        next_race_response = NextRaceDetailResponse(
            id=next_race.id,
            race_name=next_race.race_name,
            bracket_number=next_race.bracket_number,
            horse_number=next_race.horse_number,
            weight_carried=next_race.weight_carried,
            jockey_id=next_race.jockey_id,
            jockey_name=(
                jockey.jockey_name
                if jockey is not None
                else None
            ),
        )
    # 馬詳細取得APIレスポンス生成
    # 編集画面で区分値をそのまま更新データとして利用できるよう、文字列へ変換せず返却
    return HorseDetailResponse(
        # 馬ID（horse.id）
        id=horse.id,

        # 馬名
        horse_name=horse.name,

        # 生年月日
        birth_date=horse.birth_date,

        # 生年月日から競馬年齢を算出
        age=calculate_horse_age(
            horse.birth_date
        ),

        # 性別区分
        sex_type=horse.sex_type,

        # 血統・父
        sire=horse.sire,

        # 血統・母
        dam=horse.dam,

        # 血統・母父
        bms=horse.bms,

        # 脚質区分
        running_style_type=horse.running_style_type,

        # 現役・引退区分
        status_type=horse.status_type,

        # メモ
        memo=horse.memo,

        # 次走情報
        # 次走情報が存在しない場合はNone
        next_race=next_race_response,
    )
