import numpy as np
import pandas as pd
import plotly.express as px

np.set_printoptions(threshold=np.inf)
import math
from itertools import tee

from geopy import distance

# Distance matrix and the dataset are imported
df = pd.read_csv("distMatrixGeo.csv", index_col=0)
worldcapsDf = pd.read_csv("worldCapsInfo.csv", index_col=0)

D = df.to_numpy()

n = df.shape[0]

ones = np.ones((n, n))

s = (
    D
    - ((1 / n) * D @ ones)
    - ((1 / n) * ones @ D)
    + ((1 / pow(n, 2)) * ones @ D @ ones)
)

s = -0.5 * s

m = 2
w, v = np.linalg.eig(s)

lambdaM = (-w).argsort()[:m]
print(
    lambdaM
)  # since 0 and 1 are the 2 largest eigenvalues these can be picked directly
print(w)

w = w[:2]
v = v.T[:2, :]

diagEigenV = np.diag(w)


Ut = v

I = np.eye(m, n)
X = np.sqrt(diagEigenV) @ Ut

worldcapsDf["Dim 1"] = X[0]
worldcapsDf["Dim 2"] = X[1]

fig = px.scatter(
    worldcapsDf, x="Dim 1", y="Dim 2", color="ContinentName", text="CapitalName"
)
fig.update_traces(marker_size=8, textposition="top center")
fig.show()

fig = px.scatter(
    worldcapsDf, x="Dim 1", y="Dim 2", color="ContinentName", text="CountryName"
)
fig.update_traces(marker_size=8, textposition="top center")
fig.show()

fig = px.scatter(
    worldcapsDf, x="Dim 1", y="Dim 2", color="ContinentName", text="cityCountry"
)
fig.update_traces(marker_size=8, textposition="top center")
fig.show()
