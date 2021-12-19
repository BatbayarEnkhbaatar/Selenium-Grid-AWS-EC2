from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from tqdm import trange
import pandas as pd
from parsel import Selector
from urllib.parse import urljoin
import json
import csv
import uuid
import boto3

with open('../saas_dcinside_rule.json', 'r') as f:
    js = json.load(f)
options = webdriver.ChromeOptions()
options.add_argument('--user-agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36')
options.add_argument('--headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')

url = 'https://gall.dcinside.com/board/lists?id=dcbest'
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
driver.get(url)
sleep(1)

start = int(js['data'][0]['page_info']['start'])
end = int(js['data'][0]['page_info']['end'])

start_index = js['data'][0]['item'][0]['select_info']['startIdx']
index_size = js['data'][0]['item'][0]['select_info']['size']
end_index = start_index + index_size

result = []
tasks  = []
for page in trange(start, end+1):
    url = f'https://gall.dcinside.com/board/lists/?id=dcbest&page={page}'
    driver.get(url)
    sleep(1)
    selector = Selector(driver.page_source)
    # print(selector)
    # print(type(selector))
    href_list = []
    for index in range(start_index, end_index):
        href_full_xpath = js['data'][0]['item'][0]['select_info']['xpathFull']
        href_full_xpath = href_full_xpath.replace('|', str(index))
        href = selector.xpath(f'{href_full_xpath}/@href').get()
        href_list.append(urljoin(url, href))

    for href_item in href_list:
        if 'javascript' not in href:
            # driver.get(href)
            # sleep(0.5)
            # selector = Selector(driver.page_source)
            extract_full_xpath = js['data'][0]['item'][0]['click_data'][0]['item'][0]['select_info']['xpathFull']
            task_id = uuid.uuid4()
            tasks.append({
                "ID": str(task_id),
                "Link": href_item,
                "rule_data" : extract_full_xpath
            })

# Export job list as json file
# with open("tasks.json", "w", encoding="utf-8") as outcomes:
#     json.dump(tasks, outcomes, ensure_ascii=False)

# Table name
# table_name = "Spiderkim-JobDB"
# endpoint_url = "http://localhost:8000/"
#
# dynamodb = boto3.resource("dynamodb", endpoint_url= endpoint_url)
# dynamodbTable = dynamodb.Table(table_name)
list_href_length = len(href_list)
length = len(tasks)
indx =0
print("href_list", length)
print("href_list", list_href_length)
while indx < length:
    print(f"Task{indx}: ", tasks[indx])
    indx += 1
