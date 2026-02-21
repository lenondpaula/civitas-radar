# Copilot Instructions — Civitas-Radar

## Sobre o Projeto

**Civitas-Radar** é uma plataforma de **Inteligência Política e Monitoramento de Reputação Digital** em tempo real.
A aplicação simula cenários de crise e oportunidade na esfera pública, combinando dados simulados de redes sociais com notícias reais via Google News.

O visual segue o conceito **"War Room"** (Sala de Situação), com 3 temas dinâmicos (Dark, Grey, Light) e suporte bilíngue (PT-BR + ES).

---

## Stack Tecnológica

| Tecnologia | Uso |
|------------|-----|
| **Python 3.10+** | Linguagem base |
| **Streamlit** | Framework Web interativo |
| **Pandas** | Manipulação e análise de dados |
| **NumPy** | Operações numéricas |
| **Plotly** | Visualizações interativas (Donut, Timeline, Barras, Mapbox) |
| **Faker** | Geração de dados sintéticos (locale pt_BR) |
| **GoogleNews** | Coleta de notícias reais (com limpeza de links e normalização de datas) |
| **TextBlob** | Análise de sentimento |
| **Groq LLM API** | Spin Doctor via Groq (com fallback local) |
| **Selenium** | Keep-alive do app no Streamlit Cloud |

---

## Arquitetura

```
civitas-radar/
├── app/
│   └── dashboard.py              # 🎯 Dashboard Streamlit (War Room) — 3 abas + i18n + temas
├── src/
│   ├── __init__.py
│   ├── data_engine.py            # 🧠 Motor de simulação, geo e coleta (15 cenários)
│   └── ai_advisor.py             # 🏛️ Spin Doctor (Gerador de Respostas IA via Groq)
├── data/                         # 📁 Dados auxiliares e cache
├── .github/
│   ├── copilot-instructions.md   # 🤖 Este arquivo
│   └── INSTRUCTIONS.md           # 📋 Guia de contribuição e setup
├── keep_alive.py                 # ♻️ Script Selenium para manter app ativo
├── requirements.txt              # 📦 Dependências Python
├── .gitignore
└── README.md
```

---

## Convenções de Código

### Python
- Sempre usar **type hints** quando possível.
- Docstrings em português (BR) para funções públicas.
- Strings f-string como padrão.
- Imports absolutos a partir de `src/` (ex: `from src.data_engine import SimuladorRedes`).
- Encoding: UTF-8.
- Variáveis e funções em **snake_case**; classes em **PascalCase**.

### Streamlit
- Usar `st.markdown()` com `unsafe_allow_html=True` para componentes estilizados.
- CSS customizado dinâmico via `_gerar_css_tema()` — **não usar cores hardcoded**.
- Session state para persistência entre execuções.
- Layout `wide` obrigatório.

### Sistema de Temas (3 paletas dinâmicas)
As cores **não são fixas** — são definidas no dict `TEMAS` e aplicadas via `_gerar_css_tema(tema)`.

| Tema | Background | Cards | Accent |
|------|-----------|-------|--------|
| **Dark** | `#0a0e14` | `#131a27` | `#e94560` |
| **Grey** | `#1e1e2e` | `#2a2a3e` | `#e94560` |
| **Light** | `#f0f2f6` | `#ffffff` | `#cf222e` |

Cada tema define: `bg`, `card`, `accent`, `text`, `text2`, `muted`, `border`, `positivo`, `negativo`, `neutro`.

### Sistema i18n (Internacionalização)
- Dict `I18N` com chaves para PT-BR e ES.
- Todos os rótulos, abas, KPIs, botões, mensagens e onboarding são traduzidos.
- Ao adicionar novos textos, incluir ambas as traduções no dict `I18N`.
- Idioma selecionado via sidebar e armazenado em `session_state`.

---

## Módulos Principais

