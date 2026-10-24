"""
Module de gestion unifié et idempotent des Entrées/Sorties Markdown du coffre Obsidian.
Remplace tous les parsings regex manuels par un parsing PyYAML certifié et une séparation
stricte entre :
1. Frontmatter YAML (ConceptFrontmatter)
2. Titre H1 (# {title})
3. Corps analytique structuré (body)
4. Bloc dépliable de Télémétrie & Généalogie (> [!abstract]- ...)
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.config import normalize_to_macro_topic

logger = logging.getLogger("Exocortex.MarkdownIO")


# ==============================================================================
# PYAML DUMPER AVEC GUILLEMETS DOUBLES POUR RÉTROCOMPATIBILITÉ
# ==============================================================================

class QuotedStr(str):
    """Sous-classe de str indiquant à PyYAML de forcer les guillemets doubles."""
    pass


class ExocortexYamlDumper(yaml.SafeDumper):
    """Dumper PyYAML personnalisé garantissant le respect des formats de tests existants."""
    pass


def _represent_quoted_str(dumper: yaml.SafeDumper, data: str) -> yaml.ScalarNode:
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')


ExocortexYamlDumper.add_representer(QuotedStr, _represent_quoted_str)


# ==============================================================================
# MODÈLE DE FRONTMATTER PYDANTIC V2
# ==============================================================================

class ConceptFrontmatter(BaseModel):
    """Métadonnées YAML du frontmatter d'une fiche conceptuelle de l'Exocortex."""
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    id: str
    title: str
    type: str = "concept"
    origin: List[str] = Field(default_factory=lambda: ["gemini_takeout"])
    semantic_topic: str = "A_Trier"
    tags: List[str] = Field(default_factory=list)
    session_id: Optional[str] = None
    distillation_status: str = "success"
    created_at: str
    updated_at: str
    total_time_invested_min: int = 0
    summary_1_line: str = ""

    @field_validator("semantic_topic", mode="before")
    @classmethod
    def _normalize_topic(cls, v: Any) -> str:
        if v:
            return normalize_to_macro_topic(str(v).strip())
        # Topic absent : à classer, et non plus « Dev » d'office (v0.5.5, A9)
        return "A_Trier"

    @field_validator("id", "title", "created_at", "updated_at", "summary_1_line", mode="before")
    @classmethod
    def _stringify_scalar(cls, v: Any) -> str:
        if v is None:
            return ""
        return str(v).strip()

    @field_validator("total_time_invested_min", mode="before")
    @classmethod
    def _coerce_int_time(cls, v: Any) -> int:
        if v is None or v == "":
            return 0
        try:
            return int(v)
        except (ValueError, TypeError):
            return 0

    @field_validator("origin", "tags", mode="before")
    @classmethod
    def _ensure_string_list(cls, v: Any) -> List[str]:
        if v is None:
            return []
        if isinstance(v, list):
            return [str(x).strip() for x in v if str(x).strip()]
        if isinstance(v, str):
            v_strip = v.strip()
            if v_strip.startswith("[") and v_strip.endswith("]"):
                try:
                    parsed = json.loads(v_strip)
                    if isinstance(parsed, list):
                        return [str(x).strip() for x in parsed if str(x).strip()]
                except Exception:
                    pass
            # Si chaîne séparée par des virgules ou mot unique
            parts = [p.strip() for p in v_strip.split(",") if p.strip()]
            return parts if parts else ([v_strip] if v_strip else [])
        return [str(v)]


# ==============================================================================
# MODÈLE DE NOTE CONCEPTUELLE COMPLÈTE
# ==============================================================================

class ParsedConceptNote(BaseModel):
    """
    Représentation modulaire et typée d'une note conceptuelle du coffre.
    Permet la manipulation du frontmatter, du corps et de la télémétrie de manière isolée.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    frontmatter: ConceptFrontmatter
    title_h1: str
    body: str
    telemetry_lines: List[str] = Field(default_factory=list)
    file_path: Optional[Path] = None

    def append_or_replace_daily_session(
        self,
        date_str: str,
        duration_min: int,
        duration_fmt: str,
        enrichment_markdown: str,
        related_links: Optional[List[str]] = None,
    ) -> bool:
        """
        Enrichissement idempotent de la note par une session d'activité (v0.5.5, A13) :
        - les minutes de chaque date sont tenues dans le frontmatter (`screen_time_by_date`) et le
          total est recalculé : relancer une date dont la durée a changé réajuste le total au lieu
          de le figer ;
        - la section de la date est délimitée par des marqueurs HTML invisibles et remplacée en
          bloc : un sous-titre ### produit par le LLM n'est plus dupliqué à chaque relance ;
        - les callouts écrits par le LLM sont retirés de l'enrichissement.
        """
        date_pattern_source = f"Activité écran du `{date_str}`"
        screen_by_date = _screen_time_by_date(self.frontmatter)
        previous_min = screen_by_date.get(date_str)
        if previous_min is None:
            # Note antérieure à v0.5.5 : durée relue dans la ligne de télémétrie de cette date
            previous_min = next(
                (_parse_duration_fmt(line) for line in self.telemetry_lines if date_pattern_source in line),
                None,
            )

        session_block = _build_session_block(date_str, enrichment_markdown)
        self.body = _replace_session_block(self.body, date_str, session_block)

        # Temps : total = temps hors activité écran datée + somme des minutes par date
        base_min = self.frontmatter.total_time_invested_min - sum(screen_by_date.values())
        if previous_min is not None and date_str not in screen_by_date:
            base_min -= previous_min
        screen_by_date[date_str] = max(0, duration_min)
        self.frontmatter.total_time_invested_min = max(0, base_min) + sum(screen_by_date.values())
        setattr(self.frontmatter, "screen_time_by_date", dict(sorted(screen_by_date.items())))
        self.frontmatter.updated_at = max(self.frontmatter.updated_at or date_str, date_str)

        new_source_line = f">   - Activité écran du `{date_str}` ({duration_fmt})"
        for i, line in enumerate(self.telemetry_lines):
            if date_pattern_source in line:
                self.telemetry_lines[i] = new_source_line
                break
        else:
            _insert_source_line(self.telemetry_lines, new_source_line)

        # Mise à jour de la ligne de temps cumulé
        tot_min = self.frontmatter.total_time_invested_min
        tot_fmt = f"{tot_min // 60}h{tot_min % 60:02d}" if tot_min >= 60 else f"{tot_min} min"
        time_updated = False
        time_regex = re.compile(r"^>\s*-\s*\*\*Temps\s+(cumulé|estimé)\s+sur\s+ce\s+sujet\s*:\*\*.*$", re.IGNORECASE)
        for i, line in enumerate(self.telemetry_lines):
            if time_regex.match(line):
                self.telemetry_lines[i] = f"> - **Temps cumulé sur ce sujet :** {tot_fmt}"
                time_updated = True
                break

        if not time_updated:
            if self.telemetry_lines and self.telemetry_lines[0].startswith("> [!abstract]"):
                self.telemetry_lines.insert(1, f"> - **Temps cumulé sur ce sujet :** {tot_fmt}")
            else:
                self.telemetry_lines.insert(0, f"> - **Temps cumulé sur ce sujet :** {tot_fmt}")

        # Mise à jour des connexions sémantiques si fournies
        if related_links:
            links_str = ", ".join(related_links)
            conn_line = f"> - **Connexions sémantiques :** {links_str}"
            conn_updated = False
            for i, line in enumerate(self.telemetry_lines):
                if "**Connexions sémantiques" in line:
                    self.telemetry_lines[i] = conn_line
                    conn_updated = True
                    break
            if not conn_updated:
                self.telemetry_lines.append(conn_line)

        return True


