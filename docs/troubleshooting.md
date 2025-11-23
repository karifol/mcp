# トラブルシューティング

MCP サーバーの使用中に発生する可能性のある問題と解決方法を紹介します。

## 接続の問題

### Claude Desktop が接続できない

#### 症状

- Claude Desktop でツールが表示されない
- 接続エラーメッセージが表示される

#### 解決策

1. **設定ファイルの確認**

   ```bash
   # macOS
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

   # Windows
   type %APPDATA%\Claude\claude_desktop_config.json
   ```

   URL が正しいか確認してください。

2. **Claude Desktop の再起動**

   - 完全に終了してから再起動
   - macOS: Command + Q で終了
   - Windows: タスクマネージャーからプロセスを終了

3. **JSON 構文エラーのチェック**

   ```json
   {
     "mcpServers": {
       "mcp-lambda": {
         "url": "https://your-api.execute-api.ap-northeast-1.amazonaws.com/Prod/mcp"
       }
     }
   }
   ```

   - カンマの位置
   - クォートの閉じ忘れ
   - 波括弧の対応

4. **エンドポイントの確認**
   ```bash
   curl -X POST https://YOUR-ENDPOINT/mcp \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
   ```

---

### Cline が接続できない

#### 症状

- Cline でツールが表示されない
- "MCP server not responding" エラー

#### 解決策

1. **VS Code のリロード**

   - Command Palette (Cmd/Ctrl + Shift + P)
   - "Developer: Reload Window"

2. **Cline 設定の確認**

   - Cline 設定画面を開く
   - MCP Settings セクションを確認
   - URL と type が正しいか確認

3. **VS Code 拡張機能の再インストール**
   - Cline 拡張機能をアンインストール
   - VS Code を再起動
   - Cline を再インストール

---

## デプロイの問題

### sam build エラー

#### 症状

```
Build Failed
Error: PythonPipBuilder:ResolveDependencies - ...
```

#### 解決策

1. **Python バージョンの確認**

   ```bash
   python --version  # 3.13以上が必要
   ```

2. **依存関係の問題**

   ```bash
   # requirements.txtを確認
   cat src/requirements.txt

   # ローカルでインストールテスト
   pip install -r src/requirements.txt
   ```

3. **キャッシュのクリア**
   ```bash
   rm -rf .aws-sam/
   sam build --use-container
   ```

---

### sam deploy エラー

#### 症状

```
Error: Failed to create/update stack
```

#### 解決策

1. **AWS 認証情報の確認**

   ```bash
   aws sts get-caller-identity
   ```

2. **IAM 権限の確認**
   必要な権限:

   - CloudFormation
   - Lambda
   - API Gateway
   - IAM
   - S3

3. **スタック名の重複**

   ```bash
   # 既存のスタックを確認
   aws cloudformation list-stacks

   # 削除が必要な場合
   aws cloudformation delete-stack --stack-name mcp-server
   ```

4. **リージョンの確認**
   ```bash
   # samconfig.tomlを確認
   cat samconfig.toml
   ```

---

### デプロイは成功するがエンドポイントが動作しない

#### 症状

- デプロイは成功
- curl でアクセスするとエラー

#### 解決策

1. **CloudWatch Logs の確認**

   ```bash
   # 最新のログを確認
   aws logs tail /aws/lambda/McpLambdaFunction --follow
   ```

2. **Lambda 関数のテスト**

   - AWS Console で Lambda 関数を開く
   - テストイベントを作成して実行
   - エラーメッセージを確認

3. **環境変数の確認**

   ```bash
   aws lambda get-function-configuration \
     --function-name McpLambdaFunction \
     --query Environment
   ```

   必要な環境変数:

   - `AWS_LAMBDA_EXEC_WRAPPER`: `/opt/bootstrap`
   - `PORT`: `8080`

---

## ツールの問題

### ツールが表示されない

#### 症状

- `tools/list` でツールが返ってこない
- 特定のツールだけ表示されない

#### 解決策

1. **ファイルの配置を確認**

   ```bash
   ls -la src/app/tools/
   ```

   - `__init__.py` が存在するか
   - ツールファイルが `.py` 拡張子か

2. **インポートエラーのチェック**

   ```python
   # ツールファイルの先頭行を確認
   from app.main import mcp  # 正しい
   # import mcp  # 間違い
   ```

3. **デコレータの確認**

   ```python
   @mcp.tool()  # 正しい
   # @tool()  # 間違い
   ```

4. **再デプロイ**
   ```bash
   sam build
   sam deploy
   ```

---

### ツール実行時のエラー

#### 症状

```json
{
  "error": {
    "code": -32602,
    "message": "Invalid params"
  }
}
```

#### 解決策

