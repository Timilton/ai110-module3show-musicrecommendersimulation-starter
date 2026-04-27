# BestMatchMusic — Music Recommender Simulation

## Title and Summary

**BestMatchMusic** is a rule-based music recommendation engine that scores a catalog of songs against a user's taste profile and returns the top matches ranked by fit. It demonstrates how real recommender systems work under the hood — turning structured data and weighted scoring rules into personalized output — without relying on a pre-trained ML model.

This project matters because most people interact with recommendation systems every day (Spotify, YouTube, Netflix) without understanding how they work. Building one from scratch makes those systems legible and shows where human judgment, bias, and design decisions shape what you see.

---

## Original Project

This project is **Module 3** of the AI110 course series. It builds directly on the data modeling and OOP patterns introduced in **Module 2 (PawPal)**, which was a pet profile and care suggestion tool. PawPal used structured data classes and simple matching logic to suggest care routines for pets based on breed and age. BestMatchMusic applies the same idea — user profile + catalog scoring — but extends it with a multi-feature weighted algorithm, numeric proximity functions, and a formal model card evaluation.

---

## Architecture Overview

The system has four main stages:

1. **Load** — `load_songs()` reads `data/songs.csv` and casts every row into typed Python dicts (strings become floats/ints).
2. **Score** — `score_song()` runs each song through a 6-factor weighted rubric against the user's preferences and returns a total score plus a list of reasons.
3. **Rank** — `recommend_songs()` collects all scores, sorts them highest to lowest, and returns the top K.
4. **Output** — `main.py` prints the ranked results with scores and explanations to the terminal.

An OOP wrapper (`Recommender` class) exposes the same logic for the automated test suite.

See [system_diagram.md](system_diagram.md) for the full data flow and component map.

---

## Setup Instructions

**Requirements:** Python 3.9+

1. Clone the repository:
   ```bash
   git clone https://github.com/Timilton/ai110-module3show-musicrecommendersimulation-starter.git
   cd ai110-module3show-musicrecommendersimulation-starter
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Mac / Linux
   .venv\Scripts\activate           # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the recommender:
   ```bash
   python -m src.main
   ```

5. Run the test suite:
   ```bash
   pytest
   ```

---

## Sample Interactions

### Example 1 — Hip-Hop / Energetic Listener

**Input (user profile in `main.py`):**
```python
{
    "favorite_genre":      "hip-hop",
    "favorite_mood":       "energetic",
    "target_energy":       0.85,
    "target_tempo":        100,
    "target_danceability": 0.88,
    "target_acousticness": 0.10
}
```

**Output:**
```
#1  Block Party Anthem by Concrete Waves
    Genre: hip-hop  |  Mood: euphoric
    Score: 7.41 / 8.25
    Why matched:
      - genre match (+2.0)
      - energy match (+2.0)
      - tempo fit (+1.39)
      - acousticness fit (+0.92)
      - danceability fit (+0.55)

#2  Drop the Grid by Voltage CTRL
    Genre: edm  |  Mood: energetic
    Score: 6.98 / 8.25
    Why matched:
      - mood match (+1.0)
      - energy match (+2.0)
      - tempo fit (+1.21)
      - acousticness fit (+0.94)
      - danceability fit (+0.53)
```

---

### Example 2 — Chill / Lofi Listener

**Input:**
```python
{
    "favorite_genre":      "lofi",
    "favorite_mood":       "chill",
    "target_energy":       0.40,
    "target_tempo":        78,
    "target_danceability": 0.60,
    "target_acousticness": 0.75
}
```

**Output:**
```
#1  Midnight Coding by LoRoom
    Genre: lofi  |  Mood: chill
    Score: 7.89 / 8.25
    Why matched:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy match (+2.0)
      - tempo fit (+1.50)
      - acousticness fit (+0.96)
      - danceability fit (+0.51)

#2  Library Rain by Paper Lanterns
    Genre: lofi  |  Mood: chill
    Score: 7.52 / 8.25
    Why matched:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy match (+2.0)
      - tempo fit (+1.30)
      - acousticness fit (+0.89)
      - danceability fit (+0.48)