_ABSTRACT_CALLOUT_RE = re.compile(r"(?m)^>\s*\[!abstract\][^\n]*\n?(?:>[^\n]*\n?)*")


def strip_llm_callouts(markdown: str) -> str:
    """Retire les callouts [!abstract] qu'un LLM aurait écrits dans un corps (réservés à la télémétrie)."""
    return _ABSTRACT_CALLOUT_RE.sub("", markdown or "").strip()


def _session_markers(date_str: str) -> tuple:
    return f"<!-- exo:session {date_str} -->", f"<!-- /exo:session {date_str} -->"


def _build_session_block(date_str: str, enrichment_markdown: str) -> str:
    """
    Normalise l'enrichissement LLM d'une date : callouts retirés, titre « Session du » unique,
    sous-titres ### rétrogradés en #### pour rester à l'intérieur de la section, le tout balisé.
    """
    text = strip_llm_callouts(enrichment_markdown)
    text = re.sub(rf"(?m)^#+\s*Session\s+du\s+{re.escape(date_str)}\b[^\n]*\n?", "", text).strip()
    text = re.sub(r"(?m)^###\s+", "#### ", text)
    start, end = _session_markers(date_str)
    return f"{start}\n### Session du {date_str}\n\n{text}\n{end}"


def _replace_session_block(body: str, date_str: str, session_block: str) -> str:
    """Remplace la section balisée de la date, à défaut une section héritée, sinon l'ajoute en fin de corps."""
    start, end = _session_markers(date_str)
    marked = re.compile(rf"{re.escape(start)}.*?{re.escape(end)}", re.DOTALL)
    if marked.search(body):
        return marked.sub(lambda _: session_block, body).strip()
    # Section héritée (sans marqueurs) : jusqu'à la prochaine section « Session du » ou la fin
    legacy = re.compile(
        rf"(?m)^###\s+Session\s+du\s+{re.escape(date_str)}\b.*?(?=^###\s+Session\s+du\s|\Z)",
        re.DOTALL,
    )
    if legacy.search(body):
        return legacy.sub(lambda _: session_block + "\n\n", body).strip()
    return f"{body.rstrip()}\n\n{session_block}".strip()


