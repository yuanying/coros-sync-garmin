# COROS sync Garmin

このレポジトリは、COROSのアクティビティデータをGarminに同期するためのものです。

## 使い方

```bash
git clone https://github.com/yuanying/coros-sync-garmin
cd coros-sync-garmin
python -m coros_sync_garmin
```

設定する環境変数:

- `GARMIN_EMAIL`: Garmin Connectのメールアドレス
- `GARMIN_PASSWORD`: Garmin Connectのパスワード
- `COROS_EMAIL`: COROSのメールアドレス
- `COROS_PASSWORD`: COROSのパスワード

## ディレクトリ構造

- `coros_sync_garmin/`: ライブラリのソースコード
- `test/`: テストコード
- `README.md`: このドキュメント
