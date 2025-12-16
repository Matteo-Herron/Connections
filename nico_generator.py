import spacy
import numpy as np
import nltk
from nltk.corpus import words, wordnet as wn
from itertools import islice, combinations
from collections import defaultdict
from pathlib import Path
from tqdm import tqdm

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------

RAW_TEXT_PATH = Path("/Users/nicostuart/Desktop/en.txt")
VERB_OBJECTS_PATH = Path("/Users/nicostuart/Desktop/verb_objects.txt")
REPORT_PATH = Path("/Users/nicostuart/Desktop/verb_sense_report2.md")

TOTAL_LINES = 61000000
SAMPLE_SIZE = 10_000_000

MIN_OBJECTS_FOR_VERB = 4
ASSIGN_THRESHOLD = 0.40

WEIGHTS = {
    "coverage": 0.50,
    "inter_sense": 0.35,
    "assign_rate": 0.15
}

# ---------------------------------------------------------------------
# SETUP
# ---------------------------------------------------------------------

nltk.download("words", quiet=True)
nltk.download("wordnet", quiet=True)
english_vocab = set(w.lower() for w in words.words())

nlp = spacy.load("en_core_web_md")

abstract_words = {
    "thing", "something", "anything", "nothing", "it", "this", "that",
    "stuff", "object", "someone", "somebody", "anyone", "anybody",
    "everything", "more", "less", "many", "few", "several", "desire",
    "type", "kind", "form", "matter", "man", "woman"
}

# ---------------------------------------------------------------------
# STAGE 1 — VERB → OBJECT EXTRACTION
# ---------------------------------------------------------------------

def extract_verb_to_objects(docs):
    verb_objects = defaultdict(set)

    for doc in docs:
        for tok in doc:
            if tok.pos_ == "VERB":
                for child in tok.children:
                    if child.dep_ == "dobj":
                        obj = child.lemma_.lower()

                        if (
                            child.pos_ != "PRON" and
                            obj.isalpha() and
                            obj not in abstract_words and
                            obj in english_vocab
                        ):
                            verb_objects[tok.lemma_].add(obj)

    return verb_objects


