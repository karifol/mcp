# AWS SAM Template 解説 (template.yaml)

このファイルは、AWS SAM (Serverless Application Model) テンプレートです。Python アプリケーションを AWS Lambda 関数として デプロイするための設定が記述されています。

## 全体構成

### Template 形式と Transforms

```yaml
AWSTemplateFormatVersion: 2010-09-09
Transform:
  - AWS::Serverless-2016-10-31

  - AWS::LanguageExtensions
```

- **AWSTemplateFormatVersion**: CloudFormation テンプレートの形式バージョンを指定
- **Transform**:
  - `AWS::Serverless-2016-10-31`: SAM の構文を使用可能にする
  - `AWS::LanguageExtensions`: CloudFormation の拡張機能を有効にする

## Resources

### Lambda Function

```yaml
Function:
  Type: AWS::Serverless::Function
```

単一の Lambda 関数を定義しています。

#### 実行環境設定

- **Architectures**: `arm64` - ARM64 アーキテクチャを使用（コスト効率が良い）
- **Runtime**: `python3.13` - Python 3.13 ランタイムを使用
- **Timeout**: `30` - 関数のタイムアウトを 30 秒に設定
- **MemorySize**: `1024` - メモリサイズを 1024MB に設定

#### デプロイ設定

- **AutoPublishAlias**: `live` - 新しいバージョンを自動的に "live" エイリアスとして発行
- **CodeUri**: `src` - ソースコードが格納されている `src` ディレクトリを指定
- **Handler**: `run.sh` - エントリポイントとしてシェルスクリプトを使用

#### レイヤー

```yaml
Layers:
  - !Sub arn:aws:lambda:${AWS::Region}:753240598075:layer:LambdaAdapterLayerArm64:18
```

Lambda Web Adapter レイヤーを使用。これにより HTTP サーバーとしてアプリケーションを動作させることができます。

#### API Gateway 統合

```yaml
Events:
  apiReport:
    Type: Api
    Properties:
      Path: /{proxy+}
      Method: ANY
```

- **Path**: `/{proxy+}` - 全てのパスをプロキシ
- **Method**: `ANY` - 全ての HTTP メソッドを受け付け

#### 環境変数

```yaml
Environment:
  Variables:
    AWS_LAMBDA_EXEC_WRAPPER: /opt/bootstrap
    PORT: 8080
```

- **AWS_LAMBDA_EXEC_WRAPPER**: Lambda Web Adapter の実行ラッパーを指定
- **PORT**: アプリケーションがリッスンするポート番号

## Outputs

デプロイ後に取得できる情報：

### Api

```yaml
Api:
  Description: "API Gateway endpoint URL for Prod stage for Function"
  Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/mcp"
```

API Gateway のエンドポイント URL。`/mcp` パスでアクセス可能。

### Function

```yaml
Function:
  Description: "Lambda Function ARN"
  Value: !GetAtt Function.Arn
```

作成された Lambda 関数の ARN。

### FunctionIamRole

```yaml
FunctionIamRole:
  Description: "Implicit IAM Role created for Function"
  Value: !GetAtt FunctionRole.Arn
```

Lambda 関数用に自動作成された IAM ロールの ARN。

## 使用方法

このテンプレートを使用してデプロイするには：

```bash
# ビルド
sam build

# ローカルテスト
sam local start-api

# デプロイ
sam deploy --guided
```

## アーキテクチャの特徴

1. **コスト効率**: ARM64 アーキテクチャと Lambda Web Adapter を使用
2. **スケーラブル**: サーバーレスアーキテクチャで自動スケーリング
3. **シンプル**: 単一の Lambda 関数で Web アプリケーションをホスト
4. **プロキシ統合**: 全ての HTTP リクエストを Lambda 関数に転送
