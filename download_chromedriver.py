#!/usr/bin/env python3
"""
Script para baixar a versão mais recente do ChromeDriver e salvá-lo na pasta raiz do projeto.
"""

import os
import sys
import platform
import subprocess
import zipfile
import tarfile
import requests
from pathlib import Path

# URL base para o ChromeDriver
CHROMEDRIVER_BASE_URL = "https://chromedriver.storage.googleapis.com"
CHROMEDRIVER_LATEST_URL = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"


def get_chrome_version():
    """Detecta a versão do Chrome instalada no sistema."""
    system = platform.system().lower()
    
    try:
        if system == "darwin":  # macOS
            # Tenta diferentes caminhos do Chrome no macOS
            chrome_paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium"
            ]
            
            for chrome_path in chrome_paths:
                if os.path.exists(chrome_path):
                    result = subprocess.run(
                        [chrome_path, "--version"],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if result.returncode == 0:
                        version = result.stdout.strip().split()[-1]
                        return version.split('.')[0]  # Retorna major version
        
        elif system == "linux":
            result = subprocess.run(
                ["google-chrome", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                version = result.stdout.strip().split()[-1]
                return version.split('.')[0]
        
        elif system == "windows":
            # Windows
            import winreg
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Google\Chrome\BLBeacon"
                )
                version, _ = winreg.QueryValueEx(key, "version")
                winreg.CloseKey(key)
                return version.split('.')[0]
            except:
                pass
    
    except Exception as e:
        print(f"Erro ao detectar versão do Chrome: {e}")
    
    return None


def get_latest_chromedriver_version():
    """Obtém a versão mais recente do ChromeDriver disponível."""
    try:
        response = requests.get(CHROMEDRIVER_LATEST_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Pega a versão estável mais recente
        stable_version = data.get("channels", {}).get("Stable", {}).get("version")
        return stable_version
    except Exception as e:
        print(f"Erro ao obter versão mais recente: {e}")
        return None


def get_chromedriver_download_url(version):
    """Obtém a URL de download do ChromeDriver para a versão especificada."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # Mapeia a arquitetura
    if machine in ["x86_64", "amd64"]:
        arch = "x64"
    elif machine in ["arm64", "aarch64"]:
        arch = "arm64"
    else:
        arch = "x64"  # default
    
    # Determina o sistema operacional e extensão
    if system == "darwin":  # macOS
        os_name = "mac"
        if arch == "arm64":
            os_arch = "mac-arm64"
        else:
            os_arch = "mac-x64"
        ext = "zip"
    elif system == "linux":
        os_name = "linux"
        os_arch = f"linux-{arch}"
        ext = "zip"
    elif system == "windows":
        os_name = "win"
        os_arch = f"win-{arch}"
        ext = "zip"
    else:
        raise ValueError(f"Sistema operacional não suportado: {system}")
    
    # URL do Chrome for Testing
    url = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{version}/{os_arch}/chromedriver-{os_arch}.{ext}"
    
    return url, ext


def download_file(url, filepath):
    """Baixa um arquivo da URL especificada."""
    print(f"Baixando ChromeDriver de: {url}")
    
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    
    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\rProgresso: {percent:.1f}%", end='', flush=True)
    
    print()  # Nova linha após o progresso
    return filepath


def extract_chromedriver(archive_path, extract_to, ext):
    """Extrai o ChromeDriver do arquivo compactado."""
    print(f"Extraindo ChromeDriver de {archive_path}...")
    
    if ext == "zip":
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif ext == "tar.gz":
        with tarfile.open(archive_path, 'r:gz') as tar_ref:
            tar_ref.extractall(extract_to)
    
    # Remove o arquivo compactado
    os.remove(archive_path)
    
    # Encontra o executável do ChromeDriver
    for root, dirs, files in os.walk(extract_to):
        for file in files:
            if file == "chromedriver" or file == "chromedriver.exe":
                chromedriver_path = os.path.join(root, file)
                # Move para a pasta raiz
                final_path = os.path.join(extract_to, file)
                if chromedriver_path != final_path:
                    if os.path.exists(final_path):
                        os.remove(final_path)
                    os.rename(chromedriver_path, final_path)
                
                # Remove diretórios vazios
                try:
                    if os.path.exists(root) and root != extract_to:
                        os.rmdir(root)
                except:
                    pass
                
                return final_path
    
    return None


def make_executable(filepath):
    """Torna o arquivo executável (Unix/Linux/macOS)."""
    if platform.system() != "windows":
        os.chmod(filepath, 0o755)


def main():
    """Função principal."""
    print("=" * 60)
    print("Download do ChromeDriver")
    print("=" * 60)
    
    # Pasta raiz do projeto
    project_root = Path(__file__).parent
    chromedriver_path = project_root / "chromedriver"
    
    # Se já existe, pergunta se quer substituir
    if chromedriver_path.exists():
        response = input(f"ChromeDriver já existe em {chromedriver_path}. Deseja substituir? (s/N): ")
        if response.lower() != 's':
            print("Operação cancelada.")
            return
        os.remove(chromedriver_path)
    
    # Tenta detectar versão do Chrome
    chrome_version = get_chrome_version()
    if chrome_version:
        print(f"Versão do Chrome detectada: {chrome_version}")
    
    # Obtém a versão mais recente do ChromeDriver
    print("Obtendo versão mais recente do ChromeDriver...")
    latest_version = get_latest_chromedriver_version()
    
    if not latest_version:
        print("Erro: Não foi possível obter a versão mais recente do ChromeDriver.")
        sys.exit(1)
    
    print(f"Versão mais recente do ChromeDriver: {latest_version}")
    
    # Obtém URL de download
    try:
        download_url, ext = get_chromedriver_download_url(latest_version)
    except Exception as e:
        print(f"Erro ao obter URL de download: {e}")
        sys.exit(1)
    
    # Cria arquivo temporário
    temp_file = project_root / f"chromedriver_temp.{ext}"
    
    try:
        # Baixa o arquivo
        download_file(download_url, temp_file)
        
        # Extrai o ChromeDriver
        chromedriver_extracted = extract_chromedriver(temp_file, project_root, ext)
        
        if chromedriver_extracted:
            # Renomeia se necessário
            if chromedriver_extracted != str(chromedriver_path):
                if chromedriver_path.exists():
                    os.remove(chromedriver_path)
                os.rename(chromedriver_extracted, chromedriver_path)
            
            # Torna executável
            make_executable(chromedriver_path)
            
            print(f"\n✓ ChromeDriver baixado com sucesso!")
            print(f"  Localização: {chromedriver_path}")
            print(f"  Versão: {latest_version}")
        else:
            print("Erro: Não foi possível extrair o ChromeDriver.")
            sys.exit(1)
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar ChromeDriver: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        sys.exit(1)
    finally:
        # Remove arquivo temporário se ainda existir
        if temp_file.exists():
            os.remove(temp_file)


if __name__ == "__main__":
    main()
