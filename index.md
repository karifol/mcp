---
layout: default
title: ホーム
---

# 🔌 MCP Server

Model Context Protocol サーバーへようこそ! このドキュメントでは、MCP サーバーへの接続方法と使い方を説明します。

## 🚀 クイックスタート

MCP サーバーは、AWS Lambda 上で動作する HTTP MCP サーバーです。Claude Desktop や Cline などの MCP クライアントから接続して、様々なツールを利用できます。

### 主な特徴

- **🎯 シンプルな接続**: HTTP エンドポイント経由で簡単に接続
- **⚡ サーバーレス**: AWS Lambda で自動スケール
- **🔧 拡張可能**: 新しいツールを簡単に追加
- **📦 自動登録**: ツールは自動的に検出・登録

## 📋 利用可能なツール

| ツール名               | 説明             | カテゴリ |
| ---------------------- | ---------------- | -------- |
| `add`                  | 2 つの整数を加算 | 計算     |
| `multiply`             | 2 つの整数を乗算 | 計算     |
| `get_weather_forecast` | 天気予報を取得   | 天気     |

詳細は[利用可能なツール](usage/tools)を参照してください。

## 🔗 接続方法

### Claude Desktop

```json
{
  "mcpServers": {
    "mcp-lambda": {
      "url": "https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com/Prod/mcp"
    }
  }
}
```

### Cline (VS Code)

Cline の設定画面から MCP サーバーを追加し、上記の URL を設定します。

詳細な手順は[接続方法](setup/connection)を参照してください。

## 📚 ドキュメント

- [インストール](setup/installation) - サーバーのデプロイ方法
- [接続方法](setup/connection) - クライアントからの接続設定
- [利用可能なツール](usage/tools) - ツールの詳細
- [使用例](usage/examples) - 実際の使用例
- [カスタムツールの追加](development/custom-tools) - 新しいツールの作成
- [アーキテクチャ](development/architecture) - システムの詳細
- [トラブルシューティング](troubleshooting) - 問題解決

## 🤝 コントリビューション

新しいツールの追加方法については、[カスタムツールの追加](development/custom-tools)を参照してください。

## 📄 ライセンス

MIT License

---

<div style="text-align: center; margin-top: 3rem; padding: 2rem; background: #f6f8fa; border-radius: 6px;">
  <h3>🚀 今すぐ始める</h3>
  <p>MCPサーバーをデプロイして、AIアシスタントに新しい機能を追加しましょう!</p>
  <a href="setup/installation" style="display: inline-block; padding: 10px 20px; background: #2563eb; color: white; text-decoration: none; border-radius: 6px; margin-top: 1rem;">インストールガイドを見る →</a>
</div>
