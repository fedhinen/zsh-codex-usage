# zsh-codex-usage

`zsh-codex-usage` exposes `codex-usage`: a small command for a Zsh prompt that
shows the remaining Codex rate limit and its reset time. It reads the data from
the locally installed Codex CLI and stores a private cache in
`$XDG_CACHE_HOME/codex-usage` (or `~/.cache/codex-usage`).

It is independent of Sheldon, Starship, Quickshell, and ChillPill.

## Requirements

- Zsh 5.0+ to load the plugin.
- Python 3.9+; no Python packages need to be installed.
- A recent `codex` CLI authenticated with `codex login` to refresh data.

Starship is optional and is only needed for the prompt integration below. A
[Nerd Font](https://www.nerdfonts.com/) is optional; without one, replace the
`󰚩` glyph in the script or accept that it may not render.

## Installation

### Sheldon

```zsh
sheldon add codex --github fedhinen/zsh-codex-usage --use '*.plugin.zsh'
```

Ensure your `.zshrc` evaluates Sheldon:

```zsh
eval "$(sheldon source)"
```

### Manual / any plugin manager

Clone the repository anywhere you keep shell plugins, then source its plugin
file in `.zshrc` (before Starship initialization):

```zsh
git clone https://github.com/fedhinen/zsh-codex-usage.git \
  ~/.local/share/zsh/plugins/zsh-codex-usage

source ~/.local/share/zsh/plugins/zsh-codex-usage/zsh-codex-usage.plugin.zsh
```

Any plugin manager can use that same `*.plugin.zsh` file. The only action the
plugin performs is adding its `bin` directory to `PATH`.

## Starship

Add `codex_usage` to the `format` of the prompt line where you want it, then:

```toml
[custom.codex_usage]
command = "codex-usage --format starship"
when = "command -v codex-usage"
format = "[$output]($style) "
style = "bold cyan"
```

The default is the primary (shorter) window. To show both the primary and
secondary windows, use `command = "codex-usage --format starship --window both"`.
Example: `󰚩 P: 62% · S: 89%`. A trailing `~` means the displayed value is an
earlier successful result and a refresh failed.

## Usage and behaviour

```zsh
codex-usage --format starship
codex-usage --format starship --window secondary
codex-usage --format starship --window both
codex-usage --format json
```

Successful values are cached for 30 minutes. A failed refresh keeps the last
successful value, marks it with `~`, and retries after one minute. The command
uses short timeouts (2 seconds for login status and 3 seconds for the app
server), and never waits on another prompt process already refreshing the
cache.

If Codex is unavailable or not logged in, Starship receives no output and
hides the module. Use JSON output to diagnose it; the `error` field explains
the last failure. The Codex app-server protocol is experimental, so a Codex
CLI upgrade can require a plugin update.

## Development

```zsh
python3 -m unittest discover -s tests -v
python3 -m py_compile bin/codex-usage
zsh -n zsh-codex-usage.plugin.zsh
```

No third-party Python dependencies are used.
