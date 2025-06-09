# GCPセットアップ手順

## 現在のシステム状況まとめ

### 構成イメージ

```
[あなたのPC]  ---X--->  [GCP VM:8000]  ←（内部でFastAPIが動作中）
         ↑
   （ファイアウォールでブロック）

[VM内で]  curl http://127.0.0.1:8000  ← これはOK
```

### 状況の説明
- GCP（Google Cloud Platform）上に「VM（仮想マシン）」を作成し、Linuxサーバーとして利用中。
- VMの中でFastAPIサーバー（Python）がポート8000で起動している。
- GCPのファイアウォール設定により、外部（インターネット）からポート8000へのアクセスは遮断されている。
- そのため、**あなたのPCやスマホなど外部からはFastAPIサーバーにアクセスできない**。
- VM内であれば、`localhost:8000`や`127.0.0.1:8000`でFastAPIサーバーにアクセスできる。

### できること
- VM内でFastAPIサーバーにアクセスする
- VM内でPythonスクリプトを実行する
- SSHでVMに接続して操作する

### できないこと
- あなたのPCやスマホから直接FastAPIサーバーにアクセスする（ファイアウォールでブロックされているため）

---

# 以下、これまでのセットアップ手順

## 1. 初期設定
- Google Cloud SDKをインストール
- プロジェクト選択: `bc1-project`
- リージョン設定: `asia-northeast1-b`

## 2. VMインスタンス情報
```
NAME: bc1
ZONE: us-central1-c
MACHINE_TYPE: e2-micro
INTERNAL_IP: 10.128.0.2
EXTERNAL_IP: 34.59.180.248
STATUS: RUNNING
```

## 3. ファイル転送
### ローカルからVMへのファイル転送
```bash
# Google Cloud SDK Shellを使用
cd C:\blockchain
gcloud compute scp signed_transaction.pkl bc1:/home/n6321/ --zone=us-central1-c
gcloud compute scp fast_api.py bc1:/home/n6321/ --zone=us-central1-c
```

## 4. Python環境セットアップ
### 必要なパッケージのインストール
```bash
sudo apt install python3-venv python3-full -y
```

### 仮想環境の作成と有効化
```bash
python3 -m venv ~/fastapi_env
source ~/fastapi_env/bin/activate
```

### FastAPIのインストール
```bash
pip install fastapi uvicorn
```

## 5. FastAPIサーバーの起動
```bash
python3 fast_api.py
```
- サーバー起動ポート: 8000
- アクセスURL: http://34.59.180.248:8000

## 6. ファイアウォール設定
### 設定の必要性
GCPのVMインスタンスは、デフォルトでセキュリティのために外部からのアクセスを制限しています。FastAPIサーバーを外部から利用可能にするためには、明示的にファイアウォールルールを設定する必要があります。

### ファイアウォール設定の意図
1. **アクセス制御**
   - 特定のポート(8000)のみを開放
   - 必要最小限のアクセス許可による安全性の確保
   - 不要なポートは閉じたままでセキュリティを維持

2. **ネットワークセキュリティ**
   - インバウンドトラフィック（外部→VM）の制御
   - 許可するIPアドレス範囲の指定が可能
   - タグベースの制御により柔軟な設定が可能

### 設定コマンド
```bash
# ファイアウォールルール作成
gcloud compute firewall-rules create allow-fastapi --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:8000 --source-ranges=0.0.0.0/0 --target-tags=http-server

# VMインスタンスにタグを追加
gcloud compute instances add-tags bc1 --tags=http-server --zone=us-central1-c
```

### 設定の詳細説明
- `--direction=INGRESS`: 外部からVMへのアクセスを制御
- `--priority=1000`: ルールの優先順位（低い数字が優先）
- `--rules=tcp:8000`: FastAPIが使用するポート8000のみを開放
- `--source-ranges=0.0.0.0/0`: すべてのIPアドレスからのアクセスを許可
- `--target-tags=http-server`: このタグが付いたVMインスタンスにのみルールを適用

## 注意点
- VMインスタンスへのSSH接続は `gcloud compute ssh bc1 --zone=us-central1-c` で可能
- 仮想環境を使用することで、システムの Python 環境を汚さずにパッケージをインストール可能
- 本番環境では、`source-ranges`をより制限的に設定することを推奨

## 次のステップ
1. ファイアウォール設定の完了
2. FastAPIエンドポイントのテスト
3. 本番環境用の設定（セキュリティ、パフォーマンスチューニング等）
4. アクセスログのモニタリング設定
5. バックアップ戦略の検討 