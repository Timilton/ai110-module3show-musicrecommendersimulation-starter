from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to float/int."""
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":            int(row["id"]),
                "title":         row["title"],
                "artist":        row["artist"],
                "genre":         row["genre"],
                "mood":          row["mood"],
                "energy":        float(row["energy"]),
                "tempo_bpm":     float(row["tempo_bpm"]),
                "valence":       float(row["valence"]),
                "danceability":  float(row["danceability"]),
                "acousticness":  float(row["acousticness"]),
            })
    return songs

# ---------------------------------------------------------------------------
# ALGORITHM RECIPE
# ---------------------------------------------------------------------------
# Point weights (tuned to prioritize beat + pace + instrumentation):
#
#   +2.0  Genre match          — strongest structural signal (instrument palette,
#                                production style, overall sound world)
#   +1.0  Mood match           — secondary; mood varies widely within a genre so
#                                worth less than genre
#   +1.5  Tempo proximity      — your #1 vibe axis ("how fast-paced"); normalized
#                                0–1, then scaled so a perfect match = +1.5
#   +1.25 Energy proximity     — overall intensity; close partner to tempo
#   +1.0  Acousticness prox.   — captures "instrumental similarities" (organic vs
#                                electronic production feel)
#   +0.75 Danceability prox.   — beat regularity / rhythmic tightness
#
# Max possible score: 2.0 + 1.0 + 1.5 + 1.25 + 1.0 + 0.75 = 7.5
# ---------------------------------------------------------------------------

TEMPO_MIN = 55.0   # lowest BPM in dataset (classical)
TEMPO_MAX = 170.0  # highest BPM in dataset (metal)

def _proximity(song_val: float, target_val: float) -> float:
    """Returns 0.0–1.0 where 1.0 = perfect match (no difference)."""
    return 1.0 - abs(song_val - target_val)

def _tempo_proximity(song_bpm: float, target_bpm: float) -> float:
    """Normalizes BPM to 0–1 before computing proximity."""
    norm_song   = (song_bpm   - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
    norm_target = (target_bpm - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
    return 1.0 - abs(norm_song - norm_target)

def score_song(song: Dict, user_prefs: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against the user profile.

    Algorithm Recipe:
      +2.0  genre match        (categorical — exact string match)
      +1.0  mood match         (categorical — exact string match)
      +2.0  energy match       (categorical — within 0.15 of target energy)
      +1.5  tempo proximity    (numerical — top personal priority: how fast-paced)
      +1.0  acousticness prox. (numerical — organic vs. electronic instrumentation)
      +0.75 danceability prox. (numerical — beat regularity)

    Categorical rule: genre/mood award points on exact match; energy awards +2.0
    if |song_energy - target_energy| <= 0.15 (close enough to "feel the same").
    Proximity formula: (1 - |song_value - target_value|) * weight
    Tempo is normalized to 0-1 before comparing (BPM range: 55–170).
    Max possible score: 2.0 + 1.0 + 2.0 + 1.5 + 1.0 + 0.75 = 8.25

    Returns:
        (total_score, reasons)  where reasons is a list of strings explaining
        each point contribution — e.g. ["genre match (+2.0)", "energy match (+2.0)"]
    """
    reasons: List[str] = []
    total = 0.0

    # --- Categorical: Genre (+2.0) ---
    if song["genre"] == user_prefs["favorite_genre"]:
        total += 2.0
        reasons.append("genre match (+2.0)")

    # --- Categorical: Mood (+1.0) ---
    if song["mood"] == user_prefs["favorite_mood"]:
        total += 1.0
        reasons.append("mood match (+1.0)")

    # --- Categorical: Energy match (+2.0 if within 0.15 of target) ---
    if abs(song["energy"] - user_prefs["target_energy"]) <= 0.15:
        total += 2.0
        reasons.append("energy match (+2.0)")

    # --- Numerical: Tempo proximity (up to +1.5) ---
    t_score = _tempo_proximity(song["tempo_bpm"], user_prefs["target_tempo"]) * 1.5
    total += t_score
    reasons.append(f"tempo fit (+{t_score:.2f})")

    # --- Numerical: Acousticness proximity (up to +1.0) ---
    a_score = _proximity(song["acousticness"], user_prefs["target_acousticness"]) * 1.0
    total += a_score
    reasons.append(f"acousticness fit (+{a_score:.2f})")

    # --- Numerical: Danceability proximity (up to +0.75) ---
    d_score = _proximity(song["danceability"], user_prefs["target_danceability"]) * 0.75
    total += d_score
    reasons.append(f"danceability fit (+{d_score:.2f})")

    return round(total, 3), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song in the catalog and return the top-k results sorted highest to lowest."""
    scored = []
    for song in songs:
        score, reasons = score_song(song, user_prefs)
        explanation = " | ".join(reasons)
        scored.append((song, score, explanation))

    # Ranking Rule: sort by score descending, take top k
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