### `src/data_engine.py`
- `CENARIOS`: dict com **15 cenários** pré-definidos (cada um com keywords positivas, negativas e neutras):
  - Crise na Saúde, Escândalo de Corrupção, Inauguração de Obra, Viral Positivo
  - Avanço na Segurança Pública, Revolução na Educação, Crise Habitacional
  - Crise de Produto / Serviço, Escândalo de Marca, Campanha de Alto Impacto
  - Ciberataque e Vazamento de Dados, Crise Trabalhista, Cancelamento Digital
  - Prêmio / Reconhecimento, Vida Pessoal em Pauta
- `NIVEIS_GEO`: segmentação territorial hierárquica (Capital, Metropolitana, Estadual) com coordenadas reais.
- `SimuladorRedes(nivel_geo)`: classe principal — gera DataFrames com geo-localização.
  - `gerar_comentarios()`: redes sociais com Bairro/Lat/Lon.
  - `gerar_transcricoes_radio_tv()`: simulação Rádio/TV.
  - `gerar_mensagens_whatsapp()`: Dark Social com detecção de viralidade.
- `buscar_noticias_google(termo)`: notícias reais via GoogleNews.
- `_limpar_link_google(url)`: remove `&ved=`, `&usg=`, `#google_vignette` dos links.
- `_normalizar_data_google(data_str)`: converte datas relativas ("há 2 dias") para `datetime`.
- `transcrever_audio(arquivo)`: transcrição via Whisper.
- `extrair_texto_imagem(caminho)`: OCR via EasyOCR.

### `src/ai_advisor.py`
- `TONS_RESPOSTA`: 3 tons (Institucional, Militância, Empático).
- `gerar_nota_estrategica(texto, tom)`: gera nota via Groq com fallback local.
- `classificar_criticidade(texto)`: classifica criticidade (Alta/Média/Baixa).

### `app/dashboard.py`
- Dashboard "War Room" com 3 abas:
  - **📡 Radar Tradicional**: KPIs, gráficos (Donut + Timeline + Barras), Notícias, Rádio/TV, WhatsApp, Voz das Ruas.
  - **🗺️ Mapa de Crise**: density_mapbox com segmentação geográfica + tabela de dados.
  - **🏛️ Sala de Comando**: Spin Doctor — geração de notas estratégicas por IA em 3 tons.
- Sidebar: idioma, tema, escala geográfica, cenário, volume, filtros.
- Onboarding: expander "Como usar esta aplicação" com guia detalhado (bilíngue).
- CSS dinâmico: `_gerar_css_tema()` aplica tema a todos os componentes.

### `keep_alive.py`
- Script Selenium headless que visita `https://civitas-radar.streamlit.app/` periodicamente.
- Mantém o app ativo no Streamlit Cloud para evitar hibernação.

---

## Regras para Agentes de IA

1. **Respeite o sistema de temas** — use `TEMAS[tema]` para cores, nunca hardcode.
2. **Gere textos e labels em pt-BR e ES** — adicione traduções ao dict `I18N`.
3. **Prefira Plotly** para novas visualizações.
4. **Dados sensíveis de políticos são fictícios** — mantenha simulações genéricas.
5. **Nunca exponha credenciais** ou chaves de API no código.
6. **Teste alterações** com `streamlit run app/dashboard.py` antes de confirmar.
7. **Mantenha a modularidade**: lógica de dados em `src/`, visual em `app/`.
8. **Use session_state** para dados que precisam persistir entre reruns do Streamlit.
9. **Links do Google News** passam por `_limpar_link_google()` — mantenha esse tratamento.
10. **Onboarding** deve ser atualizado em ambas as línguas ao adicionar features.

---

## Como Executar

```bash
pip install -r requirements.txt
python -m textblob.download_corpora
streamlit run app/dashboard.py
```

---

*"A tecnologia e o dado só fazem sentido quando servem para contar uma verdade ou resolver um problema humano."*
