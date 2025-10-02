import pandas as pd
import housing as h


df = h.update_CSV()
if h.search_name():
    df = df[df["Owned Name"] == h.USER]
    print(f"\n{h.USER} Last Login Date was: {df['Last Login Date'].to_list()[0]}")