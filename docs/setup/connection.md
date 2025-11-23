# 接続方法

MCP クライアントからサーバーに接続する方法を説明します。

## 前提条件

- MCP サーバーのエンドポイント URL
- API キー
- MCP クライアント (Claude Desktop または Cline)

!!! info "エンドポイント URL と API キーの取得"
エンドポイント URL と API キーはサーバー管理者から提供されます。

    - URL 形式: `https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com/Prod/mcp`
    - API キーは AWS コンソールまたは以下のコマンドで取得できます:

    ```bash
    aws apigateway get-api-key --api-key <API-KEY-ID> --include-value
    ```

## Claude Desktop での接続

### 設定ファイルの編集

Claude Desktop の設定ファイルを編集します:

=== "macOS"

    ```bash
    code ~/Library/Application\ Support/Claude/claude_desktop_config.json
    ```

=== "Windows"

    ```bash
    notepad %APPDATA%\Claude\claude_desktop_config.json
    ```

=== "Linux"

    ```bash
    code ~/.config/Claude/claude_desktop_config.json
    ```

### 設定の追加

以下の設定を追加します:

```json
{
  "mcpServers": {
    "mcp-lambda": {
      "url": "https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com/Prod/mcp",
      "headers": {
        "x-api-key": "YOUR-API-KEY"
      }
    }
  }
}
```

!!! warning "URL と API キーの置き換え" - `YOUR-API-ID` と `YOUR-REGION` を実際の値に置き換えてください - `YOUR-API-KEY` を管理者から提供された API キーに置き換えてください

    例:
    ```json
    {
      "url": "https://abc123def4.execute-api.ap-northeast-1.amazonaws.com/Prod/mcp",
      "headers": {
        "x-api-key": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
      }
    }
    ```

### 複数の MCP サーバーを登録する場合

```json
{
  "mcpServers": {
    "mcp-lambda": {
      "url": "https://your-api-1.execute-api.ap-northeast-1.amazonaws.com/Prod/mcp",
      "headers": {
        "x-api-key": "YOUR-API-KEY-1"
      }
    },
    "another-mcp": {
      "url": "https://your-api-2.execute-api.us-east-1.amazonaws.com/Prod/mcp",
      "headers": {
        "x-api-key": "YOUR-API-KEY-2"
      }
    }
  }
}
```

### Claude Desktop の再起動

設定を保存したら、Claude Desktop を完全に終了して再起動します。

=== "macOS"

    1. Command + Q でClaude Desktopを終了
    2. アプリケーションから再度起動

=== "Windows"

    1. タスクマネージャーでClaude Desktopを終了
    2. スタートメニューから再度起動

### 接続の確認

Claude Desktop を開き、以下のように確認します:

1. 新しいチャットを開始
2. "利用可能なツールを教えて" と聞く
3. `add`, `multiply`, `get_weather_forecast` などのツールが表示されれば成功

## Cline (VS Code 拡張機能) での接続

### Cline のインストール

1. VS Code を開く
2. 拡張機能マーケットプレイスで "Cline" を検索
3. インストール

### MCP サーバーの追加

1. VS Code で Cline を開く (サイドバーの Cline アイコン)
2. 設定アイコン (⚙️) をクリック
3. "MCP Settings" セクションを探す
4. 以下の設定を追加:

```json
{
  "name": "mcp-lambda",
  "type": "http",
  "url": "https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com/Prod/mcp",
  "headers": {
    "x-api-key": "YOUR-API-KEY"
  }
}
```

### VS Code の再起動

設定を保存したら、VS Code をリロードします:

1. Command Palette を開く (Cmd/Ctrl + Shift + P)
2. "Developer: Reload Window" を実行

### 接続の確認

Cline のチャットで "使えるツールは?" と聞いて、ツールリストが表示されることを確認します。

## その他の MCP クライアント

### カスタムクライアント

HTTP POST リクエストで MCP Protocol に従ってリクエストを送信することで、任意のクライアントから接続できます:

```bash
curl -X POST https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com/Prod/mcp \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR-API-KEY" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
  }'
```

### Python クライアント例

```python
import requests

url = "https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com/Prod/mcp"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "YOUR-API-KEY"
}

# ツールリストの取得
response = requests.post(url, headers=headers, json={
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
})
print(response.json())

# ツールの呼び出し
response = requests.post(url, headers=headers, json={
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "add",
        "arguments": {
            "a": 5,
            "b": 10
        }
    },
    "id": 2
})
print(response.json())
```

## トラブルシューティング

### 403 Forbidden エラー

API キーが正しく設定されていない可能性があります:

1. API キーが正しいか確認
2. ヘッダー名が `x-api-key` であることを確認
3. API キーの有効期限を確認

### 接続できない

1. エンドポイント URL が正しいか確認
2. ネットワーク接続を確認
3. Claude Desktop / Cline を再起動

詳細は[トラブルシューティング](../troubleshooting.md)を参照してください。

## 次のステップ

接続が完了したら、[使用例](../usage/examples.md)を参照して実際にツールを使ってみましょう!
