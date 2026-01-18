from src.models.crawler import BaseCrawler

class SeleniumElement(BaseCrawler):
    def __init__(self, driver, driver_dict: dict = {}) -> None:

        super().__init__(driver)

        self.identifier = driver_dict.get('identifier')
        self.identifier_type = driver_dict.get('identifier_type')
        self.tag = driver_dict.get('tag')
    
    def get_element(self):
        try:
            return self.driver.find_element(self.identifier_type, self.identifier)
        except:
            return None

class List(SeleniumElement):

    def __init__(self, driver, driver_dict: dict = {}) -> None:
        super().__init__(driver, driver_dict)

        self.items = SeleniumElement(driver, driver_dict.get('items'))
    
    def get_items(self):
        try:
            list_result = self.get_element()
            return list_result.find_elements(self.items.identifier_type, self.items.identifier)
        except:
            return []