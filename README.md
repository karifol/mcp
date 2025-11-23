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
    "mcp-lambda": {
      "url": "https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com/Prod/mcp"
    }
  }
}
```

### デプロイ

```bash
sam build
sam deploy --guided
```

## 🛠️ 利用可能なツール

- **add**: 2 つの整数を加算
- **multiply**: 2 つの整数を乗算
- **get_weather_forecast**: 天気予報を取得

詳細は[ドキュメント](https://karifol.github.io/mcp/)を参照してください。

## 📁 プロジェクト構造

```
.
├── docs/                   # MkDocs ドキュメント (Markdown)
│   ├── index.md
│   ├── setup/
│   ├── usage/
│   ├── development/
│   └── troubleshooting.md
├── src/
│   ├── app/
│   │   ├── main.py        # FastMCPアプリケーション
│   │   └── tools/         # ツール定義
│   └── run.sh             # Lambdaエントリポイント
├── mkdocs.yml             # MkDocs設定
└── template.yaml          # SAM テンプレート
```

## 🔧 カスタムツールの追加

`src/app/tools/` に新しい Python ファイルを追加してツールを定義:

```python
from app.main import mcp

@mcp.tool()
def your_tool(param: str) -> str:
    """
    ツールの説明
    """
    return f"Result: {param}"
```

ツールは自動的に登録されます。

## 📖 ドキュメント

### オンラインドキュメント

完全なドキュメントは GitHub Pages で公開しています:
**https://karifol.github.io/mcp/**

### ローカルプレビュー

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

ブラウザで http://localhost:8000 を開いてプレビューできます。

### ドキュメントのビルド

```bash
mkdocs build
```

静的 HTML ファイルが `site/` ディレクトリに生成されます。

## ライセンス

MIT
