import pandas as pd
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
import os
from reportlab.platypus import PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(
    TTFont(
        "Arial",
        r"C:\Windows\Fonts\arial.ttf"
    )
)

def generate_report():

    print("\nRapor hazırlanıyor...")

    logs = pd.read_excel("logs.xlsx")
    kmeans = pd.read_excel("logs_kmeans.xlsx")
    dbscan = pd.read_excel("logs_dbscan.xlsx")

# =============================
# Genel Bilgiler
# =============================

    total_logs = len(logs)
    total_transactions = logs["TransactionID"].nunique()

    transaction_result = logs.groupby("TransactionID")["Message"].apply(list)


    success_transactions = 0
    failed_transactions = 0
    other_transactions = 0

    for messages in transaction_result:

        if any(
            "Payment Approved" in m or
            "Refund Approved" in m
            for m in messages
        ):
            success_transactions += 1

        elif any(
            "Failed" in m
            for m in messages
        ):
            failed_transactions += 1

        else:
            other_transactions += 1

        payment_transactions = (
        success_transactions + failed_transactions
    )

    success_rate = (
        success_transactions / payment_transactions
    ) * 100

    failed_rate = (
        failed_transactions / payment_transactions
    ) * 100

    # =============================
    # En Sık Hatalar
    # =============================

    error_messages = logs[
        logs["Level"] == "ERROR"
    ]

    ignore = [
        "Payment Failed",
        "Receipt Failed",
        "Refund Failed"
        ]

    top_errors = (
            error_messages[
                ~error_messages["Message"].isin(ignore)
            ]["Message"]
            .value_counts()
            .head(5)
            )

    # =============================
    # En Problemli Terminal
    # =============================

    terminal_errors = (
        error_messages.groupby("Terminal")
        .size()
        .sort_values(ascending=False)
    )

    # =============================
    # En Problemli Kasiyer
    # =============================

    cashier_errors = (
        error_messages.groupby("Cashier")
        .size()
        .sort_values(ascending=False)
    )

    # =============================
    # KMeans
    # =============================

    kmeans_cluster_count = (
        kmeans["KMeans_Cluster"]
        .nunique()
    )

    # =============================
    # DBSCAN
    # =============================

    labels = dbscan["DBSCAN_Cluster"]

    # -1 (noise) hariç gerçek küme sayısı
    dbscan_cluster_count = len(set(labels) - {-1})

    # Noise sayısı
    noise_count = (labels == -1).sum()

    # =============================
    # RAPOR
    # =============================

    styles = getSampleStyleSheet()
    styles["BodyText"].fontName = "Arial"
    styles["Heading1"].fontName = "Arial"
    styles["Heading2"].fontName = "Arial"

    pdf = SimpleDocTemplate("Smart_Log_Analyzer_Report.pdf")

    story = []

    title = styles["Heading1"]
    title.alignment = TA_CENTER

    story.append(
        Paragraph(
            "SMART LOG ANALYZER REPORT",
            title
        )
    )


    story.append(
        Paragraph(
            f"<b>Total Transactions:</b> {total_transactions}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Total Logs:</b> {total_logs}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Successful Transactions:</b> {success_transactions}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Failed Transactions:</b> {failed_transactions}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>System Transactions:</b> {other_transactions}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Success Rate:</b> %{success_rate:.2f}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Failure Rate:</b> %{failed_rate:.2f}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))


    print("\n")
    print("=" * 55)
    print("SMART LOG ANALYZER RAPORU")
    print("=" * 55)

    print(f"\nToplam Transaction : {total_transactions}")
    print(f"Toplam Log         : {total_logs}")

    print(f"\nBaşarılı İşlem     : {success_transactions}")
    print(f"Başarısız İşlem    : {failed_transactions}")
    print(f"Diğer İşlemler     : {other_transactions}")

    print(f"\nBaşarı Oranı       : %{success_rate:.2f}")
    print(f"Hata Oranı         : %{failed_rate:.2f}")

    print("\n" + "-" * 55)
    print("EN SIK GÖRÜLEN HATALAR")
    print("-" * 55)

    story.append(Paragraph("<b>Most Frequent Errors</b>", styles["Heading2"]))

    for error, count in top_errors.items():
        story.append(
            Paragraph(f"{error} : {count}", styles["BodyText"])
        )

    story.append(Spacer(1, 15))

    for error, count in top_errors.items():
        print(f"{error:<30} {count}")

    story.append(
    Paragraph(
        "<b>Most Problematic Terminals</b>",
        styles["Heading2"]
    )
)

    for terminal, count in terminal_errors.head().items():
        story.append(
            Paragraph(
                f"{terminal} : {count}",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1,15))

    print("\n" + "-" * 55)
    print("EN PROBLEMLİ TERMİNALLER")
    print("-" * 55)

    for terminal, count in terminal_errors.head().items():
        print(f"{terminal:<10} {count}")

    story.append(
    Paragraph(
        "<b>Most Problematic Cashiers</b>",
        styles["Heading2"]
    )
)

    for cashier, count in cashier_errors.head().items():
        story.append(
            Paragraph(
                f"{cashier} : {count}",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1,15))

    story.append(
    Paragraph(
        "<b>Clustering Summary</b>",
        styles["Heading2"]
    )
    )

    story.append(
        Paragraph(
            f"KMeans Cluster Count : {kmeans_cluster_count}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"DBSCAN Cluster Count : {dbscan_cluster_count}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"DBSCAN Noise : {noise_count}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1,15))
    
    print("\n" + "-" * 55)
    print("EN PROBLEMLİ KASİYERLER")
    print("-" * 55)

    for cashier, count in cashier_errors.head().items():
        print(f"{cashier:<10} {count}")

    print("\n" + "-" * 55)
    print("KÜMELEME ÖZETİ")
    print("-" * 55)

    print(f"KMeans Küme Sayısı : {kmeans_cluster_count}")

    print(f"DBSCAN Küme Sayısı : {dbscan_cluster_count}")

    print(f"DBSCAN Noise       : {noise_count}")

    print("\n" + "-" * 55)
    print("OTOMATİK YORUM")
    print("-" * 55)

    if len(top_errors) > 0:
        print(f"• En sık görülen hata: {top_errors.index[0]}")

    print(f"• En problemli terminal: {terminal_errors.idxmax()}")

    print(f"• En problemli kasiyer: {cashier_errors.idxmax()}")

    if success_rate > 80:
        print("• İşlem başarı oranı oldukça yüksek.")

    elif success_rate > 60:
        print("• İşlem başarı oranı orta seviyede.")

    else:
        print("• İşlem başarı oranı düşük, sistem incelenmelidir.")

    story.append(PageBreak())
    

    if os.path.exists("kmeans_graph.png"):
        story.append(Image("kmeans_graph.png", width=400, height=300))
        story.append(Spacer(1, 15))

    story.append(Paragraph("<b>K-Means Analysis</b>", styles["Heading2"]))
    story.append(Spacer(1, 8))

    kmeans_text = """
    K-Means algoritması, POS işlem loglarını benzer özelliklerine göre 4 farklı kümeye ayırmıştır.
    Grafikte görüldüğü üzere işlemlerin büyük bir kısmı tek bir kümede toplanmıştır.
    Bu durum, oluşturulan logların çoğunun benzer işlem adımlarına sahip olduğunu göstermektedir.
    Daha küçük kümeler ise bağlantı kopması (Connection Lost), zaman aşımı (Timeout)
    ve kart okuma hatası (Card Read Error) gibi farklı davranış sergileyen işlem
    gruplarını temsil etmektedir.
    K-Means algoritması her veriyi mutlaka bir kümeye atadığı için veri setinde
    sınıflandırılmamış bir kayıt bulunmamaktadır.
    Bu nedenle genel işlem dağılımını görmek için başarılı sonuçlar vermiştir.
    """

    story.append(Paragraph(kmeans_text, styles["BodyText"]))

    story.append(Spacer(1,20))
    
    if os.path.exists("elbow_method.png"):
            story.append(Image("elbow_method.png", width=400, height=300))
            story.append(Spacer(1, 15))
    
    story.append(Paragraph("<b>Elbow Method Analysis</b>", styles["Heading2"]))
    story.append(Spacer(1, 8))
    
    story.append(
                Paragraph(
                    """
                    Elbow Method, K-Means algoritması için en uygun küme sayısını belirlemek amacıyla
                    kullanılmıştır. Grafikte yatay eksen küme sayısını (K), dikey eksen ise WCSS
                    (Within Cluster Sum of Squares) değerini göstermektedir. Küme sayısı arttıkça
                    WCSS değeri azalmakta, ancak belirli bir noktadan sonra bu azalma yavaşlamaktadır.
                    Grafikte oluşan "dirsek (elbow)" noktası en uygun küme sayısını göstermektedir.
                    Bu projede dirsek noktası yaklaşık olarak K=4 civarında oluştuğu için K-Means
                    algoritmasında 4 küme kullanılmıştır. Böylece hem benzer işlem kayıtları başarılı
                    şekilde gruplanmış hem de gereğinden fazla küme oluşturulması önlenmiştir.
                    """,
                    styles["BodyText"]
                )
            )

    story.append(Spacer(1,20))

    story.append(PageBreak())

    if os.path.exists("dbscan_graph.png"):
        story.append(Image("dbscan_graph.png", width=400, height=300))
        story.append(Spacer(1, 15))

        story.append(Paragraph("<b>DBSCAN Analysis</b>", styles["Heading2"]))
    story.append(Spacer(1,8))

    story.append(
        Paragraph(
            """
            DBSCAN algoritması, K-Means'ten farklı olarak küme sayısını önceden belirlemeye ihtiyaç
            duymaz ve kümeleri veri yoğunluğuna göre oluşturur. Bu çalışmada işlemlerin büyük bölümü
            yoğun bir küme içerisinde yer alırken, farklı özellik gösteren bazı işlemler daha küçük
            kümeler oluşturmuştur. Veri setinde gürültü (noise) oluşmamasının nedeni, logların belirli
            senaryolara göre oluşturulmuş olması ve birbirlerine oldukça benzer yapıda bulunmalarıdır.
            Gerçek sistem loglarında ise DBSCAN algoritması aykırı davranışları ve beklenmeyen hataları
            tespit etmede daha başarılı sonuçlar verebilir.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1,20))

    story.append(Paragraph("<b>Algorithm Comparison</b>", styles["Heading2"]))
    story.append(Spacer(1,8))

    story.append(
        Paragraph(
            """
            Her iki kümeleme algoritması da benzer işlem kayıtlarını başarılı şekilde gruplandırmıştır.
            K-Means algoritması daha az sayıda ve daha büyük kümeler oluşturarak sonuçların daha kolay
            yorumlanmasını sağlamıştır. DBSCAN ise veri yoğunluğunu esas aldığı için daha esnek bir
            kümeleme yapısı sunmuş ve küme sayısını otomatik olarak belirlemiştir. Bu proje kapsamında
            kullanılan düzenli ve senaryoya dayalı log verilerinde K-Means daha anlaşılır sonuçlar
            üretirken, gerçek sistemlerden elde edilen düzensiz log verilerinde DBSCAN algoritmasının
            daha avantajlı olacağı değerlendirilmektedir.
            """,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())

    story.append(Paragraph("<b>Conclusion</b>", styles["Heading2"]))
    story.append(Spacer(1,8))
    
    story.append(
            Paragraph(
                """
                Bu proje kapsamında oluşturulan POS işlem logları üzerinde K-Means ve DBSCAN kümeleme
                algoritmaları uygulanmış ve elde edilen sonuçlar karşılaştırılmıştır. Her iki algoritma da
                benzer özellikteki işlem kayıtlarını başarılı şekilde gruplandırmıştır. K-Means algoritması
                genel işlem dağılımını daha anlaşılır biçimde gösterirken, DBSCAN algoritması veri
                yoğunluğunu dikkate alarak daha esnek bir kümeleme gerçekleştirmiştir. Elde edilen
                sonuçlar, kümeleme algoritmalarının POS loglarının analiz edilmesi, hata örüntülerinin
                belirlenmesi ve sistem davranışlarının incelenmesi amacıyla etkili bir şekilde
                kullanılabileceğini göstermektedir.
                """,
                styles["BodyText"]
            )
        )
    

    pdf.build(story)

    print("Smart_Log_Analyzer_Report.pdf oluşturuldu.")

    print("\nRapor tamamlandı.")


if __name__ == "__main__":
    generate_report()