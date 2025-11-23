# カスタムツールの追加

MCP サーバーに新しいツールを追加する方法を説明します。

## ツールの基本構造

ツールは `src/app/tools/` ディレクトリ内の Python ファイルに定義します。ファイルが追加されると、自動的に検出・登録されます。

### 基本的なツールの例

```python
"""
custom_tool.py - カスタムツールの例
"""
from app.main import mcp

@mcp.tool()
def greet(name: str) -> str:
    """
    指定された名前で挨拶します。

    Args:
        name (str): 挨拶する相手の名前

    Returns:
        str: 挨拶メッセージ
    """
    return f"こんにちは、{name}さん!"
```

## ツール作成の手順

### 1. 新しい Python ファイルを作成

`src/app/tools/` ディレクトリに新しいファイルを作成します:

```bash
touch src/app/tools/my_tool.py
```

### 2. ツールを定義

```python
"""
my_tool.py - 独自のツール
"""
from app.main import mcp

@mcp.tool()
def calculate_area(width: float, height: float) -> float:
    """
    長方形の面積を計算します。

    Args:
        width (float): 幅
        height (float): 高さ

    Returns:
        float: 面積
    """
    return width * height
```

### 3. デプロイ

```bash
sam build
sam deploy
```

### 4. 動作確認

```bash
curl -X POST https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com/Prod/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "calculate_area",
      "arguments": {
        "width": 10.5,
        "height": 20.3
      }
    },
    "id": 1
  }'
```

---

## 高度な例

### 複数の型を扱うツール

```python
from typing import List, Dict, Optional
from app.main import mcp

@mcp.tool()
def process_data(
    numbers: List[int],
    operation: str,
    multiplier: Optional[float] = 1.0
) -> Dict[str, float]:
    """
    数値リストを処理します。

    Args:
        numbers (List[int]): 処理する数値のリスト
        operation (str): 操作タイプ ('sum' または 'average')
        multiplier (Optional[float]): 結果に掛ける係数 (デフォルト: 1.0)

    Returns:
        Dict[str, float]: 処理結果を含む辞書
    """
    if operation == "sum":
        result = sum(numbers)
    elif operation == "average":
        result = sum(numbers) / len(numbers) if numbers else 0
    else:
        raise ValueError(f"未知の操作: {operation}")

    return {
        "result": result * multiplier,
        "count": len(numbers),
        "operation": operation
    }
```

---

### 外部 API を呼び出すツール

```python
import requests
from app.main import mcp

@mcp.tool()
def fetch_github_user(username: str) -> str:
    """
    GitHubユーザー情報を取得します。

    Args:
        username (str): GitHubユーザー名

    Returns:
        str: ユーザー情報
    """
    try:
        response = requests.get(
            f"https://api.github.com/users/{username}",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        return f"""
名前: {data.get('name', 'N/A')}
ユーザー名: {data['login']}
公開リポジトリ数: {data['public_repos']}
フォロワー数: {data['followers']}
プロフィール: {data['html_url']}
"""
    except requests.exceptions.RequestException as e:
        return f"エラー: ユーザー情報の取得に失敗しました - {str(e)}"
```

!!! warning "外部 API の利用"
外部 API を使用する場合は、`src/requirements.txt` に必要なパッケージを追加してください:
`    requests>=2.31.0
   `

---

### データベースと連携するツール

```python
import json
import boto3
from app.main import mcp

# DynamoDBクライアント
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('my-table')

@mcp.tool()
def save_note(title: str, content: str) -> str:
    """
    ノートをDynamoDBに保存します。

    Args:
        title (str): ノートのタイトル
        content (str): ノートの内容

    Returns:
        str: 保存結果のメッセージ
    """
    try:
        from datetime import datetime

        item = {
            'id': datetime.now().isoformat(),
            'title': title,
            'content': content,
            'created_at': datetime.now().isoformat()
        }

        table.put_item(Item=item)
        return f"ノート '{title}' を保存しました"
    except Exception as e:
        return f"エラー: {str(e)}"

@mcp.tool()
def get_notes() -> str:
    """
    保存されているすべてのノートを取得します。

    Returns:
        str: ノートのリスト
    """
    try:
        response = table.scan()
        items = response.get('Items', [])

        if not items:
            return "保存されているノートはありません"

        result = "保存されているノート:\n\n"
        for item in items:
            result += f"- {item['title']} ({item['created_at']})\n"

        return result
    except Exception as e:
        return f"エラー: {str(e)}"
```

