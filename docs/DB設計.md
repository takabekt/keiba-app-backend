# DB定義書 (PostgreSQL / Neon)

## 1. ユーザーテーブル (`app_user`)
| 論理名 | 物理名 | 型 | 制約 | 説明・補足 |
| :--- | :--- | :--- | :--- | :--- |
| **ID** | `id` | BIGINT GENERATED ALWAYS AS IDENTITY | PRIMARY KEY | 自動採番 |
| **コード** | `code` | VARCHAR(10) | NOT NULL, UNIQUE | |
| **パスワード** | `password` | VARCHAR(255) | NOT NULL | ハッシュ化して保存 |
| **名前** | `name` | VARCHAR(20) | NOT NULL | |
| **登録日時** | `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | |
| **更新日時** | `updated_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | |

---

## 2. 馬マスタテーブル (`horse`)
| 論理名 | 物理名 | 型 | 制約 | 説明・補足 |
| :--- | :--- | :--- | :--- | :--- |
| **ID** | `id` | BIGINT GENERATED ALWAYS AS IDENTITY | PRIMARY KEY | 自動採番 |
| **名前** | `name` | VARCHAR(20) | NOT NULL | |
| **生年月日** | `birth_date` | DATE | NOT NULL | |
| **性別区分** | `sex_type` | INT2 | NOT NULL | `0`: 牡 / `1`: 牝 / `2`: セン馬 |
| **血統(父)** | `sire` | VARCHAR(20) | | |
| **血統(母)** | `dam` | VARCHAR(20) | | |
| **血統(母父)** | `bms` | VARCHAR(20) | | |
| **脚質区分** | `running_style_type` | INT2 | NOT NULL | `0`: 逃げ / `1`: 先行 / `2`: 差し / `3`: 追込 |
| **現役/引退区分** | `status_type` | INT2 | NOT NULL | `0`: 現役 / `1`: 引退 |
| **メモ** | `memo` | TEXT | | |
| **登録日時** | `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | |
| **更新日時** | `updated_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | |

---

## 3. 競馬場マスタ (`racetrack`)
| 論理名 | 物理名 | 型 | 制約 | 説明・補足 |
| :--- | :--- | :--- | :--- | :--- |
| **ID** | `id` | BIGINT GENERATED ALWAYS AS IDENTITY | PRIMARY KEY | 自動採番 |
| **競馬場名** | `name` | VARCHAR(20) | NOT NULL | |
| **方向区分** | `turn_type` | INT2 | NOT NULL | `0`: 右 / `1`: 左 / `2`: 直線 |
| **登録日時** | `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | |
| **更新日時** | `updated_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | |

---

## 4. 騎手マスタ (`jockey`)
| 論理名 | 物理名 | 型 | 制約 | 説明・補足 |
| :--- | :--- | :--- | :--- | :--- |
| **ID** | `id` | BIGINT GENERATED ALWAYS AS IDENTITY | PRIMARY KEY | 自動採番 |
| **騎手名** | `jockey_name` | VARCHAR(20) | NOT NULL | |
| **登録日時** | `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | |
| **更新日時** | `updated_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | |

---

## 5. 次走情報テーブル (`next_race`)
| 論理名 | 物理名 | 型 | 制約 | 説明・補足 |
| :--- | :--- | :--- | :--- | :--- |
| **ID** | `id` | BIGINT GENERATED ALWAYS AS IDENTITY | PRIMARY KEY | 自動採番 |
| **馬ID** | `horse_id` | BIGINT | NOT NULL, FOREIGN KEY (`horse.id`) | |
| **レース名** | `race_name` | VARCHAR(50) | | |
| **枠順** | `bracket_number` | INT2 | | |
| **馬番** | `horse_number` | INT2 | | |
| **斤量** | `weight_carried` | NUMERIC(3,1) | | |
| **騎手ID** | `jockey_id` | BIGINT | FOREIGN KEY (`jockey.id`) |  |
| **登録日時** | `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | |
| **更新日時** | `updated_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | |

---

