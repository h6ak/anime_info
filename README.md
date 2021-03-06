# 概要
[アキバ総研](https://akiba-souken.com)をスクレイピングして、アニメの初回放送の情報をDBに格納する。

## 動作環境
- Python 3.5以上
- MySQL

## メインスクリプト
メインスクリプトは `anime_info/main.py` である。

### コマンドライン引数
- -f :htmlファイル名。開発時にWEBサイトのアクセス回数を減らすために使用

## 注意事項
[『アキバ総研サイト利用規約』](https://akiba-souken.com/help/rules/)の「第13条　禁止行為」で、
> 1. 当社は下記の行為を禁止事項と定め、お客様はこれを行わないこととします。
>
> （1） 法令上又は本規約上特に認められている場合を除き、全部または一部を問わず、 本サービスによって提供される情報を、当社の事前の同意なく、複写、再生、複製、送付、譲渡、頒布、配布、転売、送信、送信可能化、改変、翻案、翻訳、貸与、 またはこれらの目的で利用又は使用するために保管する行為

と書かれているので、スクレイピングで取得した情報を取り扱うには注意が必要である。
