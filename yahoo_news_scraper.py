from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import pandas as pd
import urllib.parse as ul
import re

def exists(locator):
    return locator.count() > 0


with sync_playwright() as p:
    browser = None
    try:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        search_word = input("検索したいキーワード：")
        encoded_word = ul.quote(search_word)
        page.goto(f"https://news.yahoo.co.jp/search?p={encoded_word}&ei=utf-8")
        try:
            page.wait_for_selector("ol.newsFeed_list", timeout=5000)
        except PlaywrightTimeoutError:
            print("該当する記事は0件でした。")
        else:
            count_moreinfo = 2 #何回「もっと見る」をクリックするか
            moreinfo = page.locator('button[data-cl-params*= "cl_link:auto"]')
            block_articles = page.locator("ol.newsFeed_list")
            for i in range(count_moreinfo):
                if moreinfo.count() > 0:
                    prev_count = block_articles.locator("> li").count()
                    moreinfo.click()
                    block_articles.locator(">li").nth(prev_count).wait_for()
                else:
                    break
            articles = []
            for el in block_articles.locator('a[data-cl-params*="cl_link:title"]').all():
                fields = []
                texts = el.locator("div.newsFeed_item_body > div").nth(1)
                for j in range(3):
                    if exists(texts.locator("> div").nth(j)):
                        fields.append(texts.locator("> div").nth(j).text_content())
                    else:
                        fields.append("")
                url = el.get_attribute("href")
                articles.append({"記事のタイトル" : fields[0], "記事の概要" : fields[1], "配信元・日時" : fields[2], "URL": url})
            
            df_input = pd.DataFrame(articles) #辞書データを変換
            safe_word = re.sub(r'[\\/:*?"<>|]', '_', search_word)
            df_input.to_excel(f"yahoo_search_{safe_word}.xlsx", sheet_name = "検索した記事一覧", index = False) #エクセルファイルを作成
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        if browser is not None:
            browser.close()