# 🎯 Civitas-Radar

**Inteligência Política e Monitoramento de Reputação Digital em Tempo Real**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://civitas-radar.streamlit.app)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🎯 Sobre o Projeto

O **Civitas-Radar** é uma plataforma de gestão de reputação e inteligência de marca para o cenário político, figuras públicas e grandes empresas. Funciona como uma **"War Room"** (Sala de Situação) digital, combinando simulação de redes sociais com coleta de notícias reais para monitoramento de narrativas em tempo real.

A ferramenta permite que assessores, gestores públicos e analistas políticos acompanhem o pulso digital de figuras públicas, identifiquem crises emergentes e avaliem o impacto de ações governamentais na opinião pública.

---

## ✨ Features

| Feature | Descrição |
|---------|-----------|
| 🧠 **15 Cenários de Simulação** | Crise na Saúde, Escândalo de Corrupção, Inauguração de Obra, Viral Positivo, Avanço na Segurança Pública, Revolução na Educação, Crise Habitacional, Crise de Produto / Serviço, Escândalo de Marca, Campanha de Alto Impacto, Ciberataque e Vazamento de Dados, Crise Trabalhista, Cancelamento Digital, Prêmio / Reconhecimento, Vida Pessoal em Pauta |
| 📰 **Notícias Reais** | Integração com Google News — links limpos (sem `&ved`, `&usg`, `#google_vignette`) e datas normalizadas |
| 📊 **Gráficos Interativos** | Donut Chart de sentimentos + Timeline de evolução + Barras por região |
| 🗺️ **Geo-Inteligência** | Mapa de calor (density_mapbox) com segmentação territorial: Capital, Metropolitana, Estadual |
| 🟢🔴 **Análise de Sentimento** | Classificação automática: Positivo, Negativo, Neutro |
| 📻 **Omni-Channel** | Redes Sociais + Rádio/TV Clipping + WhatsApp Sentinela (Dark Social) |
| 🏛️ **Spin Doctor (IA)** | Geração de notas estratégicas via Groq (com fallback local) em 3 tons: Institucional, Militância, Empático |
| 🌐 **Bilíngue (i18n)** | Interface completa em Português (BR) e Espanhol (América Latina) |
| 🎨 **3 Temas Visuais** | Dark (azul marinho/grafite), Grey (purple-grey), Light (branco/azul) — CSS dinâmico |
| 📈 **KPIs em Tempo Real** | Índice de Aprovação Digital, Volume de Menções, Sentimento Predominante |
| 💬 **Voz das Ruas** | Feed simulado com scroll sincronizado e sentimento visual |
| 📖 **Onboarding integrado** | Menu "Como usar esta aplicação" expansível logo abaixo do header |

---

## 🚀 Quick Start

### Instalação Local

```bash
# Clone o repositório
git clone https://github.com/lenondpaula/civitas-radar.git
cd civitas-radar

# Instale as dependências
pip install -r requirements.txt

# Baixe os corpora do TextBlob
python -m textblob.download_corpora

# Execute a aplicação
streamlit run app/dashboard.py
```

Acesse: **http://localhost:8501**

### Deploy (Streamlit Cloud)

