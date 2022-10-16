import pandas as pd
import numpy as np

data=pd.read_excel("data.xlsx")
X=data.loc[:,["A"]].to_numpy().reshape((1, data.shape[0]))
Y=data.loc[:,["B"]].to_numpy()

for ele in X:
    print(ele, end=" ")
#print(X.shape())
