# Codex usage plugin for Zsh. The command is consumed by Starship below,
# but is also available interactively as `codex-usage --format json`.

0="${(%):-%N}"
typeset -g ZSH_CODEX_USAGE_DIR="${0:A:h}"
typeset -gU path
path=("$ZSH_CODEX_USAGE_DIR/bin" $path)
unset 0
