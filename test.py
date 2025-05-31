import psycopg2

try:
    conn = psycopg2.connect(
        dbname="meri_didi",
        user="meri_didi_user",
        password="kH3yFH701UcLYW97QWiAN5CKv02NSNTF",
        host="dpg-d0ti0vm3jp1c73ekk81g-a.oregon-postgres.render.com",
        port="5432",
        sslmode="require"
    )
    print("✅ Connected!")
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)
