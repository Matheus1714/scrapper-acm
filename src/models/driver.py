from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pathlib import Path

class BaseDriver:
    ...

class ChromeDriver(BaseDriver):

    def __init__(self) -> None:
        super().__init__()

        project_root = Path(__file__).parent.parent.parent
        chromedriver_path = project_root / "chromedriver"
        
        if chromedriver_path.exists():
            service = Service(str(chromedriver_path))
            self.driver = webdriver.Chrome(service=service)
        else:
            self.driver = webdriver.Chrome()
        
        self.driver.maximize_window()