!!! info "AWS 権限"
DynamoDB などの AWS サービスを使用する場合、Lambda 関数に適切な IAM ポリシーを追加する必要があります。
`template.yaml` でポリシーを設定してください。

---

## ツール開発のベストプラクティス

### 1. 明確なドキュメント

```python
@mcp.tool()
def complex_calculation(x: int, y: int, mode: str = "add") -> int:
    """
    2つの数値に対して指定された操作を実行します。

    この関数は加算、減算、乗算、除算をサポートしています。
    除算の場合、結果は整数に切り捨てられます。

    Args:
        x (int): 1つ目の数値
        y (int): 2つ目の数値
        mode (str): 操作モード ('add', 'subtract', 'multiply', 'divide')
                   デフォルトは 'add'

    Returns:
        int: 計算結果

    Raises:
        ValueError: 未知の操作モードが指定された場合
        ZeroDivisionError: 除算で0を指定した場合

    Examples:
        >>> complex_calculation(10, 5, "add")
        15
        >>> complex_calculation(10, 5, "multiply")
        50
    """
    if mode == "add":
        return x + y
    elif mode == "subtract":
        return x - y
    elif mode == "multiply":
        return x * y
    elif mode == "divide":
        if y == 0:
            raise ZeroDivisionError("0で除算できません")
        return x // y
    else:
        raise ValueError(f"未知の操作モード: {mode}")
```

### 2. エラーハンドリング

```python
@mcp.tool()
def safe_division(a: float, b: float) -> str:
    """
    安全な除算を行います。

    Args:
        a (float): 被除数
        b (float): 除数

    Returns:
        str: 計算結果またはエラーメッセージ
    """
    try:
        if b == 0:
            return "エラー: 0で除算することはできません"
        result = a / b
        return f"結果: {result}"
    except Exception as e:
        return f"エラー: {str(e)}"
```

### 3. 型ヒントの使用

```python
from typing import List, Dict, Union, Optional

@mcp.tool()
def analyze_numbers(
    numbers: List[Union[int, float]],
    include_median: Optional[bool] = False
) -> Dict[str, float]:
    """
    数値リストを分析します。

    Args:
        numbers: 分析する数値のリスト
        include_median: 中央値を含めるかどうか

    Returns:
        分析結果を含む辞書
    """
    result = {
        "count": len(numbers),
        "sum": sum(numbers),
        "average": sum(numbers) / len(numbers) if numbers else 0,
        "min": min(numbers) if numbers else 0,
        "max": max(numbers) if numbers else 0
    }

    if include_median and numbers:
        sorted_nums = sorted(numbers)
        n = len(sorted_nums)
        if n % 2 == 0:
            result["median"] = (sorted_nums[n//2-1] + sorted_nums[n//2]) / 2
        else:
            result["median"] = sorted_nums[n//2]

    return result
```

---

## ツールのテスト

### ローカルでのテスト

```python
# tests/test_my_tool.py
from app.tools.my_tool import calculate_area

def test_calculate_area():
    assert calculate_area(10, 20) == 200
    assert calculate_area(5.5, 4.0) == 22.0
    assert calculate_area(0, 100) == 0

# テスト実行
# pytest tests/test_my_tool.py
```

### デプロイ前の確認

```bash
# ローカルでLambdaをテスト
sam local start-api

# 別のターミナルでテスト
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "calculate_area",
      "arguments": {"width": 10, "height": 20}
    },
    "id": 1
  }'
```

---

## ツールのグループ化

関連するツールは同じファイルにまとめることができます:

```python
"""
math_tools.py - 数学関連のツール
"""
from app.main import mcp
import math

@mcp.tool()
def calculate_circle_area(radius: float) -> float:
    """円の面積を計算"""
    return math.pi * radius ** 2

@mcp.tool()
def calculate_circle_circumference(radius: float) -> float:
    """円の円周を計算"""
    return 2 * math.pi * radius

@mcp.tool()
def pythagorean_theorem(a: float, b: float) -> float:
    """ピタゴラスの定理で斜辺を計算"""
    return math.sqrt(a ** 2 + b ** 2)
```

---

## 次のステップ

- [アーキテクチャ](architecture.md) - システムの詳細を理解
- [トラブルシューティング](../troubleshooting.md) - 問題解決のヒント
