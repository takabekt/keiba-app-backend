# API仕様書

## 1. 認証関連

### 1.1 ログイン処理

送信されたユーザーコードとパスワードをもとに認証を行い、成功時にはJWTトークンをHttpOnly Cookieへ保存します。

* **Method:** `POST`
* **Path:** `/api/auth/login`
* **Content-Type:** `application/json`

#### リクエストパラメータ（Body）

| パラメータ名 | 型 | 必須 | 説明 |
| :--- | :--- | :--- | :--- |
| `code` | string | ○ | ユーザーコード（最大10文字） |
| `password` | string | ○ | パスワード（平文） |

#### リクエスト例
```json
{
  "code": "kattsun",
  "password": "Password123!"
}
```
#### レスポンス例（成功時 : 200 OK）
```json
{
  "message": "ログインに成功しました。"
}
```
#### レスポンス例（失敗時 : 401 Unauthorized）
```json
{
  "message": "ユーザーコードまたはパスワードが正しくありません。"
}
```

### 1.2 認証状態確認

アプリ起動時にログイン状態を復元するため、Cookie内のJWTを検証します。

このAPIは認証状態確認専用であり、馬情報・競馬場情報などの業務データ取得には使用しません。

認証が必要な業務APIでは、それぞれ `Depends(get_current_user)` によりJWT認証を行います。

* **Method:** `GET`
* **Path:** `/api/auth/me`

#### 用途

