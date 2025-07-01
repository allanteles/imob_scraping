from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurar navegador (modo invisível)
options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
driver = webdriver.Chrome(options=options)

# Parâmetros da busca
cidade = "Governador Valadares"
tipo_imovel = "Casa"  # Ex: Casa, Apartamento
tipo_operacao = "locacao"  # locacao ou venda
pagina = 1

while True:
    # Montar URL com parâmetros
    url = (
        f"https://certaimoveis.com.br/encontrar/?template_result_list=content/result-imoveis&range=valor,dorm,suites"
        f"&para={tipo_operacao}&refs=&cidade={cidade.replace(' ', '%20')}&tipo={tipo_imovel}&valor=&_valor=&page={pagina}"
    )

    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # Aguarda carregamento dos imóveis
    time.sleep(3)

    # Encontrar imóveis
    imoveis = driver.find_elements(By.CLASS_NAME, "item-imovel-result")
    if not imoveis:
        break

    for imovel in imoveis:
        try:
            link = imovel.find_element(By.CSS_SELECTOR, "a.item-imovel-result-body").get_attribute("href")
            detalhes = imovel.find_element(By.CLASS_NAME, "item-imovel-result-detalhes")
            titulo = detalhes.find_element(By.CLASS_NAME, "item-imovel-result-ref").text.strip()
            bairro = detalhes.find_element(By.CLASS_NAME, "item-imovel-result-bairro").text.strip()
            descricao = detalhes.find_element(By.CLASS_NAME, "item-imovel-result-descricao").text.strip()
            preco = detalhes.find_element(By.CLASS_NAME, "item-imovel-result-valor").text.strip()

            # Características
            footer = imovel.find_element(By.CLASS_NAME, "item-imovel-result-footer")
            caracteristicas = footer.find_elements(By.TAG_NAME, "span")
            quartos = caracteristicas[0].text if len(caracteristicas) > 0 else ''
            suites = caracteristicas[1].text if len(caracteristicas) > 1 else ''
            banheiros = caracteristicas[2].text if len(caracteristicas) > 2 else ''
            vagas = caracteristicas[3].text if len(caracteristicas) > 3 else ''
            area = caracteristicas[4].text if len(caracteristicas) > 4 else ''

            print(f"{titulo} | {bairro} | {quartos} | {suites} | {banheiros} | {vagas} | {area} | {preco} | {link}")
        except Exception as e:
            print("Erro ao extrair imóvel:", e)

    pagina += 1

# Finaliza o navegador
driver.quit()
