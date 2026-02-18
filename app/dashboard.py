"""
Civitas-Radar — Dashboard de Inteligência Política
====================================================
Interface visual "War Room" (Sala de Situação)
Executar:  streamlit run app/dashboard.py
"""

from __future__ import annotations

import html as _html
import sys
from pathlib import Path

# Garante que o diretório raiz do projeto esteja no path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.data_engine import SimuladorRedes, buscar_noticias_google, CENARIOS, NIVEIS_GEO
from src.ai_advisor import (
    gerar_nota_estrategica,
    classificar_criticidade,
    TONS_RESPOSTA,
)

# ══════════════════════════════════════════════════════════════
# Internacionalização (i18n) — PT-BR e ES (América Latina)
# ══════════════════════════════════════════════════════════════
I18N = {
    "PT-BR": {
        "page_title": "Civitas Radar",
        "header_subtitle": "Central de Inteligência Política — Monitoramento de Reputação em Tempo Real",
        "sidebar_title": "🛰️ Painel de Controle",
        "nome_politico_label": "👤 Nome do Político / Monitorado",
        "nome_politico_help": "Digite o nome para buscar notícias reais no Google News",
        "cenario_label": "📡 Cenário de Simulação",
        "cenario_help": "Define a narrativa da simulação de redes sociais",
        "geo_label": "🗺️ Escala Geográfica",
        "geo_help": "Alterna entre bairros da capital, cidades da RM ou macrorregiões do RS",
        "volume_label": "📊 Volume de Menções",
        "btn_atualizar": "🔄 Atualizar Inteligência",
        "version_label": "Civitas-Radar v2.0 — Fase 2",
        "cenario_ativo": "Cenário ativo",
        "escala_geo": "Escala geo",
        "info_inicial": "👈 Configure os parâmetros na barra lateral e clique em **Atualizar Inteligência** para iniciar o monitoramento.",
        "spinner_msg": "⏳ Coletando inteligência…",
        "kpi_aprovacao": "📈 Índice de Aprovação Digital",
        "kpi_volume": "📢 Volume de Menções (24h)",
        "kpi_sentimento": "🎯 Sentimento Predominante",
        "acima_limiar": "Acima do limiar",
        "abaixo_limiar": "Abaixo do limiar",
        "registros_coletados": "registros coletados",
        "mencoes": "menções",
        "tab_radar": "📡 Radar Tradicional",
        "tab_mapa": "🗺️ Mapa de Crise",
        "tab_comando": "🏛️ Sala de Comando",
        "dist_sentimentos": "🟢🔴 Distribuição de Sentimentos",
        "linha_tempo": "📈 Linha do Tempo (Últimas 24h)",
        "intel_imprensa": "📰 Intel — Imprensa",
        "intel_ruas": "💬 Intel — Voz das Ruas",
        "radio_tv": "📻 Rádio Escuta / TV Clipping",
        "dark_social": "📱 Dark Social — WhatsApp Sentinela",
        "tabela_completa": "📋 Ver Tabela Completa de Dados",
        "nenhuma_noticia": "Nenhuma notícia encontrada.",
        "nenhuma_transcricao": "Nenhuma transcrição disponível.",
        "nenhuma_msg": "Nenhuma mensagem interceptada.",
        "mapa_calor": "🗺️ Mapa de Calor — Sentimento por Região",
        "escala": "Escala",
        "mencoes_mapeadas": "Total de menções mapeadas",
        "regioes_criticas": "🚨 Regiões Críticas",
        "regioes_favoraveis": "✅ Regiões Favoráveis",
        "aprovacao": "Aprovação",
        "sentimento_regiao": "📊 Sentimento por Região (Breakdown)",
        "spin_doctor_title": "🏛️ Spin Doctor — Gerador de Respostas Estratégicas",
        "spin_doctor_desc": "Selecione uma menção negativa e gere uma nota de resposta oficial com o tom desejado. O módulo usa IA generativa (Gemini) quando disponível.",
        "selecione_mencao": "🎯 Selecione a menção para responder",
        "mencao_selecionada": "Menção selecionada",
        "tom_resposta": "Tom da Resposta",
        "btn_gerar": "⚡ Gerar Defesa",
        "spin_processando": "🧠 Spin Doctor processando…",
        "nota_estrategica": "Nota Estratégica — Tom",
        "btn_copiar": "📋 Copiar Nota",
        "btn_regenerar": "🔄 Regenerar",
        "btn_exportar": "📤 Exportar PDF",
        "nenhum_negativo": "✅ Nenhuma menção negativa detectada neste cenário. Cenário sob controle!",
        "como_usar_titulo": "📖 Como usar esta aplicação",
        "como_usar_corpo": """
**Civitas-Radar** é uma plataforma de Inteligência Política e Monitoramento de Reputação Digital em tempo real.

**Passo a passo:**
1. **Configure** o nome do político/monitorado na barra lateral esquerda.
2. **Selecione** um cenário de simulação — são **10 cenários** disponíveis (Crise na Saúde, Corrupção, Inauguração, Viral Positivo, Segurança Pública, Educação, Crise Habitacional, Enchente, Estado de Emergência, Calamidade Climática).
3. **Escolha** a escala geográfica (Capital, Região Metropolitana ou Macrorregiões).
4. **Ajuste** o volume de menções desejado com o slider.
5. **Clique** em "🔄 Atualizar Inteligência" para gerar os dados.

**Abas disponíveis:**
- **📡 Radar Tradicional**: KPIs, gráficos de sentimento (Donut + Timeline), Intel Imprensa (Google News em tempo real), Voz das Ruas, Rádio/TV e WhatsApp Sentinela.
- **🗺️ Mapa de Crise**: Mapa de calor georreferenciado com sentimento por região + ranking de regiões críticas e favoráveis.
- **🏛️ Sala de Comando**: Spin Doctor — selecione menções negativas e gere notas estratégicas por IA (Gemini ou template local) com 3 tons: Institucional, Militância e Empático.

**Personalização:**
- **🌐 Idioma**: Alterne entre Português (BR) e Espanhol (América Latina) no seletor acima.
- **🎨 Tema**: Escolha entre Dark, Grey ou Light no seletor de tema.

**Dica**: Os dados de redes sociais são simulados para demonstração. As notícias são coletadas em tempo real via Google News, com links limpos e datas normalizadas.
""",
        "label_favoravel": "✅ FAVORÁVEL",
        "label_critico": "🚨 CRÍTICO",
        "label_estavel": "⚖️ ESTÁVEL",
        "critico": "Crítico",
        "neutro_mapa": "Neutro",
        "favoravel": "Favorável",
    },
    "ES": {
        "page_title": "Civitas Radar",
        "header_subtitle": "Central de Inteligencia Política — Monitoreo de Reputación en Tiempo Real",
        "sidebar_title": "🛰️ Panel de Control",
        "nome_politico_label": "👤 Nombre del Político / Monitoreado",
        "nome_politico_help": "Ingrese el nombre para buscar noticias reales en Google News",
        "cenario_label": "📡 Escenario de Simulación",
        "cenario_help": "Define la narrativa de la simulación de redes sociales",
        "geo_label": "🗺️ Escala Geográfica",
        "geo_help": "Alterna entre barrios de la capital, ciudades del área metropolitana o macrorregiones",
        "volume_label": "📊 Volumen de Menciones",
        "btn_atualizar": "🔄 Actualizar Inteligencia",
        "version_label": "Civitas-Radar v2.0 — Fase 2",
        "cenario_ativo": "Escenario activo",
        "escala_geo": "Escala geo",
        "info_inicial": "👈 Configure los parámetros en la barra lateral y haga clic en **Actualizar Inteligencia** para iniciar el monitoreo.",
        "spinner_msg": "⏳ Recopilando inteligencia…",
        "kpi_aprovacao": "📈 Índice de Aprobación Digital",
        "kpi_volume": "📢 Volumen de Menciones (24h)",
        "kpi_sentimento": "🎯 Sentimiento Predominante",
        "acima_limiar": "Por encima del umbral",
        "abaixo_limiar": "Por debajo del umbral",
        "registros_coletados": "registros recopilados",
        "mencoes": "menciones",
        "tab_radar": "📡 Radar Tradicional",
        "tab_mapa": "🗺️ Mapa de Crisis",
        "tab_comando": "🏛️ Sala de Comando",
        "dist_sentimentos": "🟢🔴 Distribución de Sentimientos",
        "linha_tempo": "📈 Línea de Tiempo (Últimas 24h)",
        "intel_imprensa": "📰 Intel — Prensa",
        "intel_ruas": "💬 Intel — Voz de las Calles",
        "radio_tv": "📻 Radio Escucha / TV Clipping",
        "dark_social": "📱 Dark Social — WhatsApp Centinela",
        "tabela_completa": "📋 Ver Tabla Completa de Datos",
        "nenhuma_noticia": "Ninguna noticia encontrada.",
        "nenhuma_transcricao": "Ninguna transcripción disponible.",
        "nenhuma_msg": "Ningún mensaje interceptado.",
        "mapa_calor": "🗺️ Mapa de Calor — Sentimiento por Región",
        "escala": "Escala",
        "mencoes_mapeadas": "Total de menciones mapeadas",
        "regioes_criticas": "🚨 Regiones Críticas",
        "regioes_favoraveis": "✅ Regiones Favorables",
        "aprovacao": "Aprobación",
        "sentimento_regiao": "📊 Sentimiento por Región (Desglose)",
        "spin_doctor_title": "🏛️ Spin Doctor — Generador de Respuestas Estratégicas",
        "spin_doctor_desc": "Seleccione una mención negativa y genere una nota de respuesta oficial con el tono deseado. El módulo usa IA generativa (Gemini) cuando está disponible.",
        "selecione_mencao": "🎯 Seleccione la mención para responder",
        "mencao_selecionada": "Mención seleccionada",
        "tom_resposta": "Tono de Respuesta",
        "btn_gerar": "⚡ Generar Defensa",
        "spin_processando": "🧠 Spin Doctor procesando…",
        "nota_estrategica": "Nota Estratégica — Tono",
        "btn_copiar": "📋 Copiar Nota",
        "btn_regenerar": "🔄 Regenerar",
        "btn_exportar": "📤 Exportar PDF",
        "nenhum_negativo": "✅ Ninguna mención negativa detectada en este escenario. ¡Escenario bajo control!",
        "como_usar_titulo": "📖 Cómo usar esta aplicación",
        "como_usar_corpo": """
**Civitas-Radar** es una plataforma de Inteligencia Política y Monitoreo de Reputación Digital en tiempo real.

**Paso a paso:**
1. **Configure** el nombre del político/monitoreado en la barra lateral izquierda.
2. **Seleccione** un escenario de simulación — hay **10 escenarios** disponibles (Crisis de Salud, Corrupción, Inauguración, Viral Positivo, Seguridad Pública, Educación, Crisis Habitacional, Inundación, Estado de Emergencia, Calamidad Climática).
3. **Elija** la escala geográfica (Capital, Región Metropolitana o Macrorregiones).
4. **Ajuste** el volumen de menciones deseado con el slider.
5. **Haga clic** en "🔄 Actualizar Inteligencia" para generar los datos.

**Pestañas disponibles:**
- **📡 Radar Tradicional**: KPIs, gráficos de sentimiento (Donut + Línea de Tiempo), Intel Prensa (Google News en tiempo real), Voz de las Calles, Radio/TV y WhatsApp Centinela.
- **🗺️ Mapa de Crisis**: Mapa de calor georreferenciado con sentimiento por región + ranking de regiones críticas y favorables.
- **🏛️ Sala de Comando**: Spin Doctor — seleccione menciones negativas y genere notas estratégicas por IA (Gemini o plantilla local) con 3 tonos: Institucional, Militancia y Empático.

**Personalización:**
- **🌐 Idioma**: Alterne entre Portugués (BR) y Español (América Latina) en el selector superior.
- **🎨 Tema**: Elija entre Dark, Grey o Light en el selector de tema.

**Consejo**: Los datos de redes sociales son simulados para demostración. Las noticias se recopilan en tiempo real a través de Google News, con enlaces limpios y fechas normalizadas.
""",
        "label_favoravel": "✅ FAVORABLE",
        "label_critico": "🚨 CRÍTICO",
        "label_estavel": "⚖️ ESTABLE",
        "critico": "Crítico",
        "neutro_mapa": "Neutro",
        "favoravel": "Favorable",
    },
}

