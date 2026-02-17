"""
Civitas-Radar — Spin Doctor (AI Advisor)
=========================================
Módulo de geração de notas estratégicas de resposta usando LLM.
Integra com Google Gemini (google-generativeai).
Possui fallback local (templates) caso a API não esteja disponível.
"""

from __future__ import annotations

import os
import random
from typing import Optional

# ──────────────────────────────────────────────────────────────
# Tons de resposta disponíveis
# ──────────────────────────────────────────────────────────────
TONS_RESPOSTA = {
    "Institucional": {
        "emoji": "🏛️",
        "descricao": "Tom sóbrio e técnico, linguagem formal de gabinete.",
        "instrucao": (
            "Responda como um assessor de comunicação institucional. "
            "Use tom sóbrio, técnico e formal. Cite dados quando possível. "
            "Evite confronto. Transmita serenidade e controle da situação."
        ),
    },
    "Militância": {
        "emoji": "✊",
        "descricao": "Tom combativo, mobilizador e assertivo.",
        "instrucao": (
            "Responda como um coordenador de campanha militante. "
            "Use tom combativo e assertivo. Confronte a narrativa adversária. "
            "Mobilize a base de apoio. Destaque conquistas e desmascare falácias."
        ),
    },
    "Empático": {
        "emoji": "🤝",
        "descricao": "Foco em solução, acolhimento e empatia com o cidadão.",
        "instrucao": (
            "Responda com empatia e foco em solução. "
            "Reconheça o problema do cidadão. Apresente medidas concretas "
            "que estão sendo tomadas. Transmita proximidade e humanidade."
        ),
    },
}


# ──────────────────────────────────────────────────────────────
# Gerador de notas via Gemini
# ──────────────────────────────────────────────────────────────
def gerar_nota_estrategica(
    texto_critico: str,
    tom: str = "Institucional",
    contexto_politico: Optional[str] = None,
    api_key: Optional[str] = None,
) -> dict:
    """
    Gera uma nota de resposta estratégica a partir de um texto crítico.

    Parameters
    ----------
    texto_critico : str
        O comentário, notícia ou transcrição negativa a ser respondida.
    tom : str
        Um dos tons em TONS_RESPOSTA: 'Institucional', 'Militância' ou 'Empático'.
    contexto_politico : str, optional
        Contexto adicional (nome do político, cargo, cenário).
    api_key : str, optional
        Chave da API Google Gemini. Se não informada, usa a variável
        de ambiente GEMINI_API_KEY. Se nenhuma disponível, usa fallback local.

    Returns
    -------
    dict
        {
            'nota': str,           # Texto da nota gerada
            'tom': str,            # Tom utilizado
            'fonte': str,          # 'gemini' ou 'fallback'
            'tokens_usados': int,  # Estimativa de tokens (0 se fallback)
        }
    """
    if tom not in TONS_RESPOSTA:
        tom = "Institucional"

    config_tom = TONS_RESPOSTA[tom]
    chave = api_key or os.environ.get("GEMINI_API_KEY", "")

    if chave:
        return _gerar_via_gemini(texto_critico, tom, config_tom, contexto_politico, chave)
    else:
        return _gerar_fallback(texto_critico, tom, config_tom, contexto_politico)


# ──────────────────────────────────────────────────────────────
# Integração real com Google Gemini
# ──────────────────────────────────────────────────────────────
def _gerar_via_gemini(
    texto: str,
    tom: str,
    config_tom: dict,
    contexto: Optional[str],
    api_key: str,
) -> dict:
    """Gera nota usando a API do Google Gemini com Instrução de Sistema."""
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        
        # 1. Definimos a Instrução de Sistema (Persona)
        # Aqui incluímos o DNA gaúcho e a expertise de Spin Doctor
        instrucao_sistema = (
            "Você é o Spin Doctor AI, um Consultor de Estratégia Política sênior e especialista em gestão de crises. "
            "Sua missão é proteger a reputação do monitorado com inteligência, ética e agilidade. "
            "Ao formular respostas, leve em conta o contexto cultural e geográfico do Rio Grande do Sul e de Porto Alegre quando aplicável. "
            f"Siga rigorosamente este tom de voz: {config_tom['instrucao']} "
            "Gere textos profissionais, sem inventar dados falsos, focados em acalmar os ânimos e retomar a narrativa."
        )

        # 2. Inicializamos o modelo com a instrução de sistema
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=instrucao_sistema
        )

        contexto_str = f"\nContexto Adicional: {contexto}" if contexto else ""

        # 3. O prompt de execução fica mais curto e direto
        prompt = (
            f"Texto crítico recebido para análise e resposta:\n\"{texto}\"\n"
            f"{contexto_str}\n\n"
            "Com base na sua instrução de sistema, gere uma nota de resposta estratégica (3-5 parágrafos). "
            "Não use markdown (negritos ou listas). Responda apenas com o texto da nota em português brasileiro."
        )

        response = model.generate_content(prompt)
        nota = response.text.strip() if response.text else ""

        return {
            "nota": nota,
            "tom": tom,
            "fonte": "gemini",
            "tokens_usados": len(prompt.split()) + len(nota.split()),
        }

    except Exception as e:
        # Se a API falhar, cai no fallback
        resultado = _gerar_fallback(texto, tom, config_tom, contexto)
        resultado["nota"] += f"\n\n⚠️ Gemini indisponível ({type(e).__name__}). Usando template local."
        return resultado


