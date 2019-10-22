# %%
test="test now "

# %%
print(test)

# %%
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

x = np.linspace(0, 20, 100)
plt.plot(x, np.sin(x))
plt.show()

# %%
y = np.linspace(0, 20, 100)
plt.plot(y, np.cos(y))
plt.show()

# %%
import pandas as pd 
data = pd.read_csv("/Users/~~/Desktop/IRIS.csv")
data.head()

# %%
a_array = np.array([1,2,3])
b_array = np.array([4,5,6])

print(a_array+b_array)