#     # dynamodbTable.put_item(
#     #     Item={
#     #         "task_id": "task_id_1",
#     #         "job_id": "job_id_1",
#     #         "status": "REGISTERED",
#     #         "rule_data": "{\"version\":\"2.0.0\",\"totalExt\":5,\"data\":[{\"parent_info\":{\"selector\":\"#srplist\",\"xpath\":\"//*[@id='srplist']\",\"xpathFull\":\"/html/body/div[9]/div[1]/div[2]/div[5]/table/tbody\",\"tag\":\"tbody\",\"id\":\"srplist\",\"class\":\"\",\"index\":4},\"item\":[{\"type\":\"extract\",\"loop\":true,\"select_info\":{\"selector\":\"#srplist > tr:nth-child(|) > td:nth-child(1) > div > a > img\",\"xpath\":\"//*[@id='srplist']/tr[|]/td[1]/div/a/img\",\"xpathFull\":\"/html/body/div[9]/div[1]/div[2]/div[5]/table/tbody/tr[|]/td[1]/div/a/img\",\"tag\":\"img\",\"id\":\"\",\"class\":\"thumb_nail\",\"index\":1,\"size\":60,\"searchKey\":\"a:nth-child(1) > img.thumb_nail\",\"startIdx\":1},\"order\":1,\"columnName\":\"data1\"},{\"type\":\"extract\",\"loop\":true,\"select_info\":{\"selector\":\"#srplist > tr:nth-child(|) > td:nth-child(3) > ul > li.discount_price > a\",\"xpath\":\"//*[@id='srplist']/tr[|]/td[3]/ul/li[2]/a\",\"xpathFull\":\"/html/body/div[9]/div[1]/div[2]/div[5]/table/tbody/tr[|]/td[3]/ul/li[2]/a\",\"tag\":\"a\",\"id\":\"\",\"class\":\"\",\"index\":1,\"size\":60,\"searchKey\":\"li.discount_price > a\",\"startIdx\":1},\"order\":2,\"columnName\":\"data2\"},{\"type\":\"extract\",\"loop\":true,\"select_info\":{\"selector\":\"#srplist > tr:nth-child(|) > td.special_offer > span\",\"xpath\":\"//*[@id='srplist']/tr[|]/td[4]/span\",\"xpathFull\":\"/html/body/div[9]/div[1]/div[2]/div[5]/table/tbody/tr[|]/td[4]/span\",\"tag\":\"span\",\"id\":\"\",\"class\":\"\",\"index\":2,\"size\":55,\"searchKey\":\"td.special_offer > span\",\"startIdx\":1},\"order\":3,\"columnName\":\"data4\"}],\"page_info\":{\"parent_info\":{\"selector\":\"#searchlist_paging\",\"xpath\":\"//*[@id='searchlist_paging']\",\"xpathFull\":\"/html/body/div[9]/div[1]/div[2]/div[5]/div\",\"tag\":\"div\",\"id\":\"searchlist_paging\",\"class\":\"paging\",\"index\":2},\"select_info\":[{\"selector\":\"#searchlist_paging > span\",\"xpath\":\"//*[@id='searchlist_paging']/span\",\"xpathFull\":\"/html/body/div[9]/div[1]/div[2]/div[5]/div/span\",\"tag\":\"span\",\"id\":\"\",\"class\":\"\",\"index\":2,\"value\":\"1\"},{\"selector\":\"#searchlist_paging > a:nth-child(3)\",\"xpath\":\"//*[@id='searchlist_paging']/a[2]\",\"xpathFull\":\"/html/body/div[9]/div[1]/div[2]/div[5]/div/a[2]\",\"tag\":\"a\",\"id\":\"\",\"class\":\"\",\"index\":3,\"value\":\"2\"},{\"selector\":\"#searchlist_paging > a:nth-child(4)\",\"xpath\":\"//*[@id='searchlist_paging']/a[3]\",\"xpathFull\":\"/html/body/div[9]/div[1]/div[2]/div[5]/div/a[3]\",\"tag\":\"a\",\"id\":\"\",\"class\":\"\",\"index\":4,\"value\":\"3\"}],\"type\":\"button\"}},{\"item\":[{\"type\":\"extract\",\"loop\":false,\"select_info\":{\"selector\":\"#srplist > tr:nth-child(1) > td:nth-child(5)\",\"xpath\":\"//*[@id='srplist']/tr[1]/td[5]\",\"xpathFull\":\"/html/body/div[9]/div[1]/div[2]/div[5]/table/tbody/tr[1]/td[5]\",\"tag\":\"td\",\"id\":\"\",\"class\":\"center\",\"index\":5,\"size\":1},\"order\":4,\"columnName\":\"data3\"}],\"page_info\":{\"parent_info\":{\"selector\":\"#searchlist_paging\",\"xpath\":\"//*[@id='searchlist_paging']\",\"xpathFull\":\"/html/body/div[9]/div[1]/div[2]/div[5]/div\",\"tag\":\"div\",\"id\":\"searchlist_paging\",\"class\":\"paging\",\"index\":2},\"select_info\":[{\"selector\":\"#searchlist_paging > span\",\"xpath\":\"//*[@id='searchlist_paging']/span\",\"xpathFull\":\"/html/body/div[9]/div[1]/div[2]/div[5]/div/span\",\"tag\":\"span\",\"id\":\"\",\"class\":\"\",\"index\":2,\"value\":\"1\"},{\"selector\":\"#searchlist_paging > a:nth-child(3)\",\"xpath\":\"//*[@id='searchlist_paging']/a[2]\",\"xpathFull\":\"/html/body/div[9]/div[1]/div[2]/div[5]/div/a[2]\",\"tag\":\"a\",\"id\":\"\",\"class\":\"\",\"index\":3,\"value\":\"2\"},{\"selector\":\"#searchlist_paging > a:nth-child(4)\",\"xpath\":\"//*[@id='searchlist_paging']/a[3]\",\"xpathFull\":\"/html/body/div[9]/div[1]/div[2]/div[5]/div/a[3]\",\"tag\":\"a\",\"id\":\"\",\"class\":\"\",\"index\":4,\"value\":\"3\"}],\"type\":\"button\"}},{\"item\":[{\"type\":\"extract\",\"loop\":false,\"select_info\":{\"selector\":\"#srplist > tr:nth-child(1) > td.special_offer > strong\",\"xpath\":\"//*[@id='srplist']/tr[1]/td[4]/strong\",\"xpathFull\":\"/html/body/div[9]/div[1]/div[2]/div[5]/table/tbody/tr[1]/td[4]/strong\",\"tag\":\"strong\",\"id\":\"\",\"class\":\"cpp_icon\",\"index\":1,\"size\":1},\"order\":5,\"columnName\":\"data5\"}],\"page_info\":{\"parent_info\":{\"selector\":\"#searchlist_paging\",\"xpath\":\"//*[@id='searchlist_paging']\",\"xpathFull\":\"/html/body/div[9]/div[1]/div[2]/div[5]/div\",\"tag\":\"div\",\"id\":\"searchlist_paging\",\"class\":\"paging\",\"index\":2},\"select_info\":[{\"selector\":\"#searchlist_paging > span\",\"xpath\":\"//*[@id='searchlist_paging']/span\",\"xpathFull\":\"/html/body/div[9]/div[1]/div[2]/div[5]/div/span\",\"tag\":\"span\",\"id\":\"\",\"class\":\"\",\"index\":2,\"value\":\"1\"},{\"selector\":\"#searchlist_paging > a:nth-child(3)\",\"xpath\":\"//*[@id='searchlist_paging']/a[2]\",\"xpathFull\":\"/html/body/div[9]/div[1]/div[2]/div[5]/div/a[2]\",\"tag\":\"a\",\"id\":\"\",\"class\":\"\",\"index\":3,\"value\":\"2\"},{\"selector\":\"#searchlist_paging > a:nth-child(4)\",\"xpath\":\"//*[@id='searchlist_paging']/a[3]\",\"xpathFull\":\"/html/body/div[9]/div[1]/div[2]/div[5]/div/a[3]\",\"tag\":\"a\",\"id\":\"\",\"class\":\"\",\"index\":4,\"value\":\"3\"}],\"type\":\"button\"}}]}",
#     #         "url": "http://gcategory.gmarket.co.kr/Listview/Category?GdlcCd=100000043",
#     #         "job_type": "entry",
#     #         "max_page": 5
#     #         "status": "in processing"
#     #     }
#     #
#     # )
#
print("Totally", length, "tasks successfully imported to DynamoDB ")