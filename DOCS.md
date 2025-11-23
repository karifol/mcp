# MkDocs Material ドキュメント

このプロジェクトは MkDocs Material を使用してドキュメントを生成しています。

## 🎨 特徴

- **美しいデザイン**: Material Design テーマ
- **日本語対応**: 完全日本語ドキュメント
- **ダーク/ライトモード**: 切り替え可能
- **検索機能**: 全文検索対応
- **コードハイライト**: シンタックスハイライト
- **レスポンシブ**: モバイル対応

## 📁 ディレクトリ構造

```
docs/
├── index.md                      # トップページ
├── setup/
│   ├── installation.md           # インストール手順
│   └── connection.md             # 接続方法
├── usage/
│   ├── tools.md                  # 利用可能なツール
│   └── examples.md               # 使用例
├── development/
│   ├── custom-tools.md           # カスタムツールの追加
│   └── architecture.md           # アーキテクチャ
└── troubleshooting.md            # トラブルシューティング
```

## 🚀 使い方

### ローカルプレビュー

```bash
# 依存関係のインストール
pip install -r requirements-docs.txt

# 開発サーバーを起動
mkdocs serve
```

http://localhost:8000 でプレビューできます。

### ビルド

```bash
mkdocs build
```

静的 HTML ファイルが `site/` ディレクトリに生成されます。

### GitHub Pages へのデプロイ

main ブランチにプッシュすると、GitHub Actions が自動的にビルド・デプロイします。

ワークフロー: `.github/workflows/pages.yml`

## 📝 ドキュメントの編集

### 新しいページの追加

1. `docs/` ディレクトリに Markdown ファイルを作成
2. `mkdocs.yml` の `nav` セクションに追加

例:

```yaml
nav:
  - ホーム: index.md
  - 新しいページ: new-page.md
```

### フロントマターの使用

各 Markdown ファイルの先頭にメタデータを追加できます（オプション）:

```yaml
---
title: ページタイトル
description: ページの説明
---
```

### 記法

MkDocs は Markdown と Markdown 拡張をサポートしています:

#### コードブロック

\```python
def hello():
print("Hello, World!")
\```

#### アドモニション（注意書き）

```
!!! note "ノート"
    これは注意書きです。
```

種類: `note`, `info`, `warning`, `danger`, `success`, `tip`

#### タブ

\```
=== "Python"
\```python
print("Hello")
\```

=== "JavaScript"
\```javascript
console.log("Hello");
\```
\```

#### 表

```markdown
| 列 1 | 列 2 |
| ---- | ---- |
| A    | B    |
```

## 🛠️ カスタマイズ

### テーマの変更

`mkdocs.yml` で色やフォントを変更できます:

```yaml
theme:
  palette:
    primary: blue
    accent: indigo
```

### プラグインの追加

`mkdocs.yml` にプラグインを追加:

```yaml
plugins:
  - search
  - your-plugin
```

## 📚 参考リンク

- [MkDocs 公式ドキュメント](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Markdown 記法](https://www.markdownguide.org/)
