import pandas as pd


def compare_results():

    print("\nKarşılaştırma hazırlanıyor...")

    kmeans = pd.read_excel("logs_kmeans.xlsx")

    dbscan = pd.read_excel("logs_dbscan.xlsx")

    result = kmeans.copy()

    result["DBSCAN_Cluster"] = dbscan["DBSCAN_Cluster"]

    result.to_excel("logs_compare.xlsx", index=False)

    print("logs_compare.xlsx oluşturuldu.")


if __name__ == "__main__":
    compare_results()