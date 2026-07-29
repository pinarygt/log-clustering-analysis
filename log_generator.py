import pandas as pd
import random
from faker import Faker
from datetime import timedelta

fake = Faker()

# POS Terminalleri
terminals = [
    "POS-01",
    "POS-02",
    "POS-03",
    "POS-04",
    "POS-05"
]

# Kasiyerler
cashiers = [
    "Cashier-1",
    "Cashier-2",
    "Cashier-3",
    "Cashier-4",
    "Cashier-5"
]

# Senaryolar
# Senaryolar
scenarios = [

    # 1 - Başarılı Chip Kart Ödemesi
    [
        "User Login",
        "Payment Started",
        "Card Inserted",
        "PIN Verified",
        "Payment Approved",
        "Receipt Printed",
        "User Logout"
    ],

    # 2 - Temassız (NFC) Ödeme
    [
        "User Login",
        "Payment Started",
        "NFC Card Detected",
        "Payment Approved",
        "Receipt Printed",
        "User Logout"
    ],

    # 3 - QR Kod ile Ödeme
    [
        "User Login",
        "Payment Started",
        "QR Code Scanned",
        "Payment Approved",
        "Receipt Printed",
        "User Logout"
    ],

    # 4 - Manyetik Kart
    [
        "User Login",
        "Payment Started",
        "Magnetic Card Read",
        "Payment Approved",
        "Receipt Printed",
        "User Logout"
    ],

    # 5 - Yanlış PIN
    [
        "User Login",
        "Payment Started",
        "Card Inserted",
        "Wrong PIN",
        "Payment Failed",
        "User Logout"
    ],

    # 6 - Kart Süresi Dolmuş
    [
        "User Login",
        "Payment Started",
        "Card Expired",
        "Payment Failed"
    ],

    # 7 - Kart Bloke
    [
        "User Login",
        "Payment Started",
        "Card Blocked",
        "Payment Failed"
    ],

    # 8 - Yetersiz Bakiye
    [
        "User Login",
        "Payment Started",
        "Insufficient Balance",
        "Payment Failed"
    ],

    # 9 - Bağlantı Koptu
    [
        "User Login",
        "Payment Started",
        "Connection Lost",
        "Payment Failed"
    ],

    # 10 - API Timeout
    [
        "User Login",
        "Payment Started",
        "API Timeout",
        "Payment Failed"
    ],

    # 11 - Database Timeout
    [
        "User Login",
        "Payment Started",
        "Database Timeout",
        "Payment Failed"
    ],

    # 12 - Yazıcı Kağıdı Bitti
    [
        "User Login",
        "Payment Started",
        "Payment Approved",
        "Paper Empty",
        "Receipt Failed",
        "User Logout"
    ],

    # 13 - Yazıcı Çevrimdışı
    [
        "User Login",
        "Payment Started",
        "Payment Approved",
        "Printer Offline",
        "Receipt Failed"
    ],

    # 14 - Kart Okunamadı
    [
        "User Login",
        "Payment Started",
        "Card Read Error",
        "Payment Failed"
    ],

    # 15 - İade İşlemi
    [
        "User Login",
        "Refund Started",
        "Refund Approved",
        "Receipt Printed",
        "User Logout"
    ],

    # 16 - İade Başarısız
    [
        "User Login",
        "Refund Started",
        "Refund Failed",
        "User Logout"
    ],

    # 17 - Bakiye Sorgulama
    [
        "User Login",
        "Balance Inquiry",
        "Card Inserted",
        "Balance Displayed",
        "User Logout"
    ],

    # 18 - Gün Sonu İşlemi
    [
        "User Login",
        "Daily Closing Started",
        "Batch Uploaded",
        "Daily Closing Completed",
        "User Logout"
    ],

    # 19 - Terminal Offline
    [
        "Terminal Offline",
        "Connection Retry",
        "Terminal Restarted"
    ],

    # 20 - İşlem İptal
    [
        "User Login",
        "Payment Started",
        "Customer Cancelled",
        "Transaction Cancelled",
        "User Logout"
    ],

    # 21 - Manuel Kart Girişi
    [
        "User Login",
        "Payment Started",
        "Manual Card Entry",
        "Payment Approved",
        "Receipt Printed",
        "User Logout"
    ],

    # 22 - Sadakat Puanı Kullanıldı
    [
        "User Login",
        "Payment Started",
        "Card Inserted",
        "Loyalty Points Applied",
        "Payment Approved",
        "Receipt Printed",
        "User Logout"
    ],

    # 23 - Taksitli Satış
    [
        "User Login",
        "Payment Started",
        "Installment Selected",
        "Payment Approved",
        "Receipt Printed",
        "User Logout"
    ],

    # 24 - Kasiyer Oturumu Zaman Aşımı
    [
        "User Login",
        "Session Timeout",
        "User Logout"
    ],

    # 25 - Güncelleme Sonrası Yeniden Başlatma
    [
        "Software Update Started",
        "Software Update Completed",
        "Terminal Restarted"
    ]
]

