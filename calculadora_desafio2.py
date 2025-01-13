from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def calculadora(consumo: list, classe: str, bandeira: str) -> tuple:
    bandeira += " - Consumo R$/kWh"
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.cemig.com.br/atendimento/valores-de-tarifas-e-servicos/")
        if classe == "Residencial":
            cabecalho_tabela = driver.find_element(By.XPATH, f"//th[contains(text(), 'B1- RESIDENCIAL NORMAL ')]")
        else:
            cabecalho_tabela = driver.find_element(By.XPATH, f"//th[contains(text(), 'B3 - DEMAIS CLASSES ')]")
        tabela = cabecalho_tabela.find_element(By.XPATH, "./ancestor::table")
        colunas = tabela.find_elements(By.XPATH, ".//thead/tr/th")
        indices_bandeiras = {
            coluna.text.strip().upper(): index for index, coluna in enumerate(colunas)
        }
        indice_bandeira = indices_bandeiras.get(bandeira.upper())
        if indice_bandeira is None:
            raise ValueError(f"Bandeira tarifária '{bandeira}' não encontrada.")
        linha_dados = tabela.find_element(By.XPATH, ".//tbody/tr")
        colunas_dados = linha_dados.find_elements(By.TAG_NAME, "td")
        tarifa = float(colunas_dados[indice_bandeira].text.replace(",", "."))
        economia_anual = 0
        economia_mensal = 0
        desconto_aplicado = 0
        cobertura = 0
        consumo_medio = sum(consumo) / len(consumo)
        tabela_descontos = {
            "residencial": [0.18, 0.22, 0.25],
            "comercial": [0.16, 0.18, 0.22],
            "industrial": [0.12, 0.15, 0.18]
        }
        if consumo_medio < 10000:
            indice_faixa = 0
            cobertura = 0.9
        elif consumo_medio <= 20000:
            indice_faixa = 1
            cobertura = 0.95
        else:
            indice_faixa = 2
            cobertura = 0.99
        if classe.lower() == "b1- residencial normal":
            desconto_aplicado = tabela_descontos["residencial"][indice_faixa]
        else:
            desconto_aplicado = tabela_descontos[classe.lower()][indice_faixa]
        economia_mensal = (consumo_medio * tarifa) * desconto_aplicado * cobertura
        economia_anual = economia_mensal * 12
        print(economia_anual)
        return (
            round(economia_anual, 2),
            round(economia_mensal, 2),
            round(desconto_aplicado, 2),
            round(cobertura, 2),
        )

    finally:
        driver.quit()

if __name__ == "__main__":
    print("Testando...")

    assert calculadora([1518, 1071, 968], "Industrial", "BANDEIRA VERMELHA 2") == (
        1349.86,
        112.49,
        0.12,
        0.90,
    ) 

    assert calculadora([1000, 1054, 1100], "Residencial", "BANDEIRA VERMELHA 1") == (
        1725.61,
        143.8,
        0.18,
        0.90
    )

    assert calculadora([973, 629, 726], "Comercial", "BANDEIRA AMARELA") == (
        1097.6,
        91.47,
        0.16,
        0.90
    )

    assert calculadora([15000, 14000, 16000], "Industrial", "BANDEIRA VERMELHA 1") == (
        21656.81,
        1804.73,
        0.15,
        0.95
    )

    assert calculadora([12000, 11000, 11400], "Residencial", "BANDEIRA VERDE") == (
        22997.8,
        1916.48,
        0.22,
        0.95
    )

    assert calculadora([17500, 16000, 16400], "Comercial", "BANDEIRA AMARELA") == (
        27938.08,
        2328.17,
        0.18,
        0.95
    )

    assert calculadora([30000, 29000, 29500], "Industrial", "BANDEIRA VERMELHA 1") == (
        53262.07,
        4438.51,
        0.18,
        0.99
    )

    assert calculadora([22000, 21000, 21400], "Residencial", "BANDEIRA AMARELA") == (
        52186.84,
        4348.9,
        0.25,
        0.99
    )

    assert calculadora([25500, 23000, 21400], "Comercial", "BANDEIRA VERDE") == (
        48697.35,
        4058.11,
        0.22,
        0.99
    )

    print("Todos os testes passaram!")
