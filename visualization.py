import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA


def visualize_clusters(file_name, cluster_column, title, output_file):

    print(f"\n{title} grafiği oluşturuluyor...")

    df = pd.read_excel(file_name)

    # Transaction bazlı grupla
    transactions = (
        df.groupby("TransactionID")
        .agg({
            "Message": lambda x: " ".join(x),
            cluster_column: "first"
        })
        .reset_index()
    )

    vectorizer = TfidfVectorizer()

    X = vectorizer.fit_transform(transactions["Message"])

    pca = PCA(n_components=2)

    X_pca = pca.fit_transform(X.toarray())

    plt.figure(figsize=(8, 6))

    scatter = plt.scatter(
        X_pca[:, 0],
        X_pca[:, 1],
        c=transactions[cluster_column],
        s=50,
        alpha=0.7
    )

    plt.colorbar(scatter, label="Cluster")

    plt.title(title)

    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")

    plt.savefig(output_file)

    plt.show()

    print(f"{output_file} oluşturuldu.")


def visualize_kmeans():
    visualize_clusters(
        "logs_kmeans.xlsx",
        "KMeans_Cluster",
        "K-Means Transaction Clustering",
        "kmeans_graph.png"
    )


def visualize_dbscan():
    visualize_clusters(
        "logs_dbscan.xlsx",
        "DBSCAN_Cluster",
        "DBSCAN Transaction Clustering",
        "dbscan_graph.png"
    )


if __name__ == "__main__":
    visualize_kmeans()
    visualize_dbscan()