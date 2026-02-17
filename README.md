# 🎯 Civitas-Radar

**Inteligência Política e Monitoramento de Reputação Digital em Tempo Real**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://civitas-radar.streamlit.app)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🎯 Sobre o Projeto

O **Civitas-Radar** é uma plataforma de gestão de reputação e inteligência de marca para o cenário político. Funciona como uma **"War Room"** (Sala de Situação) digital, combinando simulação de redes sociais com coleta de notícias reais para monitoramento de narrativas em tempo real.

A ferramenta permite que assessores, gestores públicos e analistas políticos acompanhem o pulso digital de figuras públicas, identifiquem crises emergentes e avaliem o impacto de ações governamentais na opinião pública.

---

## ✨ Features

| Feature | Descrição |
|---------|-----------|
| 🧠 **Simulação Inteligente** | 4 cenários pré-configurados com keywords realistas em pt-BR |
| 📰 **Notícias Reais** | Integração com Google News para coleta de manchetes em tempo real |
| 📊 **Gráficos Interativos** | Donut Chart de sentimentos + Timeline de evolução |
| 🟢🔴 **Análise de Sentimento** | Classificação automática: Positivo, Negativo, Neutro |
| 🎭 **War Room UI** | Interface dark mode com alto contraste e visual de sala de situação |
| 💬 **Voz das Ruas** | Feed simulado de comentários de redes sociais (X, Instagram, Facebook, TikTok) |
| 📈 **KPIs em Tempo Real** | Índice de Aprovação Digital, Volume de Menções, Sentimento Predominante |

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

### Usando GitHub Codespaces

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/lenondpaula/civitas-radar)

O projeto está otimizado para uso em GitHub Codespaces. Para começar:

1. Clique no badge acima ou acesse [github.com/codespaces](https://github.com/codespaces)
2. O ambiente será configurado automaticamente
3. Execute: `streamlit run app/dashboard.py`

> ⚠️ **Importante**: Sempre faça commit de suas mudanças antes de fechar o Codespace. [Veja o guia de recuperação](.github/CODESPACE_RECOVERY.md) caso tenha problemas.

---

## 🛠️ Stack Tecnológica

| Tecnologia | Uso |
|------------|-----|
| **Streamlit** | Framework Web interativo |
| **Pandas** | Manipulação e análise de dados |
| **NumPy** | Operações numéricas |
| **Plotly** | Visualizações interativas |
| **Faker** | Geração de dados sintéticos (pt_BR) |
| **GoogleNews** | Coleta de notícias reais |
| **TextBlob** | Análise de sentimento NLP |
| **Python 3.10+** | Linguagem base |

---

## 📁 Estrutura do Projeto

```
civitas-radar/
├── app/
│   └── dashboard.py              # 🎯 Dashboard Streamlit (War Room)
├── src/
│   ├── __init__.py
│   └── data_engine.py            # 🧠 Motor de simulação e coleta de dados
├── data/                         # 📁 Dados auxiliares e cache
├── .github/
│   ├── copilot-instructions.md   # 🤖 Instruções para agentes de IA
│   └── INSTRUCTIONS.md           # 📋 Guia de contribuição e setup
├── requirements.txt              # 📦 Dependências Python
└── README.md                     # 📖 Este arquivo
```

---

## 📡 Cenários de Simulação

| Cenário | Perfil | Negatividade |
|---------|--------|-------------|
| 🏥 **Crise na Saúde** | Crise institucional | ~80% negativo |
| 💰 **Escândalo de Corrupção** | Crise severa | ~90% negativo |
| 🏗️ **Inauguração de Obra** | Oportunidade positiva | ~70% positivo |
| 🌟 **Viral Positivo** | Narrativa favorável | ~95% positivo |

Cada cenário possui **20-26 keywords realistas** por categoria de sentimento, gerando comentários contextualizados com hashtags, emojis e menções.

---

## 🎨 Tema Visual — War Room

| Elemento | Cor |
|----------|-----|
| 🖤 Background | `#0e1117` |
| 🟥 Accent | `#e94560` |
| 📦 Cards | `#1a1a2e` |
| ✅ Positivo | `#48bb78` |
| ❌ Negativo | `#fc8181` |
| ⚪ Neutro | `#a0aec0` |

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

- 📂 **Repositório**: [github.com/lenondpaula/civitas-radar](https://github.com/lenondpaula/civitas-radar)
- 🧪 **Portfolio**: [goodluke.streamlit.app](https://goodluke.streamlit.app)

---

## 🆘 Troubleshooting

### Problemas com Codespaces

Se seu Codespace não abrir ou você tiver mudanças não commitadas:

1. **Verificar status**: Acesse [github.com/codespaces](https://github.com/codespaces) e veja o status
2. **Tentar reiniciar**: Clique em "Start" e aguarde alguns minutos
3. **Exportar mudanças**: Use "Export changes" no menu do Codespace
4. **Usar script de verificação**: Execute `.github/scripts/check_codespace_recovery.sh`
5. **Consultar guia completo**: [Guia de Recuperação de Codespaces](.github/CODESPACE_RECOVERY.md)

### Outros Problemas Comuns

- **Erro ao instalar dependências**: Certifique-se de usar Python 3.10+
- **TextBlob não funciona**: Execute `python -m textblob.download_corpora`
- **Streamlit não inicia**: Verifique se a porta 8501 está livre

---

## 📄 Licença

Este projeto faz parte do portfólio de demonstração. © 2026 Lenon de Paula.

---

*Desenvolvido com ❤️ para a Gestão Pública Inteligente*