# ──────────────────────────────────────────────────────────────
# Fallback local (templates inteligentes)
# ──────────────────────────────────────────────────────────────

_TEMPLATES_INSTITUCIONAL = [
    (
        "A gestão municipal esclarece que as informações veiculadas não correspondem "
        "à integralidade dos fatos. A administração tem atuado de forma responsável e transparente, "
        "adotando todas as providências necessárias para garantir o bom andamento dos serviços públicos.\n\n"
        "É importante destacar que os indicadores da gestão demonstram avanços significativos "
        "em diversas áreas, conforme dados oficiais disponíveis para consulta pública.\n\n"
        "Reiteramos nosso compromisso com a transparência e convidamos a imprensa e a população "
        "a acompanhar os canais oficiais para informações atualizadas."
    ),
    (
        "Em nota, a assessoria de comunicação informa que a gestão mantém rigoroso controle "
        "sobre as demandas apresentadas pela população. As medidas citadas na publicação "
        "já estão sendo devidamente encaminhadas pelos setores competentes.\n\n"
        "A administração reafirma sua dedicação ao interesse público e seguirá prestando contas "
        "de todas as ações realizadas, conforme prevê a legislação vigente.\n\n"
        "Para esclarecimentos adicionais, a ouvidoria municipal permanece à disposição."
    ),
]

_TEMPLATES_MILITANCIA = [
    (
        "Mais uma tentativa de desconstruir o trabalho sério que está sendo feito! "
        "Enquanto a oposição se limita a criticar nos bastidores, esta gestão está na rua, "
        "entregando resultados concretos para a população.\n\n"
        "Os números não mentem: investimentos recordes em infraestrutura, saúde e educação. "
        "Quem acompanha de perto sabe a verdade. Quem tenta distorcer, tem interesses claros.\n\n"
        "Seguimos firmes! A base de apoio está mais forte do que nunca. "
        "O povo sabe reconhecer quem trabalha de verdade. 💪"
    ),
    (
        "Não vamos nos calar diante de narrativas fabricadas! Esta gestão foi eleita pelo povo "
        "e é ao povo que presta contas — não a articulações de gabinete.\n\n"
        "Cada obra entregue, cada programa implementado, cada família atendida é prova "
        "do compromisso real com a nossa cidade. Os opositores que apresentem suas propostas "
        "ao invés de espalhar desinformação.\n\n"
        "A militância está atenta e mobilizada. Vamos juntos! ✊"
    ),
]

_TEMPLATES_EMPATICO = [
    (
        "Entendemos a preocupação expressa e queremos dizer que estamos ouvindo. "
        "A gestão reconhece que há desafios a superar e está trabalhando intensamente "
        "para encontrar soluções que atendam a todos.\n\n"
        "Nenhuma reclamação é ignorada. Cada demanda recebida é encaminhada "
        "aos setores responsáveis para análise e providências imediatas. "
        "Sabemos que a paciência da população tem limite e por isso estamos acelerando os processos.\n\n"
        "Convidamos quem trouxe essa preocupação a nos procurar diretamente. "
        "Juntos, vamos encontrar o melhor caminho. Estamos aqui para servir."
    ),
    (
        "Lamentamos profundamente a situação relatada. Quando um cidadão sofre, "
        "a administração também sente o peso da responsabilidade.\n\n"
        "Já acionamos as equipes competentes para verificar o caso e tomar "
        "as providências cabíveis com a máxima urgência. Não vamos descansar "
        "até que uma solução concreta seja apresentada.\n\n"
        "Nosso compromisso é com pessoas, não com números. "
        "Cada situação é tratada com a atenção que merece. Conte conosco."
    ),
]

_TEMPLATES = {
    "Institucional": _TEMPLATES_INSTITUCIONAL,
    "Militância": _TEMPLATES_MILITANCIA,
    "Empático": _TEMPLATES_EMPATICO,
}


def _gerar_fallback(
    texto: str,
    tom: str,
    config_tom: dict,
    contexto: Optional[str],
) -> dict:
    """Gera nota usando templates locais quando a API não está disponível."""
    pool = _TEMPLATES.get(tom, _TEMPLATES_INSTITUCIONAL)
    nota = random.choice(pool)

    return {
        "nota": nota,
        "tom": tom,
        "fonte": "fallback",
        "tokens_usados": 0,
    }


# ──────────────────────────────────────────────────────────────
# Utilitário: análise rápida de criticidade
# ──────────────────────────────────────────────────────────────
def classificar_criticidade(texto: str) -> str:
    """
    Classifica o nível de criticidade de um texto.

    Returns
    -------
    str
        '🔴 Alta', '🟡 Média' ou '🟢 Baixa'
    """
    texto_lower = texto.lower()

    termos_alta = [
        "escândalo", "corrupção", "denúncia", "preso", "prisão",
        "CPI", "desvio", "fraude", "propina", "impeachment",
        "morte", "morreu", "urgente", "gravíssimo", "crime",
    ]
    termos_media = [
        "reclamação", "problema", "atraso", "demora", "falta",
        "protesto", "reclama", "crítica", "insatisfação",
        "decepção", "descaso", "negligência",
    ]

    if any(t in texto_lower for t in termos_alta):
        return "🔴 Alta"
    elif any(t in texto_lower for t in termos_media):
        return "🟡 Média"
    else:
        return "🟢 Baixa"
