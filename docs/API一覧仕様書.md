# API一覧仕様

## 1. 認証関連
* `POST /api/auth/login`
  * **役割:** ログイン処理（コードとパスワードの照合）
* `GET /api/auth/me`
  * **役割:** ログイン状態確認（Cookie内JWTの有効性確認）

## 2. 馬・次走情報関連
* `GET /api/horses`
  * **役割:** 馬一覧取得（馬情報検索画面/レース回顧検索画面）
* `GET /api/horses/{id}`
  * **役割:** 馬詳細取得（詳細・編集画面用・次走予定データを含む）
* `POST /api/horses`
  * **役割:** 馬情報＋次走予定の新規登録（トランザクション処理）
* `PUT /api/horses/{id}`
  * **役割:** 馬情報＋次走予定の更新
* `DELETE /api/horses/{id}`
  * **役割:** 馬情報の削除（紐づく次走予定・レース回顧も自動カスケード削除）

## 3. レース回顧関連
* `GET /api/horses/{horse_id}/race-reviews`
  * **役割:** 対象馬のレース回顧一覧取得（特定の馬に絞ったレース回顧画面）
* `POST /api/horses/full-field-analysis`
  * **役割:** 対象馬全頭のレース回顧一覧と次走レース情報取得（全頭診断照会画面)
* `POST /api/race-reviews`
  * **役割:** レース回顧の新規登録
* `PUT /api/race-reviews/{id}`
  * **役割:** レース回顧の更新
* `DELETE /api/race-reviews/{id}`
  * **役割:** レース回顧の単体削除

## 4. 競馬場・馬場状態関連
* **`GET /api/racetracks`**
  * **役割:** 競馬場一覧取得（検索画面用）
* **`GET /api/racetracks/{id}/conditions`**
  * **役割:** 対象競馬場の馬場状態取得（照会画面用）
* **`PUT /api/racetracks/{id}/conditions`**
  * **役割:** 馬場状態の更新・登録（更新画面用）

## 5. ドロップダウンリスト用
* **`GET /api/jockeys`**
  * **役割:** 騎手一覧取得