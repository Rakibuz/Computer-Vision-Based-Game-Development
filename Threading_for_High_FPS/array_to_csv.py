import numpy as np
import csv
import pandas as pd
from pprint import pprint

df = pd.read_csv('./Threading_for_High_FPS/Encoded.csv', delimiter=',',header=None)

list_of_csv = [list(row) for row in df.values]

print(list_of_csv)




# with open('./Threading_for_High_FPS/Encoded.csv', newline='') as file:
#     reader = csv.reader(file)
#     res = list(map(tuple, reader))

# pprint(res)