# Yahoo_News_Scraper
YahooNEWSのスクレイピングツールです。
実行し、検索ワードを入力していただければヒットした記事のタイトル、概要、配信元と日時、URLを最大で150件分まとめ、1つのExcelファイルにて出力します。

使用技術（Python / Playwright / Pandas）

このファイルニは外部ライブラリが使用されています。そのため、ターミナルにて保存先のフォルダを参照し、メインファイル実行前に
pip install playwright pandas openpyxl
playwright install chromium
この二行を実行して下さい。その後、
py yahoo_news_scraper.py
を実行すると、
検索したいキーワード：
と出るため、そこに検索ワードを入力して下さい。
実行すると、数秒から数十秒後にエクセルファイルが同ファイルに保存されます。
ファイル名はyahoo_search_検索ワード.xlsxとなっています。
