---
layout: default
title: 使い方
---

# 使い方

MCPサーバーの使い方について説明します。

## 📖 使い方ガイド

- [利用可能なツール](tools) - ツールの一覧と詳細
- [使用例](examples) - 実践的な使用例

## 基本的な使い方

### Claude Desktopでの利用

MCPサーバーに接続後、自然言語でツールを呼び出せます:

```
5と10を足してください
```

Claudeが自動的に `add` ツールを使用して計算します。

### Clineでの利用

VS CodeのClineでも同様に使用できます。Clineのチャットで:

```
12と8を掛けてください
```

### HTTP APIとして利用

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
