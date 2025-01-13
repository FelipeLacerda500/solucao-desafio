def calculadora(consumo: list, tarifa: float, classe: str) -> tuple:
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
    desconto_aplicado = tabela_descontos[classe.lower()][indice_faixa]
    economia_mensal = (consumo_medio * tarifa) * desconto_aplicado * cobertura
    economia_anual = economia_mensal * 12
    return (
        round(economia_anual, 2),
        round(economia_mensal, 2),
        round(desconto_aplicado, 2),
        round(cobertura, 2),
    )

if __name__ == "__main__":
    print("Testando...")

    assert calculadora([1518, 1071, 968], 0.878460, "Industrial") == (
        1349.86,
        112.49,
        0.12,
        0.90,
    )  

    assert calculadora([1000, 1054, 1100], 0.84432, "Residencial") == (
        1725.61,
        143.8,
        0.18,
        0.90
    )

    assert calculadora([973, 629, 726], 0.818540, "Comercial") == (
        1097.6,
        91.47,
        0.16,
        0.90
    )

    assert calculadora([15000, 14000, 16000], 0.844320, "Industrial") == (
        21656.81,
        1804.73,
        0.15,
        0.95
    )

    assert calculadora([12000, 11000, 11400], 0.79969, "Residencial") == (
        22997.8,
        1916.48,
        0.22,
        0.95
    )

    assert calculadora([17500, 16000, 16400], 0.818540, "Comercial") == (
        27938.08,
        2328.17,
        0.18,
        0.95
    )

    assert calculadora([30000, 29000, 29500], 0.844320, "Industrial") == (
        53262.07,
        4438.51,
        0.18,
        0.99
    )

    assert calculadora([22000, 21000, 21400], 0.81854, "Residencial") == (
        52186.84,
        4348.9,
        0.25,
        0.99
    )

    assert calculadora([25500, 23000, 21400], 0.799669, "Comercial") == (
        48697.35,
        4058.11,
        0.22,
        0.99
    )

    print("Todos os testes passaram!")
