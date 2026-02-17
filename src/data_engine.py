"""
Civitas-Radar — Motor de Dados (Data Engine)
=============================================
Módulo responsável por:
  • Gerar comentários sintéticos (simulação de redes sociais)
  • Buscar notícias reais via Google News com fallback robusto
  • Segmentação territorial hierárquica (Capital → Metro → Estadual)
  • Simulação de transcrições de Rádio/TV (Omni-Channel)
  • Simulação de mensagens de WhatsApp (Dark Social)
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

import numpy as np
import pandas as pd
from faker import Faker

# ──────────────────────────────────────────────────────────────
# Configuração global
# ──────────────────────────────────────────────────────────────
fake = Faker("pt_BR")
Faker.seed(None)  # semente aleatória a cada execução

PLATAFORMAS = ["Twitter/X", "Facebook", "Instagram", "TikTok", "Threads", "WhatsApp"]

# ──────────────────────────────────────────────────────────────
# Segmentação Territorial Hierárquica (RS)
# Cada entrada: (nome, latitude, longitude)
# ──────────────────────────────────────────────────────────────
NIVEIS_GEO = {
    "Capital (Porto Alegre)": {
        "centro": (-30.0346, -51.2177),
        "regioes": [
            ("Centro Histórico",   -30.0310, -51.2300),
            ("Moinhos de Vento",   -30.0264, -51.2005),
            ("Cidade Baixa",       -30.0420, -51.2200),
            ("Bom Fim",            -30.0335, -51.2100),
            ("Menino Deus",        -30.0480, -51.2240),
            ("Sarandi",            -29.9680, -51.1280),
            ("Restinga",           -30.1210, -51.2340),
            ("Rubem Berta",        -29.9790, -51.1380),
            ("Partenon",           -30.0620, -51.1750),
            ("Ipanema",            -30.1280, -51.2090),
            ("Cavalhada",          -30.0980, -51.2190),
            ("Lomba do Pinheiro",  -30.0650, -51.1190),
            ("Cristal",            -30.1050, -51.2340),
            ("Navegantes",         -30.0100, -51.1840),
            ("Vila Nova",          -30.0880, -51.1580),
            ("Glória",             -30.0550, -51.1910),
            ("Humaitá",            -29.9780, -51.0990),
            ("Santa Tereza",       -30.0470, -51.1990),
            ("Floresta",           -30.0250, -51.2070),
            ("Belém Velho",        -30.1000, -51.1800),
        ],
    },
    "Região Metropolitana": {
        "centro": (-29.9200, -51.1000),
        "regioes": [
            ("Canoas",             -29.9178, -51.1740),
            ("Gravataí",           -29.9446, -50.9920),
            ("Viamão",             -30.0810, -51.0235),
            ("Novo Hamburgo",      -29.6875, -51.1319),
            ("São Leopoldo",       -29.7545, -51.1496),
            ("Cachoeirinha",       -29.9510, -51.0940),
            ("Alvorada",           -29.9910, -51.0810),
            ("Esteio",             -29.8622, -51.1787),
            ("Sapucaia do Sul",    -29.8275, -51.1450),
            ("Guaíba",             -30.1140, -51.3245),
            ("Eldorado do Sul",    -30.0860, -51.3700),
            ("Campo Bom",          -29.6755, -51.0620),
            ("Dois Irmãos",        -29.5843, -51.0890),
            ("Ivoti",              -29.5930, -51.1560),
            ("Charqueadas",        -29.9555, -51.6230),
        ],
    },
    "Macrorregiões do RS": {
        "centro": (-29.5000, -52.0000),
        "regioes": [
            ("Serra Gaúcha",       -29.1681, -51.1794),
            ("Campanha",           -31.3300, -54.1000),
            ("Missões",            -28.5500, -54.5700),
            ("Litoral Norte",      -29.3300, -49.7200),
            ("Fronteira Oeste",    -29.7500, -57.0800),
            ("Vale do Sinos",      -29.6800, -51.1300),
            ("Vale do Taquari",    -29.4500, -51.9700),
            ("Região Central",     -29.6842, -53.8069),
            ("Alto Uruguai",       -27.8800, -52.3500),
            ("Sul (Pelotas/RG)",   -31.7700, -52.3400),
            ("Hortênsias",         -29.3700, -50.8700),
            ("Planalto Médio",     -28.2600, -52.4100),
        ],
    },
}

EMISSORAS_RADIO_TV = [
    "Rádio Gaúcha",
    "Rádio Guaíba",
    "Rádio Bandeirantes POA",
    "Band News FM Porto Alegre",
    "Rádio Pampa",
    "TV RBS (Bom Dia Rio Grande)",
    "TV RBS (Jornal do Almoço)",
    "TV Band RS",
    "TV Record RS",
    "Rádio Grenal",
]

# ──────────────────────────────────────────────────────────────
# Cenários de simulação — dicionários ricos de palavras-chave
# ──────────────────────────────────────────────────────────────
CENARIOS: Dict[str, dict] = {
    "Crise na Saúde": {
        "distribuicao": {"Negativo": 0.80, "Neutro": 0.10, "Positivo": 0.10},
        "keywords": {
            "Negativo": [
                "fila enorme no hospital", "esperei 8 horas e ninguém atendeu",
                "falta de médico é um descaso total", "descaso com a saúde pública",
                "minha mãe morreu na fila de espera", "hospital sem remédio básico",
                "UBS fechada de novo", "vergonha o estado da saúde",
                "ambulância demorou 3 horas", "não tem leito disponível",
                "médico mandou voltar semana que vem", "posto de saúde caindo aos pedaços",
                "faltam profissionais na UPA", "pacientes no corredor do hospital",
                "remédio em falta há meses", "demora absurda pra marcar exame",
                "SUS completamente abandonado", "criança sem atendimento, que horror",
                "cadê o investimento na saúde?", "pronto-socorro lotado, cadê o prefeito?",
                "gente morrendo por falta de atendimento", "saúde em colapso nessa cidade",
                "filas intermináveis na farmácia popular", "negligência total com os idosos",
                "sem anestesia pra fazer cirurgia", "equipamento quebrado há semanas",
            ],
            "Neutro": [
                "fui ao hospital hoje, atendimento normal", "marquei consulta pelo app",
                "esperando resultado do exame", "o posto estava funcionando normalmente",
                "cheguei cedo e fui atendido depois", "enfermeira disse para voltar amanhã",
                "procedimento padrão, nada demais", "agendamento feito sem problemas",
            ],
            "Positivo": [
                "atendimento rápido hoje, parabéns à equipe", "rede de saúde tá melhorando",
                "agradeço ao SUS que me salvou", "fui bem atendido na UPA pelo menos",
                "os profissionais de saúde são guerreiros", "equipe excelente mesmo com dificuldades",
                "inauguram novo centro de saúde, bom demais", "os agentes comunitários são anjos",
            ],
        },
    },
    "Escândalo de Corrupção": {
        "distribuicao": {"Negativo": 0.90, "Neutro": 0.05, "Positivo": 0.05},
        "keywords": {
            "Negativo": [
                "desvio de milhões dos cofres públicos", "mais um pego com a mão na massa",
                "propina pra todo lado nessa gestão", "polícia federal tem que investigar já",
                "dinheiro do povo indo pro ralo", "caixa 2 confirmado, cadê a prisão?",
                "assessores presos por lavagem de dinheiro", "roubo descarado e ninguém faz nada",
                "superfaturamento em obra fantasma", "mais um escândalo e tudo fica por isso mesmo",
                "notas fiscais frias comprovam o esquema", "povo passando fome e eles roubando",
                "servidores fantasmas na folha de pagamento", "licitação fraudada, tá na cara",
                "procuradoria tem que agir agora", "vergonha nacional esse político",
                "desvio de verba da educação, criminoso!", "roubo de merenda escolar confirmado",
                "patrimônio incompatível com salário de político", "malas de dinheiro apreendidas",
                "banco confirmou transações suspeitas", "empresa de fachada recebia repasses",
                "denúncia grave e provas concretas", "contas secretas no exterior",
            ],
            "Neutro": [
                "aguardando resultado da investigação", "MP disse que vai analisar o caso",
                "inquérito policial foi instaurado", "defesa diz que vai provar inocência",
            ],
            "Positivo": [
                "ele é inocente, confia no processo", "político está sendo perseguido",
                "mídia distorcendo os fatos, apoio total", "tudo armação da oposição",
            ],
        },
    },
    "Inauguração de Obra": {
        "distribuicao": {"Negativo": 0.10, "Neutro": 0.20, "Positivo": 0.70},
        "keywords": {
            "Positivo": [
                "parabéns pela obra, ficou excelente!", "finalmente asfaltaram minha rua",
                "escola nova lindíssima, obrigado prefeito", "progresso real, isso sim é gestão",
                "ponte nova vai mudar a vida de muita gente", "praça reformada ficou show",
                "avanço enorme pra nossa comunidade", "creche inaugurada, meus filhos agradecem",
                "iluminação nova no bairro, muito melhor agora", "hospital reformado, parabéns equipe",
                "infraestrutura melhorando a olhos vistos", "futuro promissor com essas obras",
                "quadra esportiva nova, juventude agradece", "ciclovia inaugurada, que maravilha!",
                "moradores do bairro estão celebrando", "investimento que faz diferença de verdade",
                "saneamento básico chegou no nosso bairro!", "viaduto novo resolveu o trânsito",
            ],
            "Neutro": [
                "inauguraram a obra hoje", "obra parece boa, vamos ver se dura",
                "prefeito esteve no local da inauguração", "evento de inauguração aconteceu ontem",
                "vizinhos estão indiferentes, mas achei ok", "vamos acompanhar a manutenção",
                "será que entregam no prazo o restante?", "obra feita, agora falta a segunda etapa",
            ],
            "Negativo": [
                "obra superfaturada como sempre", "demorou 2 anos pra entregar",
                "só inaugura perto da eleição", "a qualidade parece péssima, vai cair",
                "vizinhos dizem que ninguém foi consultado", "palanque eleitoreiro de novo",
            ],
        },
    },
    "Viral Positivo": {
        "distribuicao": {"Negativo": 0.03, "Neutro": 0.02, "Positivo": 0.95},
        "keywords": {
            "Positivo": [
                "MITO! Esse político é demais!", "lenda viva da política brasileira",
                "#tamojunto com o melhor prefeito", "brabo demais, representa o povo!",
                "gênio da administração, resultados falam", "o povo elegeu certo, disparou na pesquisa",
                "orgulho do nosso estado 🔥", "melhor gestor que já tivemos",
                "aprovação nas alturas, merecido!", "todo mundo compartilhando, viralizou!",
                "esse merece reeleição fácil", "nunca vi um político tão dedicado",
                "quebrou recordes de aprovação digital", "meu voto tá garantido de novo!",
                "olha os números, resultado incontestável", "gestão de excelência, referência nacional",
                "até a oposição reconhece o trabalho", "cidade transformada em poucos meses",
                "fez mais em 1 ano que todos antes", "virou exemplo pro país inteiro!",
                "entregando obras sem parar 💪", "o cara resolve, simples assim",
            ],
            "Neutro": [
                "viralizou o vídeo do político", "bastante gente compartilhando nas redes",
            ],
            "Negativo": [
                "puro marketing, não caio nessa", "comprou seguidores certeza",
                "bot espalhando propaganda, acorda povo", "pago pra viralizar, isso sim",
            ],
        },
    },
}


# ──────────────────────────────────────────────────────────────
# Classe principal de simulação
# ──────────────────────────────────────────────────────────────
class SimuladorRedes:
    """Gerador de comentários de redes sociais baseado em cenários narrativos."""

    def __init__(self, nivel_geo: str = "Capital (Porto Alegre)") -> None:
        """
        Inicializa o simulador com um nível geográfico.

        Parameters
        ----------
        nivel_geo : str
            Chave de NIVEIS_GEO: 'Capital (Porto Alegre)',
            'Região Metropolitana' ou 'Macrorregiões do RS'.
        """
        self.fake = fake
        self.nivel_geo = nivel_geo
        self._regioes = NIVEIS_GEO.get(nivel_geo, NIVEIS_GEO["Capital (Porto Alegre)"])["regioes"]

    # ── helpers ────────────────────────────────────────────────
    @staticmethod
    def _gerar_username() -> str:
        """Cria um username realista no estilo brasileiro de redes sociais."""
        estilo = random.choice(["nome", "apelido", "handle"])
        if estilo == "nome":
            nome = fake.first_name().lower()
            sobrenome = fake.last_name().lower()
            return f"@{nome}.{sobrenome}{random.randint(1, 99)}"
        elif estilo == "apelido":
            apelidos = [
                "cidadao", "povo", "fiscal", "voz", "olho", "radar",
                "verdade", "gente", "alerta", "brasil", "nacao", "opiniao",
                "tribuna", "revolta", "democracia", "liberdade", "patriota",
            ]
            return f"@{random.choice(apelidos)}_{random.randint(100, 9999)}"
        else:
            return f"@{fake.user_name()}"

    @staticmethod
    def _gerar_timestamp_recente(horas: int = 24) -> datetime:
        """Retorna um datetime nas últimas N horas."""
        agora = datetime.now()
        delta = timedelta(seconds=random.randint(0, horas * 3600))
        return agora - delta

    @staticmethod
    def _sortear_sentimento(distribuicao: Dict[str, float]) -> str:
        """Sorteia um sentimento com base na distribuição probabilística."""
        sentimentos = list(distribuicao.keys())
        pesos = list(distribuicao.values())
        return np.random.choice(sentimentos, p=pesos)

    # ── método principal ──────────────────────────────────────
    def gerar_comentarios(self, tema: str, quantidade: int = 50) -> pd.DataFrame:
        """
        Gera um DataFrame de comentários simulados de redes sociais.

        Parameters
        ----------
        tema : str
            Nome do cenário (deve existir em CENARIOS).
        quantidade : int
            Quantidade de comentários a gerar.

        Returns
        -------
        pd.DataFrame
            Colunas: [Data, Usuario, Texto, Sentimento, Plataforma, Bairro, Latitude, Longitude]
        """
        if tema not in CENARIOS:
            raise ValueError(
                f"Cenário '{tema}' não encontrado. "
                f"Opções: {list(CENARIOS.keys())}"
            )

        config = CENARIOS[tema]
        distribuicao = config["distribuicao"]
        keywords = config["keywords"]
        registros: List[dict] = []

        for _ in range(quantidade):
            sentimento = self._sortear_sentimento(distribuicao)
            frases_pool = keywords.get(sentimento, keywords["Neutro"])
            texto_base = random.choice(frases_pool)

            # Adiciona variação natural: hashtag, menção, emoji
            texto = self._enriquecer_texto(texto_base, sentimento)

            # Geo-localização aleatória dentro do nível selecionado
            regiao = random.choice(self._regioes)
            nome_regiao, lat_base, lon_base = regiao
            # Adiciona jitter de ±0.005° (~500m) para dispersão visual
            lat = lat_base + random.uniform(-0.005, 0.005)
            lon = lon_base + random.uniform(-0.005, 0.005)

            registros.append(
                {
                    "Data": self._gerar_timestamp_recente(),
                    "Usuario": self._gerar_username(),
                    "Texto": texto,
                    "Sentimento": sentimento,
                    "Plataforma": random.choice(PLATAFORMAS),
                    "Bairro": nome_regiao,
                    "Latitude": round(lat, 6),
                    "Longitude": round(lon, 6),
                }
            )

        df = pd.DataFrame(registros)
        df = df.sort_values("Data", ascending=False).reset_index(drop=True)
        return df

    @staticmethod
    def _enriquecer_texto(texto: str, sentimento: str) -> str:
        """Acrescenta variações estilísticas ao texto base."""
        # Hashtags contextuais
        hashtags_map = {
            "Negativo": [
                "#vergonha", "#decepção", "#cadêasolução", "#socorro",
                "#inaceitável", "#descaso", "#chega", "#foracorruptos",
            ],
            "Positivo": [
                "#parabéns", "#orgulho", "#avança", "#ficadica",
                "#boaprefeito", "#gratidão", "#resultado", "#progresso",
            ],
            "Neutro": ["#política", "#acompanhando", "#informação"],
        }

        # Emojis contextuais
        emojis_map = {
            "Negativo": ["😡", "😤", "💔", "🤬", "👎", "😢", "🚨"],
            "Positivo": ["👏", "🔥", "💪", "✅", "🎉", "❤️", "🏆"],
            "Neutro": ["🤔", "📰", "📊", "👀"],
        }

        modificadores: List[str] = []

        # ~40% chance de hashtag
        if random.random() < 0.40:
            modificadores.append(random.choice(hashtags_map.get(sentimento, [])))

        # ~30% chance de emoji
        if random.random() < 0.30:
            modificadores.append(random.choice(emojis_map.get(sentimento, [])))

        # ~15% chance de menção a perfil
        if random.random() < 0.15:
            modificadores.insert(0, f"@{fake.user_name()}")

        sufixo = " ".join(modificadores)
        return f"{texto} {sufixo}".strip() if sufixo else texto

    # ── Simulação de transcrições Rádio/TV ────────────────────
    def gerar_transcricoes_radio_tv(
        self, tema: str, quantidade: int = 15
    ) -> pd.DataFrame:
        """
        Simula transcrições de veículos de Rádio e TV.

        Retorna DataFrame com colunas:
        [Timestamp, Emissora, Tipo, Transcricao, Sentimento, Bairro, Latitude, Longitude]
        """
        transcricoes_base: Dict[str, List[str]] = {
            "Positivo": [
                "...segundo informações da assessoria, o projeto foi concluído com sucesso e dentro do prazo...",
                "...moradores do bairro comemoram a chegada do novo posto de saúde na comunidade...",
                "...a secretaria de obras confirmou que 95% das metas do programa foram alcançadas...",
                "...pesquisa aponta aumento na aprovação da gestão municipal nos últimos 30 dias...",
                "...professores elogiam investimento recente em tecnologia nas escolas da rede pública...",
                "...evento de inauguração reuniu centenas de moradores que aprovaram a iniciativa...",
                "...índice de empregabilidade cresce pelo terceiro mês consecutivo na região...",
                "...programa de habitação entrega 200 unidades para famílias de baixa renda...",
            ],
            "Negativo": [
                "...ouvintes reclamam da demora no atendimento nas unidades de saúde da capital...",
                "...a denúncia publicada na manhã de hoje aponta irregularidades em contratos públicos...",
                "...moradores do bairro relatam falta de água há mais de 48 horas seguidas...",
                "...oposição protocola pedido de CPI para investigar gastos com publicidade oficial...",
                "...professores ameaçam greve caso reajuste salarial não seja aprovado esta semana...",
                "...reportagem flagra obra parada há meses sem qualquer justificativa da prefeitura...",
                "...hospital referência opera com apenas 40% dos leitos disponíveis hoje...",
                "...transporte público tem atrasos de até 50 minutos em diversas linhas nesta manhã...",
                "...empresários criticam burocracia que trava abertura de negócios na cidade...",
                "...famílias em área de risco aguardam remoção prometida há mais de um ano...",
            ],
            "Neutro": [
                "...a pauta será votada na sessão extraordinária da câmara de vereadores amanhã...",
                "...previsão do tempo indica chuva forte para a região metropolitana nas próximas horas...",
                "...coletiva de imprensa está marcada para as 14 horas no Paço Municipal...",
                "...câmara municipal debate projeto de lei sobre mobilidade urbana nesta tarde...",
                "...audiência pública sobre o orçamento participativo acontece no centro comunitário...",
            ],
        }

        if tema not in CENARIOS:
            raise ValueError(f"Cenário '{tema}' não encontrado.")

        distribuicao = CENARIOS[tema]["distribuicao"]
        registros: List[dict] = []

        for _ in range(quantidade):
            sentimento = self._sortear_sentimento(distribuicao)
            pool = transcricoes_base.get(sentimento, transcricoes_base["Neutro"])
            transcricao = random.choice(pool)

            regiao = random.choice(self._regioes)
            nome_regiao, lat_base, lon_base = regiao

            registros.append(
                {
                    "Timestamp": self._gerar_timestamp_recente(horas=12),
                    "Emissora": random.choice(EMISSORAS_RADIO_TV),
                    "Tipo": random.choice(["Rádio", "TV"]),
                    "Transcricao": transcricao,
                    "Sentimento": sentimento,
                    "Bairro": nome_regiao,
                    "Latitude": round(lat_base + random.uniform(-0.003, 0.003), 6),
                    "Longitude": round(lon_base + random.uniform(-0.003, 0.003), 6),
                }
            )

        df = pd.DataFrame(registros)
        df = df.sort_values("Timestamp", ascending=False).reset_index(drop=True)
        return df

    # ── Simulação de mensagens WhatsApp (Dark Social) ─────────
    def gerar_mensagens_whatsapp(
        self, tema: str, quantidade: int = 20
    ) -> pd.DataFrame:
        """
        Simula mensagens de grupos de WhatsApp extraídas por OCR.

        Retorna DataFrame com colunas:
        [Timestamp, Grupo, Remetente, Mensagem, Sentimento, Viralidade, Bairro]
        """
        nomes_grupos = [
            "Moradores Zona Norte", "Bairro Unido", "Comunidade Ativa",
            "Fiscais do Povo", "Vizinhança Alerta", "Grupo da Rua",
            "Política Local", "Cidadãos Conscientes", "Notícias da Cidade",
            "Denúncia Cidadã", "Saúde Pública RS", "Debates Municipais",
        ]

        mensagens_base: Dict[str, List[str]] = {
            "Positivo": [
                "gente, a obra da rua ficou ótima mesmo 👏",
                "quem viu? inauguraram o posto novo, era hora! ✅",
                "tô compartilhando pq merece visibilidade, gestão boa é assim",
                "alguém mais notou que o ônibus tá vindo no horário? 😄",
                "hospital novo ficou lindo, fui atendido rápido",
                "meu filho voltou da escola nova empolgado, valeu a espera",
            ],
            "Negativo": [
                "GENTE OLHEM ISSO!! denúncia gravíssima compartilhem!!! 🚨🚨🚨",
                "mais um escândalo e ngm faz nada, tô revoltado",
                "faltou água DE NOVO, isso é um ABSURDO!!",
                "compartilha no máximo de grupos possível, o povo tem q saber",
                "isso é URGENTE: hospital sem médico, minha vizinha quase morreu",
                "cadê o prefeito q sumiu?? vergonha!! encaminhem pra todo mundo",
                "VIRALIZOU: vídeo mostra obra abandonada, passem adiante!!!",
                "professora me mandou isso, escola caindo aos pedaços 😡",
                "recebeu essa corrente? já era verdade confirmada",
                "olha o print da denúncia, repasse urgente!!",
            ],
            "Neutro": [
                "alguém sabe o horário da reunião da associação?",
                "vi que vai ter audiência pública amanhã, vão?",
                "repassando: coletiva de imprensa às 14h no paço municipal",
                "to acompanhando, vamos ver no que dá",
            ],
        }

        # Termos indicativos de viralidade (correntes)
        termos_virais = [
            "compartilhem", "repasse", "encaminhem", "viralizou",
            "urgente", "passem adiante", "corrente", "🚨🚨🚨",
        ]

        if tema not in CENARIOS:
            raise ValueError(f"Cenário '{tema}' não encontrado.")

        distribuicao = CENARIOS[tema]["distribuicao"]
        registros: List[dict] = []

        for _ in range(quantidade):
            sentimento = self._sortear_sentimento(distribuicao)
            pool = mensagens_base.get(sentimento, mensagens_base["Neutro"])
            mensagem = random.choice(pool)

            # Detecta viralidade
            texto_lower = mensagem.lower()
            viralidade = any(t in texto_lower for t in termos_virais)

            regiao = random.choice(self._regioes)
            nome_regiao = regiao[0]

            registros.append(
                {
                    "Timestamp": self._gerar_timestamp_recente(horas=48),
                    "Grupo": random.choice(nomes_grupos),
                    "Remetente": self.fake.first_name(),
                    "Mensagem": mensagem,
                    "Sentimento": sentimento,
                    "Viralidade": "🔥 Corrente Viral" if viralidade else "—",
                    "Bairro": nome_regiao,
                }
            )

        df = pd.DataFrame(registros)
        df = df.sort_values("Timestamp", ascending=False).reset_index(drop=True)
        return df


# ──────────────────────────────────────────────────────────────
# Transcrição de áudio via Whisper (Omni-Channel real)
# ──────────────────────────────────────────────────────────────
def transcrever_audio(arquivo_audio: str, modelo: str = "base") -> Dict[str, str]:
    """
    Transcreve um arquivo de áudio usando OpenAI Whisper.

    Parameters
    ----------
    arquivo_audio : str
        Caminho para o arquivo de áudio (.mp3, .wav, .m4a, etc.).
    modelo : str
        Modelo Whisper: 'tiny', 'base', 'small', 'medium', 'large'.

    Returns
    -------
    dict
        {'texto': str, 'idioma': str}
    """
    try:
        import whisper

        model = whisper.load_model(modelo)
        result = model.transcribe(arquivo_audio, language="pt")
        return {
            "texto": result.get("text", ""),
            "idioma": result.get("language", "pt"),
        }
    except ImportError:
        return {
            "texto": "[Whisper não instalado — execute: pip install openai-whisper]",
            "idioma": "pt",
        }
    except Exception as e:
        return {
            "texto": f"[Erro na transcrição: {e}]",
            "idioma": "pt",
        }


# ──────────────────────────────────────────────────────────────
# OCR para prints de WhatsApp (Dark Social)
# ──────────────────────────────────────────────────────────────
def extrair_texto_imagem(caminho_imagem: str) -> str:
    """
    Extrai texto de uma imagem (print de WhatsApp) via EasyOCR.

    Parameters
    ----------
    caminho_imagem : str
        Caminho para o arquivo de imagem (.png, .jpg).

    Returns
    -------
    str
        Texto extraído concatenado.
    """
    try:
        import easyocr

        reader = easyocr.Reader(["pt"], gpu=False)
        resultados = reader.readtext(caminho_imagem, detail=0)
        return " ".join(resultados)
    except ImportError:
        return "[EasyOCR não instalado — execute: pip install easyocr]"
    except Exception as e:
        return f"[Erro no OCR: {e}]"


# ──────────────────────────────────────────────────────────────
# Coleta de notícias reais (Google News) + fallback
# ──────────────────────────────────────────────────────────────
def buscar_noticias_google(termo: str, qtd: int = 5) -> List[Dict[str, str]]:
    """
    Busca notícias reais no Google News.

    Caso a API falhe ou demore, retorna dados mockados para garantir
    que a demonstração nunca quebre.

    Returns
    -------
    list[dict]
        Cada dict contém: titulo, data, link, fonte.
    """
    try:
        from GoogleNews import GoogleNews

        gn = GoogleNews(lang="pt", region="BR", period="7d")
        gn.clear()
        gn.search(termo)
        resultados = gn.results()

        if not resultados:
            raise RuntimeError("Nenhum resultado retornado")

        noticias = []
        for r in resultados[:qtd]:
            noticias.append(
                {
                    "titulo": r.get("title", "Sem título"),
                    "data": r.get("date", "Recente"),
                    "link": r.get("link", "#"),
                    "fonte": r.get("media", "Fonte desconhecida"),
                }
            )
        return noticias

    except Exception:
        # ── Fallback: notícias mockadas ──────────────────────
        return _noticias_fallback(termo)


def _noticias_fallback(termo: str) -> List[Dict[str, str]]:
    """Gera notícias fictícias plausíveis quando a API não responde."""
    templates = [
        f"{termo} é destaque em debate sobre políticas públicas na câmara",
        f"Pesquisa aponta variação na aprovação de {termo} esta semana",
        f"Especialistas comentam impacto de decisões recentes de {termo}",
        f"Imprensa nacional repercute declarações de {termo} sobre economia",
        f"Portal de notícias analisa trajetória política de {termo}",
        f"Eleitores reagem nas redes após pronunciamento de {termo}",
        f"Prefeitura de {termo} anuncia pacote de medidas emergenciais",
    ]
    fontes = ["G1", "UOL Notícias", "Folha de S.Paulo", "CNN Brasil", "Estadão", "R7", "Metrópoles"]

    noticias = []
    for i in range(min(5, len(templates))):
        noticias.append(
            {
                "titulo": templates[i],
                "data": (datetime.now() - timedelta(days=random.randint(0, 6))).strftime("%d/%m/%Y"),
                "link": "#",
                "fonte": fontes[i % len(fontes)],
            }
        )
    return noticias
