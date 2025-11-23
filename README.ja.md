# ＭＣＰサーバー

このプロジェクトは、チーム内で自由に MCP(Model Context Protocol)サーバーに関数を追加できるデモプロジェクトです。

## プロジェクト構成

```
mcp/
├── README.md
├── README.ja.md          # このファイル
├── template.yaml         # AWS SAM デプロイ設定
├── samconfig.toml
└── src/
    ├── requirements.txt
    ├── run.sh
    └── app/
        ├── __main__.py
        ├── main.py       # MCPサーバーのメインファイル
        └── tools/        # ツール関数を格納するディレクトリ
            ├── __init__.py
            ├── math_tools.py
            └── weather_forecast.py
```

## 新しい関数の追加方法

### ステップ 1: 新しいツールファイルを作成

`src/app/tools/` ディレクトリ内に新しい Python ファイルを作成します。

例: `src/app/tools/my_new_tool.py`

```python
"""
新しいツールの説明
"""
from app.main import mcp


@mcp.tool()
def my_function(param1: str, param2: int) -> str:
    """
    この関数の説明をここに記述します。
    AIがこの関数を使用する際の参考情報になります。

    Args:
        param1: パラメータ1の説明
        param2: パラメータ2の説明

    Returns:
        戻り値の説明
    """
    # 関数の実装
    result = f"{param1}を{param2}回処理しました"
    return result
```

### ステップ 2: 自動読み込みの仕組み

**重要**: 新しいファイルを `src/app/tools/` ディレクトリに配置するだけで、自動的に読み込まれます。

`main.py` が自動的に `tools/` ディレクトリ内のすべてのモジュールを読み込むため、追加の設定は不要です。

### ステップ 3: デコレータの使用

関数を MCP サーバーのツールとして登録するには、`@mcp.tool()` デコレータを使用します。

```python
@mcp.tool()
def your_function_name(arg1: type1, arg2: type2) -> return_type:
    """
    関数の説明（必須）
    """
    # 実装
    return result
```

## 実装例

### 例 1: 数学計算ツール (`math_tools.py`)

```python
from app.main import mcp

@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Add two integers.
    """
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """
    Multiply two integers.
    """
    return a * b
```

### 例 2: 天気予報ツール (`weather_forecast.py`)

```python
from app.main import mcp

@mcp.tool()
def get_weather_forecast(location: str) -> str:
    """
    天気予報を取得します。
    例えば、"東京の天気を教えて" のように使用します。
    """
    return f"{location}の天気予報は晴れです。"
```

## ベストプラクティス

### 1. ファイル命名規則

- スネークケース（`my_tool.py`）を使用
- 機能が分かりやすい名前を付ける
- 関連する機能は同じファイルにまとめる

### 2. 関数のドキュメント

- 必ず docstring を記述する
- AI が関数を理解できるよう、使用例や目的を明確に記述
- パラメータと戻り値の型ヒントを必ず付ける

### 3. 型ヒント

```python
# 良い例
def process_data(text: str, count: int) -> dict:
    """データを処理します。"""
    return {"result": text * count}

# 避けるべき例
def process_data(text, count):  # 型ヒントなし
    return {"result": text * count}
```

### 4. エラーハンドリング

```python
@mcp.tool()
def safe_divide(a: float, b: float) -> float:
    """
    2つの数値を除算します。
    """
    if b == 0:
        raise ValueError("0で除算することはできません")
    return a / b
```

## ローカル開発

### 必要な環境

- Python 3.13
- pip

### セットアップ

```bash
cd src
pip install -r requirements.txt
```

### ローカル実行

```bash
cd src
python -m app
```

## デプロイ

AWS SAM を使用してデプロイします。

### 前提条件

- AWS CLI がインストール済み
- AWS SAM CLI がインストール済み
- AWS 認証情報が設定済み

### デプロイコマンド

```bash
sam build
sam deploy --guided
```

初回デプロイ後は、設定が `samconfig.toml` に保存されるため、次回以降は以下のコマンドでデプロイできます：

```bash
sam build && sam deploy
```

## トラブルシューティング

### 新しい関数が認識されない場合

1. ファイルが `src/app/tools/` ディレクトリにあることを確認
2. `@mcp.tool()` デコレータが正しく記述されているか確認
3. `from app.main import mcp` のインポートがあるか確認
4. サーバーを再起動

### 型エラーが発生する場合

- 関数の引数と戻り値に適切な型ヒントが付いているか確認
- docstring が記述されているか確認

## チーム開発のワークフロー

1. **ブランチを作成**

   ```bash
   git checkout -b feature/add-my-tool
   ```

2. **新しいツールファイルを追加**

   ```bash
   # src/app/tools/my_tool.py を作成
   ```

3. **ローカルでテスト**

   ```bash
   cd src
   python -m app
   ```

4. **コミット＆プッシュ**

   ```bash
   git add src/app/tools/my_tool.py
   git commit -m "Add my_tool with new functionality"
   git push origin feature/add-my-tool
   ```

5. **プルリクエストを作成してレビュー依頼**

## まとめ

- `src/app/tools/` に新しい `.py` ファイルを追加するだけ
- `@mcp.tool()` デコレータで関数を装飾
- 型ヒントと docstring は必須
- 自動的に読み込まれるため、設定変更は不要

チームメンバーは自由に新しいツールを追加し、MCP サーバーの機能を拡張できます！
