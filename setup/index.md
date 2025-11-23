---
layout: default
title: セットアップ
---

# セットアップ

MCP サーバーのセットアップ方法について説明します。

## 📖 セットアップガイド

- [インストール](installation) - サーバーのデプロイ方法
- [接続方法](connection) - クライアントからの接続設定

## 前提条件

- AWS アカウント
- AWS CLI (設定済み)
- AWS SAM CLI
- Python 3.13 以上
- MCP クライアント (Claude Desktop、Cline など)

## クイックスタート

### 1. デプロイ

```bash
sam build
sam deploy --guided
```

### 2. 接続設定

Claude Desktop の設定ファイルに以下を追加:

```json
{
  "mcpServers": {
    "mcp-lambda": {
      "url": "https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com/Prod/mcp"
    }
  }
}
```

### 3. 再起動

Claude Desktop または Cline を再起動して接続を確認します。

## 詳細情報

各ステップの詳細については、以下のページを参照してください:

- [インストール手順](installation)
- [接続方法の詳細](connection)
