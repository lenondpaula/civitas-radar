# 🆘 Guia de Recuperação de Codespaces

## Problema: Codespace não abre e tem mudanças não commitadas

### Identificação do Codespace
- **Nome**: orange space train
- **Status**: Não abre mais
- **Risco**: Mudanças não commitadas podem ser perdidas

---

## ✅ Soluções Recomendadas (em ordem de prioridade)

### 1️⃣ Tentar Reiniciar o Codespace via GitHub Web

1. Acesse: https://github.com/codespaces
2. Localize o Codespace "orange space train"
3. Verifique o status:
   - 🟢 **Running**: Tente acessar normalmente
   - 🟡 **Stopped**: Clique em "Start" e aguarde (pode levar 2-5 minutos)
   - 🔴 **Error**: Veja opções 2 e 3
4. Se conseguir abrir, **faça commit IMEDIATAMENTE**:
   ```bash
   git add .
   git commit -m "feat: recuperação de mudanças do codespace orange space train"
   git push
   ```

---

### 2️⃣ Exportar Mudanças via Interface do GitHub

1. Acesse: https://github.com/codespaces
2. Encontre o Codespace "orange space train"
3. Clique nos **três pontos** (...) ao lado do nome
4. Selecione uma das opções:
   - **"Export changes"** → Exporta mudanças não commitadas
   - **"Download ZIP"** → Baixa todo o conteúdo do Codespace
5. Aplique as mudanças manualmente no repositório local

---

### 3️⃣ Acessar via GitHub CLI (gh)

Se você tem o GitHub CLI instalado localmente:

```bash
# Listar todos os Codespaces
gh codespace list

# Conectar via SSH ao Codespace específico
gh codespace ssh -c orange-space-train

# Uma vez conectado, commitar as mudanças
cd /workspaces/civitas-radar  # Ou o path do seu projeto
git status
git add .
git commit -m "feat: recuperação de mudanças via CLI"
git push

# Sair do SSH
exit
```

---

### 4️⃣ Verificar Branches Automáticas

O GitHub Codespaces às vezes cria branches automáticas. Verifique:

```bash
# Localmente ou em outro ambiente
git fetch --all
git branch -r | grep -i codespace
git branch -r | grep -i orange

# Se encontrar uma branch, faça checkout:
git checkout <nome-da-branch>
git pull
```

---

### 5️⃣ Recuperar de Backups Automáticos (se disponível)

O GitHub Codespaces faz snapshots periódicos:

1. Acesse: https://github.com/codespaces
2. Clique no Codespace "orange space train"
3. No menu, procure por "Restore from snapshot" ou "Recovery"
4. Selecione o snapshot mais recente

---

## 🚨 Ações Preventivas para o Futuro

### Configurar Auto-commit
Adicione ao seu `.bashrc` ou `.zshrc` dentro do Codespace:

```bash
# Auto-commit a cada hora
while true; do
  git add .
  git commit -m "auto-save: $(date)" || true
  sleep 3600  # 1 hora
done &
```

### Usar Git Hooks
Crie `.git/hooks/pre-push`:

```bash
#!/bin/bash
# Garante que não há mudanças não commitadas antes de push
if ! git diff-index --quiet HEAD --; then
  echo "⚠️  Você tem mudanças não commitadas!"
  exit 1
fi
```

### Configurar Extensão do VS Code
Instale **"Git Auto Commit"** no seu Codespace:
1. Extensions → Buscar "Git Auto Commit"
2. Configurar intervalo (ex: 10 minutos)

---

## 📞 Suporte GitHub

Se nenhuma opção funcionar, abra um ticket de suporte:
- https://support.github.com/contact
- Categoria: **Codespaces**
- Assunto: "Codespace não abre - recuperação de mudanças não commitadas"
- Informações necessárias:
  - Nome do Codespace: **orange space train**
  - Repositório: **lenondpaula/civitas-radar**
  - Última data de acesso conhecida

---

## 🔍 Verificação de Branches Existentes

Branch identificada relacionada:
- `copilot/force-commit-in-orange-space-train`

Para verificar se contém suas mudanças:

```bash
git fetch origin copilot/force-commit-in-orange-space-train
git checkout copilot/force-commit-in-orange-space-train
git log --oneline -10
git diff main  # Compare com a branch principal
```

---

## ⚠️ Limitações Conhecidas

- **Tempo de vida**: Codespaces inativos são deletados após 30 dias (padrão)
- **Armazenamento**: Há limites de armazenamento que podem causar problemas
- **Região**: Problemas de rede/infraestrutura podem afetar acesso

---

**Última atualização**: 2026-02-17

*Criado por Copilot Agent para auxiliar na recuperação de Codespaces com mudanças não commitadas.*
