"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # User taste profile — targets mid-high energy, beat-driven, electronic production
    user_prefs = {
        "favorite_genre":  "hip-hop",
        "favorite_mood":   "energetic",
        "target_energy":   0.85,
        "target_tempo":    100,       # mid-range BPM — punchy but not frantic
        "target_danceability": 0.88,
        "target_acousticness": 0.10,  # prefers electronic/produced over organic
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print("  TOP RECOMMENDATIONS FOR YOU")
    print("=" * 50)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} by {song['artist']}")
        print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}")
        print(f"    Score: {score:.2f} / 8.25")
        print("    Why matched:")
        for reason in explanation.split(" | "):
            print(f"      - {reason}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
