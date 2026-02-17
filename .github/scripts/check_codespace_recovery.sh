#!/bin/bash

# Script de Verificação e Recuperação de Codespace
# Para o Codespace: orange space train
# Repositório: lenondpaula/civitas-radar

set -e

CODESPACE_NAME="orange-space-train"
REPO="lenondpaula/civitas-radar"

echo "🔍 Verificando opções de recuperação para Codespace: $CODESPACE_NAME"
echo "================================================"
echo ""

# Verifica se gh CLI está instalado
if ! command -v gh &> /dev/null; then
    echo "⚠️  GitHub CLI (gh) não está instalado."
    echo "   Instale com: https://cli.github.com/"
    echo ""
else
    echo "✅ GitHub CLI encontrado"
    
    # Lista Codespaces disponíveis
    echo ""
    echo "📋 Listando todos os Codespaces..."
    gh codespace list || echo "❌ Erro ao listar Codespaces. Verifique suas credenciais."
    echo ""
    
    # Tenta verificar o status do Codespace específico
    echo "🔎 Procurando Codespace 'orange space train'..."
    CODESPACE_EXISTS=$(gh codespace list | grep -i "orange" || echo "")
    
    if [ -z "$CODESPACE_EXISTS" ]; then
        echo "❌ Codespace 'orange space train' não encontrado na lista."
        echo "   Ele pode ter sido deletado ou renomeado."
    else
        echo "✅ Codespace encontrado!"
        echo "$CODESPACE_EXISTS"
        echo ""
        echo "💡 Você pode tentar conectar com:"
        echo "   gh codespace ssh -c $CODESPACE_NAME"
    fi
fi

echo ""
echo "================================================"
echo "🌿 Verificando branches remotas..."
echo "================================================"

# Busca branches que podem conter mudanças do Codespace
git fetch --all --prune

echo ""
echo "Branches que podem conter mudanças do Codespace:"
git branch -r | grep -E "(codespace|orange|copilot)" || echo "❌ Nenhuma branch suspeita encontrada"

echo ""
echo "================================================"
echo "📊 Análise de branches específicas"
echo "================================================"

# Verifica a branch copilot/force-commit-in-orange-space-train
BRANCH="copilot/force-commit-in-orange-space-train"
if git show-ref --verify --quiet "refs/remotes/origin/$BRANCH"; then
    echo ""
    echo "✅ Branch encontrada: origin/$BRANCH"
    echo ""
    echo "Últimos commits:"
    git log "origin/$BRANCH" --oneline -5
    echo ""
    echo "Diferenças em relação ao main:"
    git diff origin/main "origin/$BRANCH" --stat || echo "⚠️  Não foi possível comparar (main pode não existir)"
    echo ""
    echo "💡 Para fazer checkout desta branch:"
    echo "   git checkout $BRANCH"
    echo "   git pull origin $BRANCH"
else
    echo "❌ Branch $BRANCH não encontrada"
fi

echo ""
echo "================================================"
echo "🔧 Próximos Passos Recomendados"
echo "================================================"
echo ""
echo "1. Se o Codespace apareceu na lista:"
echo "   → Tente acessá-lo via: gh codespace ssh -c $CODESPACE_NAME"
echo "   → Uma vez dentro, execute: git add . && git commit -m 'recover' && git push"
echo ""
echo "2. Se encontrou branches suspeitas:"
echo "   → Faça checkout e verifique o conteúdo"
echo "   → Compare com sua última versão conhecida"
echo ""
echo "3. Se nada funcionou:"
echo "   → Acesse https://github.com/codespaces"
echo "   → Tente 'Export changes' no Codespace"
echo "   → Entre em contato com suporte GitHub"
echo ""
echo "📖 Para mais detalhes, consulte: .github/CODESPACE_RECOVERY.md"
echo ""