# ══════════════════════════════════════════════════════════════
# Temas visuais — paletas completas
# ══════════════════════════════════════════════════════════════
TEMAS = {
    "🌑 Dark": {
        "bg_main": "#0a0e14",
        "bg_card": "#0d1117",
        "bg_card_end": "#111d2e",
        "bg_sidebar": "#0d1117",
        "bg_sidebar_end": "#111d2e",
        "bg_kpi": "#111d2e",
        "bg_kpi_mid": "#162447",
        "bg_kpi_end": "#0d1117",
        "border": "#1c2333",
        "border_kpi": "rgba(88,166,255,0.18)",
        "border_kpi_hover": "rgba(88,166,255,0.35)",
        "glow_kpi": "rgba(88,166,255,0.06)",
        "glow_kpi_hover": "rgba(88,166,255,0.12)",
        "text_primary": "#c9d1d9",
        "text_heading": "#58a6ff",
        "text_muted": "#6e7681",
        "text_kpi_label": "#8b949e",
        "text_kpi_value": "#e6edf3",
        "accent": "#e94560",
        "tab_active": "#58a6ff",
        "tab_bg": "#0d1117",
        "plotly_bg": "rgba(0,0,0,0)",
        "plotly_font": "#c9d1d9",
        "plotly_grid": "#1c2333",
    },
    "🌫️ Grey": {
        "bg_main": "#1e1e2e",
        "bg_card": "#2a2a3d",
        "bg_card_end": "#33334d",
        "bg_sidebar": "#252538",
        "bg_sidebar_end": "#2e2e45",
        "bg_kpi": "#2a2a3d",
        "bg_kpi_mid": "#33334d",
        "bg_kpi_end": "#252538",
        "border": "#3d3d5c",
        "border_kpi": "rgba(147,130,220,0.22)",
        "border_kpi_hover": "rgba(147,130,220,0.40)",
        "glow_kpi": "rgba(147,130,220,0.08)",
        "glow_kpi_hover": "rgba(147,130,220,0.15)",
        "text_primary": "#d4d4e8",
        "text_heading": "#9382dc",
        "text_muted": "#8888aa",
        "text_kpi_label": "#a0a0c0",
        "text_kpi_value": "#ebebf5",
        "accent": "#e94560",
        "tab_active": "#9382dc",
        "tab_bg": "#252538",
        "plotly_bg": "rgba(0,0,0,0)",
        "plotly_font": "#d4d4e8",
        "plotly_grid": "#3d3d5c",
    },
    "☀️ Light": {
        "bg_main": "#f0f2f6",
        "bg_card": "#ffffff",
        "bg_card_end": "#f7f8fa",
        "bg_sidebar": "#ffffff",
        "bg_sidebar_end": "#f0f2f6",
        "bg_kpi": "#ffffff",
        "bg_kpi_mid": "#f7f8fa",
        "bg_kpi_end": "#eef1f5",
        "border": "#d0d7de",
        "border_kpi": "rgba(36,41,47,0.12)",
        "border_kpi_hover": "rgba(36,41,47,0.25)",
        "glow_kpi": "rgba(36,41,47,0.04)",
        "glow_kpi_hover": "rgba(36,41,47,0.08)",
        "text_primary": "#24292f",
        "text_heading": "#0550ae",
        "text_muted": "#656d76",
        "text_kpi_label": "#57606a",
        "text_kpi_value": "#1f2328",
        "accent": "#cf222e",
        "tab_active": "#0550ae",
        "tab_bg": "#f0f2f6",
        "plotly_bg": "rgba(0,0,0,0)",
        "plotly_font": "#24292f",
        "plotly_grid": "#d0d7de",
    },
}


