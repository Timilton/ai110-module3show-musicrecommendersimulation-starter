# System Diagram: BestMatchMusic Recommender

## Data Flow

```mermaid
flowchart TD
    A([👤 User Input\nfavorite_genre, favorite_mood\ntarget_energy, target_tempo\ntarget_danceability, target_acousticness]) --> C

    B([🗄️ Song Catalog\ndata/songs.csv\n18 songs × 10 features]) --> C

    C[📥 load_songs\nParse CSV → cast types\nreturn List of Dicts] --> D

    D[⚙️ score_song\nFor each song:\n• Genre match +2.0\n• Mood match +1.0\n• Energy match +2.0\n• Tempo proximity ×1.5\n• Acousticness prox ×1.0\n• Danceability prox ×0.75\nMax score: 8.25] --> E

    E[📊 recommend_songs\nSort all scores descending\nReturn top-K results] --> F

    F([🎵 Output\nRanked list of songs\nwith score + reason string])

    F --> G{🧪 Automated Tests\ntests/test_recommender.py\npytest}
    F --> H{👁️ Human Review\nmodel_card.md\nManual spot-check of\nrecommendation quality}

    G -->|Pass / Fail| I([Test Report])
    H -->|Evaluation notes| J([Model Card])
```

## Component Descriptions

| Component | File | Role |
|---|---|---|
| User Input | `src/main.py` | Defines the taste profile dict passed into the recommender |
| Song Catalog | `data/songs.csv` | Static dataset of 18 songs with 10 numeric/categorical features |
| Loader | `src/recommender.py → load_songs()` | Reads CSV, casts strings to int/float |
| Scorer | `src/recommender.py → score_song()` | Applies weighted scoring rules to one song vs. one user profile |
| Ranker | `src/recommender.py → recommend_songs()` | Scores all songs, sorts descending, slices top-K |
| OOP Layer | `src/recommender.py → Recommender class` | Wraps scorer in an object interface used by the test suite |
| Automated Tests | `tests/test_recommender.py` | Verifies ranking order and explanation output with pytest |
| Human Review | `model_card.md` | Documents bias, limitations, and evaluation by the developer |

## Where Humans Are Involved

```
Input design  ──→  Human writes UserProfile (taste preferences)
                   Human curates songs.csv catalog

Output review ──→  Human reads model_card.md evaluation
                   Human spot-checks whether top results "feel right"
                   Human adjusts point weights based on intuition
```