def sample_lines(path, total_lines, sample_size):
    """Reservoir-like fixed-step sampling"""
    step = max(1, total_lines // sample_size)
    lines = []

    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i % step == 0:
                lines.append(line.strip())
            if len(lines) >= sample_size:
                break

    return lines


def run_stage1_extract_verb_objects():
    print("=== STAGE 1 — Extracting verb→object lists ===")

    lines = sample_lines(RAW_TEXT_PATH, TOTAL_LINES, SAMPLE_SIZE)

    docs = nlp.pipe(lines, batch_size=10_000)
    docs = tqdm(docs, total=len(lines), desc="spaCy parsing")

    verb_objects = extract_verb_to_objects(docs)

    # Save results
    with open(VERB_OBJECTS_PATH, "w", encoding="utf-8") as f:
        for verb, objs in sorted(verb_objects.items()):
            if len(objs) > 3:
                f.write(f"{verb}: {', '.join(sorted(objs))}\n")

    print(f"Saved verb-object list → {VERB_OBJECTS_PATH}\n")


# ---------------------------------------------------------------------
# STAGE 2 — SENSE CLUSTERING + SCORING
# ---------------------------------------------------------------------

def embed_text(text):
    doc = nlp(str(text))
    v = doc.vector
    return None if np.linalg.norm(v) < 1e-8 else v

def cosine_sim(a, b):
    if a is None or b is None:
        return -1.0
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom < 1e-8:
        return -1.0
    return float(np.dot(a, b) / denom)

def cosine_dist(a, b):
    s = cosine_sim(a, b)
    return 1.0 - s if s >= -0.5 else 1.0

def build_sense_vectors(verb):
    out = []
    for syn in wn.synsets(verb, pos=wn.VERB):
        parts = syn.lemma_names() + [syn.definition()] + syn.examples()
        vecs = []

        for p in parts:
            v = embed_text(p)
            if v is not None:
                vecs.append(v)

        if vecs:
            out.append((syn, np.mean(vecs, axis=0), parts))

    return out

def assign_objects(objects, sense_vectors):
    assignments = defaultdict(list)
    unassigned = []
    per_obj = {}

    for obj in objects:
        v = embed_text(obj)
        if v is None:
            unassigned.append(obj)
            per_obj[obj] = (None, -1)
            continue

        best_sim = -2
        best_syn = None

        for syn, svec, _ in sense_vectors:
            sim = cosine_sim(v, svec)
            if sim > best_sim:
                best_sim = sim
                best_syn = syn

        if best_sim >= ASSIGN_THRESHOLD:
            assignments[best_syn].append((obj, best_sim))
            per_obj[obj] = (best_syn, best_sim)
        else:
            unassigned.append(obj)
            per_obj[obj] = (None, best_sim)

    return assignments, unassigned, per_obj

def compute_score(assignments, sense_vectors, objects, per_obj_best):
    total = len(objects)
    if total == 0:
        return 0.0, {}

    assigned_counts = {s: len(lst) for s, lst in assignments.items()}
    coverage_norm = len([1 for c in assigned_counts.values() if c > 0]) / max(1, len(sense_vectors))

    used_vecs = [vec for syn, vec, _ in sense_vectors if syn in assignments]
    inter_dist = (
        float(np.mean([cosine_dist(a, b) for a, b in combinations(used_vecs, 2)]))
        if len(used_vecs) >= 2
        else 0.0
    )

    assign_rate = sum(assigned_counts.values()) / total

    score = (
        WEIGHTS["coverage"] * coverage_norm +
        WEIGHTS["inter_sense"] * inter_dist +
        WEIGHTS["assign_rate"] * assign_rate
    )

    return max(0.0, min(1.0, score)), {
        "coverage_norm": coverage_norm,
        "inter_dist": inter_dist,
        "assign_rate": assign_rate
    }

def load_verb_objects(path):
    out = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if ":" not in line:
                continue
            verb, objs = line.split(":", 1)
            objs = [o.strip() for o in objs.split(",") if o.strip()]
            out[verb.strip()] = objs
    return out

def run_stage2_sense_analysis():
    print("=== STAGE 2 — Sense clustering + scoring ===")
    data = load_verb_objects(VERB_OBJECTS_PATH)

    results = []
    for verb, objects in tqdm(data.items(), desc="Analyzing verbs"):
        if len(objects) < MIN_OBJECTS_FOR_VERB:
            continue

        sense_vectors = build_sense_vectors(verb)
        if not sense_vectors:
            continue

        assignments, unassigned, per_obj = assign_objects(objects, sense_vectors)
        score, components = compute_score(assignments, sense_vectors, objects, per_obj)

        sense_info = []
        for syn, vec, parts in sense_vectors:
            assigned_objs = [obj for obj, sim in assignments.get(syn, [])]
            sense_info.append({
                "synset": syn.name(),
                "gloss": syn.definition(),
                "assigned": assigned_objs
            })

        sense_info.append({
            "synset": "unassigned",
            "gloss": "Objects not confidently linked to any sense",
            "assigned": unassigned
        })

        results.append({
            "verb": verb,
            "score": score,
            "components": components,
            "senses": sense_info
        })

    results.sort(key=lambda r: -r["score"])

    # Write markdown
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("# Verb Sense Report\n\n")
        for r in results:
            f.write(f"## {r['verb']}\n")
            f.write(f"**Score:** {r['score']:.4f}\n\n")
            f.write("**Components:**\n")
            for k, v in r["components"].items():
                f.write(f"- {k}: {v:.4f}\n")
            f.write("\n### Senses\n")
            for s in r["senses"]:
                f.write(f"#### {s['synset']}\n")
                f.write(f"*{s['gloss']}*\n")
                if s["assigned"]:
                    for obj in s["assigned"]:
                        f.write(f"- {obj}\n")
                else:
                    f.write("- *(none)*\n")
                f.write("\n")
            f.write("\n---\n")

    print(f"Saved full report → {REPORT_PATH}\n")


# ---------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------

def main():
    run_stage1_extract_verb_objects()
    run_stage2_sense_analysis()

if __name__ == "__main__":
    main()