def _gerar_css_tema(t: dict) -> str:
    """Gera o bloco CSS completo com base na paleta do tema selecionado."""
    return f"""
    <style>
    /* ═══ FORÇAR TEMA GLOBAL ═══ */
    :root {{ color-scheme: dark; }}

    .stApp,
    .stApp > div,
    .main .block-container {{
        background-color: {t['bg_main']} !important;
        color: {t['text_primary']} !important;
    }}

    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    [data-testid="column"] {{
        background-color: transparent !important;
    }}

    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp p, .stApp span, .stApp label, .stApp li, .stApp div {{
        color: {t['text_primary']} !important;
    }}

    .stApp .stMarkdown h4 {{
        color: {t['text_heading']} !important;
        font-weight: 700;
        letter-spacing: 0.5px;
    }}

    /* ═══ TABS ═══ */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: {t['tab_bg']} !important;
        border-bottom: 2px solid {t['border']};
        gap: 0;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent !important;
        color: {t['text_muted']} !important;
        border-bottom: 2px solid transparent;
        padding: 0.6rem 1.4rem;
        font-weight: 600;
    }}
    .stTabs [aria-selected="true"] {{
        color: {t['tab_active']} !important;
        border-bottom: 2px solid {t['tab_active']} !important;
        background-color: rgba(88,166,255,0.06) !important;
    }}

    /* ═══ INPUTS ═══ */
    .stTextInput > div > div,
    .stSelectbox > div > div,
    .stSlider > div {{
        background-color: {t['bg_card']} !important;
        color: {t['text_primary']} !important;
        border-color: {t['border']} !important;
    }}
    .stTextInput input, .stSelectbox select {{
        color: {t['text_primary']} !important;
    }}

    /* ═══ BOTÕES ═══ */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {{
        background: linear-gradient(135deg, #c9243f 0%, {t['accent']} 100%) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 700;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 12px rgba(233,69,96,0.25);
    }}
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover {{
        box-shadow: 0 4px 20px rgba(233,69,96,0.4) !important;
    }}
    .stButton > button {{
        background-color: {t['bg_card']} !important;
        color: {t['text_primary']} !important;
        border: 1px solid {t['border']} !important;
    }}

    /* ═══ EXPANDER ═══ */
    .streamlit-expanderHeader {{
        background-color: {t['bg_card']} !important;
        color: {t['text_primary']} !important;
        border: 1px solid {t['border']} !important;
    }}
    .streamlit-expanderContent {{
        background-color: {t['bg_card']} !important;
        border: 1px solid {t['border']} !important;
    }}

    /* ═══ DATAFRAME ═══ */
    .stDataFrame, .stDataFrame table {{
        background-color: {t['bg_card']} !important;
    }}
    .stDataFrame th {{
        background-color: {t['bg_card_end']} !important;
        color: {t['text_heading']} !important;
    }}
    .stDataFrame td {{
        color: {t['text_primary']} !important;
        border-color: {t['border']} !important;
    }}

    hr {{ border-color: {t['border']} !important; }}

    /* ═══ HEADER ═══ */
    .war-room-header {{
        background: linear-gradient(135deg, {t['bg_card']} 0%, {t['bg_card_end']} 40%, {t['bg_kpi_mid']} 100%);
        padding: 1.4rem 2.2rem;
        border-radius: 14px;
        margin-bottom: 1.5rem;
        border: 1px solid {t['border_kpi']};
        box-shadow: 0 0 30px {t['glow_kpi']}, inset 0 1px 0 rgba(255,255,255,0.03);
    }}
    .war-room-header h1 {{
        color: {t['accent']} !important;
        font-size: 2.1rem; margin: 0; font-weight: 800; letter-spacing: 3px;
        text-shadow: 0 0 20px rgba(233,69,96,0.3);
    }}
    .war-room-header p {{
        color: {t['text_muted']} !important;
        margin: 0.3rem 0 0 0; font-size: 0.88rem; letter-spacing: 0.5px;
    }}

    /* ═══ NEWS CARDS ═══ */
    .news-card {{
        background: linear-gradient(145deg, {t['bg_card']} 0%, {t['bg_card_end']} 100%);
        border-left: 4px solid {t['accent']};
        padding: 0.9rem 1.1rem; margin-bottom: 0.75rem; border-radius: 8px;
        border-top: 1px solid rgba(88,166,255,0.08);
        border-right: 1px solid {t['border']};
        border-bottom: 1px solid {t['border']};
    }}
    .news-card:hover {{ border-left-color: {t['tab_active']}; }}
    .news-card h4 {{ color: {t['text_kpi_value']} !important; margin: 0 0 0.3rem 0; font-size: 0.92rem; }}
    .news-card small {{ color: {t['text_muted']} !important; }}

    /* ═══ COMMENT ROWS ═══ */
    .comment-row {{
        background: linear-gradient(145deg, {t['bg_card']} 0%, {t['bg_card_end']} 100%);
        padding: 0.65rem 0.95rem; margin-bottom: 0.45rem; border-radius: 7px;
        border-left: 3px solid {t['border']};
        border-top: 1px solid rgba(255,255,255,0.02);
    }}
    .comment-row.positivo {{ border-left-color: #3fb950; }}
    .comment-row.negativo {{ border-left-color: #f85149; }}
    .comment-row.neutro   {{ border-left-color: #8b949e; }}

    /* ═══ SIDEBAR ═══ */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {t['bg_sidebar']} 0%, {t['bg_sidebar_end']} 100%) !important;
        border-right: 1px solid {t['border']};
    }}
    section[data-testid="stSidebar"] .stMarkdown h2 {{
        color: {t['accent']} !important;
        text-shadow: 0 0 12px rgba(233,69,96,0.2);
    }}
    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] small {{
        color: {t['text_muted']} !important;
    }}

    /* ═══ KPI CARDS ═══ */
    [data-testid="stMetric"] {{
        background: linear-gradient(145deg, {t['bg_kpi']} 0%, {t['bg_kpi_mid']} 50%, {t['bg_kpi_end']} 100%) !important;
        padding: 1.2rem 1.1rem; border-radius: 12px;
        border: 1px solid {t['border_kpi']} !important;
        box-shadow: 0 0 15px {t['glow_kpi']}, 0 4px 20px rgba(0,0,0,0.25),
                    inset 0 1px 0 rgba(255,255,255,0.04);
        transition: border-color 0.3s, box-shadow 0.3s;
        position: relative; overflow: hidden;
    }}
    [data-testid="stMetric"]:hover {{
        border-color: {t['border_kpi_hover']} !important;
        box-shadow: 0 0 25px {t['glow_kpi_hover']}, 0 6px 30px rgba(0,0,0,0.35),
                    inset 0 1px 0 rgba(255,255,255,0.06);
    }}
    [data-testid="stMetric"]::before {{
        content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, {t['tab_active']}, {t['accent']}, transparent);
        opacity: 0.6;
    }}
    [data-testid="stMetricLabel"] {{
        color: {t['text_kpi_label']} !important; font-weight: 600; letter-spacing: 0.3px;
    }}
    [data-testid="stMetricValue"] {{
        color: {t['text_kpi_value']} !important; font-weight: 800;
    }}
    [data-testid="stMetricDelta"] {{ font-weight: 600; }}

    /* ═══ OCULTAR BRANDING ═══ */
    #MainMenu {{visibility: hidden;}}
    header[data-testid="stHeader"] {{
        background: transparent !important;
        /* manter botão de toggle da sidebar visível */
    }}
    header[data-testid="stHeader"] .stAppDeployButton,
    header[data-testid="stHeader"] .stToolbar {{
        display: none !important;
    }}
    footer {{visibility: hidden;}}

    /* ═══ FOOTER ═══ */
    .footer-container {{
        text-align: center; color: {t['text_muted']}; font-size: 0.85rem;
        border-top: 1px solid {t['border']}; padding-top: 20px; margin-top: 30px;
    }}
    .footer-title {{
        color: {t['accent']}; font-weight: 700; font-size: 1rem; margin-bottom: 5px;
    }}
    .footer-contact a {{
        margin: 0 8px; color: {t['tab_active']} !important; text-decoration: none;
    }}
    .footer-contact a:hover {{ color: {t['accent']} !important; text-decoration: underline !important; }}
    .footer-copyright {{ margin-top: 15px; padding-top: 15px; color: {t['border']}; }}

    /* ═══ ALERTS / SPINNER / RADIO ═══ */
    .stAlert {{
        background-color: {t['bg_card_end']} !important;
        border-color: {t['border']} !important;
        color: {t['text_primary']} !important;
    }}
    .stSpinner > div {{ border-top-color: {t['accent']} !important; }}
    .stRadio label {{ color: {t['text_primary']} !important; }}
    .stRadio [role="radiogroup"] label[data-checked="true"] {{
        color: {t['tab_active']} !important;
    }}

    /* ═══ COMO USAR — expander estilizado ═══ */
    .como-usar-box {{
        background: linear-gradient(145deg, {t['bg_card']} 0%, {t['bg_card_end']} 100%);
        border: 1px solid {t['border']}; border-radius: 10px;
        padding: 1rem 1.2rem; margin-bottom: 1rem;
    }}

    </style>
    """

