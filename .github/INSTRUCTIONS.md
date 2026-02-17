# 📋 Instruções do Projeto — Civitas-Radar

## Pré-requisitos

- **Python 3.10+**
- **pip** (gerenciador de pacotes)
- **Git**
- Conexão com a internet (para Google News)

---

## 🚀 Quick Start

### 1. Clone o repositório

```bash
git clone https://github.com/lenondpaula/civitas-radar.git
cd civitas-radar
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Baixe os corpora do TextBlob

```bash
python -m textblob.download_corpora
```

### 4. Execute a aplicação

```bash
streamlit run app/dashboard.py
```

Acesse em: **http://localhost:8501**

---

## 📁 Estrutura do Projeto

```
civitas-radar/
├── app/
│   └── dashboard.py          # Dashboard Streamlit (War Room)
├── src/
│   ├── __init__.py
│   └── data_engine.py         # Motor de simulação e coleta
├── data/                      # Dados auxiliares
├── .github/
│   ├── copilot-instructions.md
│   └── INSTRUCTIONS.md        # Este arquivo
├── requirements.txt
└── README.md
```

---

## 🔧 Configuração para Desenvolvimento

### Ambiente Virtual (recomendado)

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### GitHub Codespaces

O projeto é totalmente compatível com GitHub Codespaces. Basta abrir o repositório no Codespaces e as dependências serão instaladas automaticamente.

---

## 🧪 Testando os Módulos

### Data Engine (backend)

```bash
cd /workspaces/civitas-radar
python -c "
from src.data_engine import SimuladorRedes, buscar_noticias_google, CENARIOS
sim = SimuladorRedes()
df = sim.gerar_comentarios('Crise na Saúde', quantidade=10)
print(df)
print()
noticias = buscar_noticias_google('prefeitura')
print(f'Notícias: {len(noticias)}')
"
```

### Dashboard (frontend)

```bash
streamlit run app/dashboard.py
```

---

## 📡 Cenários Disponíveis

| Cenário | Perfil | Negatividade |
|---------|--------|-------------|
| 🏥 Crise na Saúde | Crise institucional | ~80% |
| 💰 Escândalo de Corrupção | Crise severa | ~90% |
| 🏗️ Inauguração de Obra | Oportunidade positiva | ~70% positivo |
| 🌟 Viral Positivo | Narrativa favorável | ~95% positivo |

---

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Padrão de Commits

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação (sem alteração de lógica)
- `refactor:` Refatoração de código
- `test:` Testes

---

## 📄 Licença

Este projeto faz parte do portfólio de demonstração.  
© 2026 Lenon de Paula — Todos os direitos reservados.
