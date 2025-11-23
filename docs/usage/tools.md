# 利用可能なツール

MCP サーバーで提供されているツールの一覧と詳細な説明です。

## 計算ツール

### add

2 つの整数を加算します。

**パラメータ:**

| パラメータ名 | 型    | 必須 | 説明         |
| ------------ | ----- | ---- | ------------ |
| `a`          | `int` | ✅   | 1 つ目の整数 |
| `b`          | `int` | ✅   | 2 つ目の整数 |

**戻り値:**

- 型: `int`
- 説明: 2 つの整数の合計

**使用例:**

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "add",
    "arguments": {
      "a": 5,
      "b": 10
    }
  },
  "id": 1
}
```

**レスポンス:**

```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "15"
      }
    ]
  },
  "id": 1
}
```

---

### multiply

2 つの整数を乗算します。

**パラメータ:**

| パラメータ名 | 型    | 必須 | 説明         |
| ------------ | ----- | ---- | ------------ |
| `a`          | `int` | ✅   | 1 つ目の整数 |
| `b`          | `int` | ✅   | 2 つ目の整数 |

**戻り値:**

- 型: `int`
- 説明: 2 つの整数の積

**使用例:**

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "multiply",
    "arguments": {
      "a": 12,
      "b": 8
    }
  },
  "id": 1
}
```

**レスポンス:**

```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "96"
      }
    ]
  },
  "id": 1
}
```

---

## 天気ツール

### get_weather_forecast

指定された場所の天気予報を取得します。

**パラメータ:**

| パラメータ名 | 型    | 必須 | 説明                                        |
| ------------ | ----- | ---- | ------------------------------------------- |
| `location`   | `str` | ✅   | 天気予報を取得する場所 (例: "東京", "大阪") |

**戻り値:**

- 型: `str`
- 説明: 天気予報の情報

**使用例:**

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_weather_forecast",
    "arguments": {
      "location": "東京"
    }
  },
  "id": 1
}
```

**レスポンス:**

```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "東京の天気予報は晴れです。"
      }
    ]
  },
  "id": 1
}
```

!!! note "注意"
現在の実装はモックデータを返します。---

## ツールの一覧取得

すべての利用可能なツールを取得するには、`tools/list` メソッドを使用します:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "id": 1
}
```

**レスポンス例:**

```json
{
  "jsonrpc": "2.0",
  "result": {
    "tools": [
      {
        "name": "add",
        "description": "Add two integers.",
        "inputSchema": {
          "type": "object",
          "properties": {
            "a": {
              "type": "integer",
              "description": "The first integer."
            },
            "b": {
              "type": "integer",
              "description": "The second integer."
            }
          },
          "required": ["a", "b"]
        }
      },
      {
        "name": "multiply",
        "description": "Multiply two integers.",
        "inputSchema": {
          "type": "object",
          "properties": {
            "a": {
              "type": "integer",
              "description": "The first integer."
            },
            "b": {
              "type": "integer",
              "description": "The second integer."
            }
          },
          "required": ["a", "b"]
        }
      },
      {
        "name": "get_weather_forecast",
        "description": "天気予報を取得します。\n例えば、\"東京の天気を教えて\" のように使用します。",
        "inputSchema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "天気予報を取得する場所"
            }
          },
          "required": ["location"]
        }
      }
    ]
  },
  "id": 1
}
```

## 次のステップ

実際の使用例を見るには、[使用例](examples.md)を参照してください。