# ══════════════════════════════════════════════════════════════
# Configuração da página
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Civitas Radar",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inicializar session_state para idioma e tema ──────────────
if "idioma" not in st.session_state:
    st.session_state.idioma = "PT-BR"
if "tema" not in st.session_state:
    st.session_state.tema = "🌑 Dark"

# Atalhos
T = I18N[st.session_state.idioma]
tema_atual = TEMAS[st.session_state.tema]

# ── Injetar CSS dinâmico baseado no tema ──────────────────────
st.markdown(_gerar_css_tema(tema_atual), unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="war-room-header">
        <h1>🎯 CIVITAS RADAR</h1>
        <p>{T['header_subtitle']}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Controles: Idioma + Tema + Como Usar ──────────────────────
col_idioma, col_tema, col_spacer = st.columns([1, 1, 4])

with col_idioma:
    idioma_novo = st.selectbox(
        "🌐 Idioma",
        options=["PT-BR", "ES"],
        index=0 if st.session_state.idioma == "PT-BR" else 1,
        key="sel_idioma",
    )
    if idioma_novo != st.session_state.idioma:
        st.session_state.idioma = idioma_novo
        st.rerun()

with col_tema:
    tema_novo = st.selectbox(
        "🎨 Tema",
        options=list(TEMAS.keys()),
        index=list(TEMAS.keys()).index(st.session_state.tema),
        key="sel_tema",
    )
    if tema_novo != st.session_state.tema:
        st.session_state.tema = tema_novo
        st.rerun()

# Recarrega T após possível mudança
T = I18N[st.session_state.idioma]

with st.expander(T["como_usar_titulo"], expanded=False):
    st.markdown(T["como_usar_corpo"])

# ══════════════════════════════════════════════════════════════
# Barra lateral (Sidebar)
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"## {T['sidebar_title']}")
    st.divider()

    nome_politico = st.text_input(
        T["nome_politico_label"],
        value="Prefeito Silva",
        help=T["nome_politico_help"],
    )

    cenario_selecionado = st.selectbox(
        T["cenario_label"],
        options=list(CENARIOS.keys()),
        help=T["cenario_help"],
    )

    nivel_geo = st.selectbox(
        T["geo_label"],
        options=list(NIVEIS_GEO.keys()),
        help=T["geo_help"],
    )

    qtd_comentarios = st.slider(
        T["volume_label"],
        min_value=20,
        max_value=200,
        value=80,
        step=10,
    )

    st.divider()
    atualizar = st.button(
        T["btn_atualizar"],
        type="primary",
        use_container_width=True,
    )

    st.divider()
    st.caption(T["version_label"])
    st.caption(f"{T['cenario_ativo']}: **{cenario_selecionado}**")
    st.caption(f"{T['escala_geo']}: **{nivel_geo}**")

