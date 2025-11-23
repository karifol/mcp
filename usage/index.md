---
layout: default
title: 使い方
---

# 使い方

MCP サーバーの使い方について説明します。

## 📖 使い方ガイド

- [利用可能なツール](tools) - ツールの一覧と詳細
- [使用例](examples) - 実践的な使用例

## 基本的な使い方

### Claude Desktop での利用

MCP サーバーに接続後、自然言語でツールを呼び出せます:

```
5と10を足してください
```

Claude が自動的に `add` ツールを使用して計算します。

### Cline での利用

VS Code の Cline でも同様に使用できます。Cline のチャットで:

```
12と8を掛けてください
```

### HTTP API として利用

```bash
curl -X POST https://YOUR-ENDPOINT/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "add",
      "arguments": {"a": 5, "b": 10}
    },
    "id": 1
  }'
```

## 詳細情報

- [利用可能なツール一覧](tools)
- [実践的な使用例](examples)
