"""
Keiba API - 共通例外ハンドリング

FastAPIで発生したバリデーションエラーおよび
想定外エラーを共通処理し、統一したエラーレスポンスを返却します。

また、エラー内容に応じたログを出力します。
"""

import logging

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


# このファイル専用のロガー
logger = logging.getLogger(__name__)


# APIパラメーター名と画面表示名の対応
FIELD_NAME_MAP = {
    "keyword": "検索キーワード",
}


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """
    バリデーションエラー共通処理

    FastAPIの入力値検証で発生したエラーを処理し、
    HTTP 422のレスポンスを返却します。
    """

    # 複数のエラーがある場合は、先頭のエラーを使用
    error = exc.errors()[0]

    # エラー種別、エラー対象の項目名、エラー詳細を取得
    error_type = error.get("type")
    location = error.get("loc", [])
    context = error.get("ctx", {})

    # エラー対象のパラメーター名を取得
    field_name = (
        str(location[-1])
        if location
        else "入力項目"
    )

    # API上のパラメーター名を日本語表示名へ変換
    display_name = FIELD_NAME_MAP.get(
        field_name,
        field_name,
    )

    # 最大文字数超過の場合
    if error_type == "string_too_long":
        max_length = context.get("max_length")

        message = (
            f"{display_name}は"
            f"{max_length}文字以内で入力してください。"
        )
    else:
        # その他のバリデーションエラー
        message = "入力内容を確認してください。"

    # ユーザー向けメッセージとエラー詳細をWARNINGログとして出力
    logger.warning(
        "%s path=%s errors=%s",
        message,
        request.url.path,
        exc.errors(),
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "message": message,
        },
    )


async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    想定外エラー共通処理

    DB接続エラーなどの想定外例外を処理し、
    HTTP 500のレスポンスを返却します。
    """

    # スタックトレースを含むERRORログを出力
    logger.error(
        "想定外エラーが発生しました。 path=%s",
        request.url.path,
        exc_info=(
            type(exc),
            exc,
            exc.__traceback__,
        ),
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "システムエラーが発生しました。",
        },
    )
