"""Mechanical pre-pass over a draft: cheap, regex-based HINTS for the diagnosticians.

Usage:
    python3 textstats.py <file> [--json]

Flags per sentence the surface signals Williams & Bizup teach readers to notice:
  nominalizations (L3), passives (L4), long openings before the subject (L10),
  there-is / it-is-that (L9), negations (L9), hedges/intensifiers/metadiscourse (L9),
  and the sentence openings that form topic strings (L5).
These are candidates, not verdicts: a passive or nominalization is often right.
Stdlib only, so the hook/agent can run it without the uv env.
"""

import json
import re
import sys
from pathlib import Path

NOMINAL = re.compile(r"\b[a-z]{3,}(?:tion|sion|ment|ance|ence|ancy|ency|ity|ness|ysis|ure|ization|isation)s?\b", re.I)
NOMINAL_STOP = {"nation", "station", "mention", "question", "moment", "comment", "element", "government",
                "environment", "experiment", "instrument", "document", "evidence", "science", "audience",
                "city", "community", "university", "quality", "business", "nature", "future", "culture",
                "structure", "figure", "literature", "total", "general", "several", "animal", "individual",
                "natural", "national", "central", "final", "original", "local", "social", "sentence",
                "difference", "reference", "conference", "sequence", "importance", "minute", "capital",
                "material", "potential", "interval", "signal", "journal", "manual", "pressure", "measure",
                "procedure", "temperature", "feature", "picture", "position", "condition", "section", "function"}
BE = r"(?:am|is|are|was|were|be|been|being)"
IRREG = r"(?:done|made|given|taken|seen|known|shown|found|built|written|held|kept|left|lost|paid|put|said|sent|set|told|thought|understood|chosen|driven|drawn|grown|hidden|run|spoken|stolen|thrown|worn|brought|bought|caught|taught|felt|meant|read|begun|broken|forgotten|gotten)"
PASSIVE = re.compile(rf"\b{BE}\s+(?:\w+ly\s+)?(?:\w+ed|{IRREG})\b", re.I)
EXPLETIVE = re.compile(r"\b(?:there\s+(?:is|are|was|were|exists?|seems?)|it\s+(?:is|was|seems)\s+\w+(?:\s+\w+)?\s+(?:that|to))\b", re.I)
DOUBLE_NEG = re.compile(r"\b(?:not|no|never)\s+(?:un|in|im|dis|non)\w+", re.I)
NEGATION = re.compile(r"\b(?:not|no|never|none|neither|nor|nothing|cannot|\w+n't)\b", re.I)
HEDGES = ["perhaps", "possibly", "probably", "may", "might", "could", "seem", "seems", "appear", "appears",
          "suggest", "suggests", "likely", "somewhat", "relatively", "fairly", "rather", "usually", "often",
          "generally", "to some extent", "in some ways", "it is possible that", "tends to", "arguably"]
INTENSIFIERS = ["very", "really", "extremely", "clearly", "obviously", "certainly", "undoubtedly", "definitely",
                "absolutely", "totally", "completely", "highly", "truly", "of course", "indeed", "literally",
                "basically", "actually", "essentially", "particularly", "significantly", "crucially"]
METADISCOURSE = ["in this paper", "in this essay", "in this section", "i will argue", "we will argue",
                 "i will show", "this paper will", "as mentioned", "as noted above", "as discussed",
                 "it is important to note", "it should be noted", "it is worth noting", "note that",
                 "in conclusion", "to summarize", "in summary", "first of all", "the purpose of this",
                 "i would like to", "let me", "needless to say"]
SUBORD_OPENERS = re.compile(r"^(?:although|though|because|since|while|when|whereas|if|unless|after|before|"
                            r"as|despite|in|on|at|for|with|by|through|during|given|considering|according)\b", re.I)


LATEX_SKIP_ENVS = r"(?:table|tabular|tabularx|longtable|figure|equation|align|gather|multline|verbatim|lstlisting|minted|tikzpicture|thebibliography)\*?"


def strip_latex(text: str) -> str:
    if "\\begin{document}" in text:                                   # drop the preamble
        text = text.split("\\begin{document}", 1)[1]
    text = re.sub(r"(?<!\\)%.*", "", text)                             # comments
    text = re.sub(rf"\\begin\{{({LATEX_SKIP_ENVS})\}}.*?\\end\{{\1\}}", "\n\n", text, flags=re.S)
    text = re.sub(r"\\item\b(?:\[[^\]]*\])?", "\n\n", text)            # each item is its own unit
    text = re.sub(r"\\(?:begin|end)\{[^}]*\}(?:\[[^\]]*\])?", "\n\n", text)
    text = re.sub(r"\\(?:sub)*section\*?\{([^}]*)\}", r"\n\n\1.\n\n", text)
    return text


