import pandas as pd
import geopandas as gpd

# ----------------------------
# FILE PATHS
# ----------------------------
etn_path = "/home/timen/Documents/Faks/ioi clanek/nepremicnine_projekt/etn_2021_2025/processed_outputs/slovenia_apartments_modeling_v1.csv"
geojson_path = "/home/timen/Documents/Faks/ioi clanek/OB.geojson"
output_path = "/home/timen/Documents/Faks/ioi clanek/obcine_eur_m2.geojson"

# ----------------------------
# LOAD ETN DATA
# ----------------------------
df = pd.read_csv(etn_path)

# clean municipality names
df["municipality"] = df["municipality"].astype(str).str.strip()

# DODAJ TUKAJ
df["municipality"] = df["municipality"].str.title()

# remove extreme outliers
df = df[df["price_per_m2"].between(300, 15000)]

# ----------------------------
# FIX MUNICIPALITY NAME MISMATCHES
# ----------------------------
mapping = {
    "Mestna občina Ljubljana": "Ljubljana",
    "Mestna občina Maribor": "Maribor",
    "Mestna občina Koper": "Koper",
    "Mestna občina Novo mesto": "Novo mesto",
    "Mestna občina Celje": "Celje",
}

df["municipality"] = df["municipality"].replace(mapping)

# ----------------------------
# CALCULATE €/m² PER MUNICIPALITY
# ----------------------------
eur_m2 = (
    df.groupby("municipality")["price_per_m2"]
    .median()  # median is more robust than mean
    .reset_index()
)

eur_m2.columns = ["obcina", "eur_m2"]

# ----------------------------
# LOAD MUNICIPALITY GEOJSON
# ----------------------------
gdf = gpd.read_file(geojson_path)

gdf["OB_UIME"] = gdf["OB_UIME"].astype(str).str.strip()

# DODAJ TUKAJ
gdf["OB_UIME"] = gdf["OB_UIME"].str.title()
# ----------------------------
# JOIN DATA
# ----------------------------
gdf = gdf.merge(
    eur_m2,
    left_on="OB_UIME",
    right_on="obcina",
    how="left"
)

# ----------------------------
# CHECK FOR MISSING MUNICIPALITIES
# ----------------------------
missing = gdf[gdf["eur_m2"].isna()]["OB_UIME"]
if len(missing) > 0:
    print("Municipalities without price data:")
    print(missing.tolist())

# ----------------------------
# EXPORT RESULT
# ----------------------------
gdf.to_file(output_path, driver="GeoJSON")

print("GeoJSON created:", output_path)