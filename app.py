from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, session, flash
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash
from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import generate_csrf
from crypto.crypto_combined import encrypt_combined, decrypt_combined
from dotenv import load_dotenv
from flask import jsonify
from functools import wraps
from flask import request, jsonify, redirect, url_for, flash, session
import os
import smtplib
import logging


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

csrf = CSRFProtect(app)
load_dotenv()


# Konfigurasi email pengirim (App Password Gmail), memerlukan konfigurasi di google settings terlebih dahulu
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Folder konfigurasi
UPLOAD_FOLDER = 'uploads'
ENCRYPTED_FOLDER = 'encrypted_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ENCRYPTED_FOLDER'] = ENCRYPTED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024  # Max 30MB

# Tipe file yang diperbolehkan
ALLOWED_EXTENSIONS = {'pdf'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Tipe foto profil yang diperbolehkan
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png'}
def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS



# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_datawaris'

mysql = MySQL(app)

# Pastikan folder ada
for folder in [UPLOAD_FOLDER, ENCRYPTED_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Proteksi halaman supaya harus login
def login_required(f):
 
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            if request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']:
                return jsonify({'error': 'Anda harus login terlebih dahulu'}), 401
            flash('Anda harus login terlebih dahulu.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@login_required
def index():
    return render_template('home.html')

@app.route('/demo')
@login_required
def demo():
    return render_template('index.html')

@app.route('/pages/about')
@login_required
def about():
    return render_template('about.html')

@app.route('/pages/contact')
@login_required
def contact():
    return render_template('contact.html')

@app.route('/enkripsi')
@login_required
def enkripsi():
    return render_template('enkripsi.html')

@app.route('/dekripsi')
@login_required
def dekripsi():
    return render_template('dekripsi.html')

# Route profile
@app.route('/profile')
@login_required
def profile():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (session['username'],))
    user = cur.fetchone()
    cur.close()

    if user:
        user_data = {
            'id': user[0],
            'username': user[1],
            'password': user[2],
            'nama_lengkap': user[3],
            'role': user[4],
            'email': user[5] if len(user) > 5 else '',
            'foto_profil': user[6] if len(user) > 6 else '',
            'created_at': user[7] if len(user) > 7 else ''
        }
    else:
        user_data = {}

    return render_template("profile.html", user=user_data)

# Route edit profil
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        nama = request.form['nama_lengkap']
        email = request.form['email']
        foto = request.files.get('foto_profil')
        filename = None

        if foto and foto.filename != '':
            if allowed_image(foto.filename):
                filename = secure_filename(foto.filename)
                foto.save(os.path.join('static/uploads', filename))

                cur.execute("""
                    UPDATE users
                    SET nama_lengkap = %s, email = %s, foto_profil = %s
                    WHERE username = %s
                """, (nama, email, filename, session['username']))
            else:
                flash('Tipe file tidak diizinkan. Hanya gambar .jpg, .jpeg, .png yang diperbolehkan.', 'danger')
                return redirect(url_for('edit_profile'))
        else:
            # Jika tidak mengunggah foto baru
            cur.execute("""
                UPDATE users
                SET nama_lengkap = %s, email = %s
                WHERE username = %s
            """, (nama, email, session['username']))

        mysql.connection.commit()
        cur.close()
        flash('Profil berhasil diperbarui!', 'success')
        return redirect(url_for('profile'))

    # Ambil data pengguna untuk ditampilkan
    cur.execute("SELECT * FROM users WHERE username = %s", (session['username'],))
    user = cur.fetchone()
    cur.close()

    user_data = {
        'id': user[0],
        'username': user[1],
        'password': user[2],
        'nama_lengkap': user[3],
        'role': user[4],
        'email': user[5] if len(user) > 5 else '',
        'foto_profil': user[6] if len(user) > 6 else '',
        'created_at': user[7] if len(user) > 7 else ''
    }

    return render_template('edit_profile.html', user=user_data)


# Fungsi rute untuk history dan delete history
@app.route('/history')
@login_required
def history():
    username = session['username']
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user:
        user_id = user[0]
        cur.execute("SELECT idhistory, namaFile, aksi, waktu, email FROM history WHERE users_id = %s ORDER BY waktu DESC", (user_id,))
        histories = cur.fetchall()
    else:
        histories = []
    cur.close()

    histories_dict = []
    for h in histories:
        histories_dict.append({
            'idhistory': h[0],
            'namaFile': h[1],
            'aksi': h[2],
            'waktu': h[3],
            'email': h[4]
        })

    return render_template('history.html', histories=histories_dict)


@app.route('/history/delete/<int:idhistory>', methods=['POST'])
@login_required
def delete_history(idhistory):
    username = session['username']

    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if not user:
        flash('User tidak ditemukan.', 'danger')
        return redirect(url_for('history'))

    user_id = user[0]

    cur.execute("DELETE FROM history WHERE idhistory = %s AND users_id = %s", (idhistory, user_id))
    mysql.connection.commit()
    cur.close()

    flash('Riwayat berhasil dihapus.', 'success')
    return redirect(url_for('history'))

# Fungsi rute untuk login dan logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[0], password):
            session['username'] = username
            flash('Login berhasil!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', csrf_token=generate_csrf())

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('login'))


# Fungsi rute untuk mengenkripsi file
@app.route('/encrypt_file', methods=['POST'])
@login_required
def encrypt_file():
    if 'file' not in request.files or 'email' not in request.form:
        return jsonify({'error': 'File dan email wajib diisi'}), 400

    uploaded_file = request.files['file']
    recipient_email = request.form['email']
    custom_key = request.form['custom_key'].encode()
    
    if uploaded_file.filename != '':
        file_data = uploaded_file.read()
        uploaded_file.seek(0)

    if uploaded_file.filename == '':
        return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
    
    if not allowed_file(uploaded_file.filename):
        return jsonify({'error': 'Tipe file tidak diizinkan. Hanya file PDF yang diperbolehkan'}), 400

    filename = secure_filename(uploaded_file.filename)
    file_path = save_uploaded_file(uploaded_file, filename)

    with open(file_path, 'rb') as f:
        file_data = f.read()

    encrypted_data = encrypt_combined(file_data, custom_key)

    filename_wo_ext = os.path.splitext(filename)[0]
    encrypted_filename = filename_wo_ext + '.enc'
    encrypted_file_path = save_encrypted_file(encrypted_data, encrypted_filename)

    try:
        send_email_keys(recipient_email,custom_key.decode(),filename)
    except Exception as e:
        return jsonify({'error': f'Gagal mengirim email: {str(e)}'}), 500

    # --- Simpan riwayat enkripsi ke database ---
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
    user_id = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO history (users_id, namaFile, aksi, email) VALUES (%s, %s, %s, %s)",
        (user_id, uploaded_file.filename, 'enkripsi', recipient_email)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({
    'encrypted_file_url': url_for('download_file', filename=encrypted_filename)
}), 200

logging.basicConfig(filename='email_errors.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

# Fungsi untuk mengirimkan email dan pesan kunci
def send_email_keys(recipient,custom_key, filename):
    message = MIMEMultipart()
    message['From'] = EMAIL_ADDRESS
    message['To'] = recipient
    message['Subject'] = 'Kunci Enkripsi Anda'

    body = f'''
Berikut adalah kunci enkripsi Anda untuk file "{filename}":

Kunci: {custom_key}

Simpan informasi ini dengan aman untuk keperluan dekripsi.
'''

    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(message)
    except smtplib.SMTPAuthenticationError:
        logging.error("SMTP Authentication failed. Periksa EMAIL_PASSWORD dan akses Gmail.")
        raise Exception("Autentikasi email gagal.")
    except smtplib.SMTPRecipientsRefused:
        logging.error(f"Alamat email ditolak: {recipient}")
        raise Exception("Email tujuan tidak valid.")
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error: {e}")
        raise Exception("Terjadi kesalahan saat mengirim email.")
    except Exception as e:
        logging.error(f"Kesalahan umum saat kirim email: {e}")
        raise

# Fungsi untuk mendekripsi file
@app.route('/decrypt_file', methods=['POST'])
@login_required
def decrypt_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    print("Filename:", file.filename)
    print("File size from request.files:", file.content_length)
    print("Request.files keys:", request.files.keys())
    print("Request.form keys:", request.form.keys())

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    encrypted_file_data = file.read()
    print("Encrypted file size after read():", len(encrypted_file_data))
    print("First 20 bytes:", encrypted_file_data[:20])

    try:
        custom_key = request.form.get('custom_key').encode()
    except Exception as e:
        return jsonify({'error': f'Invalid key: {str(e)}'}), 400

    try:
        final_decrypted = decrypt_combined(encrypted_file_data, custom_key)
        print(final_decrypted[:5])
    except ValueError as e:
        if 'padding is incorrect' in str(e).lower():
            return jsonify({'error': 'Kata kunci salah atau file tidak sesuai.'}), 400
        else:
            return jsonify({'error': f'Dekripsi gagal: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Kesalahan tidak terduga: {str(e)}'}), 500


    original_filename = file.filename.replace('.enc', '.pdf')
    if not original_filename.lower().endswith('.pdf'):
        original_filename += '.pdf'

    decrypted_file_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
    with open(decrypted_file_path, 'wb') as f:
        f.write(final_decrypted)

    # --- Simpan riwayat dekripsi ke database ---
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
    user_id = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO history (users_id, namaFile, aksi) VALUES (%s, %s, %s)",
        (user_id, file.filename, 'dekripsi')
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({
        'decrypted_file_url': f'/download/{original_filename}',
        'filename': original_filename
    })

@app.route('/download/<filename>', methods=['GET'])
@login_required
def download_file(filename):
    safe_filename = secure_filename(filename)

    encrypted_path = os.path.join(app.config['ENCRYPTED_FOLDER'], safe_filename)
    if os.path.exists(encrypted_path):
        return send_from_directory(app.config['ENCRYPTED_FOLDER'], safe_filename, as_attachment=True)

    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
    if os.path.exists(upload_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], safe_filename, as_attachment=True)

    return jsonify({'error': 'File not found'}), 404

# Simpan file upload
def save_uploaded_file(file, filename):
    filename = secure_filename(filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return file_path


# Simpan file hasil enkripsi
def save_encrypted_file(encrypted_data, filename):
    encrypted_file_path = os.path.join(app.config['ENCRYPTED_FOLDER'], filename)
    with open(encrypted_file_path, 'wb') as f:
        f.write(encrypted_data)
        
        print(f"[DEBUG] Encrypted file saved: {encrypted_file_path}")
        print(f"[DEBUG] Encrypted data size: {len(encrypted_data)} bytes")
        
    return encrypted_file_path

# Pesan error kalau ukuran terlalu besar
@app.errorhandler(413)
def file_too_large(e):
    return jsonify({'error': 'Ukuran file terlalu besar. Maksimal 30MB'}), 413


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
