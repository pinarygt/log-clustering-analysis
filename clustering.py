import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def run_kmeans():

    print("\nK-Means çalıştırılıyor...")

    # Excel'i oku
    df = pd.read_excel("logs.xlsx")

        # Transaction bazlı grupla
    transactions = (
    df.groupby("TransactionID")["Message"]
    .apply(lambda x: " ".join(x))
    .reset_index()
    )

    print(f"\nToplam işlem sayısı: {len(transactions)}")

    print(transactions.head(10))
    print("Transaction sayısı:", len(transactions))
    # TF-IDF
    vectorizer = TfidfVectorizer()

    X = vectorizer.fit_transform(transactions["Message"])

    # K-Means
    kmeans = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    transactions["KMeans_Cluster"] = kmeans.fit_predict(X)
    result = df.merge(
        transactions[["TransactionID", "KMeans_Cluster"]],
        on="TransactionID"
    )

    result.to_excel("logs_kmeans.xlsx", index=False)

    print("K-Means tamamlandı.")
    print("logs_kmeans.xlsx oluşturuldu.")

    print("\n========== İŞLEM KÜMELERİ ==========\n")

    for cluster in sorted(transactions["KMeans_Cluster"].unique()):

        print(f"\n--- Cluster {cluster} ---")

        examples = transactions[
            transactions["KMeans_Cluster"] == cluster
        ]["Message"].head(3)

        for example in examples:
            print(example)
            print("-" * 50)


if __name__ == "__main__":
    run_kmeans()