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
tipo_operacao = "aluguel"  # ou "venda"
tipo_imovel = "apartamento"
cidade = "governador-valadares"
bairro = "todos-os-bairros"
quartos = "0-quartos"
suites = "0-suite-ou-mais"
vagas = "0-vaga-ou-mais"
banheiros = "0-banheiro-ou-mais"
# Filtros adicionais
portaria = "sem-portaria-24horas"
lazer = "sem-area-lazer"
dce = "sem-dce"
mobilia = "sem-mobilia"
area_privativa = "sem-area-privativa"
area_servico = "sem-area-servico"
box = "sem-box-despejo"
circuito_tv = "sem-circuito-tv"

# Faixa de valores
valorminimo = 0
valormaximo = 0
pagina = 1

while True:
    # Montar URL da página atual
    url = (
        f"https://www.carlosamaralimoveis.com.br/{tipo_operacao}/{tipo_imovel}/{cidade}/{bairro}/"
        f"{quartos}/{suites}/{vagas}/{banheiros}/{portaria}/{lazer}/{dce}/{mobilia}/"
        f"{area_privativa}/{area_servico}/{box}/{circuito_tv}/?valorminimo={valorminimo}&valormaximo={valormaximo}&pagina={pagina}"
    )

    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # Aceitar cookies se o botão aparecer
    try:
        aceitar_cookies = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cc-dismiss")))
        aceitar_cookies.click()
        time.sleep(1)
    except:
        pass  # Se não aparecer, segue normalmente

    # Aguarda carregamento dos imóveis
    time.sleep(3)

    # Pegar todos os imóveis na página
    imoveis = driver.find_elements(By.CLASS_NAME, "col-12.col-sm-12.col-md-12.col-md-7.col-xl-7")
    if not imoveis:
        break

    for imovel in imoveis:
        try:
            titulo = imovel.find_element(By.TAG_NAME, "h5").text
            caracteristicas = imovel.find_elements(By.CLASS_NAME, "caracteristicas-card-imoveis")
            quartos = caracteristicas[0].text if len(caracteristicas) > 0 else ''
            banheiros = caracteristicas[2].text if len(caracteristicas) > 2 else ''
            vagas = caracteristicas[4].text if len(caracteristicas) > 4 else ''
            area = caracteristicas[6].text if len(caracteristicas) > 6 else ''
            preco = caracteristicas[8].text if len(caracteristicas) > 8 else ''
            link = imovel.find_element(By.TAG_NAME, "a").get_attribute("href")

            print(f"{titulo} | {quartos}Q | {banheiros}B | {vagas}V | {area}m² | {preco} | {link}")
        except Exception as e:
            print("Erro ao extrair imóvel:", e)

    pagina += 1

# Finaliza o navegador
driver.quit()
