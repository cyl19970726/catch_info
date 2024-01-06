from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

# 网址
url = 'https://b.csgmall.com.cn/mall-view/product/search?keyword=%E9%BD%90%E5%BF%83'
next_url = 'https://b.csgmall.com.cn/mall-view/product/search?keyword=%E9%BD%90%E5%BF%83'

# 设置Selenium WebDriver
# 这里假设 chromedriver 已经在您的 PATH 中
driver = webdriver.Chrome()


try:
    # 创建一个空的DataFrame
    df = pd.DataFrame(columns=['Item ID', 'Sales Volume', 'Price', 'Old Price', 'Title'])

    driver.get(next_url)
    cookies = driver.get_cookies()
    print("Cookies:", cookies)

    while True:
        # 为当前会话添加保存的 Cookie
        for cookie in cookies:
            driver.add_cookie(cookie)


        # 等待网页动态加载内容，这里等待10秒
        # 根据您网页的加载速度，您可能需要调整这个时间
        time.sleep(10)

        # 获取网页的源代码
        html = driver.page_source

        # 使用 BeautifulSoup 解析网页
        soup = BeautifulSoup(html, 'html.parser')

        # 找到商品信息的元素，这里的选择器可能需要调整
        good_list_box = soup.find('div', class_='goods-list-box')
        goods = good_list_box.find_all('li', class_='goods-item')

        for item in goods:
            item_id = item['data-item-id']
            sales_volume = item.find('span', class_='shop-sales-volume').text
            price = item.find('p', class_='price').find('i').text
            old_price = item.find('span', class_='oldPrice').find('i').text
            title = item.find('h3', class_='title').find('a')['title']
            
            # 将数据添加到DataFrame的一行
            
            df = df._append({'Item ID': item_id, 'Sales Volume': sales_volume, 'Price': price, 'Old Price': old_price, 'Title': title}, ignore_index=True)

            # print(f"Item ID: {item_id}")
            # print(f"Sales Volume: {sales_volume}")
            # print(f"Price: {price}")
            # print(f"Old Price: {old_price}")
            # print(f"Title: {title}")
            # print("=====================================================================================================")

        # jump to next page 
        try:
    
            next_page_button = driver.find_element('css selector', '.layui-laypage-next')
            # next_page_button.click()
            
            # Get the page number of the next page
            next_page_number = next_page_button.get_attribute('data-page')
            
            print(f"Next page number: {next_page_number}")
            # Append the page number to the URL
            next_url = url + f'&pageNum={next_page_number}'
            print(next_url)
            driver.get(next_url)
        except NoSuchElementException:
            print("No more pages.")
            break

finally:

    # 关闭浏览器
    driver.quit()
    # 将DataFrame保存为Excel文件
    df.to_excel('./record2.xlsx', index=False)
    
