import math
from itertools import tee

import googlemaps
import numpy as np
import pandas as pd
from geopy import distance

# Kaggle dataset from https://www.kaggle.com/nikitagrec/world-capitals-gps

df = pd.read_csv("worldCaps.csv")

names = df["CapitalName"].unique().tolist()

uniqueDf = df.copy()
uniqueDf = uniqueDf.drop_duplicates("CapitalName")
names = [str(elem) for elem in names]
names = [name for name in names if name != "nan"]

distMatrix = pd.DataFrame(index=names, columns=names)

for (i, row1) in uniqueDf.iterrows():
    if row1["CapitalName"] in names:

        LatOrigin = row1["CapitalLatitude"]
        LongOrigin = row1["CapitalLongitude"]
        origin = (LatOrigin, LongOrigin)

        for (j, row2) in uniqueDf.iterrows():
            if row2["CapitalName"] in names:
                if row1["CapitalName"] == row2["CapitalName"]:
                    distMatrix.at[row1["CapitalName"], row2["CapitalName"]] = 0
                else:
                    val = str(distMatrix.at[row1["CapitalName"], row2["CapitalName"]])
                    if val == "nan" or val == "NaN":

                        LatDestination = row2["CapitalLatitude"]
                        LongDestination = row2["CapitalLongitude"]

                        destination = (LatDestination, LongDestination)
                        geodesicDist = distance.distance(origin, destination).km
                        geodesicDist = math.pow(geodesicDist, 2)
                        geodesicDist = round(geodesicDist)

                        distMatrix.at[
                            row1["CapitalName"], row2["CapitalName"]
                        ] = geodesicDist
                        distMatrix.at[
                            row2["CapitalName"], row1["CapitalName"]
                        ] = geodesicDist

uniqueDf["cityCountry"] = uniqueDf["CapitalName"] + ", " + uniqueDf["CountryName"]


distMatrix.to_csv("distMatrixGeo.csv")
uniqueDf.to_csv("worldCapsInfo.csv")

print(distMatrix)
