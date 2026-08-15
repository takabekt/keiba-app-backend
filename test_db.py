import bcrypt
from database import SessionLocal
from sqlalchemy import text


def main():
    # ハッシュ化したいパスワード
    raw_password = "Password123!"

    # bcrypt でパスワードをハッシュ化
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(raw_password.encode("utf-8"), salt)
    hashed_password = hashed_bytes.decode("utf-8")

    print(f"🔑 生成されたハッシュ化パスワード: {hashed_password}")

    # DBセッション開始
    db = SessionLocal()
    try:
        # 1. 接続確認（SQL実行）
        result = db.execute(text("SELECT CURRENT_DATABASE(), VERSION();")).fetchone()
        print(f"✅ DB接続成功! 接続先DB: {result[0]}")

        # 2. 既存ユーザー 'admin' のパスワードをハッシュ化値で更新
        update_stmt = text(
            "UPDATE app_user SET password = :hashed_password WHERE code = :code"
        )
        db.execute(
            update_stmt, {"hashed_password": hashed_password, "code": "admin"}
        )
        db.commit()
        print("🎉 'admin' ユーザーのパスワードをハッシュ化値に更新しました！")

    except Exception as e:
        db.rollback()
        print(f"❌ エラーが発生しました: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()