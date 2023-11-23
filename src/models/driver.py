from selenium import webdriver

class BaseDriver:
    ...

class ChromeDriver(BaseDriver):

    def __init__(self) -> None:
        super().__init__()

        self.driver = webdriver.Chrome()
        self.driver.maximize_window()