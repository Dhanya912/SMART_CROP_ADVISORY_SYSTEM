# -*- coding: utf-8 -*-
"""
disease_agent.py — Crop-aware leaf disease detection.

Replaces the old "demo" agent that spread probability almost evenly across
39 classes (every answer came back at ~6.7% confidence, so the UI looked
like nothing was ever detected).
"""

import os, csv
import numpy as np
from utils.logger import get_logger
import i18n

logger = get_logger(__name__)

DISEASES = {
    'Apple___Apple_scab': ('Apple Scab', 'Moderate', 'Fungal',
        ['Apply captan fungicide.', 'Prune infected leaves.'], 'Use scab-resistant varieties.'),
    'Apple___Black_rot': ('Black Rot', 'High', 'Fungal',
        ['Prune infected branches.', 'Apply copper fungicide.'], 'Maintain orchard sanitation.'),
    'Corn_(maize)___Northern_Leaf_Blight': ('Maize Northern Leaf Blight', 'Moderate', 'Fungal',
        ['Apply azoxystrobin.', 'Use resistant hybrids.'], 'Rotate crops to break cycle.'),
    'Corn_(maize)___Common_rust': ('Maize Common Rust', 'Moderate', 'Fungal',
        ['Apply propiconazole at first pustules.', 'Plant resistant hybrids.'],
        'Avoid late sowing; scout weekly.'),
    'Tomato___Late_blight': ('Tomato Late Blight', 'Very High', 'Fungal',
        ['Remove infected plants.', 'Apply mancozeb.', 'Avoid overhead watering.'],
        'Use certified disease-free seeds.'),
    'Tomato___Early_blight': ('Tomato Early Blight', 'Moderate', 'Fungal',
        ['Apply chlorothalonil.', 'Remove lower leaves.'], 'Mulch soil surface.'),
    'Tomato___Septoria_leaf_spot': ('Tomato Septoria Leaf Spot', 'Moderate', 'Fungal',
        ['Apply mancozeb weekly.', 'Remove spotted lower leaves.'], 'Keep foliage dry; stake plants.'),
    'Tomato___Leaf_Mold': ('Tomato Leaf Mold', 'Moderate', 'Fungal',
        ['Improve ventilation.', 'Apply chlorothalonil.'], 'Avoid high humidity.'),
    'Tomato___Yellow_Leaf_Curl_Virus': ('Yellow Leaf Curl Virus', 'High', 'Viral',
        ['Remove infected plants.', 'Control whitefly.'], 'Use virus-resistant varieties.'),
    'Tomato___Bacterial_spot': ('Tomato Bacterial Spot', 'High', 'Bacterial',
        ['Spray copper oxychloride.', 'Destroy badly infected plants.'],
        'Use clean seed and rotate away from solanaceae.'),
    'Potato___Late_blight': ('Potato Late Blight', 'Very High', 'Fungal',
        ['Apply mancozeb immediately.', 'Destroy infected plants.'], 'Use certified seed potatoes.'),
    'Potato___Early_blight': ('Potato Early Blight', 'Moderate', 'Fungal',
        ['Apply chlorothalonil.', 'Remove infected leaves.'], 'Avoid overhead irrigation.'),
    'Grape___Black_rot': ('Grape Black Rot', 'High', 'Fungal',
        ['Apply mancozeb.', 'Remove mummified berries.'], 'Maintain canopy airflow.'),
    'Grape___Leaf_blight': ('Grape Leaf Blight', 'Moderate', 'Fungal',
        ['Apply copper fungicide.', 'Remove affected leaves.'], 'Prune for airflow.'),
    'Healthy': ('No Disease Detected', 'None', 'None',
        ['Continue regular monitoring.'], 'Maintain balanced fertilisation.'),
}

CORE_KEYS = list(DISEASES.keys())
KEYS = list(DISEASES.keys())

DATA_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'plant_disease.csv')


def _enrich_from_dataset():
    if not os.path.exists(DATA_CSV):
        return
    try:
        meta = {}
        with open(DATA_CSV, newline='', encoding='utf-8') as f:
            for r in csv.DictReader(f):
                cls = (r.get('disease_class') or '').strip()
                if not cls or cls in DISEASES or cls in meta:
                    continue
                meta[cls] = (
                    (r.get('disease_name') or 'Unknown').strip(),
                    (r.get('severity') or 'Moderate').strip(),
                    (r.get('cause_type') or 'Fungal').strip(),
                    [(r.get('treatment') or 'Consult local agronomist.').strip()],
                    'Follow good field sanitation and monitor regularly.')
        DISEASES.update(meta)
        KEYS.extend(meta.keys())
        if meta:
            logger.info(f"DiseaseAgent: taxonomy extended with {len(meta)} classes "
                        f"from plant_disease.csv (total {len(DISEASES)})")
    except Exception as e:
        logger.warning(f"plant_disease.csv load failed: {e}")


_enrich_from_dataset()

CROP_TOKENS = {
    'tomato': ['tomato'], 'potato': ['potato'], 'maize': ['corn', 'maize'],
    'corn': ['corn', 'maize'], 'apple': ['apple'], 'grape': ['grape'],
    'pepper': ['pepper'], 'peach': ['peach'], 'cherry': ['cherry'],
    'strawberry': ['strawberry'], 'orange': ['orange', 'citrus'],
    'soybean': ['soybean'], 'rice': ['rice'], 'wheat': ['wheat'],
}


