import pandas as pd
import os
import housing as h

df = h.update_CSV()

if h.search_name():
    df = df[df["Owned Name"] == h.USER]
    print(df.head(200))