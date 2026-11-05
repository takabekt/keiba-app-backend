"""
Keiba API - 騎手一覧取得APIルーティング

馬情報の次走予定入力画面および
レース回顧登録・編集画面の騎手選択プルダウンで利用する
騎手一覧取得APIを提供します。

騎手マスタに登録されている全騎手情報を取得し、
騎手名カナ順（50音順）で返却します。
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models.jockey import Jockey
from schemas import JockeyResponse

router = APIRouter(
    prefix="/api/jockeys",
    tags=["騎手"]
)


@router.get(
    "",
    response_model=list[JockeyResponse]
)
async def get_jockeys(
    db: Session = Depends(get_db)
):
    """
    騎手一覧取得API

    騎手マスタに登録されている全騎手情報を取得し、
    騎手名カナ順で返却する。
    """

    # 騎手マスタを騎手名カナ順で取得
    jockeys = (
        db.query(Jockey)
        .order_by(Jockey.jockey_name_kana)
        .all()
    )

    result = []

    # APIレスポンス生成
    for jockey in jockeys:
        result.append(
            JockeyResponse(
                id=jockey.id,
                jockey_name=jockey.jockey_name
            )
        )

    return result
