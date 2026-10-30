#!/usr/bin/env bash
# Busca no acervo para o agente /advogado.
#
#   buscar.sh ementa  "<regex>" [esfera]   normas cujo tema (ementa) bate com o termo
#   buscar.sh texto   "<regex>" [esfera]   normas cujo corpo cita o termo (mais lento)
#   buscar.sh juris   "<regex>"            súmulas, temas e precedentes
#   buscar.sh uf      <UF> "<regex>"       ementas da legislação de um estado
#   buscar.sh mun     <UF> "<regex>"       ementas da legislação municipal do estado
#
# esfera: federal (padrão), reguladores, tratados, tudo
# Saída: caminho | revogada? | ementa. Ignora pastas internas de auditoria (_*).
set -euo pipefail
cd "$(dirname "$0")/../.."

modo="${1:-}"; shift || true
LIMITE="${LIMITE:-40}"
IGN=(--glob '!**/_*/**' --glob '!**/_*' --glob '*.md')

pastas() {
  case "${1:-federal}" in
    # ordem de prioridade: leis primeiro, MPs e decretos por último
    federal) echo constituicao.md federal/emendas-constitucionais federal/leis-complementares federal/leis-ordinarias \
                  federal/decretos-lei federal/leis-delegadas federal/decretos federal/medidas-provisorias ;;
    reguladores) echo reguladores ;;
    tratados) echo tratados ;;
    tudo) echo constituicao.md federal reguladores tratados jurisprudencia ;;
    *) echo "$1" ;;
  esac
}

# roda o rg pasta a pasta, na ordem dada, com as normas mais recentes primeiro
procurar() {
  local regex="$1"; shift
  for p in "$@"; do
    [ -e "$p" ] || continue
    rg -l -i "${IGN[@]}" "$regex" "$p" 2>/dev/null | sort -t/ -k3,3r -k4r || true
  done
}

resumir() {
  # recebe caminhos no stdin, imprime caminho | status | ementa
  head -n "$LIMITE" | while read -r f; do
    rev=$(grep -m1 '^revogada:' "$f" 2>/dev/null | awk '{print $2}')
    ti=$(grep -m1 '^titulo:' "$f" 2>/dev/null | cut -d: -f2- | tr -d '"')
    em=$(grep -m1 '^ementa:' "$f" 2>/dev/null | cut -d: -f2- | tr -d '"' | cut -c1-220)
    [ "$rev" = "true" ] && st="REVOGADA" || st="vigente?"
    echo "$f | $st |$ti —$em"
  done
}

case "$modo" in
  ementa)
    # shellcheck disable=SC2046
    procurar "^ementa:.*${1}" $(pastas "${2:-federal}") | resumir ;;
  texto)
    # shellcheck disable=SC2046
    procurar "$1" $(pastas "${2:-federal}") | resumir ;;
  juris)
    { rg -i -m2 "${IGN[@]}" "$1" jurisprudencia 2>/dev/null || true; } | cut -c1-400 | head -n "$((LIMITE * 2))" ;;
  uf)
    procurar "^ementa:.*${2}" "estaduais/$1" | resumir ;;
  mun)
    procurar "^ementa:.*${2}" "municipais/$1" | resumir ;;
  *)
    sed -n '2,12p' "$0"; exit 1 ;;
esac
