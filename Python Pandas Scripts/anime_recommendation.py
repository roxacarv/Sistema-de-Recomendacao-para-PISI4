from matplotlib.font_manager import json_dump
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing

bucket = 'output/ratings_preprocessed_small_set_2.csv'
#ratings = pd.read_csv(bucket, encoding="latin-1")
ratings = pd.read_csv(bucket)
#ratings.to_json("ratings.json")
#r = ratings[["user_id", "English name", "rating"]]
ratings.to_parquet("rsmall.parquet.gzip", compression="gzip")
#r.to_parquet("r.parquet.gzip", compression="gzip")

animes_pivot = ratings.pivot_table(columns="user_id", index="English name", values="rating")
animes_pivot.fillna(0, inplace=True)

print(ratings.shape)

#animes_pivot.to_csv("pivot.csv")

#animes_pivot.to_parquet("pivot.parquet.gzip", compression="gzip")

from scipy.sparse import csr_matrix

animes_sparse = csr_matrix(animes_pivot)

# Usando métrica chebyshev
#knn_model = NearestNeighbors(algorithm="brute", n_neighbors=20)
#knn_model.fit(animes_pivot)

#animes_pivot_csv = pd.read_csv("./static/datasets/animes_pivot.csv")
import json
animes_names_index = list(dict(animes_pivot.iloc[:,0]).keys())
with open("names_index.json", "w") as f:
    json.dump(animes_names_index, f, indent=4)
#print(animes_names_index)

#distances_model, suggestions_model = knn_model.kneighbors(animes_pivot.iloc[0, :].values.reshape(1, -1))

#print(suggestions_model)