def strip_markup(text: str) -> str:
    if "\\begin{" in text or "\\section" in text:
        text = strip_latex(text)
    text = re.sub(r"```.*?```", " ", text, flags=re.S)            # code fences
    text = re.sub(r"\$\$.*?\$\$|\$[^$]+\$", " MATH ", text, flags=re.S)  # math
    text = re.sub(r"\\(?:cite|ref|eqref|label|autoref)\w*\{[^}]*\}", "", text)
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?\{([^}]*)\}", r"\1", text)  # \emph{x} -> x
    text = re.sub(r"\\[a-zA-Z]+\*?", "", text)
    text = re.sub(r"^\s*(?:#+|[-*+]|\d+\.)\s+", "", text, flags=re.M)  # md headings/bullets
    text = re.sub(r"[*_`]|\[\[|\]\]", "", text)
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)  # frontmatter
    return text


def sentences(par: str) -> list[str]:
    par = re.sub(r"\s+", " ", par).strip()
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"“(])", par)
    return [p for p in parts if len(p.split()) > 2]


def find_terms(s: str, terms: list[str]) -> list[str]:
    low = s.lower()
    return [t for t in terms if re.search(rf"\b{re.escape(t)}\b", low)]


def analyze_sentence(s: str) -> dict:
    words = s.split()
    noms = [m.group(0) for m in NOMINAL.finditer(s) if m.group(0).lower().rstrip("s") not in NOMINAL_STOP
            and m.group(0).lower() not in NOMINAL_STOP]
    intro = 0
    if SUBORD_OPENERS.match(s) and "," in s:
        intro = len(s.split(",", 1)[0].split())
    flags = {
        "words": len(words),
        "opening": " ".join(words[:7]),
        "intro_words": intro,
        "nominalizations": noms,
        "passives": [m.group(0) for m in PASSIVE.finditer(s)],
        "expletives": [m.group(0) for m in EXPLETIVE.finditer(s)],
        "negations": len(NEGATION.findall(s)),
        "double_negatives": [m.group(0) for m in DOUBLE_NEG.finditer(s)],
        "hedges": find_terms(s, HEDGES),
        "intensifiers": find_terms(s, INTENSIFIERS),
        "metadiscourse": find_terms(s, METADISCOURSE),
    }
    return {k: v for k, v in flags.items() if v or k in ("words", "opening")}


def analyze(text: str) -> dict:
    pars = [p for p in re.split(r"\n\s*\n", strip_markup(text)) if len(p.split()) > 5]
    out, all_s = [], []
    for i, p in enumerate(pars, 1):
        ss = [analyze_sentence(s) for s in sentences(p)]
        all_s += ss
        out.append({"paragraph": i, "sentences": ss, "topic_string": [s["opening"] for s in ss]})
    n = max(len(all_s), 1)
    lengths = [s["words"] for s in all_s]
    summary = {
        "paragraphs": len(pars), "sentences": len(all_s),
        "avg_sentence_words": round(sum(lengths) / n, 1), "max_sentence_words": max(lengths, default=0),
        "long_sentences_gt35": sum(l > 35 for l in lengths),
        "long_intros_gt10": sum(s.get("intro_words", 0) > 10 for s in all_s),
        "nominalizations_per_sentence": round(sum(len(s.get("nominalizations", [])) for s in all_s) / n, 2),
        "sentences_with_passive": sum(bool(s.get("passives")) for s in all_s),
        "expletives": sum(len(s.get("expletives", [])) for s in all_s),
        "hedges": sum(len(s.get("hedges", [])) for s in all_s),
        "intensifiers": sum(len(s.get("intensifiers", [])) for s in all_s),
        "metadiscourse": sum(len(s.get("metadiscourse", [])) for s in all_s),
    }
    return {"summary": summary, "paragraphs": out}


def brief(r: dict) -> str:
    lines = ["SUMMARY " + json.dumps(r["summary"])]
    for p in r["paragraphs"]:
        lines.append(f"\n¶{p['paragraph']}")
        for j, s in enumerate(p["sentences"], 1):
            marks = []
            if s["words"] > 35: marks.append(f"LONG({s['words']})")
            if s.get("intro_words", 0) > 10: marks.append(f"INTRO({s['intro_words']})")
            for k, tag in [("nominalizations", "NOM"), ("passives", "PASS"), ("expletives", "EXPL"),
                           ("hedges", "HEDGE"), ("intensifiers", "INT"), ("metadiscourse", "META"), ("double_negatives", "DNEG")]:
                if s.get(k): marks.append(f"{tag}:{','.join(s[k])}")
            if s.get("negations", 0) > 1: marks.append(f"NEG×{s['negations']}")
            lines.append(f"  s{j} [{s['opening']}…] " + " ".join(marks))
    return "\n".join(lines)


if __name__ == "__main__":
    r = analyze(Path(sys.argv[1]).read_text())
    print(json.dumps(r, indent=1) if "--json" in sys.argv else brief(r))
