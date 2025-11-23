# GitHub Pages Setup Guide

このリポジトリの GitHub Pages を有効にするには、以下の手順を実行してください。

## 手順

1. **GitHub リポジトリの設定にアクセス**

   - リポジトリのページに移動
   - `Settings` タブをクリック

2. **GitHub Pages の設定**

   - 左サイドバーから `Pages` を選択
   - `Build and deployment` セクションで:
     - **Source**: `GitHub Actions` を選択

3. **変更をプッシュ**

   ```bash
   git add .
   git commit -m "Add GitHub Pages documentation"
   git push origin main
   ```

4. **デプロイの確認**
   - リポジトリの `Actions` タブで、ワークフローが実行されることを確認
   - デプロイが完了すると、`Settings > Pages` にサイトの URL が表示されます
   - 通常、URL は `https://USERNAME.github.io/REPOSITORY/` の形式です

## アクセス

デプロイ後、以下の URL でドキュメントにアクセスできます:

- `https://karifol.github.io/mcp/`

## トラブルシューティング

### ワークフローが失敗する場合

1. **Permissions の確認**

   - `Settings > Actions > General` に移動
   - `Workflow permissions` セクションで `Read and write permissions` が有効になっていることを確認

2. **GitHub Pages の有効化**
   - `Settings > Pages` で Source が `GitHub Actions` に設定されていることを確認

### ページが表示されない場合

- デプロイには数分かかることがあります
- ブラウザのキャッシュをクリアしてみてください
- `Actions` タブでデプロイが成功していることを確認してください
