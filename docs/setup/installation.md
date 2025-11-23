# インストール

MCP サーバーを AWS Lambda にデプロイする方法を説明します。

## 前提条件

以下のツールが必要です:

- AWS アカウント
- AWS CLI (設定済み)
- AWS SAM CLI
- Python 3.13 以上

## AWS SAM CLI のインストール

=== "macOS"

    ```bash
    brew tap aws/tap
    brew install aws-sam-cli
    ```

=== "Linux"

    ```bash
    # AWS SAM CLIのダウンロードとインストール
    wget https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip
    unzip aws-sam-cli-linux-x86_64.zip -d sam-installation
    sudo ./sam-installation/install
    ```

=== "Windows"

    ```powershell
    # MSIインストーラーをダウンロード
    # https://github.com/aws/aws-sam-cli/releases/latest
    ```

## リポジトリのクローン

```bash
git clone https://github.com/karifol/mcp.git
cd mcp
```

## デプロイ

### 1. ビルド

```bash
sam build
```

### 2. デプロイ (初回)

初回デプロイ時はガイド付きモードを使用します:

```bash
sam deploy --guided
```

以下の質問に答えます:

- **Stack Name**: `mcp-server` (任意の名前)
- **AWS Region**: `ap-northeast-1` (東京リージョン)
- **Parameter LambdaFunctionName**: デフォルトのまま Enter
- **Parameter ApiGatewayName**: デフォルトのまま Enter
- **Confirm changes before deploy**: `Y`
- **Allow SAM CLI IAM role creation**: `Y`
- **Disable rollback**: `N`
- **Save arguments to configuration file**: `Y`

### 3. デプロイ (2 回目以降)

設定が保存されているので、簡単にデプロイできます:

```bash
sam deploy
```

## デプロイ結果の確認

デプロイが完了すると、以下の情報が表示されます:

```
Outputs
----------------------------------------------------------------------------------
Key                 Api
Description         API Gateway endpoint URL for Prod stage for Function
Value               https://xxxxx.execute-api.ap-northeast-1.amazonaws.com/Prod/mcp

Key                 Function
Description         Lambda Function ARN
Value               arn:aws:lambda:ap-northeast-1:xxxxx:function:McpLambdaFunction
```

!!! success "API エンドポイント"
`Value` に表示されている URL が、MCP サーバーのエンドポイントです。
この URL をクライアント設定で使用します。

## エンドポイントのテスト

デプロイが成功したか確認します:

```bash
curl -X POST https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com/Prod/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
  }'
```

利用可能なツールのリストが返ってくれば成功です。

## 次のステップ

デプロイが完了したら、[接続方法](connection.md)を参照してクライアントからの接続を設定してください。

## トラブルシューティング

### デプロイエラー

!!! failure "Error: Unable to upload artifact"
S3 バケットの作成に失敗している可能性があります。AWS CLI の認証情報を確認してください。

### タイムアウトエラー

!!! failure "Function timeout"
Lambda 関数のタイムアウトを延長してください (template.yaml の `Timeout` を調整)。

詳細は[トラブルシューティング](../troubleshooting.md)を参照してください。
