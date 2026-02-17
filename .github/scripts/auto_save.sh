#!/bin/bash

# Auto-save Script para Codespaces
# Faz commits automáticos periodicamente para prevenir perda de dados

# Configurações
INTERVAL_MINUTES=${1:-30}  # Padrão: 30 minutos
BRANCH=$(git branch --show-current)
REPO_ROOT=$(git rev-parse --show-toplevel)

echo "🔄 Auto-save ativado para branch: $BRANCH"
echo "⏱️  Intervalo: $INTERVAL_MINUTES minutos"
echo "📁 Repositório: $REPO_ROOT"
echo ""
echo "Pressione Ctrl+C para parar"
echo "================================================"
echo ""

# Função para fazer commit
auto_commit() {
    cd "$REPO_ROOT" || exit 1
    
    # Verifica se há mudanças
    if ! git diff-index --quiet HEAD --; then
        TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
        
        echo "📝 Mudanças detectadas às $TIMESTAMP"
        
        # Adiciona todos os arquivos
        git add .
        
        # Faz commit com timestamp
        git commit -m "auto-save: $TIMESTAMP" --quiet
        
        echo "✅ Commit criado: auto-save: $TIMESTAMP"
        
        # Tenta fazer push (pode falhar se houver conflitos)
        if git push origin "$BRANCH" --quiet 2>/dev/null; then
            echo "☁️  Push realizado com sucesso"
        else
            echo "⚠️  Push falhou (pode haver conflitos). Commit salvo localmente."
        fi
        
        echo ""
    else
        echo "✓ Sem mudanças às $(date '+%H:%M:%S')"
    fi
}

# Loop principal
INTERVAL_SECONDS=$((INTERVAL_MINUTES * 60))

while true; do
    auto_commit
    sleep "$INTERVAL_SECONDS"
done
