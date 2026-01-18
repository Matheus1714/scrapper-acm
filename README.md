# Scrapper ACM

![Banner ACM](.github/banner.png)

This project aims to automate the retrieval of academic works from the ACM Digital Library for bibliographic research.

## Setup

### Pré-requisitos

- Python 3.9 ou superior
- pipenv instalado (`pip install pipenv`)

### Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd scrapper-acm
```

2. Instale as dependências usando pipenv:
```bash
pipenv install
```

3. Ative o ambiente virtual:
```bash
pipenv shell
```

4. (Opcional) Baixe o ChromeDriver localmente:
```bash
python download_chromedriver.py
```

O script irá:
- Detectar a versão do Chrome instalada no sistema
- Baixar a versão mais recente compatível do ChromeDriver
- Salvar o executável na pasta raiz do projeto

**Nota:** Se o ChromeDriver não for baixado localmente, o Selenium tentará usar o driver do sistema ou do PATH.

### Execução

Com o ambiente virtual ativado, execute o script:

```bash
python main.py
```

Ou execute diretamente com pipenv:

```bash
pipenv run python main.py
```

## Dependências

- selenium: Para automação do navegador
- webdriver-manager: Para gerenciamento automático dos drivers do Selenium
- requests: Para download do ChromeDriver (usado pelo script de download)