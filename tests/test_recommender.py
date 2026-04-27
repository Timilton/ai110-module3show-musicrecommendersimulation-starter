from src.recommender import Song, UserProfile, Recommender, score_song, recommend_songs

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


# --- OOP interface tests ---

def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# --- score_song unit tests ---

def _pop_song() -> dict:
    return {
        "id": 99, "title": "Perfect Match", "artist": "X",
        "genre": "pop", "mood": "happy",
        "energy": 0.80, "tempo_bpm": 100.0,
        "valence": 0.9, "danceability": 0.70, "acousticness": 0.50,
    }

def _pop_user() -> dict:
    return {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "target_tempo": 100.0,
        "target_danceability": 0.70,
        "target_acousticness": 0.50,
    }


def test_score_song_perfect_match_equals_max():
    """A song that matches every feature exactly should score the maximum 8.25."""
    score, reasons = score_song(_pop_song(), _pop_user())
    assert score == 8.25, f"Expected 8.25, got {score}"


def test_score_song_no_categorical_match():
    """A song with wrong genre and mood should score lower than max by at least 3.0."""
    song = _pop_song()
    song["genre"] = "metal"
    song["mood"] = "angry"
    score, _ = score_song(song, _pop_user())
    assert score <= 5.25, f"Expected <= 5.25 without genre/mood match, got {score}"


def test_score_song_reasons_contain_genre_match():
    """When genre matches, the reasons list must include a genre match entry."""
    _, reasons = score_song(_pop_song(), _pop_user())
    assert any("genre match" in r for r in reasons)


def test_recommend_songs_returns_exactly_k():
    """recommend_songs should return exactly k results even with a large catalog."""
    songs = [_pop_song() for _ in range(10)]
    for i, s in enumerate(songs):
        s["id"] = i
    results = recommend_songs(_pop_user(), songs, k=3)
    assert len(results) == 3


def test_score_is_within_valid_range():
    """All scores should be between 0 and 8.25 regardless of input."""
    song = _pop_song()
    user = _pop_user()
    # Worst case: completely opposite values
    song["genre"] = "classical"
    song["mood"] = "melancholic"
    song["energy"] = 0.0
    song["tempo_bpm"] = 55.0
    song["danceability"] = 0.0
    song["acousticness"] = 1.0
    score, _ = score_song(song, user)
    assert 0.0 <= score <= 8.25
