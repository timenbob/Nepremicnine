import pandas as pd
import geopandas as gpd


file = "/home/timen/Documents/Faks/ioi clanek/obcine_eur_m2.geojson"

gdf = gpd.read_file("/home/timen/Documents/Faks/ioi clanek/obcine_eur_m2.geojson")

for _, row in gdf.iterrows():
    print(row["OB_UIME"], row["eur_m2"])