## 6. レース回顧テーブル (`race_review`)
| 論理名 | 物理名 | 型 | 制約 | 説明・補足 |
| :--- | :--- | :--- | :--- | :--- |
| **ID** | `id` | BIGINT GENERATED ALWAYS AS IDENTITY | PRIMARY KEY | 自動採番 |
| **馬ID** | `horse_id` | BIGINT | NOT NULL, FOREIGN KEY (`horse.id`) | |
| **レース名** | `race_name` | VARCHAR(50) | NOT NULL | |
| **日付** | `date` | DATE | NOT NULL | |
| **クラス区分** | `race_class` | INT2 | NOT NULL | `0`: G1 / `1`: G2 / `2`: G3 / `3`: L (リステッド) / `4`: OP / `5`: 3勝クラス / `6`: 2勝クラス / `7`: 1勝クラス / `8`: 未勝利 / `9`: 新馬 |
| **競馬場ID** | `racetrack_id` | BIGINT | NOT NULL, FOREIGN KEY (`racetrack.id`) | |
| **馬場種別** | `track_type` | INT2 | NOT NULL | `0`: 芝 / `1`: ダート |
| **距離** | `distance` | INT4 | NOT NULL | 例: 1600 (m) |
| **馬場状態区分** | `condition_type` | INT2 | NOT NULL | `0`: 良 / `1`: 稍重 / `2`: 重 / `3`: 不良 |
| **クッション値** | `cushion_value` | NUMERIC(3,1) | | |
| **タイム** | `finish_time` | VARCHAR(10) | | |
| **着順** | `finish_position` | INT2 | NOT NULL | |
| **人気** | `popularity` | INT2 | NOT NULL | |
| **頭数** | `head_count` | INT2 | NOT NULL | |
| **枠順** | `bracket_number` | INT2 | NOT NULL | |
| **馬番** | `horse_number` | INT2 | NOT NULL | |
| **斤量** | `weight_carried` | NUMERIC(3,1) | NOT NULL | |
| **馬体重** | `horse_weight` | NUMERIC(4,1) | NOT NULL | |
| **通過順** | `corner_positions` | VARCHAR(15) | NOT NULL | |
| **上がり** | `last_3f_time` | NUMERIC(3,1) | NOT NULL | |
| **着差** | `margin` | VARCHAR(10) | NOT NULL | |
| **ペース** | `pace_type` | INT2 | | `0`: スロー / `1`: ミドル / `2`: ハイ |
| **騎手ID** | `jockey_id` | BIGINT | FOREIGN KEY (`jockey.id`) | |
| **メモ** | `memo` | TEXT | | |
| **騎手コメント** | `jockey_comment` | TEXT | | |
| **登録日時** | `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | |
| **更新日時** | `updated_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | |

---

## 7. 競馬場状態テーブル (`track_condition`)
| 論理名 | 物理名 | 型 | 制約 | 説明・補足 |
| :--- | :--- | :--- | :--- | :--- |
| **ID** | `id` | BIGINT GENERATED ALWAYS AS IDENTITY | PRIMARY KEY | 自動採番 |
| **競馬場ID** | `racetrack_id` | BIGINT | NOT NULL, FOREIGN KEY (`racetrack.id`) | |
| **馬場種別** | `track_type` | INT2 | NOT NULL | `0`: 芝 / `1`: ダート |
| **日付** | `date` | DATE | NOT NULL | |
| **馬場状態区分** | `condition_type` | INT2 | NOT NULL | `0`: 良 / `1`: 稍重 / `2`: 重 / `3`: 不良 |
| **クッション値** | `cushion_value` | NUMERIC(3,1) | | |
| **トラックバイアス** | `track_bias` | VARCHAR(20) | | |
| **メモ** | `memo` | TEXT | | |
| **登録日時** | `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | |
| **更新日時** | `updated_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | |

## 8. インデックス定義

取得クエリの最適化および外部キー（JOIN）処理の高速化のため、以下のインデックスを作成する。

