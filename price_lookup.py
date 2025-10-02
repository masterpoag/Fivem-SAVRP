import pandas as pd
import os
import housing as h

df = h.update_CSV()

h.autocorrect_name

if h.search_name(pd.read_csv(h.HOUSING_FILE)["House Name"].to_list()):
    df = df[df["House Name"] == h.USER]

price = float(df["Total Value or Daily Rent Price"].sum().replace(",","").replace("$",""))
downpayment = float(df["Downpayment"].sum().replace(",","").replace("$",""))


print(f""" Base Price: {price:,.2f} | Downpayment: {downpayment:,.2f}
- 4 Weeks Total: {(price*1.01):,.2f} | Per Week: {((price*1.01-downpayment)/4):,.2f}
- 8 Weeks Total: {(price*1.03):,.2f} | Per Week: {((price*1.03-downpayment)/8):,.2f}
- 12 Weeks Total: {(price*1.05):,.2f} | Per Week: {((price*1.05-downpayment)/12):,.2f}
- 16 Weeks Total: {(price*1.07):,.2f} | Per Week: {((price*1.07-downpayment)/16):,.2f}""")