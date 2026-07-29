from log_generator import generate_logs
from clustering import run_kmeans
from dbscan import run_dbscan
from compare import compare_results
from visualization import visualize_kmeans, visualize_dbscan
from report import generate_report


def main():

    print("=" * 50)
    print("SMART LOG ANALYZER")
    print("=" * 50)

    print("\n1) Loglar oluşturuluyor...")
    generate_logs()

    print("\n2) K-Means çalışıyor...")
    run_kmeans()

    print("\n3) DBSCAN çalışıyor...")
    run_dbscan()

    print("\n4) Sonuçlar karşılaştırılıyor...")
    compare_results()

    print("\n5) K-Means grafiği oluşturuluyor...")
    visualize_kmeans()
    
    print("\n6) DBSCAN grafiği oluşturuluyor...")
    visualize_dbscan()

    print("\n7) Analiz raporu hazırlanıyor...")
    generate_report()

    print("\n" + "=" * 50)
    print("PROJE BAŞARIYLA TAMAMLANDI")
    print("=" * 50)


if __name__ == "__main__":
    main()