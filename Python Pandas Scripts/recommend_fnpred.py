from __future__ import print_function

import argparse
import os
from turtle import st
import pandas as pd
import numpy as np

from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing
from sklearn.externals import joblib

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--n_neighbors', type=int,
                        default=10)
    parser.add_argument('--metric', type=str,
                        default="manhattan")
    parser.add_argument('--algorithm', type=str,
                        default="brute")

    parser.add_argument('--output-data-dir', type=str,
                        default=os.environ["SM_OUTPUT_DATA_DIR"])
    parser.add_argument('--model-dir', type=str,
                        default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--train', type=str,
                        default=os.environ["SM_CHANNEL_TRAIN"])

    args = parser.parse_args()

    file = os.path.join(args.train, "rsmall.parquet.gzip")
    df = pd.read_parquet(file, engine="pyarrow")

    animes_pivot = df.pivot_table(columns="user_id", index="English name", values="rating")
    animes_pivot.fillna(0, inplace=True)

    from scipy.sparse import csr_matrix
    animes_sparse = csr_matrix(animes_pivot)

    n_neighbors = args.n_neighbors
    metric = args.metric
    algorithm = args.algorithm

    knn_model = NearestNeighbors(algorithm=algorithm, n_neighbors=n_neighbors)
    knn_model.fit(animes_sparse)

    print("Model has been fitted")

    joblib.dump(knn_model, os.path.join(args.model_dir, "model.joblib"))


def model_fn(model_dir):
    knn_model = joblib.load(os.path.join(model_dir, "model.joblib"))
    return knn_model

def predict_fn(input_data, model):
    distance, suggestions = model.kneighbors(input_data.reshape(1, -1))
    return suggestions
