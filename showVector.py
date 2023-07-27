import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
from matplotlib.font_manager import FontProperties
matplotlib.rcParams['axes.unicode_minus'] = False  # Solve the problem that minus sign '-' is displayed as a square


# Load the title vectors
title_vectors = np.load('title_vectors.npy')

# Check if title_vectors has a third dimension, if not, raise an error
if title_vectors.shape[1] < 3:
    raise ValueError("title_vectors needs to have at least 3 dimensions for a 3D plot.")

# Load the original data (titles)
data = pd.read_excel('phone2.xlsx', engine='openpyxl')

# Create a 3D scatter plot of the title vectors
fig = plt.figure(figsize=(20, 20))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(title_vectors[:, 0], title_vectors[:, 1], title_vectors[:, 2])

# Set the font properties to SimHei
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)

# Use the font properties in the annotate function
for i, title in enumerate(data['title']):
    ax.text(title_vectors[i, 0], title_vectors[i, 1], title_vectors[i, 2], title, fontproperties=font)

# Show the plot using Streamlit
st.pyplot(fig)
