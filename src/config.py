from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

NCBI_EMAIL = os.getenv("NCBI_EMAIL", "")
NCBI_API_KEY = os.getenv("NCBI_API_KEY", "")
NCBI_TOOL = os.getenv("NCBI_TOOL", "pots-eds-research-landscape")

DEFAULT_START_YEAR = 1990
DEFAULT_END_YEAR = 2026
DEFAULT_MAX_RECORDS = 20000
BATCH_SIZE = 200

CONCEPT_QUERIES = {
    "POTS": '"postural orthostatic tachycardia syndrome"[Title/Abstract]',
    "EDS": '"Ehlers-Danlos syndrome"[Title/Abstract]',
    "hEDS": '"hypermobile Ehlers-Danlos syndrome"[Title/Abstract]',
    "MCAS": '"mast cell activation syndrome"[Title/Abstract]',
}

TOPIC_KEYWORDS = {
    "autonomic_testing": ["tilt table", "head-up tilt", "autonomic", "heart rate variability", "baroreflex", "orthostatic"],
    "genetics": ["gene", "genetic", "variant", "mutation", "genome", "sequencing", "hereditary"],
    "treatment": ["treatment", "therapy", "ivabradine", "midodrine", "fludrocortisone", "beta blocker", "exercise"],
    "pain": ["pain", "headache", "migraine", "fibromyalgia", "nociplastic"],
    "gastrointestinal": ["gastrointestinal", "gastrointestinal", "constipation", "diarrhea", "nausea", "gastroparesis", "motility"],
    "mental_health": ["anxiety", "depression", "mental health", "psychiatric", "psychological", "cognition", "brain fog"],
    "long_covid": ["long covid", "long-covid", "post-acute sequelae", "PASC", "COVID-19"],
    "mast_cell": ["mast cell", "MCAS", "mastocytosis", "histamine"],
    "pregnancy": ["pregnancy", "pregnant", "maternal", "obstetric", "postpartum"],
    "pediatrics": ["child", "children", "adolescent", "pediatric", "paediatric"],
}

CONDITION_KEYWORDS = {
    "gastroparesis": [
        "gastroparesis",
    ],
    "gi_dysmotility": [
        "gastrointestinal dysmotility",
        "intestinal dysmotility",
        "gut dysmotility",
    ],
    "ibs": [
        "irritable bowel syndrome",
        "ibs",
    ],
    "gerd": [
        "gastroesophageal reflux disease",
        "gastroesophageal reflux",
        "gerd",
    ],
    "constipation": [
        "constipation",
    ],
    "migraine": [
        "migraine",
        "migraines",
    ],
    "headache": [
        "headache",
        "headaches",
    ],
    "small_fiber_neuropathy": [
        "small fiber neuropathy",
        "small-fiber neuropathy",
    ],
    "neuropathy": [
        "neuropathy",
        "neuropathic pain",
    ],
    "chiari_malformation": [
        "chiari malformation",
        "chiari i malformation",
    ],
    "tinnitus": [
        "tinnitus",
    ],
    "dysautonomia": [
        "dysautonomia",
        "autonomic dysfunction",
    ],
    "orthostatic_intolerance": [
        "orthostatic intolerance",
    ],
    "syncope": [
        "syncope",
        "fainting",
    ],
    "chronic_pain": [
        "chronic pain",
    ],
    "fibromyalgia": [
        "fibromyalgia",
    ],
    "pelvic_pain": [
        "pelvic pain",
    ],
    "joint_instability": [
        "joint instability",
        "joint dislocation",
        "joint subluxation",
    ],
    "tmj": [
        "temporomandibular disorder",
        "temporomandibular disorders",
        "tmj disorder",
    ],
    "endometriosis": [
        "endometriosis",
    ],
    "pelvic_floor_dysfunction": [
        "pelvic floor dysfunction",
        "pelvic floor disorder",
    ],
    "menstrual_disorders": [
        "menstrual disorder",
        "menstrual disorders",
        "menstrual dysfunction",
    ],
    "pregnancy": [
        "pregnancy",
        "pregnant",
    ],
    "pregnancy_complications": [
        "pregnancy complication",
        "pregnancy complications",
        "obstetric complication",
        "obstetric complications",
    ],
    "me_cfs": [
        "myalgic encephalomyelitis",
        "chronic fatigue syndrome",
        "me/cfs",
    ],
    "long_covid": [
        "long covid",
        "long COVID",
        "post-covid condition",
        "post-acute sequelae of SARS-CoV-2",
    ],
    "mast_cell_disorders": [
        "mast cell activation syndrome",
        "mastocytosis",
        "mast cell disorder",
        "mast cell disorders",
    ],
    "anaphylaxis": [
        "anaphylaxis",
    ],
    "anxiety": [
        "anxiety",
        "anxiety disorder",
        "anxiety disorders",
    ],
    "depression": [
        "depression",
        "depressive disorder",
        "depressive disorders",
    ],
    "tachycardia": [
        "tachycardia",
    ],
    "hypotension": [
        "hypotension",
    ],
    "sleep_disorders": [
        "sleep disorder",
        "sleep disorders",
        "insomnia",
    ],
    "marfan_syndrome": [
        "marfan syndrome",
    ],
    "loeys_dietz_syndrome": [
        "loeys-dietz syndrome",
        "loeys dietz syndrome",
    ],
    "connective_tissue_disorder": [
        "connective tissue disorder",
        "connective tissue disorders",
    ],
}

INTRINSIC_CONCEPTS = {
    "connective_tissue_disorder",
    "tachycardia",
    "dysautonomia",
    "orthostatic_intolerance",
    "hypotension",
    "syncope",
    "joint_instability",
    "mast_cell_disorders",
}

SYMPTOM_FEATURE_CONCEPTS = {
    "chronic_pain",
    "headache",
    "migraine",
    "constipation",
    "pelvic_pain",
    "anxiety",
    "depression",
    "sleep_disorders",
    "tinnitus",
    "menstrual_disorders",
    "pregnancy",
    "pregnancy_complications",
    "anaphylaxis",
}

MECHANISM_CONCEPTS = {
    "neuropathy",
    "small_fiber_neuropathy",
}

EXTERNAL_CONDITIONS = {
    "gastroparesis",
    "gi_dysmotility",
    "ibs",
    "gerd",
    "fibromyalgia",
    "endometriosis",
    "me_cfs",
    "long_covid",
    "marfan_syndrome",
    "loeys_dietz_syndrome",
    "chiari_malformation",
    "pelvic_floor_dysfunction",
    "tmj",
}