| 対象テーブル | インデックス名 | 対象カラム | 目的・用途 |
| :--- | :--- | :--- | :--- |
| `race_review` | `idx_race_review_horse_date` | `horse_id`, `date DESC` | 対象馬のレース回顧を日付の新しい順で取得するため |
| `next_race` | `idx_next_race_horse` | `horse_id` | 対象馬の次走予定データを高速取得するため |
| `track_condition` | `idx_track_condition_racetrack_date` | `racetrack_id`, `date` | 対象競馬場の指定日（今週）の馬場状態を高速取得するため |
| `horse` | `idx_horse_name` | `name` | 馬名での絞り込み検索・50音順ソートの高速化のため |
| `next_race` | `idx_next_race_race_name` | `race_name` | 次走レース名での絞り込み検索の高速化のため |

## 9. ER図

```mermaid
erDiagram
    app_user {
        BIGINT id PK "ID"
        VARCHAR code "ログインコード"
        VARCHAR password "パスワード"
        VARCHAR name "名前"
        TIMESTAMP created_at "登録日時"
        TIMESTAMP updated_at "更新日時"
    }

    horse {
        BIGINT id PK "ID"
        VARCHAR name "馬名"
        DATE birth_date "生年月日"
        INT2 sex_type "性別区分"
        VARCHAR sire "父"
        VARCHAR dam "母"
        VARCHAR bms "母父"
        INT2 running_style_type "脚質区分"
        INT2 status_type "現役/引退区分"
        TEXT memo "メモ"
        TIMESTAMP created_at "登録日時"
        TIMESTAMP updated_at "更新日時"
    }

    jockey {
        BIGINT id PK "ID"
        VARCHAR name "騎手名"
        TIMESTAMP created_at "登録日時"
        TIMESTAMP updated_at "更新日時"
    }

    racetrack {
        BIGINT id PK "ID"
        VARCHAR name "競馬場名"
        INT2 turn_type "方向区分"
        TIMESTAMP created_at "登録日時"
        TIMESTAMP updated_at "更新日時"
    }

    next_race {
        BIGINT id PK "ID"
        BIGINT horse_id FK "馬ID"
        VARCHAR race_name "レース名"
        INT2 bracket_number "枠順"
        INT2 horse_number "馬番"
        NUMERIC weight_carried "斤量"
        BIGINT jockey_id FK "騎手ID"
        TIMESTAMP created_at "登録日時"
        TIMESTAMP updated_at "更新日時"
    }

    track_condition {
        BIGINT id PK "ID"
        BIGINT racetrack_id FK "競馬場ID"
        INT2 track_type "馬場種別"
        DATE date "日付"
        INT2 condition_type "馬場状態区分"
        NUMERIC cushion_value "クッション値"
        VARCHAR track_bias "トラックバイアス"
        TEXT memo "メモ"
        TIMESTAMP created_at "登録日時"
        TIMESTAMP updated_at "更新日時"
    }

    race_review {
        BIGINT id PK "ID"
        BIGINT horse_id FK "馬ID"
        VARCHAR race_name "レース名"
        DATE date "日付"
        INT2 race_class "クラス区分"
        BIGINT racetrack_id FK "競馬場ID"
        INT2 track_type "馬場種別"
        INT4 distance "距離"
        INT2 condition_type "馬場状態区分"
        NUMERIC cushion_value "クッション値"
        VARCHAR finish_time "タイム"
        INT2 finish_position "着順"
        INT2 popularity "人気"
        INT2 head_count "頭数"
        INT2 bracket_number "枠順"
        INT2 horse_number "馬番"
        NUMERIC weight_carried "斤量"
        NUMERIC horse_weight "馬体重"
        VARCHAR corner_positions "通過順"
        NUMERIC last_3f_time "上がり"
        VARCHAR margin "着差"
        INT2 pace_type "ペース"
        BIGINT jockey_id FK "騎手ID"
        TEXT memo "メモ"
        TEXT jockey_comment "騎手コメント"
        TIMESTAMP created_at "登録日時"
        TIMESTAMP updated_at "更新日時"
    }

    horse ||--o| next_race : "1頭につき1つの次走予定"
    horse ||--o{ race_review : "1頭につき複数の回顧メモ"
    jockey ||--o{ next_race : "予定騎手として紐付け"
    jockey ||--o{ race_review : "騎乗実績として紐付け"
    racetrack ||--o{ race_review : "開催場所"
    racetrack ||--o{ track_condition : "日付・種別ごとの馬場状態"