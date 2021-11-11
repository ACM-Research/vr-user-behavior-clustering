import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def linePlot(vidChunkData):
    
    title = 'Video Chunk Silhouette Score Comparison'

    # constructs data rows for each Video, Chunk in that video, silhouette score for that chunk
    df_dict = {'Video':[row['Video'] for row in vidChunkData], 'Chunks':[row['Chunks'] for row in vidChunkData],'Sil Score':[row['Sil Score'] for row in vidChunkData]}
    df = pd.DataFrame.from_dict(df_dict)
    
    print(df.head())

    # denotes x-axis as chunks, y-axis as sil-score, plots a line per each 'Video'
    linePlot = sns.lineplot(x='Chunks', y='Sil Score', hue='Video', data=df).set(title=title)
    plt.show()


def barGraph(rowData):
    df_dict = {'Algorithm': [row['Algorithm'] for row in rowData], 'Video Type':[row['Video Type'] for row in rowData], 'Sil Score': [row['Sil Score'] for row in rowData]}
    df = pd.DataFrame.from_dict(df_dict)
    print(df.head())
    # colors based on algorithm & y values are those algorithms silhouette score
    barG = sns.catplot(x="Video Type", y="Sil Score", hue="Algorithm", kind="bar", data=df)
    barG.fig.suptitle('Algorithm Silhouette Score Comparison') # provides title
    plt.show()

    # line below saves figure
    #barG.savefig('output.png')

# Data is presume, you can change for your own needs, although may require changing 
# implementation of methods above
rowData = [{'Algorithm':'BK','Video Type': 'No moving', "Sil Score":.95},
           {'Algorithm':'KM','Video Type': 'No moving', "Sil Score":.45},
           {'Algorithm':'DB','Video Type': 'No moving', "Sil Score":.75},
           {'Algorithm':'BK','Video Type': 'No moving', "Sil Score":.4},
           {'Algorithm':'BK','Video Type': 'Moving', "Sil Score": .4},
           {'Algorithm':'KM','Video Type': 'Moving', 'Sil Score':.5},
           {'Algorithm':'DB','Video Type': 'Moving', 'Sil Score':.66}]

vidChunkData = [{'Video':'1','Chunks': 1, "Sil Score":.95},
           {'Video':'1','Chunks':2, "Sil Score":.45},
           {'Video':'1','Chunks': 3, "Sil Score":.75},
           {'Video':'1','Chunks': 4, "Sil Score":.4},
           {'Video':'1','Chunks': 5, "Sil Score": .4},
           {'Video':'1','Chunks': 6, 'Sil Score':.5},
           {'Video':'1','Chunks': 7, 'Sil Score':.66},
           {'Video':'2','Chunks': 1, "Sil Score":-.45},
           {'Video':'2','Chunks':2, "Sil Score":.44},
           {'Video':'2','Chunks': 3, "Sil Score":.56},
           {'Video':'2','Chunks': 4, "Sil Score":.43},
           {'Video':'2','Chunks': 5, "Sil Score": .22},
           {'Video':'2','Chunks': 6, 'Sil Score':.88},
           {'Video':'2','Chunks': 7, 'Sil Score':.66}]

#barGraph(rowData)
#linePlot(vidChunkData)
