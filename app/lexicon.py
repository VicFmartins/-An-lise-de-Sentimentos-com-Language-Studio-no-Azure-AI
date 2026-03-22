POSITIVE_WORDS = {
    "bom", "boa", "otimo", "otima", "excelente", "rapido", "rapida", "gostei", "eficiente",
    "confiavel", "recomendo", "estavel", "intuitivo", "satisfeito", "feliz", "maravilhoso",
    "incrivel", "pratico", "funcionou", "positivo", "seguro", "agradavel",
}

NEGATIVE_WORDS = {
    "ruim", "pessimo", "pessima", "lento", "lenta", "bug", "erro", "falha", "instavel",
    "confuso", "frustrante", "horrivel", "odiei", "triste", "irritante", "quebrado",
    "problema", "negativo", "caro", "dificil", "inseguro", "travando",
}

NEGATIONS = {"nao", "nunca", "jamais", "nem"}

ASPECT_KEYWORDS = {
    "preco": ["preco", "valor", "custo", "mensalidade"],
    "atendimento": ["atendimento", "suporte", "time", "equipe"],
    "produto": ["produto", "app", "aplicativo", "plataforma", "sistema", "servico"],
    "desempenho": ["desempenho", "velocidade", "performance", "latencia"],
    "entrega": ["entrega", "prazo", "envio"],
    "ux": ["interface", "ux", "usabilidade", "experiencia", "tela"],
}