# Rastgele eklenecek ek loglar
extra_logs = [
    "SMS Sent",
    "Email Receipt Sent",
    "Inventory Updated",
    "Fraud Check Passed",
    "Customer Notified",
    "Transaction Archived",
    "Loyalty Points Added",
    "Campaign Applied",
    "Tax Calculated",
    "Bank Response Received"
]

logs = []

transaction_id = 1000

for i in range(250):

    transaction_id += 1

    scenario = random.choice(scenarios)

    terminal = random.choice(terminals)

    cashier = random.choice(cashiers)

    current_time = fake.date_time_this_year()

    for message in scenario:

        if (
            "Error" in message
            or "Failed" in message
            or "Timeout" in message
            or "Lost" in message
        ):
            level = "ERROR"

        elif "Slow" in message:
            level = "WARNING"

        else:
            level = "INFO"

        logs.append({

            "TransactionID": transaction_id,

            "Timestamp": current_time,

            "Terminal": terminal,

            "Cashier": cashier,

            "Level": level,

            "Message": message

        })

        current_time += timedelta(seconds=random.randint(2,6))

def generate_logs():

    scenario = random.choice(scenarios)

        # Senaryonun kopyasını oluştur
    transaction_logs = scenario.copy()

        # %60 ihtimalle 1 ek log
    if random.random() < 0.60:
            position = random.randint(1, len(transaction_logs)-1)
            transaction_logs.insert(
                position,
                random.choice(extra_logs)
            )

        # %30 ihtimalle ikinci ek log
    if random.random() < 0.30:
            position = random.randint(1, len(transaction_logs)-1)
            transaction_logs.insert(
                position,
                random.choice(extra_logs)
            )

    terminal = random.choice(terminals)

    cashier = random.choice(cashiers)

    current_time = fake.date_time_this_year()

    for message in transaction_logs:

        if any(word in message for word in [
            "Error",
            "Failed",
            "Timeout",
            "Lost",
            "Expired",
            "Blocked",
            "Offline"
        ]):
            level = "ERROR"

        elif any(word in message for word in [
                        "Retry",
                        "Warning",
                        "Slow",
                        "Cancelled"
                    ]):
            level = "WARNING"

        else:
            level = "INFO"

            logs.append({

                "TransactionID": transaction_id,
                "Timestamp": current_time,
                "Terminal": terminal,
                "Cashier": cashier,
                "Level": level,
                "Message": message

            })

            current_time += timedelta(seconds=random.randint(2,6))

    df = pd.DataFrame(logs)

    df = df.sort_values("Timestamp")

    df.to_excel("logs.xlsx", index=False)

    print(f"{len(df)} adet log oluşturuldu.")
    print("logs.xlsx oluşturuldu.")

    if __name__ == "__main__":
        generate_logs()