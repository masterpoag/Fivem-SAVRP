import pandas as pd
import os
import housing as h

df = h.update_CSV()

h.autocorrect_name

if h.search_name(pd.read_csv(h.HOUSING_FILE)["House Name"].to_list()):
    df = df[df["House Name"] == h.USER]

price = float(df["Total Value or Daily Rent Price"].sum().replace(",","").replace("$",""))
downpayment = float(df["Downpayment"].sum().replace(",","").replace("$",""))

def payment_options(price: float, downpayment: float, interest: float, weeks: int):
    total = price * (interest)
    weekly = (total - downpayment) / weeks
    return f"- {weeks} Weeks Total: {total:,.2f} | Per Week: {weekly:,.2f}"
    


print(f""" Base Price: {price:,.2f} | Downpayment: {downpayment:,.2f}
{payment_options(price, downpayment, 1.01, 4)}
{payment_options(price, downpayment, 1.03, 8)}
{payment_options(price, downpayment, 1.05, 12)}
{payment_options(price, downpayment, 1.07, 16)}""")