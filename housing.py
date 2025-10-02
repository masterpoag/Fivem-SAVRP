import pandas as pd
import os
import requests
from fuzzywuzzy import process


HOUSING_FILE = "housing_list.csv"
GID = "350990051"
spreadsheet = "1_-vGokj0WeXfgWDNolNJsRMOjg6I0oVIx95iOxkliNw"
url = f"https://docs.google.com/spreadsheets/d/{spreadsheet}/export?format=csv&gid={GID}"

USER = ""

def update_CSV() -> pd.DataFrame: 
    """Updates the CSV using the spreedsheet url to download a new google sheets to HOUSING_FILE and returns the dataFrame of it."""
    response = requests.get(url)
    df = pd.DataFrame()
    if response.status_code == 200:
        with open(HOUSING_FILE, "wb") as f:
            f.write(response.content)
        df = pd.read_csv(HOUSING_FILE).query("`MLO/SHELL/IPL`.notna()")
        df.to_csv(HOUSING_FILE, index=False)
        print("Downloaded sheet.csv")
        return df
    else:
        print("Failed to download:", response.status_code)
        return None


def search_name(valid_names="") -> bool:
    """Searches for a name in the spreadsheet that the user requests if found stores it in USER"""
    global USER
    uInput = str(input("Search\n> "))
    USER = autocorrect_name(uInput) if valid_names == "" else autocorrect_name(uInput, valid_names=valid_names)
    if USER == "No Name Found":
        print("Either Does Exist or Name Was Badly Miss Typed")
        return False
    print("Searching for: " + USER)
    return True


def autocorrect_name(input_name, threshold=70, valid_names=None) -> str:
    """Trys to find the name given in the csv to autocorrect"""
    if valid_names is None:
        if not os.path.exists(HOUSING_FILE):
            print("Housing file not found.")
            return "No Results Found"
        valid_names = pd.read_csv(HOUSING_FILE)["Owned Name"].dropna().to_list()
    match, score = process.extractOne(input_name, valid_names)
    print(threshold)
    return match if score >= threshold else "No Results Found"



if __name__ == "__main__":
    df = update_CSV()
    print(f"Full Size: {len(df)}")
    unowned = df.query("`Owned Name`.isna()")
    print(f"Unowned Size: {len(unowned)}")
    own = unowned.query("`Rental/Mortgage` == 'Sale'")
    print(f"Buyable Size: {len(own)}")
    own.to_csv("output.csv",index=False)



