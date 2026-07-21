import pandas as pd
import statsapi

season = 2025
top_n = 100

#Get the top 100 players by OPS
ops = statsapi.league_leader_data("ops", season=season, limit=top_n)
ops_df = pd.DataFrame(ops)
ops_df.columns = ["OPS_rank", "Player", "team", "value"]
ops_df = ops_df[["Player", "OPS_rank"]]

#Get the top 100 players by hits
h = statsapi.league_leader_data("hits", season=season, limit=top_n)
h_df = pd.DataFrame(h)
h_df.columns = ["Hits_rank", "Player", "team", "value"]
h_df = h_df[["Player", "Hits_rank"]]

#Get the top 100 players by RBI
rbi = statsapi.league_leader_data("runsBattedIn", season=season, limit=top_n)
rbi_df = pd.DataFrame(rbi)
rbi_df.columns = ["RBI_rank", "Player", "team", "value"]
rbi_df = rbi_df[["Player", "RBI_rank"]]

#Get the top 100 players by Total Bases
tb = statsapi.league_leader_data("totalBases", season=season, limit=top_n)
tb_df = pd.DataFrame(tb)
tb_df.columns = ["TB_rank", "Player", "team", "value"]
tb_df = tb_df[["Player", "TB_rank"]]

#Merge the four stat tables into one table
combined = ops_df.merge(h_df, on="Player", how="outer")
combined = combined.merge(rbi_df, on="Player", how="outer")
combined = combined.merge(tb_df, on="Player", how="outer")

#If a player is not ranked in the top 100 for a stat, we give them a default rank of 101
combined = combined.fillna(101)

#Create our combined ranking
combined["combined_rank"] = (combined["OPS_rank"] + combined["Hits_rank"] + combined["RBI_rank"] + combined["TB_rank"])

#Sort our table by this combined ranking
combined = combined.sort_values("combined_rank")

#Output the table to CSV, so we can read it in Excel
combined.to_csv("output2.csv", index=False, encoding="utf-8-sig")
