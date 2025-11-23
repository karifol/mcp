# MCP Server Documentation

Model Context Protocol (MCP) サーバーへようこそ! このドキュメントでは、MCP サーバーへの接続方法と使い方を説明します。

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

詳細は[利用可能なツール](usage/tools.md)を参照してください。

## 🔗 接続方法

=== "Claude Desktop"

    ```json
    {
      "mcpServers": {
        "mcp-lambda": {
          "url": "https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com/Prod/mcp"
        }
      }
    }
    ```

=== "Cline (VS Code)"

    Clineの設定画面からMCPサーバーを追加し、上記のURLを設定します。

詳細な手順は[接続方法](setup/connection.md)を参照してください。

## 📚 次のステップ

1. [インストール](setup/installation.md) - サーバーのデプロイ方法
2. [接続方法](setup/connection.md) - クライアントからの接続設定
3. [使用例](usage/examples.md) - 実際の使用例を確認
4. [トラブルシューティング](troubleshooting.md) - 問題が発生した場合

## 📄 ライセンス

MIT License