def _candidates(crop):
    crop = (crop or '').strip().lower()
    tokens = None
    for name, toks in CROP_TOKENS.items():
        if crop and (crop.startswith(name) or name in crop):
            tokens = toks
            break
    if not tokens:
        return list(CORE_KEYS)
    sel = [k for k in KEYS if any(t in k.lower() for t in tokens) and k != 'Healthy']
    if not sel:
        sel = [k for k in CORE_KEYS if k != 'Healthy']
    curated = [k for k in sel if k in CORE_KEYS]
    others = [k for k in sel if k not in CORE_KEYS]
    return (curated + others)[:8] + ['Healthy']


def _features(path):
    from PIL import Image
    img = Image.open(path).convert('RGB').resize((128, 128))
    a = np.asarray(img, dtype=float) / 255.0
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    mx = a.max(axis=2); mn = a.min(axis=2)
    val = mx
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)

    green = (g > r + 0.04) & (g > b + 0.04) & (val > 0.15)
    yellow = (r > 0.45) & (g > 0.40) & (b < 0.35) & (np.abs(r - g) < 0.22)
    brown = (r > 0.22) & (r > g + 0.03) & (g >= b) & (val < 0.62) & (sat > 0.15)
    rust = (r > 0.35) & (r > g + 0.12) & (b < 0.32)
    dark = val < 0.22
    grey = (sat < 0.12) & (val > 0.35) & (val < 0.85)

    n = a.shape[0] * a.shape[1]
    return {'green': float(green.sum()) / n, 'yellow': float(yellow.sum()) / n,
            'brown': float(brown.sum()) / n, 'red': float(rust.sum()) / n,
            'dark': float(dark.sum()) / n, 'grey': float(grey.sum()) / n,
            'contrast': float(val.std()), 'brightness': float(val.mean()),
            'saturation': float(sat.mean())}


def _score(key, f):
    """Evidence score for one disease. Lesion coverage drives the healthy /
    diseased decision; colour signature decides which disease."""
    name = key.lower()
    lesion = min(1.0, f['brown'] + f['red'] + f['dark'] + 0.6 * f['yellow'])
    L = np.sqrt(lesion)
    y, br, rd, dk, gr = (np.sqrt(f['yellow']), np.sqrt(f['brown']),
                         np.sqrt(f['red']), np.sqrt(f['dark']), np.sqrt(f['grey']))

    if key == 'Healthy':
        return 0.3 + 2.5 * f['green'] - 12.0 * L - 1.5 * f['contrast']

    s = 0.4 + 6.0 * L + 0.9 * f['contrast']
    if 'late_blight' in name: s += 1.8 * br + 1.6 * dk + 0.8 * f['contrast']
    if 'early_blight' in name: s += 1.7 * br + 1.1 * y
    if 'leaf_spot' in name or 'septoria' in name or 'spot' in name: s += 1.6 * dk + 1.3 * br + 0.9 * f['contrast']
    if 'scab' in name: s += 1.7 * dk + 1.2 * br + 0.7 * gr
    if 'rot' in name: s += 1.7 * dk + 1.1 * br
    if 'rust' in name: s += 2.4 * rd + 1.0 * br
    if 'virus' in name or 'curl' in name or 'mosaic' in name: s += 2.4 * y - 1.0 * dk
    if 'mold' in name or 'mould' in name: s += 1.6 * y + 1.1 * gr
    if 'bacterial' in name: s += 1.5 * dk + 1.2 * br
    if 'northern' in name: s += 1.5 * br + 1.0 * f['contrast']
    s -= 2.5 * max(0.0, f['green'] - 0.75)
    return s


def _softmax(vals, temp=0.28):
    v = np.array(vals, dtype=float) / max(temp, 1e-6)
    v -= v.max()
    e = np.exp(v)
    return e / e.sum()


class DiseaseDetectionAgent:
    def __init__(self):
        self.mode = 'vision-heuristic'
        logger.info(f"DiseaseAgent ready ({self.mode}; {len(DISEASES)} classes, "
                    f"{len(CORE_KEYS)} core scored classes).")

    def detect(self, path, lang='en', crop=None):
        if not path or not os.path.exists(path):
            return {'error': 'Image not found'}
        try:
            f = _features(path)
        except Exception as e:
            logger.warning(f"Image read failed: {e}")
            return {'error': 'Could not read the image. Please upload a clear JPG or PNG leaf photo.'}

        cands = _candidates(crop)
        probs = _softmax([_score(k, f) for k in cands])
        order = np.argsort(probs)[::-1]

        best = cands[order[0]]
        conf = round(float(probs[order[0]]) * 100, 1)
        name, sev, cause, treat, prev = DISEASES.get(best, DISEASES['Healthy'])

        return {'disease_key': best, 'disease_name': name, 'confidence': conf,
                'severity': i18n.status(sev, lang), 'severity_raw': sev,
                'cause': cause, 'treatment': treat, 'prevention': prev,
                'status': 'healthy' if sev == 'None' else 'diseased',
                'crop_used': (crop or 'auto-detect'),
                'image_features': {k: round(v, 4) for k, v in f.items()},
                'top3': [{'disease': DISEASES.get(cands[i], DISEASES['Healthy'])[0],
                          'confidence': round(float(probs[i]) * 100, 1)} for i in order[:3]]}
