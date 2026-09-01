import matplotlib.pyplot as plt
from AsteroidData import CollectAsteroidData
import streamlit as st
from datetime import timedelta, date
import matplotlib

matplotlib.use("TkAgg")  
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

API_KEY = st.secrets["nasa_key"]
today = date.today()
next_days = today + timedelta(days=3)

class PlotNewPoint:
    def __init__(self):
        self.kmeans = joblib.load("kmeans_modelv3.joblib")
        self.X_pca = joblib.load("training_x_pcav2.joblib")
        
    def plot_new_point(self, asteroid_name):
        collect_asteroid_data = CollectAsteroidData(today=today, next_days=next_days, API_KEY=API_KEY)

        cluster = collect_asteroid_data.get_asteroid_cluster_group(asteroid_name).get("Cluster")
        point = collect_asteroid_data.get_asteroid_cluster_group(asteroid_name).get("point")

        fig, ax = plt.subplots(figsize=(8, 6))

        sns.scatterplot(x=self.X_pca[:, 0], y=self.X_pca[:, 1], hue=self.kmeans.labels_, palette="viridis", alpha=0.5, ax=ax)

        centers = self.kmeans.cluster_centers_

        ax.scatter(
            centers[:, 0], 
            centers[:, 1], 
            color='black',       
            marker='x',          
            s=250,               
            linewidths=4,        
            label='Centroids'    
        )

        ax.scatter(
            point[0, 0],
            point[0, 1],
            c=[cluster],
            cmap="viridis",
            s=300,
            marker="*",
            edgecolor="black",
            linewidth=2,
            label=f"New Point (Cluster {cluster})",
        )

        ax.legend()
        return fig 



    