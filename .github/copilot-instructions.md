# Copilot Instructions — Civitas-Radar

## Sobre o Projeto

**Civitas-Radar** é uma plataforma de **Inteligência Política e Monitoramento de Reputação Digital** em tempo real.
A aplicação simula cenários de crise e oportunidade na esfera pública, combinando dados simulados de redes sociais com notícias reais via Google News.

O visual segue o conceito **"War Room"** (Sala de Situação), com tema escuro, vermelho accent (#e94560) e alto contraste.

---

## Stack Tecnológica

| Tecnologia | Uso |
|------------|-----|
| **Python 3.10+** | Linguagem base |
| **Streamlit** | Framework Web interativo |
| **Pandas** | Manipulação e análise de dados |
| **NumPy** | Operações numéricas |
| **Plotly** | Visualizações interativas (Donut, Timeline) |
| **Faker** | Geração de dados sintéticos (locale pt_BR) |
| **GoogleNews** | Coleta de notícias reais |
| **TextBlob** | Análise de sentimento |

---

## Arquitetura

```
civitas-radar/
├── app/
│   └── dashboard.py          # 🎯 Dashboard Streamlit (War Room) — 3 abas
├── src/
│   ├── __init__.py
│   ├── data_engine.py         # 🧠 Motor de simulação, geo e coleta de dados
│   └── ai_advisor.py          # 🏛️ Spin Doctor (Gerador de Respostas IA)
├── data/                      # 📁 Dados auxiliares e cache
├── .github/
│   ├── copilot-instructions.md
│   └── INSTRUCTIONS.md
├── requirements.txt           # 📦 Dependências
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
- CSS customizado inline via `<style>` tags.
- Session state para persistência entre execuções.
- Layout `wide` obrigatório.

### Tema Visual (War Room)
- Background principal: `#0e1117`
- Card background: `#1a1a2e`
- Accent color: `#e94560`
- Text primary: `#e2e8f0`
- Text secondary: `#8892b0`
- Text muted: `#718096`
- Positivo: `#48bb78` / Negativo: `#fc8181` / Neutro: `#a0aec0`
- Border: `#2d3748`

---

## Módulos Principais

### `src/data_engine.py`
- `CENARIOS`: dict com 4 cenários pré-definidos (cada um com keywords positivas, negativas e neutras).
- `NIVEIS_GEO`: segmentação territorial hierárquica (Capital, Metropolitana, Estadual) com coordenadas reais.
- `SimuladorRedes(nivel_geo)`: classe principal — gera DataFrames com geo-localização.
  - `gerar_comentarios()`: redes sociais com Bairro/Lat/Lon.
  - `gerar_transcricoes_radio_tv()`: simulação Rádio/TV.
  - `gerar_mensagens_whatsapp()`: Dark Social com detecção de viralidade.
- `buscar_noticias_google(termo)`: notícias reais via GoogleNews.
- `transcrever_audio(arquivo)`: transcrição via Whisper.
- `extrair_texto_imagem(caminho)`: OCR via EasyOCR.

### `src/ai_advisor.py`
- `TONS_RESPOSTA`: 3 tons (Institucional, Militância, Empático).
- `gerar_nota_estrategica(texto, tom)`: gera nota via Gemini com fallback local.
- `classificar_criticidade(texto)`: classifica criticidade (Alta/Média/Baixa).

### `app/dashboard.py`
- Dashboard "War Room" com 3 abas:
  - **Radar Tradicional**: KPIs, gráficos, feeds, Rádio/TV, WhatsApp.
  - **Mapa de Crise**: densidade geográfica de sentimentos (density_mapbox).
  - **Sala de Comando**: Spin Doctor — geração de notas estratégicas por IA.
- Sidebar com controle de escala geográfica e parâmetros.

---

## Regras para Agentes de IA

1. **Sempre mantenha o tema War Room** — não altere as cores accent sem instrução explícita.
2. **Gere textos e labels em pt-BR** salvo indicação contrária.
3. **Prefira Plotly** para novas visualizações.
4. **Dados sensíveis de políticos são fictícios** — mantenha simulações genéricas.
5. **Nunca exponha credenciais** ou chaves de API no código.
6. **Teste alterações** com `streamlit run app/dashboard.py` antes de confirmar.
7. **Mantenha a modularidade**: lógica de dados em `src/`, visual em `app/`.
8. **Use session_state** para dados que precisam persistir entre reruns do Streamlit.

---

## Como Executar

```bash
pip install -r requirements.txt
python -m textblob.download_corpora
streamlit run app/dashboard.py
```

---

*"A tecnologia e o dado só fazem sentido quando servem para contar uma verdade ou resolver um problema humano."*
