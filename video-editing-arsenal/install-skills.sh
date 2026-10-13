#!/usr/bin/env bash
# Symlinks the standalone vendored skills into ~/.claude/skills.
# Nate's kit and claude-youtube-editor are workspaces: open Claude Code inside those folders instead.
set -eu
here="$(cd "$(dirname "$0")" && pwd)/skills"
dest="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$dest"
link() { ln -sfn "$1" "$dest/$2" && echo "linked $2"; }
link "$here/01-watch-and-understand/video-use" video-use
link "$here/03-rough-cut-local/claude-code-video-editing-skill" video-editing-rough-cut
link "$here/04-face-safe-reels/ghost-editor" ghost-editor
link "$here/08-render-any-html/open-edit" open-edit
for s in "$here"/05-hyperframes-official/skills/*/; do link "${s%/}" "$(basename "$s")"; done
for s in "$here"/07-capture-and-utilities/digitalsamba-skills/*/; do link "${s%/}" "$(basename "$s")"; done