1. **パラメータの型を確認**

   ```python
   @mcp.tool()
   def add(a: int, b: int) -> int:  # int型を要求
       return a + b
   ```

   リクエスト:

   ```json
   {
     "arguments": {
       "a": 5, // 正しい
       "b": "10" // 間違い: 文字列ではなく数値
     }
   }
   ```

2. **必須パラメータの確認**

   ```python
   def func(required: str, optional: str = "default"):
       pass
   ```

3. **CloudWatch Logs でスタックトレースを確認**
   ```bash
   aws logs tail /aws/lambda/McpLambdaFunction --follow
   ```

---

## パフォーマンスの問題

### レスポンスが遅い

#### 症状

- ツールの実行に時間がかかる
- タイムアウトエラー

#### 解決策

1. **メモリの増加**

   ```yaml
   # template.yaml
   Function:
     Type: AWS::Serverless::Function
     Properties:
       MemorySize: 2048 # 1024 から増加
   ```

2. **タイムアウトの延長**

   ```yaml
   Function:
     Type: AWS::Serverless::Function
     Properties:
       Timeout: 60 # 30 から延長
   ```

3. **コードの最適化**
   - 不要な処理を削除
   - 外部 API 呼び出しの最適化
   - キャッシュの活用

---

### コールドスタート遅延

#### 症状

- 初回実行が遅い
- しばらく使わないと遅くなる

#### 解決策

1. **Provisioned Concurrency の設定**

   ```yaml
   Function:
     Type: AWS::Serverless::Function
     Properties:
       AutoPublishAlias: live
       ProvisionedConcurrencyConfig:
         ProvisionedConcurrentExecutions: 1
   ```

2. **定期的なウォームアップ**
   ```yaml
   WarmUpEvent:
     Type: Schedule
     Properties:
       Schedule: rate(5 minutes)
   ```

---

## エラーコード一覧

| コード | 意味             | 原因               | 解決策                         |
| ------ | ---------------- | ------------------ | ------------------------------ |
| -32700 | Parse error      | 不正な JSON        | JSON フォーマットを確認        |
| -32600 | Invalid Request  | 不正なリクエスト   | JSON-RPC フォーマットを確認    |
| -32601 | Method not found | 存在しないメソッド | メソッド名を確認               |
| -32602 | Invalid params   | 不正なパラメータ   | パラメータの型と必須項目を確認 |
| -32603 | Internal error   | サーバー内部エラー | CloudWatch Logs を確認         |

---

## デバッグ方法

### ローカルでのテスト

```bash
# ローカルでLambdaを起動
sam local start-api

# 別のターミナルでテスト
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
  }'
```

### ログの有効化

```python
# ツールファイルにログを追加
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

@mcp.tool()
def my_tool(param: str) -> str:
    logger.info(f"my_tool called with param: {param}")
    result = process(param)
    logger.info(f"my_tool result: {result}")
    return result
```

### CloudWatch Logs の確認

```bash
# リアルタイムでログを監視
aws logs tail /aws/lambda/McpLambdaFunction --follow

# 特定の時間範囲のログを取得
aws logs tail /aws/lambda/McpLambdaFunction \
  --since 1h \
  --filter-pattern "ERROR"
```

---

## よくある質問 (FAQ)

### Q: 複数の MCP サーバーを同時に使えますか?

A: はい、Claude Desktop の設定ファイルに複数のサーバーを登録できます:

```json
{
  "mcpServers": {
    "mcp-lambda-1": {
      "url": "https://api1.example.com/mcp"
    },
    "mcp-lambda-2": {
      "url": "https://api2.example.com/mcp"
    }
  }
}
```

### Q: 既存のツールを削除するには?

A: ツールファイルを削除して再デプロイ:

```bash
rm src/app/tools/old_tool.py
sam build
sam deploy
```

### Q: ツールの実行結果をキャッシュできますか?

A: はい、DynamoDB や ElastiCache を使用できます:

```python
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cache-table')

@mcp.tool()
def cached_tool(key: str) -> str:
    # キャッシュチェック
    response = table.get_item(Key={'id': key})
    if 'Item' in response:
        return response['Item']['value']

    # 処理実行
    result = expensive_operation(key)

    # キャッシュ保存
    table.put_item(Item={'id': key, 'value': result})
    return result
```

### Q: 認証を追加できますか?

A: API Gateway で複数の認証方法をサポート:

- API Key
- Lambda Authorizer
- Cognito User Pools
- IAM 認証

詳細は[接続方法](setup/connection.md#認証の追加-オプション)を参照。

---

## サポート

### 問題が解決しない場合

1. **GitHub で Issue を作成**

   - https://github.com/karifol/mcp/issues

2. **ログを添付**

   - CloudWatch Logs のスタックトレース
   - エラーメッセージ全文
   - 使用した設定ファイル

3. **環境情報を記載**
   - OS (macOS/Windows/Linux)
   - Claude Desktop/Cline のバージョン
   - AWS リージョン
   - Python バージョン
