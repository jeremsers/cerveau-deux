"""
Générateur unique des journaux épisodiques 01_Episodique/AAAA-MM-JJ.md (v0.5.6, A10).

Avant cette version, le cold start Takeout et la consolidation nocturne écrivaient chacun leur
propre journal : un journal cold start bloquait la consolidation de son jour, et le journal
nocturne écrasait les sessions Gemini du jour le plus récent. Désormais un journal est composé de
sections balisées, chacune remplacée séparément par son producteur :
- `telemetrie`  : consolidation nocturne (activité écran, tunnels, synthèse) ;
- `sessions_ia` : ingestion Takeout (sessions de chat de la journée).
Le frontmatter est fusionné clé par clé.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Optional, Tuple

import yaml

from src.config import settings
from src.utils.atomic_io import atomic_write_text

SECTION_TELEMETRY = "telemetrie"
SECTION_AI_SESSIONS = "sessions_ia"
SECTION_ORDER = (SECTION_TELEMETRY, SECTION_AI_SESSIONS)

_FRONTMATTER_RE = re.compile(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n?(.*)$", re.DOTALL)
_SECTION_RE = re.compile(r"<!-- exo:section (\w+) -->\n?(.*?)\n?<!-- /exo:section \1 -->", re.DOTALL)


def journal_path(date_str: str):
    return settings.EPISODIC_DIR / f"{date_str}.md"


def read_journal(date_str: str) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """
    Retourne (frontmatter, sections) d'un journal. Un journal antérieur à v0.5.6 (sans balises)
    est converti : un journal cold start devient la section `sessions_ia`, tout autre journal la
    section `telemetrie`.
    """
    path = journal_path(date_str)
    if not path.exists():
        return {}, {}
    raw = path.read_text(encoding="utf-8", errors="replace")
    match = _FRONTMATTER_RE.match(raw)
    frontmatter: Dict[str, Any] = {}
    body = raw
    if match:
        try:
            loaded = yaml.safe_load(match.group(1))
            frontmatter = loaded if isinstance(loaded, dict) else {}
        except yaml.YAMLError:
            frontmatter = {}
        body = match.group(2)

    sections = {name: content.strip() for name, content in _SECTION_RE.findall(body)}
    if not sections and body.strip():
        legacy_body = re.sub(r"^\s*#\s+[^\n]*\n", "", body.strip(), count=1).strip()
        legacy_key = SECTION_AI_SESSIONS if frontmatter.get("origin") == "takeout_cold_start" else SECTION_TELEMETRY
        sections[legacy_key] = legacy_body
    return frontmatter, sections


def journal_has_section(date_str: str, section: str) -> bool:
    return section in read_journal(date_str)[1]


def write_journal_section(
    date_str: str,
    section: str,
    content: str,
    frontmatter_updates: Optional[Dict[str, Any]] = None,
    source: Optional[str] = None,
) -> Any:
    """Remplace une seule section du journal de la date (les autres sont conservées), écriture atomique."""
    frontmatter, sections = read_journal(date_str)
    frontmatter.pop("origin", None)  # remplacé par la liste `sources`
    frontmatter.update(frontmatter_updates or {})
    frontmatter["date"] = date_str
    frontmatter["type"] = "episodic_journal"
    if source:
        sources = list(frontmatter.get("sources") or [])
        if source not in sources:
            sources.append(source)
        frontmatter["sources"] = sources
    sections[section] = content.strip()

    ordered = [s for s in SECTION_ORDER if s in sections] + sorted(s for s in sections if s not in SECTION_ORDER)
    fm_yaml = yaml.safe_dump(
        {"date": frontmatter.pop("date"), "type": frontmatter.pop("type"), **frontmatter},
        sort_keys=False,
        allow_unicode=True,
    )
    blocks = [f"<!-- exo:section {name} -->\n{sections[name]}\n<!-- /exo:section {name} -->" for name in ordered]
    text = f"---\n{fm_yaml}---\n\n# Journal Épisodique — {date_str}\n\n" + "\n\n".join(blocks) + "\n"
    return atomic_write_text(journal_path(date_str), text)
