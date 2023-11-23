from selenium.webdriver.common.by import By
from settings import URL_SEARCH

DRIVER_DICT = {
    'url_search': URL_SEARCH,
    'list_result': {
        'identifier': '//ul[contains(@class, "items-results")]',
        'identifier_type': By.XPATH,
        'tag': 'ul',
        'items': {
            'identifier': '//li[contains(@class, "item-container")]',
            'identifier_type': By.XPATH,
            'tag': 'li',
        }
    },
    'pagination': {
        'identifier': '//a[contains(@class, "pagination") and contains(@class, "next")]',
        'identifier_type': By.XPATH,
        'tag': 'a',
    },
    'number_of_pages': {
        'identifier': '//ul[contains(@class, "pagination") and contains(@class, "list")]/li[last()]',
        'identifier_type': By.XPATH,
        'tag': 'li',
    },
    'data_dicts':[
        {
            'name': 'title',
            'identifier': '//*[contains(@class, "title") and contains(@class, "citation")]',
            'identifier_type': By.XPATH,
            'tag': '',
        },
        {
            'name': 'abstract',
            'identifier': '//*[contains(@class, "abstractSection")]',
            'identifier_type': By.XPATH,
            'tag': '',
        },
        {
            'name': 'doi',
            'identifier': '//*[contains(@class, "doi") and contains(@class, "item")]',
            'identifier_type': By.XPATH,
            'tag': '',
        }
    ]
}