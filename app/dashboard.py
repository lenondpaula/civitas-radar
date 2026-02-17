"""
Civitas-Radar — Dashboard de Inteligência Política
====================================================
Interface visual "War Room" (Sala de Situação)
Executar:  streamlit run app/dashboard.py
"""

from __future__ import annotations

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
# Configuração da página
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Civitas Radar",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS tema "War Room" ───────────────────────────────────────
st.markdown(
    """
    <style>
    /* Fundo escuro geral */
    .stApp {
        background-color: #0e1117;
        color: #c5c6c8;
    }

    /* Header principal */
    .war-room-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 1.2rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #e94560;
        box-shadow: 0 0 20px rgba(233, 69, 96, 0.15);
    }
    .war-room-header h1 {
        color: #e94560;
        font-size: 2rem;
        margin: 0;
        font-weight: 800;
        letter-spacing: 2px;
    }
    .war-room-header p {
        color: #8892b0;
        margin: 0.25rem 0 0 0;
        font-size: 0.9rem;
    }

    /* Cards de notícia */
    .news-card {
        background: #1a1a2e;
        border-left: 4px solid #e94560;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.75rem;
        border-radius: 6px;
    }
    .news-card h4 {
        color: #e2e8f0;
        margin: 0 0 0.3rem 0;
        font-size: 0.92rem;
    }
    .news-card small {
        color: #718096;
    }

    /* Tabela de comentários */
    .comment-row {
        background: #1a1a2e;
        padding: 0.6rem 0.9rem;
        margin-bottom: 0.4rem;
        border-radius: 6px;
        border-left: 3px solid #4a5568;
    }
    .comment-row.positivo { border-left-color: #48bb78; }
    .comment-row.negativo { border-left-color: #fc8181; }
    .comment-row.neutro   { border-left-color: #a0aec0; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1a1a2e;
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #e94560;
    }

    /* Métricas */
    [data-testid="stMetric"] {
        background: #16213e;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #2d3748;
    }
    [data-testid="stMetricLabel"] {
        color: #8892b0 !important;
    }

    /* Esconder branding */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}

    /* Footer profissional */
    .footer-container {
        text-align: center;
        color: #718096;
        font-size: 0.85rem;
        border-top: 1px solid #2d3748;
        padding-top: 20px;
        margin-top: 30px;
    }
    .footer-title {
        color: #e94560;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 5px;
    }
    .footer-contact a {
        margin: 0 8px;
        color: #e94560 !important;
        text-decoration: none;
    }
    .footer-contact a:hover {
        text-decoration: underline !important;
    }
    .footer-copyright {
        margin-top: 15px;
        padding-top: 15px;
        color: #4a5568;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────
st.markdown(
    """
    <div class="war-room-header">
        <h1>🎯 CIVITAS RADAR</h1>
        <p>Central de Inteligência Política — Monitoramento de Reputação em Tempo Real</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════════════════════
# Barra lateral (Sidebar)
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🛰️ Painel de Controle")
    st.divider()

    nome_politico = st.text_input(
        "👤 Nome do Político / Monitorado",
        value="Prefeito Silva",
        help="Digite o nome para buscar notícias reais no Google News",
    )

    cenario_selecionado = st.selectbox(
        "📡 Cenário de Simulação",
        options=list(CENARIOS.keys()),
        help="Define a narrativa da simulação de redes sociais",
    )

    nivel_geo = st.selectbox(
        "🗺️ Escala Geográfica",
        options=list(NIVEIS_GEO.keys()),
        help="Alterna entre bairros da capital, cidades da RM ou macrorregiões do RS",
    )

    qtd_comentarios = st.slider(
        "📊 Volume de Menções",
        min_value=20,
        max_value=200,
        value=80,
        step=10,
    )

    st.divider()
    atualizar = st.button(
        "🔄 Atualizar Inteligência",
        type="primary",
        use_container_width=True,
    )

    st.divider()
    st.caption("Civitas-Radar v2.0 — Fase 2")
    st.caption(f"Cenário ativo: **{cenario_selecionado}**")
    st.caption(f"Escala geo: **{nivel_geo}**")

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
    with st.spinner("⏳ Coletando inteligência…"):
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
    st.info(
        "👈 Configure os parâmetros na barra lateral e clique em "
        "**Atualizar Inteligência** para iniciar o monitoramento."
    )
    st.stop()

# ── KPIs Globais ──────────────────────────────────────────────
sentimento_map = {"Positivo": 100, "Neutro": 50, "Negativo": 0}
df["Score"] = df["Sentimento"].map(sentimento_map)

indice_aprovacao = round(df["Score"].mean(), 1)
volume_mencoes = len(df)
sentimento_predominante = df["Sentimento"].value_counts().idxmax()
color_map = {"Positivo": "#48bb78", "Negativo": "#fc8181", "Neutro": "#a0aec0"}

label_sentimento = {
    "Positivo": "✅ FAVORÁVEL",
    "Negativo": "🚨 CRÍTICO",
    "Neutro": "⚖️ ESTÁVEL",
}

col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

with col_kpi1:
    delta_color = "normal" if indice_aprovacao >= 50 else "inverse"
    st.metric(
        label="📈 Índice de Aprovação Digital",
        value=f"{indice_aprovacao}%",
        delta=f"{'Acima' if indice_aprovacao >= 50 else 'Abaixo'} do limiar",
        delta_color=delta_color,
    )

with col_kpi2:
    st.metric(
        label="📢 Volume de Menções (24h)",
        value=f"{volume_mencoes:,}".replace(",", "."),
        delta=f"{volume_mencoes} registros coletados",
        delta_color="off",
    )

with col_kpi3:
    st.metric(
        label="🎯 Sentimento Predominante",
        value=label_sentimento.get(sentimento_predominante, sentimento_predominante),
        delta=f"{df['Sentimento'].value_counts().iloc[0]} menções",
        delta_color="off",
    )

st.divider()

# ══════════════════════════════════════════════════════════════
# ABAS PRINCIPAIS
# ══════════════════════════════════════════════════════════════
tab_radar, tab_mapa, tab_comando = st.tabs([
    "📡 Radar Tradicional",
    "🗺️ Mapa de Crise",
    "🏛️ Sala de Comando",
])

# ──────────────────────────────────────────────────────────────
# ABA 1: RADAR TRADICIONAL
# ──────────────────────────────────────────────────────────────
with tab_radar:
    # ── Gráficos ──────────────────────────────────────────────
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("#### 🟢🔴 Distribuição de Sentimentos")
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
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#c5c6c8",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
            margin=dict(t=10, b=40, l=10, r=10),
        )
        fig_donut.update_traces(
            textinfo="percent+label",
            textfont_size=13,
            marker=dict(line=dict(color="#0e1117", width=2)),
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_chart2:
        st.markdown("#### 📈 Linha do Tempo (Últimas 24h)")
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
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#c5c6c8",
            xaxis=dict(showgrid=False, color="#8892b0"),
            yaxis=dict(showgrid=True, gridcolor="#2d3748", color="#8892b0"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
            margin=dict(t=10, b=40, l=10, r=10),
            hovermode="x unified",
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

    st.divider()

    # ── Feed: Imprensa + Voz das Ruas ─────────────────────────
    col_news, col_social = st.columns(2)

    with col_news:
        st.markdown("#### 📰 Intel — Imprensa")
        if noticias:
            for n in noticias:
                link_html = (
                    f'<a href="{n["link"]}" target="_blank" style="color:#e94560;text-decoration:none;">Abrir ↗</a>'
                    if n["link"] != "#"
                    else ""
                )
                st.markdown(
                    f"""
                    <div class="news-card">
                        <h4>{n['titulo']}</h4>
                        <small>📅 {n['data']}  •  🏢 {n['fonte']}  {link_html}</small>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.warning("Nenhuma notícia encontrada.")

    with col_social:
        st.markdown("#### 💬 Intel — Voz das Ruas")
        icone_sentimento = {"Positivo": "🟢", "Negativo": "🔴", "Neutro": "⚪"}
        for _, row in df.head(15).iterrows():
            classe = row["Sentimento"].lower()
            icone = icone_sentimento.get(row["Sentimento"], "⚪")
            st.markdown(
                f"""
                <div class="comment-row {classe}">
                    <strong>{row['Usuario']}</strong>
                    <span style="float:right;font-size:0.8rem;color:#718096">{row['Plataforma']}</span>
                    <br/>
                    <span style="color:#e2e8f0">{icone} {row['Texto']}</span>
                    <br/>
                    <small style="color:#4a5568">{row['Data'].strftime('%d/%m %H:%M')} • {row['Bairro']}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # ── Omni-Channel: Rádio/TV + WhatsApp ─────────────────────
    col_radio, col_wpp = st.columns(2)

    with col_radio:
        st.markdown("#### 📻 Rádio Escuta / TV Clipping")
        if df_radio is not None and not df_radio.empty:
            for _, row in df_radio.head(10).iterrows():
                sent_icon = {"Positivo": "🟢", "Negativo": "🔴", "Neutro": "⚪"}.get(row["Sentimento"], "⚪")
                tipo_icon = "📺" if row["Tipo"] == "TV" else "📻"
                st.markdown(
                    f"""
                    <div class="news-card">
                        <h4>{tipo_icon} {row['Emissora']} <span style="float:right">{sent_icon}</span></h4>
                        <small style="color:#e2e8f0">"{row['Transcricao']}"</small><br/>
                        <small>🕐 {row['Timestamp'].strftime('%d/%m %H:%M')} • {row['Bairro']}</small>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("Nenhuma transcrição disponível.")

    with col_wpp:
        st.markdown("#### 📱 Dark Social — WhatsApp Sentinela")
        if df_wpp is not None and not df_wpp.empty:
            for _, row in df_wpp.head(10).iterrows():
                sent_icon = {"Positivo": "🟢", "Negativo": "🔴", "Neutro": "⚪"}.get(row["Sentimento"], "⚪")
                viral_badge = (
                    f'<span style="color:#fc8181;font-weight:700;"> {row["Viralidade"]}</span>'
                    if row["Viralidade"] != "—"
                    else ""
                )
                st.markdown(
                    f"""
                    <div class="comment-row {row['Sentimento'].lower()}">
                        <strong>📱 {row['Grupo']}</strong>{viral_badge}
                        <br/>
                        <span style="color:#e2e8f0">{sent_icon} {row['Mensagem']}</span>
                        <br/>
                        <small style="color:#4a5568">{row['Remetente']} • {row['Timestamp'].strftime('%d/%m %H:%M')} • {row['Bairro']}</small>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("Nenhuma mensagem interceptada.")

    # ── Tabela completa ───────────────────────────────────────
    with st.expander("📋 Ver Tabela Completa de Dados", expanded=False):
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
    st.markdown("#### 🗺️ Mapa de Calor — Sentimento por Região")
    st.caption(f"Escala: **{nivel_geo}** • Total de menções mapeadas: **{len(df)}**")

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
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#c5c6c8",
            margin=dict(t=0, b=0, l=0, r=0),
            height=520,
            coloraxis_colorbar=dict(
                title="Aprovação",
                tickvals=[0, 50, 100],
                ticktext=["Crítico", "Neutro", "Favorável"],
            ),
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_rank:
        st.markdown("##### 🚨 Regiões Críticas")
        for _, row in bairro_sentimento.head(5).iterrows():
            cor = "#fc8181" if row["Aprovação"] < 40 else "#f6e05e" if row["Aprovação"] < 60 else "#48bb78"
            st.markdown(
                f"""
                <div style="background:#1a1a2e;padding:0.6rem;margin-bottom:0.4rem;border-radius:6px;
                            border-left:3px solid {cor};">
                    <strong style="color:#e2e8f0">{row['Bairro']}</strong><br/>
                    <small style="color:{cor}">Aprovação: {row['Aprovação']}% • {int(row['Menções'])} menções</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("##### ✅ Regiões Favoráveis")
        for _, row in bairro_sentimento.tail(5).iloc[::-1].iterrows():
            cor = "#48bb78" if row["Aprovação"] >= 60 else "#f6e05e" if row["Aprovação"] >= 40 else "#fc8181"
            st.markdown(
                f"""
                <div style="background:#1a1a2e;padding:0.6rem;margin-bottom:0.4rem;border-radius:6px;
                            border-left:3px solid {cor};">
                    <strong style="color:#e2e8f0">{row['Bairro']}</strong><br/>
                    <small style="color:{cor}">Aprovação: {row['Aprovação']}% • {int(row['Menções'])} menções</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Gráfico de barras por região
    st.divider()
    st.markdown("#### 📊 Sentimento por Região (Breakdown)")

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
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#c5c6c8",
        xaxis=dict(showgrid=False, color="#8892b0", tickangle=-45),
        yaxis=dict(showgrid=True, gridcolor="#2d3748", color="#8892b0"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5),
        margin=dict(t=10, b=80, l=10, r=10),
        height=380,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ──────────────────────────────────────────────────────────────
# ABA 3: SALA DE COMANDO (Spin Doctor)
# ──────────────────────────────────────────────────────────────
with tab_comando:
    st.markdown("#### 🏛️ Spin Doctor — Gerador de Respostas Estratégicas")
    st.caption(
        "Selecione uma menção negativa e gere uma nota de resposta oficial "
        "com o tom desejado. O módulo usa IA generativa (Gemini) quando disponível."
    )

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
        st.success("✅ Nenhuma menção negativa detectada neste cenário. Cenário sob controle!")
    else:
        # Seletor de menção
        opcoes = [
            f"{row['Criticidade']} [{row['Origem']}] {row['Conteúdo'][:80]}..."
            for _, row in items_negativos.iterrows()
        ]
        selecionado_idx = st.selectbox(
            "🎯 Selecione a menção para responder",
            range(len(opcoes)),
            format_func=lambda i: opcoes[i],
        )

        texto_selecionado = items_negativos.iloc[selecionado_idx]["Conteúdo"]

        st.markdown(
            f"""
            <div class="news-card" style="border-left-color:#fc8181;">
                <h4 style="color:#fc8181;">Menção selecionada</h4>
                <span style="color:#e2e8f0">{texto_selecionado}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Controles do Spin Doctor
        col_tom, col_btn = st.columns([3, 1])

        with col_tom:
            tom_selecionado = st.radio(
                "Tom da Resposta",
                options=list(TONS_RESPOSTA.keys()),
                format_func=lambda t: f"{TONS_RESPOSTA[t]['emoji']} {t} — {TONS_RESPOSTA[t]['descricao']}",
                horizontal=True,
            )

        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            gerar = st.button("⚡ Gerar Defesa", type="primary", use_container_width=True)

        # Geração da nota
        if gerar:
            with st.spinner("🧠 Spin Doctor processando…"):
                resultado = gerar_nota_estrategica(
                    texto_critico=texto_selecionado,
                    tom=tom_selecionado,
                    contexto_politico=f"Político: {nome_politico} | Cenário: {cenario_selecionado}",
                )

            emoji_tom = TONS_RESPOSTA[resultado["tom"]]["emoji"]
            fonte_badge = "🤖 Gemini" if resultado["fonte"] == "gemini" else "📋 Template"

            st.markdown(
                f"""
                <div style="background:#1a1a2e;padding:1.2rem;border-radius:10px;
                            border:1px solid #2d3748;margin-top:1rem;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.8rem;">
                        <span style="color:#e94560;font-weight:700;font-size:1rem;">
                            {emoji_tom} Nota Estratégica — Tom {resultado['tom']}
                        </span>
                        <span style="color:#718096;font-size:0.8rem;">{fonte_badge}</span>
                    </div>
                    <div style="color:#e2e8f0;line-height:1.7;white-space:pre-wrap;">{resultado['nota']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Ações de acompanhamento
            col_a1, col_a2, col_a3 = st.columns(3)
            with col_a1:
                st.button("📋 Copiar Nota", use_container_width=True)
            with col_a2:
                st.button("🔄 Regenerar", use_container_width=True)
            with col_a3:
                st.button("📤 Exportar PDF", use_container_width=True)

# ══════════════════════════════════════════════════════════════
# Footer Profissional
# ══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    """
    <div class="footer-container">
        <div class="footer-title">
            🎯 Civitas-Radar | Inteligência Política em Tempo Real
        </div>
        <div style="font-size: 0.9rem; margin-bottom: 1rem; font-style: italic; color: #8892b0;">
            Monitoramento de Reputação Digital — War Room Dashboard
        </div>
        <div style="margin-bottom: 1rem; color: #8892b0;">
            Streamlit + Python + Plotly + GoogleNews + TextBlob
        </div>
        <div style="border-top: 1px solid #2d3748; padding-top: 1rem; margin-top: 1rem;">
            <div style="font-weight: 600; color: #e94560; margin-bottom: 0.5rem;">Lenon de Paula</div>
            <div style="font-size: 0.85rem; color: #8892b0; margin-bottom: 0.75rem;">
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