# ══════════════════════════════════════════════════════════════
# Lógica de processamento (ao clicar no botão)
# ══════════════════════════════════════════════════════════════

# Inicializa o estado da sessão
if "df_comentarios" not in st.session_state:
    st.session_state.df_comentarios = None
    st.session_state.noticias = None
    st.session_state.df_radio_tv = None
    st.session_state.df_whatsapp = None

if atualizar:
    with st.spinner(T["spinner_msg"]):
        simulador = SimuladorRedes(nivel_geo=nivel_geo)
        st.session_state.df_comentarios = simulador.gerar_comentarios(
            cenario_selecionado, quantidade=qtd_comentarios
        )
        st.session_state.df_radio_tv = simulador.gerar_transcricoes_radio_tv(
            cenario_selecionado, quantidade=max(15, qtd_comentarios // 4)
        )
        st.session_state.df_whatsapp = simulador.gerar_mensagens_whatsapp(
            cenario_selecionado, quantidade=max(10, qtd_comentarios // 5)
        )
        st.session_state.noticias = buscar_noticias_google(nome_politico)

# ══════════════════════════════════════════════════════════════
# Renderização do Dashboard
# ══════════════════════════════════════════════════════════════
df = st.session_state.df_comentarios
noticias = st.session_state.noticias
df_radio = st.session_state.df_radio_tv
df_wpp = st.session_state.df_whatsapp

if df is None:
    st.info(T["info_inicial"])
    st.stop()

# ── KPIs Globais ──────────────────────────────────────────────
sentimento_map = {"Positivo": 100, "Neutro": 50, "Negativo": 0}
df["Score"] = df["Sentimento"].map(sentimento_map)

indice_aprovacao = round(df["Score"].mean(), 1)
volume_mencoes = len(df)
sentimento_predominante = df["Sentimento"].value_counts().idxmax()
color_map = {"Positivo": "#3fb950", "Negativo": "#f85149", "Neutro": "#8b949e"}

label_sentimento = {
    "Positivo": T["label_favoravel"],
    "Negativo": T["label_critico"],
    "Neutro": T["label_estavel"],
}

col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

with col_kpi1:
    delta_color = "normal" if indice_aprovacao >= 50 else "inverse"
    st.metric(
        label=T["kpi_aprovacao"],
        value=f"{indice_aprovacao}%",
        delta=f"{T['acima_limiar'] if indice_aprovacao >= 50 else T['abaixo_limiar']}",
        delta_color=delta_color,
    )

with col_kpi2:
    st.metric(
        label=T["kpi_volume"],
        value=f"{volume_mencoes:,}".replace(",", "."),
        delta=f"{volume_mencoes} {T['registros_coletados']}",
        delta_color="off",
    )

with col_kpi3:
    st.metric(
        label=T["kpi_sentimento"],
        value=label_sentimento.get(sentimento_predominante, sentimento_predominante),
        delta=f"{df['Sentimento'].value_counts().iloc[0]} {T['mencoes']}",
        delta_color="off",
    )

st.divider()

# ══════════════════════════════════════════════════════════════
# ABAS PRINCIPAIS
# ══════════════════════════════════════════════════════════════
tab_radar, tab_mapa, tab_comando = st.tabs([
    T["tab_radar"],
    T["tab_mapa"],
    T["tab_comando"],
])

# ──────────────────────────────────────────────────────────────
# ABA 1: RADAR TRADICIONAL
# ──────────────────────────────────────────────────────────────
with tab_radar:
    # ── Gráficos ──────────────────────────────────────────────
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown(f"#### {T['dist_sentimentos']}")
        contagem = df["Sentimento"].value_counts().reset_index()
        contagem.columns = ["Sentimento", "Quantidade"]

        fig_donut = px.pie(
            contagem,
            names="Sentimento",
            values="Quantidade",
            hole=0.55,
            color="Sentimento",
            color_discrete_map=color_map,
        )
        fig_donut.update_layout(
            paper_bgcolor=tema_atual["plotly_bg"],
            plot_bgcolor=tema_atual["plotly_bg"],
            font_color=tema_atual["plotly_font"],
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
            margin=dict(t=10, b=40, l=10, r=10),
        )
        fig_donut.update_traces(
            textinfo="percent+label",
            textfont_size=13,
            marker=dict(line=dict(color=tema_atual["bg_main"], width=2)),
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_chart2:
        st.markdown(f"#### {T['linha_tempo']}")
        df_ts = df.copy()
        df_ts["Hora"] = df_ts["Data"].dt.floor("h")
        timeline = (
            df_ts.groupby(["Hora", "Sentimento"])
            .size()
            .reset_index(name="Menções")
        )
        fig_timeline = px.area(
            timeline,
            x="Hora",
            y="Menções",
            color="Sentimento",
            color_discrete_map=color_map,
            line_shape="spline",
        )
        fig_timeline.update_layout(
            paper_bgcolor=tema_atual["plotly_bg"],
            plot_bgcolor=tema_atual["plotly_bg"],
            font_color=tema_atual["plotly_font"],
            xaxis=dict(showgrid=False, color=tema_atual["text_muted"]),
            yaxis=dict(showgrid=True, gridcolor=tema_atual["plotly_grid"], color=tema_atual["text_muted"]),
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
            margin=dict(t=10, b=40, l=10, r=10),
            hovermode="x unified",
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

    st.divider()

    # ── Feed: Imprensa + Voz das Ruas ─────────────────────────
    col_news, col_social = st.columns(2)

    with col_news:
        st.markdown(f"#### {T['intel_imprensa']}")
        if noticias:
            news_cards_html = ""
            for n in noticias:
                titulo_safe = _html.escape(str(n['titulo']))
                fonte_safe = _html.escape(str(n['fonte']))
                data_safe = _html.escape(str(n['data']))
                link_html = (
                    f'<a href="{n["link"]}" target="_blank" style="color:{tema_atual["accent"]};text-decoration:none;">Abrir ↗</a>'
                    if n["link"] != "#"
                    else ""
                )
                news_cards_html += f"""
                <div class="news-card">
                    <h4>{titulo_safe}</h4>
                    <small>📅 {data_safe}  •  🏢 {fonte_safe}  {link_html}</small>
                </div>
                """
            st.markdown(news_cards_html, unsafe_allow_html=True)
        else:
            st.warning(T["nenhuma_noticia"])

    with col_social:
        st.markdown(f"#### {T['intel_ruas']}")
        icone_sentimento = {"Positivo": "🟢", "Negativo": "🔴", "Neutro": "⚪"}
        for _, row in df.head(15).iterrows():
            classe = row["Sentimento"].lower()
            icone = icone_sentimento.get(row["Sentimento"], "⚪")
            usuario_safe = _html.escape(str(row['Usuario']))
            texto_safe = _html.escape(str(row['Texto']))
            plataforma_safe = _html.escape(str(row['Plataforma']))
            bairro_safe = _html.escape(str(row['Bairro']))
            row_html = (
                f"<div class=\"comment-row {classe}\">"
                f"<strong>{usuario_safe}</strong>"
                f"<span style=\"float:right;font-size:0.8rem;color:{tema_atual['text_muted']}\">"
                f"{plataforma_safe}</span>"
                "<br/>"
                f"<span style=\"color:{tema_atual['text_primary']}\">{icone} {texto_safe}</span>"
                "<br/>"
                f"<small style=\"color:{tema_atual['text_muted']}\">"
                f"{row['Data'].strftime('%d/%m %H:%M')} • {bairro_safe}</small>"
                "</div>"
            )
            st.markdown(row_html, unsafe_allow_html=True)

    st.divider()

    # ── Omni-Channel: Rádio/TV + WhatsApp ─────────────────────
    col_radio, col_wpp = st.columns(2)

    with col_radio:
        st.markdown(f"#### {T['radio_tv']}")
        if df_radio is not None and not df_radio.empty:
            radio_html = ""
            for _, row in df_radio.head(10).iterrows():
                sent_icon = {"Positivo": "🟢", "Negativo": "🔴", "Neutro": "⚪"}.get(row["Sentimento"], "⚪")
                tipo_icon = "📺" if row["Tipo"] == "TV" else "📻"
                emissora_safe = _html.escape(str(row['Emissora']))
                transcricao_safe = _html.escape(str(row['Transcricao']))
                bairro_safe = _html.escape(str(row['Bairro']))
                radio_html += f"""
                <div class="news-card">
                    <h4>{tipo_icon} {emissora_safe} <span style="float:right">{sent_icon}</span></h4>
                    <small style="color:{tema_atual['text_primary']}">"{transcricao_safe}"</small><br/>
                    <small>🕐 {row['Timestamp'].strftime('%d/%m %H:%M')} • {bairro_safe}</small>
                </div>
                """
            st.markdown(radio_html, unsafe_allow_html=True)
        else:
            st.info(T["nenhuma_transcricao"])

    with col_wpp:
        st.markdown(f"#### {T['dark_social']}")
        if df_wpp is not None and not df_wpp.empty:
            wpp_html = ""
            for _, row in df_wpp.head(10).iterrows():
                sent_icon = {"Positivo": "🟢", "Negativo": "🔴", "Neutro": "⚪"}.get(row["Sentimento"], "⚪")
                viralidade_safe = _html.escape(str(row['Viralidade']))
                viral_badge = (
                    f'<span style="color:{tema_atual["accent"]};font-weight:700;"> {viralidade_safe}</span>'
                    if row["Viralidade"] != "—"
                    else ""
                )
                grupo_safe = _html.escape(str(row['Grupo']))
                msg_safe = _html.escape(str(row['Mensagem']))
                remetente_safe = _html.escape(str(row['Remetente']))
                bairro_safe = _html.escape(str(row['Bairro']))
                wpp_html += f"""
                <div class="comment-row {row['Sentimento'].lower()}">
                    <strong>📱 {grupo_safe}</strong>{viral_badge}
                    <br/>
                    <span style="color:{tema_atual['text_primary']}">{sent_icon} {msg_safe}</span>
                    <br/>
                    <small style="color:{tema_atual['text_muted']}">{remetente_safe} • {row['Timestamp'].strftime('%d/%m %H:%M')} • {bairro_safe}</small>
                </div>
                """
            st.markdown(wpp_html, unsafe_allow_html=True)
        else:
            st.info(T["nenhuma_msg"])

    # ── Tabela completa ───────────────────────────────────────
    with st.expander(T["tabela_completa"], expanded=False):
        st.dataframe(
            df[["Data", "Usuario", "Texto", "Sentimento", "Plataforma", "Bairro"]].style.map(
                lambda v: (
                    "color: #48bb78" if v == "Positivo"
                    else "color: #fc8181" if v == "Negativo"
                    else "color: #a0aec0"
                ),
                subset=["Sentimento"],
            ),
            use_container_width=True,
            height=400,
        )

# ──────────────────────────────────────────────────────────────
# ABA 2: MAPA DE CRISE (Geo-Inteligência)
# ──────────────────────────────────────────────────────────────
with tab_mapa:
    st.markdown(f"#### {T['mapa_calor']}")
    st.caption(f"{T['escala']}: **{nivel_geo}** • {T['mencoes_mapeadas']}: **{len(df)}**")

    # KPIs por região (top 5 mais negativas)
    bairro_sentimento = (
        df.groupby("Bairro")["Score"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "Aprovação", "count": "Menções"})
        .sort_values("Aprovação")
        .reset_index()
    )
    bairro_sentimento["Aprovação"] = bairro_sentimento["Aprovação"].round(1)

    col_map, col_rank = st.columns([3, 1])

    with col_map:
        # Mapa de calor com density_mapbox
        centro = NIVEIS_GEO[nivel_geo]["centro"]

        fig_map = px.density_mapbox(
            df,
            lat="Latitude",
            lon="Longitude",
            z="Score",
            radius=25,
            center=dict(lat=centro[0], lon=centro[1]),
            zoom=10 if "Capital" in nivel_geo else 8 if "Metropolitana" in nivel_geo else 6,
            mapbox_style="carto-darkmatter",
            color_continuous_scale=["#fc8181", "#f6e05e", "#48bb78"],
            range_color=[0, 100],
            hover_data={"Bairro": True, "Sentimento": True},
        )
        fig_map.update_layout(
            paper_bgcolor=tema_atual["plotly_bg"],
            font_color=tema_atual["plotly_font"],
            margin=dict(t=0, b=0, l=0, r=0),
            height=520,
            coloraxis_colorbar=dict(
                title="Aprovação",
                tickvals=[0, 50, 100],
            ticktext=[T["critico"], T["neutro_mapa"], T["favoravel"]],
            ),
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_rank:
        st.markdown(f"##### {T['regioes_criticas']}")
        for _, row in bairro_sentimento.head(5).iterrows():
            cor = "#fc8181" if row["Aprovação"] < 40 else "#f6e05e" if row["Aprovação"] < 60 else "#48bb78"
            bairro_safe = _html.escape(str(row['Bairro']))
            st.markdown(
                f"""
                <div style="background:{tema_atual['bg_card']};padding:0.6rem;margin-bottom:0.4rem;border-radius:6px;
                            border-left:3px solid {cor};">
                    <strong style="color:{tema_atual['text_primary']}">{bairro_safe}</strong><br/>
                    <small style="color:{cor}">{T['aprovacao']}: {row['Aprovação']}% • {int(row['Menções'])} {T['mencoes']}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(f"##### {T['regioes_favoraveis']}")
        for _, row in bairro_sentimento.tail(5).iloc[::-1].iterrows():
            cor = "#48bb78" if row["Aprovação"] >= 60 else "#f6e05e" if row["Aprovação"] >= 40 else "#fc8181"
            bairro_safe = _html.escape(str(row['Bairro']))
            st.markdown(
                f"""
                <div style="background:{tema_atual['bg_card']};padding:0.6rem;margin-bottom:0.4rem;border-radius:6px;
                            border-left:3px solid {cor};">
                    <strong style="color:{tema_atual['text_primary']}">{bairro_safe}</strong><br/>
                    <small style="color:{cor}">{T['aprovacao']}: {row['Aprovação']}% • {int(row['Menções'])} {T['mencoes']}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Gráfico de barras por região
    st.divider()
    st.markdown(f"#### {T['sentimento_regiao']}")

    bairro_breakdown = (
        df.groupby(["Bairro", "Sentimento"])
        .size()
        .reset_index(name="Menções")
    )
    fig_bar = px.bar(
        bairro_breakdown,
        x="Bairro",
        y="Menções",
        color="Sentimento",
        color_discrete_map=color_map,
        barmode="stack",
    )
    fig_bar.update_layout(
        paper_bgcolor=tema_atual["plotly_bg"],
        plot_bgcolor=tema_atual["plotly_bg"],
        font_color=tema_atual["plotly_font"],
        xaxis=dict(showgrid=False, color=tema_atual["text_muted"], tickangle=-45),
        yaxis=dict(showgrid=True, gridcolor=tema_atual["plotly_grid"], color=tema_atual["text_muted"]),
        legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5),
        margin=dict(t=10, b=80, l=10, r=10),
        height=380,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ──────────────────────────────────────────────────────────────
# ABA 3: SALA DE COMANDO (Spin Doctor)
# ──────────────────────────────────────────────────────────────
with tab_comando:
    st.markdown(f"#### {T['spin_doctor_title']}")
    st.caption(T["spin_doctor_desc"])

    # Filtra itens negativos de todas as fontes
    negativos_redes = df[df["Sentimento"] == "Negativo"][["Texto", "Plataforma", "Bairro"]].head(10)
    negativos_redes = negativos_redes.rename(columns={"Texto": "Conteúdo"})
    negativos_redes["Origem"] = "🌐 Redes Sociais"
    negativos_redes["Criticidade"] = negativos_redes["Conteúdo"].apply(classificar_criticidade)

    items_negativos = negativos_redes[["Conteúdo", "Origem", "Criticidade"]].copy()

    if df_radio is not None and not df_radio.empty:
        neg_radio = df_radio[df_radio["Sentimento"] == "Negativo"][["Transcricao", "Emissora"]].head(5)
        if not neg_radio.empty:
            neg_radio = neg_radio.rename(columns={"Transcricao": "Conteúdo", "Emissora": "Origem"})
            neg_radio["Origem"] = "📻 " + neg_radio["Origem"]
            neg_radio["Criticidade"] = neg_radio["Conteúdo"].apply(classificar_criticidade)
            items_negativos = pd.concat([items_negativos, neg_radio[["Conteúdo", "Origem", "Criticidade"]]], ignore_index=True)

    if df_wpp is not None and not df_wpp.empty:
        neg_wpp = df_wpp[df_wpp["Sentimento"] == "Negativo"][["Mensagem", "Grupo", "Viralidade"]].head(5)
        if not neg_wpp.empty:
            neg_wpp = neg_wpp.rename(columns={"Mensagem": "Conteúdo", "Grupo": "Origem"})
            neg_wpp["Origem"] = "📱 " + neg_wpp["Origem"]
            neg_wpp["Criticidade"] = neg_wpp["Conteúdo"].apply(classificar_criticidade)
            items_negativos = pd.concat([items_negativos, neg_wpp[["Conteúdo", "Origem", "Criticidade"]]], ignore_index=True)

    if items_negativos.empty:
        st.success(T["nenhum_negativo"])
    else:
        # Seletor de menção
        opcoes = [
            f"{row['Criticidade']} [{row['Origem']}] {row['Conteúdo'][:80]}..."
            for _, row in items_negativos.iterrows()
        ]
        selecionado_idx = st.selectbox(
            T["selecione_mencao"],
            range(len(opcoes)),
            format_func=lambda i: opcoes[i],
        )

        texto_selecionado = items_negativos.iloc[selecionado_idx]["Conteúdo"]
        texto_sel_safe = _html.escape(str(texto_selecionado))

        st.markdown(
            f"""
            <div class="news-card" style="border-left-color:{tema_atual['accent']};">
                <h4 style="color:{tema_atual['accent']};">{T['mencao_selecionada']}</h4>
                <span style="color:{tema_atual['text_primary']}">{texto_sel_safe}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Controles do Spin Doctor
        col_tom, col_btn = st.columns([3, 1])

        with col_tom:
            tom_selecionado = st.radio(
                T["tom_resposta"],
                options=list(TONS_RESPOSTA.keys()),
                format_func=lambda t: f"{TONS_RESPOSTA[t]['emoji']} {t} — {TONS_RESPOSTA[t]['descricao']}",
                horizontal=True,
            )

        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            gerar = st.button(T["btn_gerar"], type="primary", use_container_width=True)

        # Geração da nota
        if gerar:
            with st.spinner(T["spin_processando"]):
                resultado = gerar_nota_estrategica(
                    texto_critico=texto_selecionado,
                    tom=tom_selecionado,
                    contexto_politico=f"Político: {nome_politico} | Cenário: {cenario_selecionado}",
                )

            emoji_tom = TONS_RESPOSTA[resultado["tom"]]["emoji"]
            fonte_badge = "🤖 Gemini" if resultado["fonte"] == "gemini" else "📋 Template"

            nota_safe = _html.escape(str(resultado['nota']))
            st.markdown(
                f"""
                <div style="background:{tema_atual['bg_card']};padding:1.2rem;border-radius:10px;
                            border:1px solid {tema_atual['border']};margin-top:1rem;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.8rem;">
                        <span style="color:{tema_atual['accent']};font-weight:700;font-size:1rem;">
                            {emoji_tom} {T['nota_estrategica']} {resultado['tom']}
                        </span>
                        <span style="color:{tema_atual['text_muted']};font-size:0.8rem;">{fonte_badge}</span>
                    </div>
                    <div style="color:{tema_atual['text_primary']};line-height:1.7;white-space:pre-wrap;">{nota_safe}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Ações de acompanhamento
            col_a1, col_a2, col_a3 = st.columns(3)
            with col_a1:
                st.button(T["btn_copiar"], use_container_width=True)
            with col_a2:
                st.button(T["btn_regenerar"], use_container_width=True)
            with col_a3:
                st.button(T["btn_exportar"], use_container_width=True)

# ══════════════════════════════════════════════════════════════
# Footer Profissional
# ══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    f"""
    <div class="footer-container">
        <div class="footer-title">
            🎯 Civitas-Radar | Inteligência Política em Tempo Real
        </div>
        <div style="font-size: 0.9rem; margin-bottom: 1rem; font-style: italic; color: {tema_atual['text_muted']};">
            Monitoramento de Reputação Digital — War Room Dashboard
        </div>
        <div style="margin-bottom: 1rem; color: {tema_atual['text_muted']};">
            Streamlit + Python + Plotly + GoogleNews + TextBlob
        </div>
        <div style="border-top: 1px solid {tema_atual['border']}; padding-top: 1rem; margin-top: 1rem;">
            <div style="font-weight: 600; color: {tema_atual['accent']}; margin-bottom: 0.5rem;">Lenon de Paula</div>
            <div style="font-size: 0.85rem; color: {tema_atual['text_muted']}; margin-bottom: 0.75rem;">
                Especialista em Ciência de Dados e IA | Jornalista | Desenvolvedor de Soluções Avançadas
            </div>
            <div class="footer-contact" style="margin-bottom: 0.75rem;">
                <a href="mailto:lenondpaula@gmail.com">📧 lenondpaula@gmail.com</a>
                <a href="https://wa.me/5555981359099">💬 +55 (55) 98135-9099</a>
            </div>
            <div class="footer-contact" style="margin-bottom: 0.75rem;">
                <a href="https://www.linkedin.com/in/lenonmpaula/">🔗 LinkedIn</a>
                <a href="https://github.com/lenondpaula">🐙 GitHub</a>
                <a href="https://t.me/+5555981359099">📲 Telegram</a>
                <a href="https://goodluke.streamlit.app/">🧪 GoodLuke AI Hub</a>
            </div>
            <div class="footer-copyright">
                © 2026 Lenon de Paula
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
