from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import os

class BaseDriver:
    ...

class ChromeDriver(BaseDriver):

    def __init__(self, user_data_dir: str = None, profile_directory: str = "Default") -> None:
        """
        Inicializa o ChromeDriver com opções para evitar detecção do Cloudflare.
        
        Args:
            user_data_dir: Caminho para o diretório de dados do usuário do Chrome.
                          Se None, usa o perfil padrão do Chrome.
                          Exemplo no macOS: ~/Library/Application Support/Google/Chrome
            profile_directory: Nome do perfil a ser usado (padrão: "Default")
        """
        super().__init__()

        project_root = Path(__file__).parent.parent.parent
        chromedriver_path = project_root / "chromedriver"
        
        # Configurar opções do Chrome
        chrome_options = Options()
        
        # Se user_data_dir foi fornecido, usar o perfil do Chrome
        if user_data_dir:
            user_data_dir = os.path.expanduser(user_data_dir)  # Expande ~ para o caminho completo
            chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
            chrome_options.add_argument(f"--profile-directory={profile_directory}")
        
        # Opções para evitar detecção de automação
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Outras opções úteis
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        
        # Inicializar o driver
        if chromedriver_path.exists():
            service = Service(str(chromedriver_path))
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            self.driver = webdriver.Chrome(options=chrome_options)
        
        # Executar script para remover propriedades que indicam automação
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.driver.maximize_window()