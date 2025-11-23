# 使用例

Claude Desktop や Cline での MCP サーバーの使用例を紹介します。

## Claude Desktop での使用

### 基本的な計算

**プロンプト例:**

```
5と10を足してください
```

**Claude の動作:**

1. `add` ツールを自動的に選択
2. パラメータ `a=5`, `b=10` でツールを呼び出し
3. 結果 `15` を返す

---

**プロンプト例:**

```
12と8を掛けてください
```

**Claude の動作:**

1. `multiply` ツールを選択
2. パラメータ `a=12`, `b=8` でツールを呼び出し
3. 結果 `96` を返す

---

### 天気予報の取得

**プロンプト例:**

```
東京の天気を教えて
```

**Claude の動作:**

1. `get_weather_forecast` ツールを選択
2. パラメータ `location="東京"` でツールを呼び出し
3. 天気予報を返す

---

### 複数のツールの組み合わせ

**プロンプト例:**

```
3と7を足した結果を、5で掛けてください
```

**Claude の動作:**

1. `add` ツールで 3 + 7 = 10 を計算
2. `multiply` ツールで 10 × 5 = 50 を計算
3. 最終結果 `50` を返す

---

## Cline での使用

### コード生成と計算の組み合わせ

**プロンプト例:**

```
配列 [3, 5, 7, 9] の要素をすべて足した合計を計算してください
```

**Cline の動作:**

1. `add` ツールを複数回使用して計算
2. または、Python コードを生成して実行

---

### 条件分岐を含む処理

**プロンプト例:**

```
AとBの2つの数値を入力として受け取り、
Aが10より大きい場合はAとBを掛け算、
そうでなければ足し算する関数を作ってください
```

**Cline の動作:**

1. 関数のコードを生成
2. テストケースで `add` や `multiply` ツールを使用して検証

---

## HTTP API としての直接利用

### cURL での使用

#### ツールリストの取得

```bash
curl -X POST https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com/Prod/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
  }'
```

#### 加算の実行

```bash
curl -X POST https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com/Prod/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "add",
      "arguments": {
        "a": 100,
        "b": 200
      }
    },
    "id": 2
  }'
```

---

### Python での使用

```python
import requests

# MCPサーバーのURL
MCP_URL = "https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com/Prod/mcp"

def call_mcp_tool(tool_name: str, arguments: dict) -> dict:
    """MCPツールを呼び出す"""
    response = requests.post(MCP_URL, json={
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        },
        "id": 1
    })
    return response.json()

# 使用例
result = call_mcp_tool("add", {"a": 15, "b": 25})
print(f"結果: {result['result']['content'][0]['text']}")  # 出力: 結果: 40

result = call_mcp_tool("multiply", {"a": 6, "b": 7})
print(f"結果: {result['result']['content'][0]['text']}")  # 出力: 結果: 42

result = call_mcp_tool("get_weather_forecast", {"location": "大阪"})
print(f"天気: {result['result']['content'][0]['text']}")
```

---

### JavaScript での使用

```javascript
const MCP_URL =
  "https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com/Prod/mcp";

async function callMCPTool(toolName, arguments) {
  const response = await fetch(MCP_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      method: "tools/call",
      params: {
        name: toolName,
        arguments: arguments,
      },
      id: 1,
    }),
  });

  return await response.json();
}

// 使用例
(async () => {
  const result1 = await callMCPTool("add", { a: 30, b: 12 });
  console.log("結果:", result1.result.content[0].text); // 出力: 結果: 42

  const result2 = await callMCPTool("multiply", { a: 9, b: 8 });
  console.log("結果:", result2.result.content[0].text); // 出力: 結果: 72

  const result3 = await callMCPTool("get_weather_forecast", {
    location: "福岡",
  });
  console.log("天気:", result3.result.content[0].text);
})();
```

---

## 実践的な使用例

### データ処理パイプライン

複数のツールを組み合わせてデータ処理を行う例:

```python
def process_numbers(numbers: list) -> int:
    """数値リストを処理して合計と積を計算"""
    # 合計を計算
    total = numbers[0]
    for num in numbers[1:]:
        result = call_mcp_tool("add", {"a": total, "b": num})
        total = int(result['result']['content'][0]['text'])

    # 積を計算
    product = numbers[0]
    for num in numbers[1:]:
        result = call_mcp_tool("multiply", {"a": product, "b": num})
        product = int(result['result']['content'][0]['text'])

    return total, product

# 実行
numbers = [2, 3, 4, 5]
total, product = process_numbers(numbers)
print(f"合計: {total}, 積: {product}")  # 出力: 合計: 14, 積: 120
```

---

### バッチ処理

複数の場所の天気を一度に取得:

```python
locations = ["東京", "大阪", "名古屋", "福岡", "札幌"]

for location in locations:
    result = call_mcp_tool("get_weather_forecast", {"location": location})
    weather = result['result']['content'][0]['text']
    print(f"{location}: {weather}")
```

---

## エラーハンドリング

```python
def safe_call_mcp_tool(tool_name: str, arguments: dict):
    """エラーハンドリング付きのMCPツール呼び出し"""
    try:
        response = requests.post(MCP_URL, json={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            },
            "id": 1
        }, timeout=10)

        response.raise_for_status()
        data = response.json()

        if 'error' in data:
            print(f"エラー: {data['error']['message']}")
            return None

        return data['result']['content'][0]['text']

    except requests.exceptions.Timeout:
        print("タイムアウトエラー")
        return None
    except requests.exceptions.RequestException as e:
        print(f"リクエストエラー: {e}")
        return None
    except Exception as e:
        print(f"予期しないエラー: {e}")
        return None

# 使用例
result = safe_call_mcp_tool("add", {"a": 10, "b": 20})
if result:
    print(f"結果: {result}")
```

---

## 次のステップ

- [カスタムツールの追加](../development/custom-tools.md) - 独自のツールを作成
- [トラブルシューティング](../troubleshooting.md) - 問題が発生した場合
