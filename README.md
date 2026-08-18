# UD Accounting Hoop Challenge

A Streamlit accounting-classification game. Students match definition
basketballs to account hoops under a ten-second shot clock. Correct answers
earn 10 points; incorrect answers and shot-clock violations cost 2 points,
with a minimum score of zero.

Scores and completion times are submitted to a Google Form. The published
leaderboard keeps each student's highest score and uses the fastest time among
attempts earning that score as the tie-breaker. See `LEADERBOARD_SETUP.md` for
the Google integration details.

### How to run it on your own machine

Prerequisite: install `uv` if you don't already have it.

```
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

1. Sync the dependencies

   ```
   $ uv sync
   ```

2. Run the app

   ```
   $ uv run streamlit run streamlit_app.py
   ```
