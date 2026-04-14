# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---
BestMatchMusic

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

My recommendor is intended to find similar songs based off vibe, instrumentals, and melody, which groups these songs together to be in a recommendor

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

The model looks at six things about each song: its genre, mood, energy level, tempo (how fast the beat is), acousticness (how organic or electronic it sounds), and danceability (how easy it is to dance to). It also asks the user for their preferences — what genre and mood they like, what energy level they want, and how acoustic they want the sound to be.

Once it has that information, it gives each song in the catalog a score by comparing it to what the user said they like. Genre is the most important factor, worth up to 2 points, because genre shapes the overall sound more than anything else. Mood is worth 1 point. Energy is also worth up to 2 points — if a song's energy is close enough to what the user wants, it gets full credit. Tempo, acousticness, and danceability are each scored by how close the song is to the user's target — the closer the match, the more points it gets.

All those points are added up, and the songs with the highest total scores get recommended. The main change from the starter logic was adding energy as a strong scoring category and adjusting the weights so that tempo and acousticness reflect how much those actually affect the listening experience.



## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---
There is 18 songs in the datasets, and the model uses different generes such as pop and rock. I added about 10 songs to the dataset to see how accuarate the model is, and the only musical genre that is missing is rap/ trap.

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

- Some strengths that this project has is that the algorithmic aspect works really strong, mapping out other songs similarities to each other based on the categories provided. 

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

Limitations that the model has is the acousticness, since the model hasnt been properly trained to know this field properly to match to other songs. On the dataset, I compared it to other songs, and it can't correctly score based on this field due to the limitation the model has. 

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

To evaluate the recommender, I tested two different user profiles. The first was a high-energy pop listener who likes happy songs and is not into acoustic music. The second was a chill listener who prefers lofi, calm moods, and more acoustic sounds. For each profile, I looked at whether the top results actually matched what that type of person would want such as the right genre, the right vibe, and a similar energy level.

What I was looking for was whether the ranking made sense intuitively. If I said I liked pop and happy songs, the first result should not be a slow acoustic folk track. The tests confirmed that the pop/happy profile consistently surfaced the pop song at the top, and the chill/lofi profile pushed the lofi song higher.

What surprised me was how much the acousticness score affected rankings even when genre and mood already matched well. A song could match on genre and mood but still rank lower than expected because its acousticness was far off from the user's target. It made me realize that the numerical proximity scores can quietly override the categorical matches if the gap is large enough.

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

- Some future work I would include is to use an actual LLM API, so that the model can search these songs on the web to know what artist are similar to them, their background information and how the songs actually sound. I would also use Pydantic's Basemodel class function instead of the dataclass decorator since Pydantic would help with type coercion and validation at construction. 

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

- Some things that I learned is to give categories different weights based on how important it can effect the outcome, and using the top k algorthim making sure that its sorted. 
