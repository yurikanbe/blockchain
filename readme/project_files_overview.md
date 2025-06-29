# ブロックチェーンプロジェクト - ファイル機能概要

## 目次
1. [コアファイル](#コアファイル)
2. [トランザクション関連](#トランザクション関連)
3. [テスト・デモファイル](#テストデモファイル)
4. [設定・ドキュメント](#設定ドキュメント)
5. [データファイル](#データファイル)

---

## コアファイル

### blockchain.py
**機能**: ブロックチェーンの基本機能を実装するメインクラス
- `Blockchain`クラスでブロックチェーンロジックを定義
- Proof of Work（PoW）アルゴリズム実装（難易度: 10）
- トランザクション検証・ブロック作成・チェーン検証機能
- データの永続化（pickle形式）

**予測実行結果**: 
- 直接実行不可（クラス定義のみ）
- 他のスクリプトから`import blockchain`でインポートして使用

### main.py
**機能**: FastAPI RESTサーバーのメインエンドポイント
- `/transaction_pool` (GET/POST): トランザクションプール管理
- `/chain` (GET/POST): ブロックチェーン管理
- ポート8000でHTTPサーバー起動

**予測実行結果**:
```bash
python main.py
# → FastAPIサーバーが起動（http://127.0.0.1:8000）
# → APIエンドポイントが利用可能になる
```

### mining.py
**機能**: マイニング（ブロック生成）プロセス
- トランザクションプールから未処理トランザクションを取得
- Proof of Workを実行して新しいブロックを生成
- 生成したブロックをネットワークに送信

**予測実行結果**:
```bash
python mining.py
# → 新しいブロックが生成される
# → ブロックチェーンの長さが1増加
# → マイナー報酬（256コイン）が付与される
# → "Chain is posted." または "Received chain is ignored." メッセージが表示
```

---

## トランザクション関連

### post_transaction.py
**機能**: デジタル署名付きトランザクションの作成・送信
- ECDSA秘密鍵で署名されたトランザクション生成
- FastAPIサーバーのトランザクションプールへ送信
- 署名済みトランザクションをpickleファイルに保存

**予測実行結果**:
```bash
python post_transaction.py
# → {"message": "Transaction is posted."} 
# または {"message": "Transaction verification failed."}
# → signed_transaction.pkl ファイルが生成される
```

### sign_transaction.py
**機能**: トランザクションのデジタル署名作成
- 指定された秘密鍵でトランザクションに署名
- 署名済みトランザクションをpickleファイルに保存

**予測実行結果**:
```bash
python sign_transaction.py
# → 署名済みトランザクションがsigned_transaction.pklに保存される
# → 実行時にエラーは表示されない（正常終了）
```

### verify_transaction.py
**機能**: トランザクション署名の検証
- pickleファイルから署名済みトランザクションを読み込み
- ECDSA公開鍵で署名を検証

**予測実行結果**:
```bash
python verify_transaction.py
# → 現在は不完全（実装途中）
# → signed_transaction.pklファイルが必要
```

### transaction.py
**機能**: 基本的なトランザクション構造のデモ
- 署名なしの簡単なトランザクションデータ作成
- JSONフォーマットでのトランザクション表示

**予測実行結果**:
```bash
python transaction.py
# → 2つのサンプルトランザクションが配列形式で表示される
# → 各トランザクションにtime, sender, receiver, amountが含まれる
```

---

## テスト・デモファイル

### signature.py
**機能**: ECDSA署名システムのデモンストレーション
- 新しい秘密鍵・公開鍵ペアの生成
- テキストへの署名と検証のデモ

**予測実行結果**:
```bash
python signature.py
# → 秘密鍵: [64文字の16進数文字列]
# → 公開鍵: [128文字の16進数文字列]  
# → 署名: [署名の16進数文字列]
# → "署名は正しいですこれは送信したい文字です"
```

### hash_test.py
**機能**: SHA256ハッシュ関数のテスト
- 異なる入力に対するハッシュ値の計算と比較

**予測実行結果**:
```bash
python hash_test.py
# → "こんにちは"のハッシュ値
# → "こんちは"のハッシュ値
# → 2つの異なるハッシュ値が表示される
```

### fast_api.py
**機能**: FastAPIの基本動作テスト
- シンプルなHTTPサーバーの起動テスト

**予測実行結果**:
```bash
python fast_api.py
# → HTTPサーバーが0.0.0.0:8000で起動
# → GET / → "hello" レスポンス
```

---

## ネットワーク関連

### get_transactions.py
**機能**: リモートサーバーからトランザクションプールを取得
- 外部サーバー（130.211.213.169:5000）からデータ取得

**予測実行結果**:
```bash
python get_transactions.py
# → リモートサーバーのトランザクション一覧が表示される
# → ネットワークエラーの場合は例外が発生
```

### reuse_transactions.py
**機能**: 既存トランザクションの再利用・転送
- リモートサーバーからトランザクションを取得
- 最初のトランザクションを同じサーバーに再送信

**予測実行結果**:
```bash
python reuse_transactions.py
# → 既存トランザクションの再送信結果が表示される
# → サーバーからのレスポンスメッセージが出力される
```

---

## 設定・ドキュメント

### requirements.txt
**機能**: Pythonパッケージ依存関係の定義
- 必要なライブラリとバージョン指定

### readme/内のマークダウンファイル
- **gcloud_cheatsheet.md**: Google Cloud関連コマンド集
- **nft_app_specification.md**: NFTアプリの仕様書
- **aws_cost_estimation.md**: AWSコスト見積もり
- **venv_cheatsheet.md**: Python仮想環境の使い方
- **gcp_setup_notes.md**: Google Cloud Platform設定メモ

---

## データファイル

### blockchain_data.pkl
**機能**: ブロックチェーンデータの永続化
- チェーン全体の状態保存
- mining.py実行時に自動生成・更新

### transaction_data.pkl
**機能**: トランザクションプールの永続化
- 未処理トランザクションの保存
- APIサーバー再起動時のデータ復元用

### signed_transaction.pkl
**機能**: 署名済みトランザクションの一時保存
- post_transaction.py, sign_transaction.py実行時に生成
- verify_transaction.pyで検証に使用

---

## 実行順序の推奨パターン

### 基本的なブロックチェーン操作:
1. `python main.py` - APIサーバー起動
2. `python post_transaction.py` - トランザクション送信
3. `python mining.py` - ブロック生成
4. 手動でAPIエンドポイント確認 (`/chain`, `/transaction_pool`)

### 署名・検証テスト:
1. `python signature.py` - 新しいキーペア生成
2. `python sign_transaction.py` - トランザクション署名
3. `python verify_transaction.py` - 署名検証

### ネットワーク操作:
1. `python get_transactions.py` - リモートデータ取得
2. `python reuse_transactions.py` - トランザクション転送

---

## 注意事項

- **ネットワーク**: 外部サーバー（130.211.213.169:5000）への接続が必要なファイルあり
- **依存関係**: main.py実行前にrequirements.txtのパッケージインストール必要
- **ポート**: main.pyとfast_api.pyが同じポート8000を使用（同時実行不可）
- **データ整合性**: pickleファイルは実行順序に依存する場合あり

---

*最終更新: 各ファイルの機能確認完了* 