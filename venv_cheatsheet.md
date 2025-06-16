# Python仮想環境（venv）チートシート

## 1. 仮想環境の基本概念
- 仮想環境とは：プロジェクトごとに独立したPython環境を作成する仕組み
- メリット：
  - プロジェクトごとに異なるバージョンのパッケージを使用可能
  - システムのPython環境を汚さない
  - 依存関係の競合を防ぐ

## 2. 基本的なコマンド

### 仮想環境の作成
```bash
# プロジェクトディレクトリで実行
python -m venv venv
```

### 仮想環境の有効化
```bash
# Windowsの場合
.\venv\Scripts\activate

# Linux/Macの場合
source venv/bin/activate
```

### 仮想環境の無効化
```bash
deactivate
```

## 3. パッケージ管理

### パッケージのインストール
```bash
# 個別のパッケージをインストール
pip install パッケージ名

# requirements.txtから一括インストール
pip install -r requirements.txt
```

### パッケージの確認
```bash
# インストール済みパッケージの一覧表示
pip list

# 特定のパッケージの情報確認
pip show パッケージ名
```

### パッケージのアンインストール
```bash
pip uninstall パッケージ名
```

## 4. よくある操作手順

### 新規プロジェクトの開始
1. プロジェクトディレクトリの作成
2. 仮想環境の作成
3. 仮想環境の有効化
4. 必要なパッケージのインストール

### 既存プロジェクトの開始
1. プロジェクトディレクトリに移動
2. 仮想環境の有効化
3. 必要なパッケージのインストール（初回のみ）

## 5. トラブルシューティング

### 仮想環境が認識されない場合
- パスが正しいか確認
- 仮想環境が正しく作成されているか確認
- コマンドプロンプトを再起動

### パッケージのインストールエラー
- インターネット接続を確認
- pipをアップグレード：`python -m pip install --upgrade pip`
- 仮想環境が有効になっているか確認

## 6. 便利なコマンド

### 現在のPythonバージョン確認
```bash
python --version
```

### pipのバージョン確認
```bash
pip --version
```

### 仮想環境の場所確認
```bash
# Windowsの場合
where python

# Linux/Macの場合
which python
```

## 7. 注意事項
- 仮想環境のフォルダ（venv）はGitにコミットしない
- requirements.txtは必ずGitにコミットする
- プロジェクトを共有する際は、requirements.txtを更新する 