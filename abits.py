from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import math
import time

# Configurar navegador (modo invisível)
options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
driver = webdriver.Chrome(options=options)

# Parâmetros da busca
cidade = "Governador Valadares - MG"
categoria = "6"
tipo_operacao = "venda"

# Acessar primeira página para pegar total de registros
url_base = (
    f"https://abits.com.br/pesquisa?transacao={tipo_operacao}"
    f"&cidade%5B%5D={cidade.replace(' ', '+')}"
    f"&categoria%5B%5D={categoria}"
    f"&estado_imovel%5B%5D=&faixa_valor_locacao=&faixa_valor_venda=&referencia="
)

driver.get(url_base)
time.sleep(2)

# Extrair total de registros
try:
    total_registros_text = driver.find_element(By.ID, "total_busca").text
    total_registros = int(total_registros_text.split()[0])
    imoveis_por_pagina = len(driver.find_elements(By.CLASS_NAME, "feat_property"))
    total_paginas = math.ceil(total_registros / imoveis_por_pagina)
except Exception as e:
    print("Erro ao obter total de registros:", e)
    driver.quit()
    exit()

# Loop por páginas
for pagina in range(1, total_paginas + 1):
    url = url_base + f"&page={pagina}"
    driver.get(url)
    time.sleep(2)

    imoveis = driver.find_elements(By.CLASS_NAME, "feat_property")

    for imovel in imoveis:
        try:
            link = imovel.get_attribute("onclick").split("'")[1]

            img_el = imovel.find_elements(By.CSS_SELECTOR, ".thumb img")
            img = img_el[0].get_attribute("src") if img_el else ''

            preco_el = imovel.find_elements(By.CLASS_NAME, "fp_price")
            preco = preco_el[0].text.strip() if preco_el else ''

            ref_el = imovel.find_elements(By.CLASS_NAME, "dtls_headr")
            ref = ref_el[0].text.strip() if ref_el else ''

            h4_elements = imovel.find_elements(By.TAG_NAME, "h4")
            titulo = h4_elements[1].text.strip() if len(h4_elements) > 1 else (h4_elements[0].text.strip() if h4_elements else '')

            p_elements = imovel.find_elements(By.TAG_NAME, "p")
            endereco = p_elements[1].text.strip() if len(p_elements) > 1 else (p_elements[0].text.strip() if p_elements else '')

            detalhes = imovel.find_elements(By.CLASS_NAME, "list-inline-item")
            quartos = detalhes[0].text if len(detalhes) > 0 else ''
            vagas = detalhes[1].text if len(detalhes) > 1 else ''

            print(f"{ref} | {titulo} | {endereco} | {quartos} | {vagas} | {preco} | {img} | {link}")
        except Exception as e:
            print("Erro ao extrair imóvel:", e)

driver.quit()
