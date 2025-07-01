from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

# Configuração
options = Options()
options.add_argument("--headless")  # comente essa linha se quiser ver o navegador
driver = webdriver.Chrome(options=options)

# Abrir site
driver.get("https://www.perimimoveis.com.br")
time.sleep(2)

# Clica no botão "Comprar"
#botao_comprar = driver.find_element(By.ID, "BtCheckLocacao")
botao_comprar = driver.find_element(By.ID, "BtCheckVenda")
driver.execute_script("arguments[0].click();", botao_comprar)
#botao_comprar.click()
time.sleep(1)

# Oculta o iframe do chatbot
driver.execute_script("""
    let iframe = document.querySelector('#gbt-frame');
    if (iframe) {
        iframe.style.display = 'none';
    }
""")


# Seleciona filtros
tipo_select = Select(driver.find_element(By.ID, "TIPOIMO"))
tipo_select.select_by_visible_text("Casa")

quartos_select = Select(driver.find_element(By.ID, "QUARTOS"))
quartos_select.select_by_value("2")

driver.find_element(By.ID, "VALORMINIMO").send_keys("30000000")
driver.find_element(By.ID, "VALORMAXIMO").send_keys("50000000")

# Clica em buscar
buscar = driver.find_element(By.NAME, "buscar")
driver.execute_script("arguments[0].click();", buscar)
# time.sleep(2)

pagina = 1

while True:
    print(f"\n📄 Página {pagina}")
    # time.sleep(2)

    # Captura os imóveis da página atual
    imoveis = driver.find_elements(By.CLASS_NAME, "box_imovel_list_conteudo")
    
    for imovel in imoveis:
        try:
            codigo = imovel.find_element(By.XPATH, ".//div[@class='col-xs-4']/strong").text
            preco = imovel.find_element(By.XPATH, ".//div[@class='col-xs-8 text-right']/strong").text
            local = imovel.find_elements(By.CLASS_NAME, "col-xs-12")[0].text
            tipo = imovel.find_elements(By.CLASS_NAME, "col-xs-12")[1].text
            link  = imovel.find_element(By.CSS_SELECTOR, ".btn-mais-info").find_element(By.XPATH, "..").get_attribute("href")
            print(f"{codigo} | {local} | {tipo} | {preco} | {link}")
        except Exception as e:
            print("Erro ao ler imóvel:", e)

    # Verifica se há link "Próximo"
    try:
        proximo = driver.find_element(By.XPATH, "//a[contains(text(), 'Próximo')]")
        driver.execute_script("arguments[0].click();", proximo)
        pagina += 1
        # time.sleep(2)
    except NoSuchElementException:
        print("\n✅ Não há mais páginas.")
        break

# Fecha navegador
driver.quit()