```

---

### Example 3 — Rock / Intense Listener

**Input:**
```python
{
    "favorite_genre":      "rock",
    "favorite_mood":       "intense",
    "target_energy":       0.90,
    "target_tempo":        150,
    "target_danceability": 0.65,
    "target_acousticness": 0.10
}
```

**Output:**
```
#1  Storm Runner by Voltline
    Genre: rock  |  Mood: intense
    Score: 8.10 / 8.25
    Why matched:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy match (+2.0)
      - tempo fit (+1.48)
      - acousticness fit (+0.99)
      - danceability fit (+0.51)

#2  Shattered Signal by Iron Veil
    Genre: metal  |  Mood: angry
    Score: 6.44 / 8.25
    Why matched:
      - energy match (+2.0)
      - tempo fit (+1.43)
      - acousticness fit (+0.96)
      - danceability fit (+0.42)
```

---

## Design Decisions

**Why weighted rules instead of ML?**
The catalog has only 18 songs — not enough data to train a model. A rule-based scorer is fully transparent: you can read exactly why a song ranked where it did. Real systems like Spotify use collaborative filtering and embeddings at scale, but the underlying idea (similarity scoring) is the same.

**Why is genre weighted the highest (+2.0)?**
Genre encodes the most information about how a song actually sounds — instrument palette, production style, tempo range, and structure. Mood (+1.0) varies too much within a genre to be the top signal.

**Why treat energy as categorical (within-0.15 threshold) instead of numeric proximity?**
Energy in the 0.0–1.0 range already compresses a lot of perceptual difference. A strict proximity function would penalize songs that "feel" the same energy but score 0.16 apart. The threshold makes the match feel more natural.

**Trade-off: No diversity control**
The current ranker always picks the most similar songs. In a real product this creates a filter bubble — if you love lofi, you only ever hear lofi. A future version would add a diversity penalty to ensure the top-5 spans at least two genres.

**Trade-off: Static catalog**
Songs are loaded from a CSV at runtime. Adding or removing songs requires editing the file manually. A real system would use a database (e.g. MongoDB Atlas with vector search) so the catalog scales without code changes.

---

## Testing Summary

**What worked:**
- The ranking logic correctly surfaces the genre+mood match at the top when all features align.
- The proximity functions scale cleanly — a perfect tempo match contributes the full 1.5 points, and the contribution degrades smoothly as BPM diverges.
- The test suite (`pytest`) caught an early bug where the OOP `Recommender.recommend()` was returning unsorted songs.

**What didn't work at first:**
- Acousticness proximity unexpectedly dominated rankings for some profiles. A song could match on genre and mood but rank lower than expected because its acousticness score was far off. This revealed that numerical proximity scores can quietly override categorical matches when the gap is large.
- The catalog has no rap/trap or R&B-dominant profiles, so users with those preferences get poor genre matches and the system falls back entirely on numerical proximity — which feels wrong.

**What I learned:**
Feature weights are design decisions, not math. Every weight encodes an assumption about what matters. Changing genre from +2.0 to +0.5 completely scrambled the results, which made it clear that the "algorithm" is really just a formalized version of someone's opinion about music.

---

## Reflection

Building this project changed how I think about every recommendation I see. Spotify's "Discover Weekly," YouTube's autoplay, and Netflix's "Because you watched..." are all doing some version of this — comparing your profile against a catalog and returning the highest-scoring matches. The difference is scale (millions of songs vs. 18) and the fact that they use embeddings and user behavior data instead of hand-written rules.

The most surprising thing was how much human judgment is baked into a system that looks objective. Every weight, every feature choice, every threshold is a decision someone made. If the catalog doesn't include rap, rap listeners get bad recommendations — not because the algorithm is broken, but because the data doesn't represent them. That's a form of bias that has nothing to do with the math.

This project made it concrete: AI systems don't discover preferences, they reflect the assumptions of whoever built and curated them. Understanding that is the first step to building fairer systems.

---

## Files

```
├── src/
│   ├── recommender.py     # Core logic: Song, UserProfile, Recommender, score_song, recommend_songs
│   └── main.py            # CLI runner with sample user profile
├── data/
│   └── songs.csv          # 18-song catalog with 10 features per song
├── tests/
│   └── test_recommender.py
├── model_card.md          # Bias, evaluation, and limitations documentation
├── system_diagram.md      # Data flow and component diagram
└── requirements.txt
```
