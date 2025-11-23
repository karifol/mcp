# MCP Server

Model Context Protocol (MCP) サーバー - AWS Lambda 上で動作する HTTP MCP サーバー

## 📚 ドキュメント

詳細なドキュメントは GitHub Pages で公開しています:
**https://karifol.github.io/mcp/**

ドキュメントには以下の情報が含まれています:

- MCP サーバーの概要
- セットアップ手順
- Claude Desktop / Cline での接続方法
- 利用可能なツールの一覧
- 使用例
- トラブルシューティング

## 🚀 クイックスタート

### Claude Desktop での接続

`claude_desktop_config.json` に以下を追加:

```json
{
  "mcpServers": {
    "mcp": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "<YOUR-API-ENDPOINT>",
        "--header",
        "x-api-key:<API-KEY>"
      ]
    }
  }
}
```

!!! info "API キーの取得"
デプロイ後、以下のコマンドで API キーを取得できます:
`` bash
    aws apigateway get-api-key --api-key $(aws cloudformation describe-stacks --stack-name <STACK-NAME> --query 'Stacks[0].Outputs[?OutputKey==`ApiKey`].OutputValue' --output text) --include-value
     ``

### デプロイ

```bash
sam build
sam deploy --guided
```

## 🛠️ 利用可能なツール

[ドキュメント](https://karifol.github.io/mcp/)を参照してください。

## 📁 プロジェクト構造

```
.
├── mkdocs.yml             # MkDocs設定
├── docs/                  # ドキュメント
│   ├── requirements.txt   # ドキュメント用パッケージ
│   ├── index.md
│   ├── setup/
│   ├── usage/
│   ├── stylesheets/
│   └── troubleshooting.md
├── src/                   # アプリケーション
│   ├── app/
│   │   ├── main.py        # FastMCPアプリケーション
│   │   └── tools/         # ツール定義
│   └── run.sh             # Lambdaエントリポイント
└── template.yaml          # SAM テンプレート
```

## 📖 ドキュメント

### オンラインドキュメント

完全なドキュメントは GitHub Pages で公開しています:
**https://karifol.github.io/mcp/**