def _parse_duration_fmt(text: str) -> Optional[int]:
    """Minutes d'une durée affichée « 2h05 », « 45 min » ou « 45m » (dernier motif trouvé)."""
    m = re.search(r"(\d+)h(\d{2})\b", text)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    m = re.search(r"(\d+)\s*m(?:in)?\b", text)
    return int(m.group(1)) if m else None


def _screen_time_by_date(fm: "ConceptFrontmatter") -> Dict[str, int]:
    raw = (fm.model_extra or {}).get("screen_time_by_date") or {}
    out: Dict[str, int] = {}
    if isinstance(raw, dict):
        for k, v in raw.items():
            try:
                out[str(k)] = int(v)
            except (TypeError, ValueError):
                continue
    return out


def _insert_source_line(telemetry_lines: List[str], new_source_line: str) -> None:
    """Insère proprement une ligne de source sous le marqueur Sources épisodiques."""
    sources_idx = -1
    for i, line in enumerate(telemetry_lines):
        if "**Sources épisodiques :**" in line:
            sources_idx = i
            break

    if sources_idx != -1:
        telemetry_lines.insert(sources_idx + 1, new_source_line)
    else:
        if not telemetry_lines:
            telemetry_lines.append("> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)")
        telemetry_lines.append("> - **Sources épisodiques :**")
        telemetry_lines.append(new_source_line)


# ==============================================================================
# FONCTIONS DE PARSING ET DE SÉRIALISATION
# ==============================================================================

def parse_concept_string(raw_text: str, file_path: Optional[Path] = None) -> ParsedConceptNote:
    """
    Parse le contenu brut d'un fichier Markdown de concept :
    - Extrait et valide le frontmatter YAML via PyYAML (avec fallback de réparation).
    - Extrait le titre H1.
    - Isole le corps textuel pur.
    - Extrait le bloc de télémétrie dépliable.
    """
    match = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)$", raw_text, re.DOTALL)
    yaml_data: Dict[str, Any] = {}
    remainder: str = raw_text

    if match:
        yaml_raw = match.group(1)
        remainder = match.group(2)
        try:
            loaded = yaml.safe_load(yaml_raw)
            if isinstance(loaded, dict):
                yaml_data = loaded
            else:
                yaml_data = {}
        except yaml.YAMLError as y_err:
            logger.warning("YAML mal formé détecté (fichier %s). Tentative de récupération : %s", file_path, y_err)
            yaml_data = _fallback_line_yaml_parse(yaml_raw)
    else:
        # Aucun frontmatter détecté
        yaml_data = {}

    # Extraction du titre H1
    h1_match = re.search(r"^(#\s+(.+?))\s*$", remainder, re.MULTILINE)
    if h1_match:
        title_h1 = h1_match.group(2).strip()
        content_after_h1 = remainder[h1_match.end():]
    else:
        title_h1 = str(yaml_data.get("title") or (file_path.stem if file_path else "Sans Titre")).strip()
        content_after_h1 = remainder

    # Extraction du callout de télémétrie de l'Exocortex : repéré par son en-tête « Généalogie »
    # (un callout [!abstract] écrit par un LLM dans le corps ne capture plus la suite, A13),
    # à défaut le DERNIER callout [!abstract] de la note
    callout_match = re.search(r"(?m)^(>\s*\[!abstract\]-?\s*Généalogie[^\n]*)", content_after_h1)
    if not callout_match:
        all_callouts = list(re.finditer(r"(?m)^(>\s*\[!abstract\]-?[^\n]*)", content_after_h1))
        callout_match = all_callouts[-1] if all_callouts else None
    if callout_match:
        body = content_after_h1[:callout_match.start()].strip()
        callout_raw = content_after_h1[callout_match.start():]
        telemetry_lines = [line.rstrip() for line in callout_raw.strip().splitlines() if line.strip()]
    else:
        body = content_after_h1.strip()
        telemetry_lines = []

    # Complétion des champs obligatoires du frontmatter si manquants
    default_id = file_path.stem if file_path else "unknown_id"
    if "id" not in yaml_data:
        yaml_data["id"] = default_id
    if "title" not in yaml_data:
        yaml_data["title"] = title_h1
    if "created_at" not in yaml_data:
        yaml_data["created_at"] = ""
    if "updated_at" not in yaml_data:
        yaml_data["updated_at"] = str(yaml_data.get("created_at") or "")

    frontmatter = ConceptFrontmatter(**yaml_data)
    return ParsedConceptNote(
        frontmatter=frontmatter,
        title_h1=title_h1,
        body=body,
        telemetry_lines=telemetry_lines,
        file_path=file_path,
    )


