import pandas as pd
import os
import housing as h

df = h.update_CSV()

print(df.columns)

df.query(input("What is the query?\n>")).head(200).to_csv("Queryoutput.csv",index=False)