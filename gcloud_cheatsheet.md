# gcloud (Google Cloud SDK) コマンド チートシート

このファイルは、GCPの操作でよく使う`gcloud`コマンドをまとめたものです。

> **【重要】**
> コマンド例の中にある `[PROJECT_ID]` や `[INSTANCE_NAME]` のような角括弧 `[]` は、**「ここにあなたの情報を入力してください」** という意味のプレースホルダーです。
> 実際のコマンドでは、**角括弧は入力せず**、あなたのプロジェクトIDやインスタンス名に置き換えてください。

---

## 1. 初期設定 & 認証

### `gcloud init`
**目的**: `gcloud`の初期設定を行います。プロジェクトやアカウント、デフォルトリージョンなどを対話形式で設定できます。
```bash
gcloud init
```

### `gcloud auth login`
**目的**: Googleアカウントで認証し、`gcloud`がGCPリソースにアクセスする権限を与えます。
```bash
gcloud auth login
```

### `gcloud config list`
**目的**: 現在の設定（プロジェクト、アカウント、リージョンなど）の一覧を表示します。
```bash
gcloud config list
```

### `gcloud config set`
**目的**: 特定の設定項目（プロジェクト、リージョン、ゾーン）を永続的に変更します。
```bash
# プロジェクトを設定
gcloud config set project [PROJECT_ID]

# リージョンを設定
gcloud config set compute/region [REGION]

# ゾーンを設定
gcloud config set compute/zone [ZONE]
```

---

## 2. VMインスタンスの管理

### `gcloud compute instances list`
**目的**: プロジェクト内のすべてのVMインスタンスの一覧を表示します。
```bash
gcloud compute instances list
```

### `gcloud compute instances start / stop`
**目的**: VMインスタンスを起動または停止します。
```bash
# 起動
gcloud compute instances start [INSTANCE_NAME] --zone [ZONE]

# 停止
gcloud compute instances stop [INSTANCE_NAME] --zone [ZONE]
```

### `gcloud compute instances describe`
**目的**: VMインスタンスの詳細情報（IPアドレス、マシンタイプなど）を表示します。
```bash
gcloud compute instances describe [INSTANCE_NAME] --zone [ZONE]
```

---

## 3. SSH接続 & ファイル転送

### `gcloud compute ssh`
**目的**: VMインスタンスにSSHで接続します。
```bash
gcloud compute ssh [INSTANCE_NAME] --zone [ZONE]
```

### `gcloud compute scp`
**目的**: ローカルPCとVMインスタンス間でファイルを安全にコピーします。
```bash
# ローカル → VM
gcloud compute scp [LOCAL_FILE_PATH] [INSTANCE_NAME]:~/[REMOTE_FILE_NAME] --zone [ZONE]

# VM → ローカル
gcloud compute scp [INSTANCE_NAME]:~/[REMOTE_FILE_NAME] [LOCAL_FILE_PATH] --zone [ZONE]
```
> `~` はVMのホームディレクトリを意味します。

### gcloud compute scp blockchain.py bc1:/home/kannd/blockchain/ 
### --zone=us-central1-c
### gcloud compute scp fast_api.py bc1:/home/kannd/blockchain/ 
### --zone=us-central1-c
### gcloud compute scp requirements.txt bc1:/home/kannd/blockchain/ 
### --zone=us-central1-c
### gcloud compute scp transaction.py bc1:/home/kannd/blockchain/ 
### --zone=us-central1-c
### gcloud compute scp signature.py bc1:/home/kannd/blockchain/ --zone=us-central1-c
---

## プロジェクトファイルはblockchain

## 4. ファイアウォールルール

### `gcloud compute firewall-rules list`
**目的**: プロジェクト内のファイアウォールルールを一覧表示します。
```bash
gcloud compute firewall-rules list
```

### `gcloud compute firewall-rules create`
**目的**: 新しいファイアウォールルールを作成します。
```bash
# 例: ポート8000へのTCPアクセスを全IPアドレスから許可
gcloud compute firewall-rules create allow-port-8000 \
    --allow tcp:8000 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=http-server
```

---

## おまけ

### 特定のVMのIPアドレスだけを取得
```bash
gcloud compute instances describe [INSTANCE_NAME] --format='get(networkInterfaces[0].accessConfigs[0].natIP)' --zone [ZONE]
``` 