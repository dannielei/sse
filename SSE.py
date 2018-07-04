from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from pyquery import PyQuery as pq


browser=webdriver.Chrome()
wait=WebDriverWait(browser, 5)


def search():
    try:
        browser.get('http://www.sse.com.cn/disclosure/listedinfo/announcement/')

        js1 = "document.getElementById('start_date').removeAttribute('readonly')"
        browser.execute_script(js1)
        start = browser.find_element_by_css_selector('#start_date').send_keys('2017-04-11')
        browser.switch_to.frame(start)
        sleep(2)

        js2 = "document.getElementById('end_date').removeAttribute('readonly')"
        browser.execute_script(js2)
        end = browser.find_element_by_css_selector('#end_date').send_keys('2017-04-25')
        browser.switch_to.frame(end)
        sleep(2)

        key = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                            'body > div.page_content.bgimg1 > div.container > div:nth-child(2) > div.col-sm-9 > div > div > div > div > div.sse_wrap_cn_con > div.sse_con_query.clearfix.js_Search.search_jumpj.searchJ.announcement_L > div.input-group > input')))
        key.send_keys('停牌')

        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btnQuery')))
        submit.click()
        # get_products()


    except TimeoutException:
        return search()


def next_page(page):
    try:
        next = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.classPage') and (By.CSS_SELECTOR, "[page='{}']".format(page))))
        next.click()
        sleep(2)
        get_products()
        return True
    except:
        return False


def get_products():
    html=browser.page_source
    doc=pq(html)

    items=doc('.just_this_only').items()
    for item in items:
        product={
            'href':item.find('.hidden-xs').attr('href'),
            'title': item.find('[href]').text()
        }
        print(product)


def main():
    search()

    sleep(2)
    get_products()
    print('1')

    for page in range(2, 100):
        check = next_page(page)
        if not check:
            break
        print('click next page: {}'.format(page))

    # get_products()





if __name__ == '__main__':
    main()

