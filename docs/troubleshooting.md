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

   サーバー管理者に連絡して、タイムアウト設定の延長を依頼してください。

3. **処理の最適化**

   大量のデータを扱う場合や複雑な処理を行う場合は、処理を分割するか、サーバー管理者に相談してください。

---

### コールドスタート遅延

#### 症状

- 初回実行が遅い
- しばらく使わないと遅くなる

#### 解決策

AWS Lambda 特有の現象です。初回実行やしばらく使われていない場合、数秒かかることがあります。これは正常な動作です。頻繁に使用する場合は、サーバー管理者に Provisioned Concurrency の設定を依頼してください。

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

### CloudWatch Logs の確認

サーバー管理者は以下のコマンドでログを確認できます:

```bash
# リアルタイムでログを監視
aws logs tail /aws/lambda/McpLambdaFunction --follow

# 特定の時間範囲のログを取得
aws logs tail /aws/lambda/McpLambdaFunction \
  --since 1h \
  --filter-pattern "ERROR"
```

エラーが発生した場合は、エラーメッセージとタイムスタンプをサーバー管理者に伝えてください。

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

A: サーバー管理者に連絡して、ツールの削除とサーバーの再デプロイを依頼してください。

### Q: ツールの実行結果をキャッシュできますか?

A: サーバー側でキャッシュ機能を実装することは可能です。詳細はサーバー管理者にお問い合わせください。

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