```text
アプリ起動
↓
GET /api/auth/me
↓
Cookie内JWTを検証
↓
認証状態を復元
#### レスポンス例（成功時 : 200 OK）
```json
{
  "authenticated": true
}
```
#### レスポンス例（失敗時 : 401 Unauthorized）
```json
{
  "detail": {
    "message": "トークンの有効期限が切れています。"
  }
}
```
## 2. 馬・次走情報関連

### 2.1 馬一覧取得処理

馬情報検索画面用。全件または入力された検索キーワードをもとに、**馬名**または**次走レース名**に該当する馬の一覧データを**馬名順（50音順）**で取得します。

* **Method:** `GET`
* **Path:** `/api/horses`
* **Content-Type:** `application/json`

#### リクエストパラメータ（Query）

| パラメータ名 | 型 | 必須 | 説明 |
| :--- | :--- | :--- | :--- |
| `keyword` | string | × | 検索キーワード（馬名 または 次走レース名の部分一致）<br>※未指定の場合は全件取得 |

#### リクエスト例
`GET /api/horses?keyword=ダービー`

#### レスポンス例（成功時 : 200 OK）
```json
[
  {
    "id": 1,
    "name": "クロワデュノール",
    "age": 4,
    "sexType": 0,
    "statusType": 0,
    "nextRaceName": "日本ダービー"
  }
]
```
#### レスポンス例（失敗時 : 400 Bad Request）
```json
{
  "message": "検索条件パラメータの形式が不正です。"
}
```


### 2.2 馬詳細情報取得処理

馬情報詳細画面（照会画面）用。パスパラメータで受け取った馬IDをもとに、馬の基本情報・次走情報・過去のレース回顧一覧をまとめて取得します。

* **Method:** `GET`
* **Path:** `/api/horses/{id}`
* **Content-Type:** `application/json`

#### リクエストパラメータ（Path）

| パラメータ名 | 型 | 必須 | 説明 |
| :--- | :--- | :--- | :--- |
| `id` | number | ○ | 馬ID (`horse.id`) |

#### リクエスト例
`GET /api/horses/1`

#### レスポンス例（成功時 : 200 OK）
```json
{
  "id": 1,
  "name": "クロワデュノール",
  "memo":"次走レース本命候補",
  "nextRace": {
    "raceName": "日本ダービー",
    "bracketNumber": 1,
    "horseNumber": 2,
    "weightCarried": 57.0,
    "jockeyName": "北村友一"
  },
  "raceReviews": [
    {
      "id": 10,
      "raceName": "東京スポーツ杯2歳S",
      "date": "2024-11-16",
      "raceClass": 2,
      "racetrackName": "東京",
      "turnType": 1,
      "trackType": 0,
      "distance": 1800,
      "conditionType": 0,
      "cushionValue": 9.6,
      "finishTime": "1:46.8",
      "finishPosition": 1,
      "popularity": 1,
      "headCount": 9,
      "bracketNumber": 8,
      "horseNumber": 9,
      "weightCarried": 56.0,
      "horseWeight": 482.0,
      "cornerPositions": "2-2-2",
      "last3fTime": 33.3,
      "margin": "+0.1",
      "paceType": 0,
      "jockeyName": "北村友一",
      "memo": "好位追走から直線楽に抜け出す強い競馬。",
      "jockeyComment": "手応え十分でした。"
    }
  ]
}
```
#### レスポンス例（失敗時 : 404 Not Found）
```json
{
  "message": "指定された馬情報が見つかりません。"
}
```

### 2.3 馬情報登録処理

馬情報登録画面用。送信されたデータをもとに、馬マスタ（`horse`）および次走情報（`next_race`）を同時に新規登録します。

* **Method:** `POST`
* **Path:** `/api/horses`
* **Content-Type:** `application/json`

#### リクエストパラメータ（Body）

| パラメータ名 | 型 | 必須 | 説明 |
| :--- | :--- | :--- | :--- |
| `name` | string | ○ | 馬名（最大20文字） |
| `birthDate` | string | ○ | 生年月日（形式: `YYYY-MM-DD`） |
| `sexType` | number | ○ | 性別区分（`0`: 牡 / `1`: 牝 / `2`: セン） |
| `sire` | string | × | 血統(父)（最大20文字） |
| `dam` | string | × | 血統(母)（最大20文字） |
| `bms` | string | × | 血統(母父)（最大20文字） |
| `runningStyleType` | number | ○ | 脚質区分（`0`: 逃げ / `1`: 先行 / `2`: 差し / `3`: 追込） |
| `statusType` | number | ○ | 現役/引退区分（`0`: 現役 / `1`: 引退） |
| `memo` | string | × | メモ |
| `nextRace` | object | × | 次走情報（未定・なしの場合は `null` または省略可能） |
| `nextRace.raceName` | string | × | レース名（最大50文字） |
| `nextRace.bracketNumber` | number | × | 枠順 |
| `nextRace.horseNumber` | number | × | 馬番 |
| `nextRace.weightCarried` | number | × | 斤量（例: `57.0`） |
| `nextRace.jockeyId` | number | × | 騎手ID (`jockey.id`) |

#### リクエスト例
```json
{
  "name": "クロワデュノール",
  "birthDate": "2022-03-21",
  "sexType": 0,
  "sire": "キタサンブラック",
  "dam": "ライジングクロス",
  "bms": "Holy Roman Emperor",
  "runningStyleType": 1,
  "statusType": 0,
  "memo": "期待の2歳馬",
  "nextRace": {
    "raceName": "日本ダービー",
    "bracketNumber": 1,
    "horseNumber": 2,
    "weightCarried": 57.0,
    "jockeyId": 5
  }
}
```
#### レスポンス例（成功時 : 201 Created）
```json
{
  "id": 1,
  "message": "馬情報を登録しました。"
}
```
#### レスポンス例（失敗時 : 400 Bad Request）
```json
{
  "message": "必須項目が不足しているか、入力値の形式が不正です。"
}
```

### 2.4 馬情報更新処理

馬情報編集画面用。対象の馬IDを指定し、馬マスタ（`horse`）および次走情報（`next_race`）の内容を更新します。

* **Method:** `PUT`
* **Path:** `/api/horses/{id}`
* **Content-Type:** `application/json`

#### リクエストパラメータ（Path）

| パラメータ名 | 型 | 必須 | 説明 |
| :--- | :--- | :--- | :--- |
| `id` | number | ○ | 馬ID (`horse.id`) |

#### リクエストパラメータ（Body）

| パラメータ名 | 型 | 必須 | 説明 |
| :--- | :--- | :--- | :--- |
| `name` | string | ○ | 馬名（最大20文字） |
| `birthDate` | string | ○ | 生年月日（形式: `YYYY-MM-DD`） |
| `sexType` | number | ○ | 性別区分（`0`: 牡 / `1`: 牝 / `2`: セン） |
| `sire` | string | × | 血統(父)（最大20文字） |
| `dam` | string | × | 血統(母)（最大20文字） |
| `bms` | string | × | 血統(母父)（最大20文字） |
| `runningStyleType` | number | ○ | 脚質区分（`0`: 逃げ / `1`: 先行 / `2`: 差し / `3`: 追込） |
| `statusType` | number | ○ | 現役/引退区分（`0`: 現役 / `1`: 引退） |
| `memo` | string | × | メモ |
| `nextRace` | object | × | 次走情報（クリア・未定の場合は `null`） |
| `nextRace.raceName` | string | × | レース名（最大50文字） |
| `nextRace.bracketNumber` | number | × | 枠順 |
| `nextRace.horseNumber` | number | × | 馬番 |
| `nextRace.weightCarried` | number | × | 斤量（例: `57.0`） |
| `nextRace.jockeyId` | number | × | 騎手ID (`jockey.id`) |

#### リクエスト例
`PUT /api/horses/1`

```json
{
  "name": "クロワデュノール",
  "birthDate": "2022-03-21",
  "sexType": 0,
  "sire": "キタサンブラック",
  "dam": "ライジングクロス",
  "bms": "Holy Roman Emperor",
  "runningStyleType": 1,
  "statusType": 0,
  "memo": "次走ダービーへ向けて調整中",
  "nextRace": {
    "raceName": "日本ダービー",
    "bracketNumber": 1,
    "horseNumber": 2,
    "weightCarried": 57.0,
    "jockeyId": 5
  }
}
```
#### レスポンス例（成功時 : 200 OK）
```json
{
  "message": "馬情報を更新しました。"
}
```
#### レスポンス例（失敗時 : 404 Not Found）
```json
{
  "message": "対象の馬情報が存在しません。"
}
```

#### レスポンス例（失敗時 : 400 Bad Request）
```json
{
  "message": "馬情報の更新に失敗しました。入力内容を確認してください。"
}
```

### 2.5 馬情報削除処理

馬情報詳細・編集画面用。指定された馬IDに紐づく馬マスタ（`horse`）および関連する全データ（次走情報、レース回顧）を一括で削除します。

* **Method:** `DELETE`
* **Path:** `/api/horses/{id}`
* **Content-Type:** `application/json`

#### リクエストパラメータ（Path）

| パラメータ名 | 型 | 必須 | 説明 |
| :--- | :--- | :--- | :--- |
| `id` | number | ○ | 削除対象の馬ID (`horse.id`) |

#### リクエスト例
`DELETE /api/horses/1`

#### レスポンス例（成功時 : 200 OK）
```json
{
  "message": "馬情報を削除しました。"
}
```

#### レスポンス例（失敗時 : 404 Not Found）
```json
{
  "message": "対象の馬情報が存在しません。"
}
```

## 3. レース回顧関連

### 3.1 レース回顧一覧取得処理

レース回顧検索画面用。指定された馬IDをもとに、過去のレース回顧一覧を**日付の新しい順（降順）**で取得します。

* **Method:** `GET`
* **Path:** `/api/race-reviews`
* **Content-Type:** `application/json`

#### リクエストパラメータ（Query）

| パラメータ名 | 型 | 必須 | 説明 |
| :--- | :--- | :--- | :--- |
| `horseId` | number | × | 馬ID（指定した馬の回顧のみ取得する場合） |
| `keyword` | string | × | 検索キーワード（レース名・メモなどの部分一致） |

#### リクエスト例
`GET /api/race-reviews?horseId=1`

#### レスポンス例（成功時 : 200 OK）
```json
[
  {
    "id": 10,
    "horseId": 1,
    "horseName": "クロワデュノール",
    "raceName": "東京スポーツ杯2歳S",
    "date": "2024-11-16",
    "raceClass": 2,
    "racetrackId": 3,
    "racetrackName": "東京",
    "trackType": 0,
    "distance": 1800,
    "conditionType": 0,
    "cushionValue": 9.6,
    "finishTime": "1:46.8",
    "finishPosition": 1,
    "popularity": 1,
    "headCount": 9,
    "bracketNumber": 8,
    "horseNumber": 9,
    "weightCarried": 56.0,
    "horseWeight": 482.0,
    "cornerPositions": "2-2-2",
    "last3fTime": 33.3,
    "margin": "+0.1",
    "paceType": 0,
    "jockeyId": 5,
    "jockeyName": "北村友一",
    "memo": "好位追走から直線楽に抜け出す強い競馬。",
    "jockeyComment": "手応え十分でした。"
  }
]
```
#### レスポンス例（失敗時 : 400 Bad Request）
```json
{
  "message": "検索条件パラメータの形式が不正です。"
}
```

### 3.2 対象馬全頭のレース回顧一覧と次走レース情報取得処理

全頭診断照会画面用。指定された馬IDをもとに、次走レース情報と過去のレース回顧一覧を**日付の新しい順（降順）**で取得します。

* **Method:** `POST`
* **Path:** `/api/horses/full-field-analysis`
* **Content-Type:** `application/json`

#### リクエストパラメータ（Body）

| パラメータ名 | 型 | 必須 | 説明 |
| :--- | :--- | :--- | :--- |
| `horseIds` | number[] | 〇 | 複数の馬ID |

#### リクエスト例
```json
{
  "horseIds": [1, 5]
}
```

#### レスポンス例（成功時 : 200 OK）
```json
[
  {
    "horseId": 1,
    "horseName": "クロワデュノール",
    "memo":"次走レース本命候補",
    "nextRace": {
      "raceName": "日本ダービー",
      "bracketNumber": 1,
      "horseNumber": 2,
      "weightCarried": 57.0,
      "jockeyId": 5,
      "jockeyName": "北村友一",
    },
    "raceReviews": [
      {
        "id": 10,
        "raceName": "東京スポーツ杯2歳S",
        "date": "2024-11-16",
        "finishPosition": 1,
        "margin": "+0.1",
        "jockeyName": "北村友一",
        "memo": "好位追走から直線楽に抜け出す強い競馬。"
      },
      {
        "id": 5,
        "raceName": "2歳新馬",
        "date": "2024-06-09",
        "finishPosition": 1,
        "margin": "+0.4",
        "jockeyName": "北村友一",
        "memo": "上々の勝ち上がり。"
      }
    ]
  },
  {
    "horseId": 5,
    "horseName": "サトノカルナバ",
    "memo":"次走レース本命候補",
    "nextRace": {
      "raceName": "日本ダービー",
      "bracketNumber": 3,
      "horseNumber": 5,
      "weightCarried": 57.0,
      "jockeyId": 12,
      "jockeyName": "ルメール",
    },
    "raceReviews": [
      {
        "id": 8,
        "raceName": "共同通信杯",
        "date": "2025-02-16",
        "finishPosition": 2,
        "margin": "-0.2",
        "jockeyName": "ルメール",
        "memo": "直線でスムーズさを欠くシーンあり。"
      }
    ]
  }
]
```
#### レスポンス例（失敗時 : 400 Bad Request）
```json
{
  "message": "リクエストボディの形式が不正です。馬IDの指定を確認してください。"
}
```

### 3.3 レース回顧登録処理

レース回顧登録画面用。送信されたデータをもとに、レース回顧テーブル（`race_review`）へ新規データを登録します。

* **Method:** `POST`
* **Path:** `/api/race-reviews`
* **Content-Type:** `application/json`

#### リクエストパラメータ（Body）

| パラメータ名 | 型 | 必須 | 説明 |
| :--- | :--- | :--- | :--- |
| `horseId` | number | ○ | 馬ID (`horse.id`) |
| `raceName` | string | ○ | レース名（最大50文字） |
| `date` | string | ○ | 日付（形式: `YYYY-MM-DD`） |
| `raceClass` | number | ○ | クラス区分（`0`: G1 / `1`: G2 / `2`: G3 / `3`: L / `4`: OP / `5`: 3勝 / `6`: 2勝 / `7`: 1勝 / `8`: 未勝利 / `9`: 新馬） |
| `racetrackId` | number | ○ | 競馬場ID (`racetrack.id`) |
| `trackType` | number | ○ | 馬場種別（`0`: 芝 / `1`: ダート） |
| `distance` | number | ○ | 距離（例: `1800`） |
| `conditionType` | number | ○ | 馬場状態区分（`0`: 良 / `1`: 稍重 / `2`: 重 / `3`: 不良） |
| `cushionValue` | number | × | クッション値（例: `9.6`） |
| `finishTime` | string | × | タイム（最大10文字、例: `"1:46.8"`） |
| `finishPosition` | number | ○ | 着順 |
| `popularity` | number | ○ | 人気 |
| `headCount` | number | ○ | 頭数 |
| `bracketNumber` | number | ○ | 枠順 |
| `horseNumber` | number | ○ | 馬番 |
| `weightCarried` | number | ○ | 斤量（例: `56.0`） |
| `horseWeight` | number | ○ | 馬体重（例: `482.0`） |
| `cornerPositions` | string | ○ | 通過順（最大15文字、例: `"2-2-2"`） |
| `last3fTime` | number | ○ | 上がり3Fタイム（例: `33.3`） |
| `margin` | string | ○ | 着差（最大10文字、例: `"+0.1"`） |
| `paceType` | number | × | ペース区分（`0`: スロー / `1`: ミドル / `2`: ハイ） |
| `jockeyId` | number | × | 騎手ID (`jockey.id`) |
| `memo` | string | × | メモ |
| `jockeyComment` | string | × | 騎手コメント |

#### リクエスト例
```json
{
  "horseId": 1,
  "raceName": "東京スポーツ杯2歳S",
  "date": "2024-11-16",
  "raceClass": 2,
  "racetrackId": 3,
  "trackType": 0,
  "distance": 1800,
  "conditionType": 0,
  "cushionValue": 9.6,
  "finishTime": "1:46.8",
  "finishPosition": 1,
  "popularity": 1,
  "headCount": 9,
  "bracketNumber": 8,
  "horseNumber": 9,
  "weightCarried": 56.0,
  "horseWeight": 482.0,
  "cornerPositions": "2-2-2",
  "last3fTime": 33.3,
  "margin": "+0.1",
  "paceType": 0,
  "jockeyId": 5,
  "memo": "好位追走から直線楽に抜け出す強い競馬。",
  "jockeyComment": "手応え十分でした。"
}
```
#### レスポンス例（成功時 : 201 Created）
```json
{
  "id": 10,
  "message": "レース回顧を登録しました。"
}
```
#### レスポンス例（失敗時 : 400 Bad Request）
```json
{
  "message": "必須項目が不足しているか、入力値の形式が不正です。"
}
```

### 3.4 レース回顧更新処理

レース回顧編集画面用。対象のレース回顧IDを指定し、レース回顧テーブル（`race_review`）の内容を更新します。

* **Method:** `PUT`
* **Path:** `/api/race-reviews/{id}`
* **Content-Type:** `application/json`

#### リクエストパラメータ（Path）

| パラメータ名 | 型 | 必須 | 説明 |
| :--- | :--- | :--- | :--- |
| `id` | number | ○ | レース回顧ID (`race_review.id`) |

#### リクエストパラメータ（Body）

| パラメータ名 | 型 | 必須 | 説明 |
| :--- | :--- | :--- | :--- |
| `raceName` | string | ○ | レース名（最大50文字） |
| `date` | string | ○ | 日付（形式: `YYYY-MM-DD`） |
| `raceClass` | number | ○ | クラス区分（`0`: G1 / `1`: G2 / `2`: G3 / `3`: L / `4`: OP / `5`: 3勝 / `6`: 2勝 / `7`: 1勝 / `8`: 未勝利 / `9`: 新馬） |
| `racetrackId` | number | ○ | 競馬場ID (`racetrack.id`) |
| `trackType` | number | ○ | 馬場種別（`0`: 芝 / `1`: ダート） |
| `distance` | number | ○ | 距離（例: `1800`） |
| `conditionType` | number | ○ | 馬場状態区分（`0`: 良 / `1`: 稍重 / `2`: 重 / `3`: 不良） |
| `cushionValue` | number | × | クッション値（例: `9.6`） |
| `finishTime` | string | × | タイム（最大10文字、例: `"1:46.8"`） |
| `finishPosition` | number | ○ | 着順 |
| `popularity` | number | ○ | 人気 |
| `headCount` | number | ○ | 頭数 |
| `bracketNumber` | number | ○ | 枠順 |
| `horseNumber` | number | ○ | 馬番 |
| `weightCarried` | number | ○ | 斤量（例: `56.0`） |
| `horseWeight` | number | ○ | 馬体重（例: `482.0`） |
| `cornerPositions` | string | ○ | 通過順（最大15文字、例: `"2-2-2"`） |
| `last3fTime` | number | ○ | 上がり3Fタイム（例: `33.3`） |
| `margin` | string | ○ | 着差（最大10文字、例: `"+0.1"`） |
| `paceType` | number | × | ペース区分（`0`: スロー / `1`: ミドル / `2`: ハイ） |
| `jockeyId` | number | × | 騎手ID (`jockey.id`) |
| `memo` | string | × | メモ |
| `jockeyComment` | string | × | 騎手コメント |

#### リクエスト例
`PUT /api/race-reviews/10`

```json
{
  "raceName": "東京スポーツ杯2歳S",
  "date": "2024-11-16",
  "raceClass": 2,
  "racetrackId": 3,
  "trackType": 0,
  "distance": 1800,
  "conditionType": 0,
  "cushionValue": 9.6,
  "finishTime": "1:46.8",
  "finishPosition": 1,
  "popularity": 1,
  "headCount": 9,
  "bracketNumber": 8,
  "horseNumber": 9,
  "weightCarried": 56.0,
  "horseWeight": 482.0,
  "cornerPositions": "2-2-2",
  "last3fTime": 33.3,
  "margin": "+0.1",
  "paceType": 0,
  "jockeyId": 5,
  "memo": "好位追走から直線楽に抜け出す強い競馬。次走も期待。",
  "jockeyComment": "手応え十分でした。"
}
```
#### レスポンス例（成功時 : 200 OK）
```json
{
  "message": "レース回顧を更新しました。"
}
```
#### レスポンス例（失敗時 : 404 Not Found）
```json
{
  "message": "対象のレース回顧が存在しません。"
}
```
#### レスポンス例（失敗時 : 400 Bad Request）
```json
{
  "message": "レース回顧の更新に失敗しました。入力内容を確認してください。"
}
```

### 3.5 レース回顧削除処理

レース回顧詳細・編集画面用。指定されたレース回顧ID（`race_review.id`）をもとに、対象のレース回顧レコードを削除します。

* **Method:** `DELETE`
* **Path:** `/api/race-reviews/{id}`
* **Content-Type:** `application/json`

#### リクエストパラメータ（Path）

| パラメータ名 | 型 | 必須 | 説明 |
| :--- | :--- | :--- | :--- |
| `id` | number | ○ | 削除対象のレース回顧ID (`race_review.id`) |

#### リクエスト例
`DELETE /api/race-reviews/10`

#### レスポンス例（成功時 : 200 OK）
```json
{
  "message": "レース回顧を削除しました。"
}
```
#### レスポンス例（失敗時 : 404 Not Found）
```json
{
  "message": "対象のレース回顧が存在しません。"
}
```

## 4. 競馬場・馬場状態関連

### 4.1 競馬場一覧取得処理

競馬場検索・選択画面用。競馬場マスタ（`racetrack`）に登録されている全競馬場データを取得します。

* **Method:** `GET`
* **Path:** `/api/racetracks`
* **Content-Type:** `application/json`

#### リクエストパラメータ
なし（全件取得）

#### リクエスト例
`GET /api/racetracks`

#### レスポンス例（成功時 : 200 OK）
```json
[
  {
    "id": 1,
    "name": "東京",
    "turnType": 1
  },
  {
    "id": 2,
    "name": "中山",
    "turnType": 0
  },
  {
    "id": 3,
    "name": "新潟",
    "turnType": 2
  }
]
```
#### レスポンス例（失敗時 : 500 Internal Server Error）
```json
{
  "message": "競馬場一覧の取得に失敗しました。"
}
```

### 4.2 競馬場詳細・馬場状態取得処理

競馬場詳細（照会）画面用。指定された競馬場ID（`racetrack.id`）をもとに、競馬場の基本情報および紐づく馬場状態履歴（`track_condition`）の一覧データを取得します。

* **Method:** `GET`
* **Path:** `/api/racetracks/{id}/conditions`
* **Content-Type:** `application/json`

#### リクエストパラメータ（Path）

| パラメータ名 | 型 | 必須 | 説明 |
| :--- | :--- | :--- | :--- |
| `id` | number | ○ | 競馬場ID (`racetrack.id`) |

#### リクエスト例
`GET /api/racetracks/1/conditions`

#### レスポンス例（成功時 : 200 OK）
```json
{
  "id": 1,
  "name": "東京",
  "turnType": 1,
  "trackConditions": [
    {
      "id": 101,
      "trackType": 0,
      "date": "2026-05-31",
      "conditionType": 0,
      "cushionValue": 9.8,
      "trackBias": "内・前有利",
      "memo": "Cコース使用初日。絶好の馬場状態。"
    },
    {
      "id": 102,
      "trackType": 1,
      "date": "2026-05-31",
      "conditionType": 0,
      "cushionValue": null,
      "trackBias": "フラット",
      "memo": "乾燥気味でやや時計がかかる。"
    }
  ]
}
```
#### レスポンス例（失敗時 : 404 Not Found）
```json
{
  "message": "指定された競馬場情報が存在しません。"
}
```

### 4.3 馬場状態更新・登録処理

馬場状態編集画面用。指定された競馬場ID（`racetrack.id`）に対し、馬場状態データ（`track_condition`）の更新または新規追加を行います。

* **Method:** `PUT`
* **Path:** `/api/racetracks/{id}/conditions`
* **Content-Type:** `application/json`

#### リクエストパラメータ（Path）

| パラメータ名 | 型 | 必須 | 説明 |
| :--- | :--- | :--- | :--- |
| `id` | number | ○ | 競馬場ID (`racetrack.id`) |

#### リクエストパラメータ（Body）

| パラメータ名 | 型 | 必須 | 説明 |
| :--- | :--- | :--- | :--- |
| `trackType` | number | ○ | 馬場種別（`0`: 芝 / `1`: ダート） |
| `date` | string | ○ | 日付（形式: `YYYY-MM-DD`） |
| `conditionType` | number | ○ | 馬場状態区分（`0`: 良 / `1`: 稍重 / `2`: 重 / `3`: 不良） |
| `cushionValue` | number | × | クッション値（例: `9.8`） |
| `trackBias` | string | × | トラックバイアス（最大20文字、例: `"内・前有利"`） |
| `memo` | string | × | メモ |

#### リクエスト例
`PUT /api/racetracks/1/conditions`

```json
{
  "trackType": 0,
  "date": "2026-08-09",
  "conditionType": 0,
  "cushionValue": 9.8,
  "trackBias": "内・前有利",
  "memo": "開幕週でインコースが良好。高速馬場。"
}
```
#### レスポンス例（成功時 : 200 OK）
```json
{
  "message": "馬場状態を更新しました。"
}
```
#### レスポンス例（失敗時 : 404 Not Found）
```json
{
  "message": "対象の競馬場が存在しません。"
}
```
#### レスポンス例（失敗時 : 400 Bad Request）
```json
{
  "message": "馬場状態の更新に失敗しました。入力内容を確認してください。"
}
```

## 5. マスタ・共通データ関連

### 5.1 騎手一覧取得処理（ドロップダウン用）

馬情報の次走予定入力や、レース回顧の登録・編集画面における「騎手選択ドロップダウン」用。騎手マスタ（`jockey`）に登録されている全騎手データを軽量な形式で取得します。

* **Method:** `GET`
* **Path:** `/api/jockeys`
* **Content-Type:** `application/json`

#### リクエストパラメータ
なし（全件取得）

#### リクエスト例
`GET /api/jockeys`

#### レスポンス例（成功時 : 200 OK）
```json
[
  {
    "id": 1,
    "jockeyName": "ルメール"
  },
  {
    "id": 2,
    "jockeyName": "川田将雅"
  },
  {
    "id": 5,
    "jockeyName": "北村友一"
  }
]
```
#### レスポンス例（失敗時 : 500 Internal Server Error）
```json
{
  "message": "騎手一覧の取得に失敗しました。"
}
```
