from matplotlib import pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from modules.YTDownloader import YoutubeScrapper as YTD
import librosa 
import os
import numpy as np
from sklearn.preprocessing import StandardScaler 
from sklearn.decomposition import PCA
from sklearn.svc import SVC
SAMPLE_RATE = 44100
class Analyzer:
    
    def __init__(self, data, label_reference, output_path, num_cols):
        self.num_cols = num_cols
        self.output_path = output_path
        self.training_data = data
        self.label_reference = label_reference
        self.moods_list = self.training_data["training_labels"].tolist()
        self.training_data_raw = self.training_data.drop(["titles", "training_labels", "hash", "Unnamed: 0"], axis = 1)
        self.predict = {
            "KNN": predictKNN,
        }

    def analyze(self, raw_data):
        return self.extrapolate_features(raw_data = raw_data)

    def extrapolate_features(self, raw_data):
        print("Analyzing raw data...")
        data = librosa.feature.chroma_cqt(y=raw_data, sr=SAMPLE_RATE, fmin=80, n_chroma=self.num_cols, n_octaves = 6, bins_per_octave=96)
        
        fig, ax = plt.subplots(nrows=2, sharex=True)
        img = librosa.display.specshow(librosa.amplitude_to_db(np.abs(librosa.stft(raw_data)), ref=np.max),
                                    y_axis='log', x_axis='time', ax=ax[0])
        fig.colorbar(img, ax=[ax[0]])
        ax[0].label_outer()
        img = librosa.display.specshow(data, y_axis='chroma', x_axis='time', ax=ax[1])
        fig.colorbar(img, ax=[ax[1]])
        plt.show()

        local_average_v = [[] for _ in range(self.num_cols)]
        local_average_p = [[] for _ in range(self.num_cols)]
        local_n = [[] for _ in range(self.num_cols)]
        i = 0

        for keys in data:
            n = 0
            total_n = 0
            prev = keys[0]
            for instances in keys:
                total_n += 1
                if n == 1 :
                    prev = (keys[n] - prev)
                elif n > 1 :
                    prev += (keys[n] - keys[n - 1])
                if instances >= 0.5:
                    n += 1
            
            local_average_v[i].append(pow(prev/(keys.size - 1), 2))
            local_average_p[i].append(np.average(keys))
            local_n[i].append(n/total_n)
            i += 1

            if abs(prev/(keys.size - 1)) == 0.0 and np.average(keys) == 0.0 and n == 0.0:
                return 0
            for value in [abs(prev/(keys.size - 1)), np.average(keys), n]:
                if np.isnan(value) or np.isinf(value):
                    return 0
        
        tempo = librosa.feature.tempo(y=raw_data, sr=SAMPLE_RATE)
        d = {}
        d["tempos"] = tempo
        KEYS = [str(i) for i in range(self.num_cols)]

        for j in range(self.num_cols):
            d[KEYS[j] + "_AP"] = local_average_p[j]
            d[KEYS[j] + "_NI"] = local_n[j] 
            d[KEYS[j] + "_AV"] = local_average_v[j]


        df = pd.DataFrame(data=d)
        print(df)
        print("Finished analyzing raw data...")
        return df
    
def predictKNN(self, features, nearest_neighbor, pca_dim):

    print("Predicting... with: ")
    print("Nearest neighbor = ", nearest_neighbor)
    self.training_data_raw = self.training_data_raw.append(features, ignore_index=True)
    print("Added song to raw data DataFrame.")
    scalar = StandardScaler()
    scaled_df = pd.DataFrame(scalar.fit_transform(self.training_data_raw))
    print("Normalized DataFrame.")
    pca = PCA(n_components = pca_dim)
    pca.fit(scaled_df)
    pca_df = pca.transform(scaled_df)
    print("Applied principle component analysis to DataFrame.")
    df = pd.DataFrame(pca_df,columns=[ "PC" + str(i) for i in range(pca_dim)])
    Tree = KNeighborsClassifier(n_neighbors= nearest_neighbor)
    print("Build nearest Neighbor Tree.")
    Tree.fit(df.iloc[:len(self.moods_list)], self.moods_list)
    enum_value = Tree.predict([df.iloc[len(self.moods_list)].to_numpy()])[0]
    print("Applied Nearest Neighbor Search.")
    label =  self.label_reference[enum_value]
    color = label["color"]
    mood = label["mood"]
    prediction = {
        "enum_value" : enum_value,
        "mood" : mood,
        "color" : {
            "rgb" : color,
            "hex" : '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2]) 
        }
    }
    print("Prediction: ", prediction)
    return prediction