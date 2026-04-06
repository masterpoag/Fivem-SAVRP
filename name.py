import pandas as pd
import os
import housing as h

df = h.update_CSV()

print(h.temp(str(input("Search\n> "))))
