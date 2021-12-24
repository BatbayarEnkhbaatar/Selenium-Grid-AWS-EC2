from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from tqdm import trange
from parsel import Selector
from urllib.parse import urljoin
import json
import uuid
import boto3
import putintem

dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000/")
dynamodbTable = dynamodb.Table("Spiderkim-JobDB")

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
                "xpath_link": href_item,
                "rule_data" : extract_full_xpath
            })

list_href_length = len(href_list)
length = len(tasks)
indx = 0
#print("href_list", length)
#print("href_list", list_href_length)
job_id = "job_id_001"
task_status = "ongoing"
task_ids = [task["ID"] for task in tasks]
task_urls = [link["xpath_link"] for link in tasks ]
task_rule_data = [rule_data["rule_data"] for rule_data in tasks]

for i in range(length):
    putintem.dyna_input_item(job_id, task_ids[i], task_status, task_rule_data[i], task_urls[i])
    # print("Inserted ", task_ids[i])
print("Totally", length, "tasks successfully imported to DynamoDB ")


##  aws dynamodb scan --table-name jobs_database --select "COUNT" --endpoint http://localhost:4566/dynamodb