A aplicação está disponível em: **[civitas-radar.streamlit.app](https://civitas-radar.streamlit.app)**

O arquivo `keep_alive.py` mantém a aplicação ativa no Streamlit Cloud via Selenium headless.

---

## 🛠️ Stack Tecnológica

| Tecnologia | Uso |
|------------|-----|
| **Streamlit** | Framework Web interativo |
| **Pandas** | Manipulação e análise de dados |
| **NumPy** | Operações numéricas |
| **Plotly** | Visualizações interativas (Donut, Timeline, Barras, Mapbox) |
| **Faker** | Geração de dados sintéticos (pt_BR) |
| **GoogleNews** | Coleta de notícias reais |
| **TextBlob** | Análise de sentimento NLP |
| **Groq LLM API** | Spin Doctor via Groq (com fallback local) |
| **Selenium** | Keep-alive do app no Streamlit Cloud |
| **Python 3.10+** | Linguagem base |

---

## 📁 Estrutura do Projeto

```
civitas-radar/
├── app/
│   └── dashboard.py              # 🎯 Dashboard Streamlit (War Room) — 3 abas + i18n + temas
├── src/
│   ├── __init__.py
│   ├── data_engine.py            # 🧠 Motor de simulação, geo e coleta de dados (15 cenários)
│   └── ai_advisor.py             # 🏛️ Spin Doctor (Gerador de Respostas IA via Groq)
├── data/                         # 📁 Dados auxiliares e cache
├── .github/
│   ├── copilot-instructions.md   # 🤖 Instruções para agentes de IA
│   └── INSTRUCTIONS.md           # 📋 Guia de contribuição e setup
├── keep_alive.py                 # ♻️ Script Selenium para manter app ativo
├── requirements.txt              # 📦 Dependências Python
├── .gitignore
└── README.md                     # 📖 Este arquivo
```

---

## 📡 Cenários de Simulação

### Lista atualizada (15 cenários)

| Cenário | Perfil | Sentimento Dominante |
|---------|--------|---------------------|
| 🏥 **Crise na Saúde** | Crise institucional | ~80% negativo |
| 💰 **Escândalo de Corrupção** | Crise severa | ~90% negativo |
| 🏗️ **Inauguração de Obra** | Oportunidade positiva | ~70% positivo |
| 🌟 **Viral Positivo** | Narrativa favorável | ~95% positivo |
| 🛡️ **Avanço na Segurança Pública** | Positivo | ~75% positivo |
| 📚 **Revolução na Educação** | Positivo | ~75% positivo |
| 🏠 **Crise Habitacional** | Negativo | ~82% negativo |
| 🧪 **Crise de Produto / Serviço** | Crise operacional | ~70% negativo |
| 🧯 **Escândalo de Marca** | Reputação em risco | ~75% negativo |
| 🚀 **Campanha de Alto Impacto** | Oportunidade | ~60% positivo |
| 🧠 **Ciberataque e Vazamento de Dados** | Crise crítica | ~80% negativo |
| 🧰 **Crise Trabalhista** | Crise interna | ~70% negativo |
| 📵 **Cancelamento Digital** | Crise reputacional | ~75% negativo |
| 🏆 **Prêmio / Reconhecimento** | Narrativa favorável | ~70% positivo |
| 👥 **Vida Pessoal em Pauta** | Exposição pública | ~55% negativo |

Cada cenário possui **20-26 keywords realistas** por categoria de sentimento, gerando comentários contextualizados com hashtags, emojis e menções.

---

## 🎨 Temas Visuais

A aplicação oferece **3 temas** com CSS dinâmico que se aplica a todos os componentes:

| Tema | Background | Accent | Ideal para |
|------|-----------|--------|-----------|
| 🌑 **Dark** | Azul marinho / grafite (`#0a0e14`) | `#e94560` | War Room clássica |
| 🌫️ **Grey** | Purple-grey (`#1e1e2e`) | `#e94560` | Ambientes com luz moderada |
| ☀️ **Light** | Branco / azul (`#f0f2f6`) | `#cf222e` | Apresentações e projeções |

---

## 🌐 Internacionalização

| Idioma | Cobertura |
|--------|-----------|
| 🇧🇷 **Português (BR)** | Interface completa + onboarding |
| 🇪🇸 **Español (LatAm)** | Interface completa + onboarding |

Todos os rótulos, KPIs, abas, botões, mensagens e o menu "Como usar" são traduzidos.

---

## 🏛️ Spin Doctor (IA)

O módulo de geração de respostas estratégicas permite:

1. Selecionar menções negativas de qualquer canal (Redes Sociais, Rádio/TV, WhatsApp) **ou** inserir um texto manual
2. Classificar a criticidade automaticamente (🔴 Alta / 🟡 Média / 🟢 Baixa)
3. Gerar nota oficial em 3 tons:
   - **Institucional** — formal, técnico, governamental
   - **Militância** — mobilizador, assertivo, contra-ataque
   - **Empático** — acolhedor, humano, próximo do cidadão
4. Fonte: Groq (quando API configurada) ou template local

### Configuração da API (Groq)

No Streamlit Cloud, adicione a chave em **Secrets**:

```toml
GROQ_API_KEY = "sua-chave-aqui"
```

Localmente, também é possível definir a variável de ambiente `GROQ_API_KEY`.

---

## 👨‍💻 Autor

**Lenon de Paula**
Especialista em Ciência de Dados e IA | Jornalista | Desenvolvedor de Soluções Avançadas

Profissional com formação em Jornalismo (UFSM) e pós-graduação em Ciência de Dados e Inteligência Artificial (Uninter), além de Políticas Públicas e Gestão Governamental. Atua na Secretaria de Comunicação da Prefeitura de Santa Maria (RS), desenvolvendo soluções baseadas em dados para a gestão pública.

> *"A tecnologia e o dado só fazem sentido quando servem para contar uma verdade ou resolver um problema humano."*

- 📧 [lenondpaula@gmail.com](mailto:lenondpaula@gmail.com)
- 💼 [LinkedIn](https://www.linkedin.com/in/lenonmpaula/)
- 🐙 [GitHub](https://github.com/lenondpaula)
- 💬 [WhatsApp](https://wa.me/5555981359099)
- 📲 [Telegram](https://t.me/+5555981359099)
- 🧪 [GoodLuke AI Hub](https://goodluke.streamlit.app/)

---

## 🔗 Links Úteis

- 🌐 **App Live**: [civitas-radar.streamlit.app](https://civitas-radar.streamlit.app)
- 📂 **Repositório**: [github.com/lenondpaula/civitas-radar](https://github.com/lenondpaula/civitas-radar)
- 🧪 **Portfolio**: [goodluke.streamlit.app](https://goodluke.streamlit.app)

---

## 📄 Licença

Este projeto faz parte do portfólio de demonstração. © 2026 Lenon de Paula.

---

*Desenvolvido com ❤️ para a Gestão Pública Inteligente*
