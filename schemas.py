"""
Keiba API - リクエスト / レスポンス スキーマ定義

Pydanticモデルを使用して、APIに入力されるデータの
バリデーションおよびレスポンス出力のデータ構造を定義します。
"""

from datetime import date

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """
    ログインリクエスト
    """

    # ユーザーコード
    code: str = Field(
        ...,
        max_length=10,
        description="ユーザーコード",
    )

    # パスワード
    password: str = Field(
        ...,
        description="パスワード",
    )


class LoginSuccessResponse(BaseModel):
    """
    ログイン成功レスポンス
    """

    # ログイン結果メッセージ
    message: str = "ログインに成功しました。"


class ErrorDetail(BaseModel):
    """
    エラー詳細情報

    後ほど削除する。
    """

    # エラーメッセージ
    message: str


class ErrorResponse(BaseModel):
    """
    共通エラーレスポンス（401、404など）
    """

    # エラーメッセージ
    message: str


class UserResponse(BaseModel):
    """
    ユーザー情報レスポンス

    動作確認用のため、後ほど削除する。
    """

    # ユーザーID
    id: int

    # ユーザーコード
    code: str

    # ユーザー名
    name: str


class AuthCheckResponse(BaseModel):
    """
    認証確認レスポンス
    """

    # 認証状態
    authenticated: bool


class HorseResponse(BaseModel):
    """
    馬一覧情報レスポンス
    """

    # 馬ID
    id: int

    # 馬名
    horse_name: str

    # 性別名
    gender: str

    # 競馬年齢
    age: int

    # 次走レース名
    # 次走情報が存在しない場合はNone
    next_race_name: str | None = None


class JockeyResponse(BaseModel):
    """
    騎手一覧レスポンス
    """

    # 騎手ID
    id: int

    # 騎手名
    jockey_name: str


class NextRaceDetailResponse(BaseModel):
    """
    次走情報詳細レスポンス

    馬詳細取得APIで返却する次走情報を定義する。
    次走情報の各項目は未確定の場合があるため、Noneを許可する。
    """

    # 次走情報ID
    id: int

    # レース名
    race_name: str | None = None

    # 枠順
    bracket_number: int | None = None

    # 馬番
    horse_number: int | None = None

    # 斤量
    weight_carried: float | None = None

    # 騎手ID
    jockey_id: int | None = None

    # 騎手名
    jockey_name: str | None = None


class HorseDetailResponse(BaseModel):
    """
    馬情報詳細レスポンス

    馬詳細取得APIで返却する馬の基本情報と
    次走情報を定義する。
    """

    # 馬ID
    id: int

    # 馬名
    horse_name: str

    # 生年月日
    birth_date: date

    # 競馬年齢
    age: int

    # 性別区分
    # 0: 牡 / 1: 牝 / 2: セン
    sex_type: int

    # 血統（父）
    sire: str | None = None

    # 血統（母）
    dam: str | None = None

    # 血統（母父）
    bms: str | None = None

    # 脚質区分
    # 0: 逃げ / 1: 先行 / 2: 差し / 3: 追込
    running_style_type: int

    # 現役・引退区分
    # 0: 現役 / 1: 引退
    status_type: int

    # メモ
    memo: str | None = None

    # 次走情報
    # 次走情報が存在しない場合はNone
    next_race: NextRaceDetailResponse | None = None