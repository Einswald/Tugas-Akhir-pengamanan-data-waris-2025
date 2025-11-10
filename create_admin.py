import pymysql
from werkzeug.security import generate_password_hash
import getpass

conn = None

print("=== Buat Admin Baru ===")
username = input("Username: ")
password = getpass.getpass("Password: ")
nama_lengkap = input("Nama Lengkap: ")
role = input("Role (admin/superadmin): ").strip().lower()

if role not in ['admin', 'superadmin']:
    print("Role harus 'admin' atau 'superadmin'.")
    exit()

hashed_password = generate_password_hash(password)

try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='db_datawaris',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            print("Username sudah digunakan.")
            exit()

        sql = """
        INSERT INTO users (username, password, nama_lengkap, role)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (username, hashed_password, nama_lengkap, role))
        conn.commit()
        print("✅ User berhasil dibuat.")

except Exception as e:
    print("❌ Terjadi kesalahan:", e)
finally:
    if conn:
        conn.close()
