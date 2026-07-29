import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def elbow_method():

    print("Elbow Method çalışıyor...")

    df = pd.read_excel("logs.xlsx")

    transactions = (
        df.groupby("TransactionID")["Message"]
        .apply(lambda x: " ".join(x))
        .reset_index()
    )

    vectorizer = TfidfVectorizer()

    X = vectorizer.fit_transform(transactions["Message"])

    wcss = []

    for k in range(1, 11):

        kmeans = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        kmeans.fit(X)

        wcss.append(kmeans.inertia_)

    plt.figure(figsize=(8,5))

    plt.plot(range(1,11), wcss, marker="o")

    plt.title("Elbow Method")

    plt.xlabel("K Değeri")

    plt.ylabel("WCSS")

    plt.grid(True)

    plt.savefig("elbow_method.png")

    plt.show()


if __name__ == "__main__":
    elbow_method()