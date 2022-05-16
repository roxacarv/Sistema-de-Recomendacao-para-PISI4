import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing

bucket='animes_with_reviews.csv'
animes_reviews_with = pd.read_csv(bucket, encoding="latin-1")
animes_reviews = pd.read_csv(bucket, encoding="latin-1")

animes_reviews = animes_reviews[["profile", "anime_uid", "user_score", "title", "genre", "aired", "episodes", "popularity", "score", "times_score"]]
# animes_reviews.to_csv("animes_with_reviews.csv")

final_reviews = animes_reviews[animes_reviews["times_score"] > 40]

final_reviews.drop_duplicates(["profile", "title"], inplace=True)

# Faz uma transposição do dataset, transformando os perfis em colunas
animes_transposition = final_reviews.pivot_table(columns="profile", index="title", values="user_score")
# Preenche os espaços contendo NaN com um float(0)
animes_transposition.fillna(0, inplace=True)

from scipy.sparse import csr_matrix

animes_sparse = csr_matrix(animes_transposition)

# Usando métrica chebyshev
knn_model = NearestNeighbors(algorithm="auto", metric="chebyshev", n_neighbors=10)
knn_model.fit(animes_transposition)

animes_names_index = list(dict(animes_transposition.iloc[:,-1]).keys())

def calculate_knn_distance(anime_index):
    distances_model, suggestions_model = knn_model.kneighbors(animes_transposition.iloc[anime_index, :].values.reshape(1, -1))
    for i in range(len(suggestions_model)):
        print(animes_transposition.index[suggestions_model[i]])

def get_recommended_animes(anime_name):
    if anime_name in animes_names_index:
        aindex = animes_names_index.index(anime_name)+2
        if aindex >= 0 and aindex <= len(animes_transposition):
            calculate_knn_distance(anime_index=aindex)
    else:
        print("There is no anime with that name")

get_recommended_animes(anime_name="Absolute Duo")