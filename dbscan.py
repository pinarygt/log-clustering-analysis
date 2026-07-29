import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN


def run_dbscan():

    print("\nDBSCAN çalıştırılıyor...")

    df = pd.read_excel("logs.xlsx")
    transactions = (
    df.groupby("TransactionID")["Message"]
    .apply(lambda x: " ".join(x))
    .reset_index()
    )

    vectorizer = TfidfVectorizer()

    X = vectorizer.fit_transform(transactions["Message"])

    from sklearn.cluster import DBSCAN

    for eps in [0.3, 0.5, 0.7, 0.9, 1.1]:
        dbscan = DBSCAN(
            eps=eps,
            min_samples=3
        )

        labels = dbscan.fit_predict(X)

        cluster_count = len(set(labels)) - (1 if -1 in labels else 0)
        noise_count = list(labels).count(-1)

        print(
            f"eps={eps} | Küme={cluster_count} | Noise={noise_count}"
        )

    transactions["DBSCAN_Cluster"] = dbscan.fit_predict(X)

    df = df.merge(
        transactions[
            ["TransactionID", "DBSCAN_Cluster"]
        ],
        on="TransactionID"
    )

    df.to_excel("logs_dbscan.xlsx", index=False)

    print("DBSCAN tamamlandı.")

    print("logs_dbscan.xlsx oluşturuldu.")

    print("\n========== DBSCAN KÜMELERİ ==========\n")

    for cluster in sorted(df["DBSCAN_Cluster"].unique()):

        print(f"\n--- Cluster {cluster} ---")

        messages = (
            df[df["DBSCAN_Cluster"] == cluster]["Message"]
            .drop_duplicates()
        )

        for message in messages:
            print(message)


if __name__ == "__main__":
    run_dbscan()