def _fallback_line_yaml_parse(yaml_raw: str) -> Dict[str, Any]:
    """Parsing ligne par ligne de repli pour réparer un frontmatter YAML corrompu."""
    data: Dict[str, Any] = {}
    current_list_key: Optional[str] = None
    for line in yaml_raw.splitlines():
        line_clean = line.strip()
        if not line_clean or line_clean.startswith("#"):
            continue
        if line_clean.startswith("- "):
            val = line_clean[2:].strip().strip("'\"")
            if current_list_key and isinstance(data.get(current_list_key), list):
                data[current_list_key].append(val)
            continue
        if ":" in line_clean:
            k, v = line_clean.split(":", 1)
            k = k.strip()
            v = v.strip().strip("'\"")
            if v == "":
                data[k] = []
                current_list_key = k
            else:
                current_list_key = None
                data[k] = v
    return data


def parse_concept_file(file_path: Path) -> ParsedConceptNote:
    """Lit et parse une note Markdown de concept depuis le système de fichiers."""
    raw_text = file_path.read_text(encoding="utf-8", errors="replace")
    return parse_concept_string(raw_text, file_path=file_path)


def serialize_concept_note(note: ParsedConceptNote) -> str:
    """
    Sérialise une note conceptuelle au format Markdown standard de l'Exocortex :
    1. Bloc frontmatter délimité par '---' et généré par yaml.safe_dump.
    2. Titre H1 `# {title}`.
    3. Corps analytique structuré.
    4. Callout final de télémétrie et de généalogie.
    """
    fm_dict = note.frontmatter.model_dump(exclude_none=True)
    # Alias du titre (v0.5.5, B18) : les fichiers sont nommés par slug, mais de nombreux liens
    # [[Titre]] (fusions, connexions suggérées) visent le titre ; Obsidian les résout via aliases.
    title_alias = (note.frontmatter.title or "").strip()
    aliases = [str(a) for a in (fm_dict.get("aliases") or []) if str(a).strip()]
    if title_alias and not re.search(r"[\[\]|#^]", title_alias) and title_alias not in aliases:
        aliases.append(title_alias)
    if aliases:
        fm_dict["aliases"] = aliases
    processed_dict: Dict[str, Any] = {}
    for k, v in fm_dict.items():
        if isinstance(v, str):
            processed_dict[k] = QuotedStr(v)
        elif isinstance(v, list):
            processed_dict[k] = [QuotedStr(item) if isinstance(item, str) else item for item in v]
        else:
            processed_dict[k] = v

    yaml_dump = yaml.dump(
        processed_dict,
        Dumper=ExocortexYamlDumper,
        sort_keys=False,
        allow_unicode=True,
    )

    clean_telemetry_lines: List[str] = []
    has_header = False
    for line in note.telemetry_lines:
        s = line.strip()
        if not s:
            continue
        if not s.startswith(">"):
            s = f"> {s}"
        if "[!abstract]" in s:
            has_header = True
        clean_telemetry_lines.append(s)

    if not clean_telemetry_lines:
        tot_min = note.frontmatter.total_time_invested_min
        tot_fmt = f"{tot_min // 60}h{tot_min % 60:02d}" if tot_min >= 60 else f"{tot_min} min"
        clean_telemetry_lines = [
            "> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)",
            f"> - **Temps estimé sur ce sujet :** {tot_fmt}",
            "> - **Sources épisodiques :**",
            "> - **Connexions sémantiques suggérées :** —",
        ]
    elif not has_header:
        clean_telemetry_lines.insert(0, "> [!abstract]- Généalogie & Télémétrie (Généré par l'Exocortex)")

    telemetry_block = "\n".join(clean_telemetry_lines)
    title = note.title_h1 or note.frontmatter.title or "Sans Titre"
    body = note.body.strip()

    parts = [
        f"---\n{yaml_dump}---",
        f"# {title}",
        body,
        telemetry_block,
    ]
    return "\n\n".join(parts) + "\n"


def write_concept_file(note: ParsedConceptNote, target_path: Optional[Path] = None) -> Path:
    """Écrit la note conceptuelle sérialisée sur disque de manière atomique."""
    dest = target_path or note.file_path
    if dest is None:
        raise ValueError("Aucun chemin de fichier spécifié pour l'écriture de la note.")

    dest.parent.mkdir(parents=True, exist_ok=True)
    content = serialize_concept_note(note)
    dest.write_text(content, encoding="utf-8")
    note.file_path = dest
    return dest
