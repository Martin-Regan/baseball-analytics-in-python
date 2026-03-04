import statsapi
import pandas as pd

stat = "onBasePlusSlugging"

top_n = 10

season = 2025

leaders = statsapi.league_leader_data(stat, season=season, statGroup="hitting", limit=top_n)

df = pd.DataFrame(leaders, columns=["Rank", "Player", "Team", stat])
df[stat] = pd.to_numeric(df[stat], errors="coerce")

df = df.sort_values(stat, ascending=False).reset_index(drop=True)

gap = df.loc[0, stat] - df.loc[df.index[-1], stat]

print(df)
print(f"\nGap between #1 and #{len(df)}: {gap:.3f}")