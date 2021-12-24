from multiprocessing import freeze_support
from time import sleep
from parsel import Selector
from selenium import webdriver
import multiprocessing as m
import concurrent.futures
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import dynamodb
def scrap(current_task):
    # for index in range(length_total):
    ongoing_task = current_task
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    # options.add_argument("enable-automation")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("---maxSession=5")
    chrome = DesiredCapabilities.CHROME
    driver = webdriver.Remote(command_executor="http://15.164.226.76:4444", desired_capabilities=chrome,
                              options=options)
    ongoing_task = dynamodb.get_item_by_id(current_task)
    print(ongoing_task)
    if len(ongoing_task) == 1:
        task_id = [task["task_id"] for task in ongoing_task][0]
        job_id = [job["job_id"] for job in ongoing_task][0]
        xpath_link = [xpath_link["xpath_link"] for xpath_link in ongoing_task][0]
        rule_data = [rule_data["rule_data"] for rule_data in ongoing_task][0]
        # print(rule_data)
        if 'javascript' not in xpath_link:
            driver.get(xpath_link)
            selector2 = Selector(driver.page_source)
            title = selector2.xpath(f'{rule_data}/text()').get()
            dynamodb.update_item(task_id, job_id, "completed", xpath_link, rule_data)
            print(task_id, "HAS COMPLETED")
            dynamodb.input_item(job_id, task_id, title, xpath_link)
        else:
            print("it is error found")
            dynamodb.update_item(task_id, job_id, "completed", xpath_link, rule_data)
        driver.quit()

if __name__ == "__main__":

    result = []
    task_id_list = []
    index = 0
    length_total = dynamodb.get_count_item("ongoing")
    indexs = 0
    indexss = 10
    with concurrent.futures.ProcessPoolExecutor() as executor:
        current_task_list = dynamodb.get_an10_item("ongoing")
        # print(current_task_list)
        current_tasks = [task["task_id"] for task in current_task_list]
        print(current_tasks)
        results =[executor.submit(scrap, current_task) for current_task in current_tasks]
        for result in results:
            print(result)