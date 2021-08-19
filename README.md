# 概要
本を読んでいて感動した文章を投稿するwebサイト  
ブクエモ！：https://powerful-meadow-04553.herokuapp.com/  

# 使用技術
| 技術 | 採用理由・目的 |  
| ------------- | ------------- |  
| Flask | ルーティング, テーブル定義, 軽量, カスタムがしやすいため |  
| SQLAlchemy | sqliteとやり取り, ログイン情報管理, 開発の効率化のため |  
| pylance, flake8 | コード解析, コードフォーマットのため |  
| gunicorn | NginxとFlaskを接続, リソース消費が少ないため |  