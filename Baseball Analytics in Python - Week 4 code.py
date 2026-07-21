import pandas as pd
import statsapi

season = 2025
top_n = 100

#Get the top 100 pitchers by Strikeouts
so = statsapi.league_leader_data("strikeOuts", season=season, limit=top_n)
so_df = pd.DataFrame(so)
so_df.columns = ["Strikeouts_rank", "Player", "team", "value"]
so_df = so_df[["Player", "Strikeouts_rank"]]

#Get the top 100 pitchers by K/9
k9 = statsapi.league_leader_data("strikeoutsPer9", season=season, limit=top_n, statGroup="pitching")
k9_df = pd.DataFrame(k9)
k9_df.columns = ["K9_rank", "Player", "team", "value"]
k9_df = k9_df[["Player", "K9_rank"]]

#Get the top 100 players by ERA
era = statsapi.league_leader_data("era", season=season, limit=top_n)
era_df = pd.DataFrame(era)
era_df.columns = ["ERA_rank", "Player", "team", "value"]
era_df = era_df[["Player", "ERA_rank"]]

#Get the top 100 players by WHIP
whip = statsapi.league_leader_data("whip", season=season, limit=top_n)
whip_df = pd.DataFrame(whip)
whip_df.columns = ["WHIP_rank", "Player", "team", "value"]
whip_df = whip_df[["Player", "WHIP_rank"]]

#Merge the four stat tables into one table
combined = so_df.merge(k9_df, on="Player", how="outer")
combined = combined.merge(era_df, on="Player", how="outer")
combined = combined.merge(whip_df, on="Player", how="outer")

#If a player is not ranked in the top 100 for a stat, we give them a default rank of 101
combined = combined.fillna(101)

#Create our combined ranking
combined["combined_rank"] = (combined["Strikeouts_rank"] + combined["K9_rank"] + combined["ERA_rank"] + combined["WHIP_rank"])

#Sort our table by this combined ranking
combined = combined.sort_values("combined_rank")

#Output the table to CSV, so we can read it in Excel
combined.to_csv("Pitchers Ranking.csv", index=False, encoding="utf-8-sig")
