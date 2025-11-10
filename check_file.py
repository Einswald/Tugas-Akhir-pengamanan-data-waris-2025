def check_file(enc_filename):
    try:
        with open(enc_filename, 'rb') as f:
            data = f.read()

            if len(data) < 24:
                print("File terlalu pendek untuk berisi dua IV.")
                return

            aes_iv = data[:16]
            blowfish_iv = data[16:24]
            ciphertext_preview = data[24:40]
            
            print("Ukuran total file (byte):", len(data))
            print("="*40)
            print("=== Informasi dari file terenkripsi ===")
            print("AES IV        (16 byte):", aes_iv.hex())
            print("Blowfish IV   (8 byte) :", blowfish_iv.hex())
            print("Ciphertext (preview)   :", ciphertext_preview.hex())
    except FileNotFoundError:
        print(f"File '{enc_filename}' tidak ditemukan.")
    except Exception as e:
        print("Terjadi kesalahan:", str(e))


if __name__ == '__main__':
    file_enc = 'downloads/SPAW_Sumarni_05122024.enc'  # File
    check_file(file_enc)
