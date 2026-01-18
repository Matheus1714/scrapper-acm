from src.models.driver import ChromeDriver
from src.models.elements import SeleniumElement, List
from src.drivers.DRIVER_ACM import DRIVER_DICT
from selenium.webdriver.common.by import By

import csv
import time

class ACM(ChromeDriver):

    def __init__(self) -> None:
        super().__init__()

        driver_dict = DRIVER_DICT

        self.url = driver_dict.get('url_search')

        self.list_result = List(self.driver, driver_dict.get('list_result'))

        self.pagination = SeleniumElement(self.driver, driver_dict.get('pagination'))
        self.number_of_pages = SeleniumElement(self.driver, driver_dict.get('number_of_pages'))
        
        self.data_dicts = driver_dict.get('data_dicts')
    
    def get_page_number(self):
        try:
            number_of_pages_element = self.number_of_pages.get_element()
            number_of_pages = int(number_of_pages_element.text)
            return number_of_pages
        except:
            return 1
    
    def get_data(self)->dict:
        data = {}
        for work_dict in self.data_dicts:
            se = SeleniumElement(self.driver, work_dict)
            element = se.get_element()

            name = work_dict.get('name')
            content = '' if element is None else element.text

            data[name] = content
        
        data['url'] = self.driver.current_url

        return data
    
    def save_csv(self, works:list, file_name:str = 'acm.csv'):
        csv_file = file_name
        fieldnames = ["title", "abstract", "doi", "url"]

        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(works)
        
        print(f"CSV file '{csv_file}' created successfully.")

    def main(self):
        self.driver.get(self.url)

        number_of_pages = self.get_page_number()
        page_number = 0

        works = []

        while page_number < number_of_pages:
            time.sleep(3)
            number_of_items = len(self.list_result.get_items())

            for index in range(number_of_items):
                items = self.list_result.get_items()

                item = items[index]
                time.sleep(1)
                work_link = item.find_element(By.XPATH, './/*[contains(@class, "title")]//a')
                try:
                    work_link.click()
                except:
                    self.driver.execute_script("arguments[0].click()", work_link)

                time.sleep(3)

                data = self.get_data()
                works.append(data)

                self.driver.back()

                time.sleep(3)

            if page_number != number_of_pages - 1:
                pagination = self.pagination.get_element()
                try:
                    pagination.click()
                except:
                    self.driver.execute_script("arguments[0].click()", pagination)

            time.sleep(3)

            page_number += 1

            number_of_pages = self.get_page_number()
    
            self.save_csv(works, file_name = f'acm_page_{page_number}.csv')