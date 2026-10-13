#!/usr/bin/env bash
# Clones the picks that can't be vendored (no license, AGPL/GPL, or engines) into ./_external
set -u
cd "$(dirname "$0")"
mkdir -p _external
repos=(
  # review gate, cut audit, capture, sound design (no license)
  krusemediallc/video-editor-agent
  # Google Flow / Veo 3.1 driver (no license)
  GTAI-1/flow-mcp
  # full production system + reviewer/checkpoint protocol (AGPL-3)
  calesthio/OpenMontage
  # deep video analysis skill (GPL-3)
  bsisduck/video-analyzer-skill
  # official Remotion skills
  remotion-dev/skills
  # B-roll indexing/search
  video-db/skills
  6v17/VideoSeek
  # silence cutting with NLE export
  WyattBlue/auto-editor
  # filler-aware transcription
  nyrahealth/CrisperWhisper
  m-bain/whisperX
  # rotoscopy engines
  facebookresearch/sam3
  pq-yang/MatAnyone2
  # capture
  simonw/shot-scraper
  # video-to-audio SFX
  hkchengrex/MMAudio
  # NLE bridge
  samuelgursky/davinci-resolve-mcp
  # more skills
  heygen-com/hyperframes-community-skills
  veedstudio/open-edit
  zhuyansen/awesome-claude-video-skills
)
for r in "${repos[@]}"; do
  d="_external/${r//\//__}"
  if [ -d "$d/.git" ]; then git -C "$d" pull -q --ff-only && echo "updated $r"
  else git clone -q --depth 1 "https://github.com/$r.git" "$d" && echo "cloned  $r" || echo "FAILED  $r"; fi
done
