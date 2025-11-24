from prettytable import PrettyTable
from colorama import Fore,Back,Style,init
from create import lihatproduk,judul
import pandas as pd
import inquirer
import os

init(autoreset=True)

def tambahproduk():
    columns_required = ["id", "nama", "kategori", "harga", "gender", "stok"]
    try:
        df = pd.read_csv('produk.csv')
        for col in columns_required:
            if col not in df.columns:
                raise ValueError(Fore.RED + "Struktur produk.csv tidak sesuai: kolom '" + col + "' tidak ditemukan")
    except FileNotFoundError:
        df = pd.DataFrame(columns=columns_required)
    except ValueError as e:
        print(str(e))
        return

    if df.empty:
        next_id = 1
    else:
        try:
            next_id = int(df['id'].max()) + 1
        except Exception:
            print(Fore.RED + "Kolom ID mengandung nilai tidak valid.")
            return

    nama = input(Fore.YELLOW + "Masukkan nama produk: ").strip()
    if not nama:
        print(Fore.RED + "Nama produk tidak boleh kosong.")
        return
    print()
    kategori_choices = ["Atasan", "Bawahan", "Sepatu", "Pelengkap"]
    gender_choices = ["Pria", "Wanita", "Unisex"]
    kategori_prompt = [
        inquirer.List("kategori", message="Pilih kategori", choices=[f"{i+1}. {v}" for i, v in enumerate(kategori_choices)])
    ]
    ans = inquirer.prompt(kategori_prompt)
    if not ans:
        return
    kategori_ans = ans["kategori"]
    kategori = kategori_choices[int(kategori_ans.split(".")[0]) - 1]
    gender_prompt = [
        inquirer.List("gender", message="Pilih gender", choices=[f"{i+1}. {v}" for i, v in enumerate(gender_choices)])
    ]
    ans = inquirer.prompt(gender_prompt)
    if not ans:
        return
    gender_ans = ans["gender"]
    gender = gender_choices[int(gender_ans.split(".")[0]) - 1]
    try:
        harga = int(input(Fore.YELLOW + "Masukkan harga (angka): ").strip())
        if harga <= 0:
            print(Fore.RED + "Harga harus > 0.")
            return
    except ValueError:
        print(Fore.RED + "Harga harus berupa angka.")
        return
    try:
        stok = int(input(Fore.YELLOW + "Masukkan stok (angka): ").strip())
        if stok < 0:
            print(Fore.RED + "Stok tidak boleh negatif.")
            return
    except ValueError:
        print(Fore.RED + "Stok harus berupa angka.")
        return
    new_row = {"id": next_id, "nama": nama, "kategori": kategori, "harga": harga, "gender": gender, "stok": stok}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    try:
        df.to_csv('produk.csv', index=False)
        print("Produk berhasil ditambahkan:")
        table = PrettyTable()
        table.field_names = ["ID", "Nama", "Kategori", "Harga", "Gender", "Stok"]
        table.add_row([next_id, nama, kategori, harga, gender, stok])
        print(table)
    except Exception as e:
        print(f"Gagal menyimpan produk: {e}")

def updateproduk():
    try:
        df = pd.read_csv('produk.csv')
        df.columns = df.columns.str.strip()
    except FileNotFoundError:
        print(Fore.RED + "File tidak ditemukan.")
        return

    filtered_df = lihatproduk()
    if filtered_df is None:
        return

    try:
        pesan_id = int(input(Fore.YELLOW + "Masukkan ID produk yang mau diubah: "))
    except ValueError:
        print(Fore.RED + "Input harus berupa angka.")
        return
    
    if pesan_id not in filtered_df['id'].values:
        print(Fore.RED + "ID produk tidak valid.")
        return

    produk = df[df['id'] == pesan_id]
    stok = produk['stok'].values[0]
    print()
    indeks = produk.index[0]
    pilih = [
            inquirer.List("opsi",
                    message="PILIH KATEGORI YANG MAU DIUBAH",
                    choices=["1. Nama", "2. Kategori", "3. Stok", "4. Harga", "5. Gender"],
                ),
    ]
    answer = inquirer.prompt(pilih)
    ubah = answer["opsi"]
    if "1" in ubah:
        nama_baru = input(Fore.YELLOW + "Masukkan nama baru produk: ")
        if nama_baru != produk['nama'].values[0]:
            df.at[indeks, 'nama'] = nama_baru
            df.to_csv('produk.csv', index=False)
            print(Fore.GREEN + "Produk berhasil diupdate!")
        else:
            print(Fore.RED + "Nama sama dengan sebelumnya, tidak diubah.")
    elif "2" in ubah:
        menu = [
            inquirer.List("opsi",
                message="UBAH KATEGORI",
                choices=["👕. Atasan", "👖. Bawahan", "👟. Sepatu", "⌚. Pelengkap"],
            ),
        ]
        answer = inquirer.prompt(menu)
        kategori_baru = answer["opsi"]
        if "👕" in kategori_baru:
            kategori_baru = "Atasan"
        elif "👖" in kategori_baru:
            kategori_baru = "Bawahan"
        elif "👟" in kategori_baru:
            kategori_baru = "Sepatu"
        else:
            kategori_baru = "Pelengkap"
        if kategori_baru != produk['kategori'].values[0]:
            df.at[indeks, 'kategori'] = kategori_baru
            df.to_csv('produk.csv', index=False)
            print(Fore.GREEN + "Produk berhasil diupdate!")
        else:
            print(Fore.RED + "Kategori sama dengan sebelumnya, tidak diubah.")
    elif "3" in ubah:
        try:
            stok_baru = int(input(Fore.YELLOW + "Masukkan stok baru produk: "))
        except ValueError:
            print(Fore.RED + "Stok harus berupa angka.")
            return
        if stok >= 0 and stok_baru != produk['stok'].values[0]:
            df.at[indeks, 'stok'] = stok_baru
            df.to_csv('produk.csv', index=False)
            print(Fore.GREEN + "Produk berhasil diupdate!")
        else:
            print(Fore.RED + "Stok sama dengan sebelumnya, tidak diubah.")
    elif "4" in ubah:
        try:
            harga_baru = int(input(Fore.YELLOW + "Masukkan harga baru produk: "))
        except ValueError:
            print(Fore.RED + "Harga harus berupa angka.")
            return
        if harga_baru != produk['harga'].values[0]:
            df.at[indeks, 'harga'] = harga_baru
            df.to_csv('produk.csv', index=False)
            print(Fore.GREEN + "Produk berhasil diupdate!")
        else:
            print(Fore.RED + "Harga sama dengan sebelumnya, tidak diubah.")
    else:
        menu = [
            inquirer.List("opsi",
                message="UBAH GENDER",
                choices=["Pria", "Wanita", "Unisex"],
            ),
        ]
        answer = inquirer.prompt(menu)
        gender_baru = answer["opsi"]
        if gender_baru != produk['gender'].values[0]:
            df.at[indeks, 'gender'] = gender_baru
            df.to_csv('produk.csv', index=False)
            print(Fore.GREEN + "Produk berhasil diupdate!")
        else:
            print(Fore.RED + "Gender sama dengan sebelumnya, tidak diubah.")

def hapusproduk():
    try:
        df = pd.read_csv('produk.csv')
    except FileNotFoundError:
        print(Fore.RED + "File produk.csv tidak ditemukan.")
        return
    if df.empty:
        print(Fore.RED + "Tidak ada data produk.")
        return
    table = PrettyTable()
    table.field_names = df.columns.tolist()
    for _, row in df.iterrows():
        table.add_row(row.tolist())
    print(table)
    try:
        id_str = input(Fore.YELLOW + "Masukkan ID produk yang akan dihapus: ").strip()
        id_produk = int(id_str)
    except ValueError:
        print(Fore.RED + "ID harus berupa angka valid.")
        return
    if id_produk not in df['id'].values:
        print(Fore.RED + "ID produk tidak ditemukan.")
        return
    nama_produk = df.loc[df['id'] == id_produk, 'nama'].values[0]
    konfirmasi = input(Fore.YELLOW + f"Yakin hapus produk '{nama_produk}' (ID {id_produk})? [y/n]: ").strip().lower()
    if konfirmasi != 'y':
        print(Fore.GREEN + "Penghapusan dibatalkan.")
        return
    
    try:
        df_baru = df[df['id'] != id_produk]
        df_baru.to_csv('produk.csv', index=False)
        print(Fore.GREEN + f"Produk dengan ID {id_produk} berhasil dihapus.")
    except Exception as e:
        print(Fore.RED + f"Gagal menghapus produk: {e}")

def verifikasitopup():
    try:
        df_topup = pd.read_csv('topup.csv')
    except FileNotFoundError:
        print(Fore.RED + "Tidak ada antrian top up.")
        return

    pending_topups = df_topup[pd.isna(df_topup['status']) | (df_topup['status'] == '')].copy()

    if pending_topups.empty:
        print(Fore.RED + "Tidak ada antrian top up.")
        return

    table = PrettyTable()
    table.field_names = ['No', 'Username', 'Nominal', 'Waktu']
    
    pending_topups['no_urut'] = range(1, len(pending_topups) + 1)

    for _, row in pending_topups.iterrows():
        table.add_row([int(row['no_urut']), row['username'], row['top_up'], row['waktu']])

    print(Fore.YELLOW + "Daftar Antrian Top Up (Pending):")
    print(table)

    try:
        pilihan = int(input(Fore.YELLOW + "Pilih nomor antrian untuk diverifikasi (0 untuk batal): "))
        if pilihan == 0:
            return
        if not (1 <= pilihan <= len(pending_topups)):
            print(Fore.RED + "Pilihan tidak valid.")
            return
        
        verifikasi = pending_topups[pending_topups['no_urut'] == pilihan].iloc[0]
        username = verifikasi['username']
        nominal = verifikasi['top_up']

        action_question = [
            inquirer.List("action",
                        message=f"Verifikasi top up untuk {username} sebesar {nominal}",
                        choices=["✅ Setujui", "❎ Tolak"],
            ),
        ]
        answer = inquirer.prompt(action_question)    
        action = answer["action"]
        
        if action == "✅ Setujui":
            df_akun = pd.read_csv('akun.csv')
            user_index = df_akun.index[df_akun['username'] == username].tolist()
            if user_index:
                df_akun.loc[user_index[0], 'saldo'] += nominal
                df_akun.to_csv('akun.csv', index=False)
                df_topup.loc[verifikasi.name, 'status'] = 'Berhasil'
                print(Fore.GREEN + f"Top up untuk {username} sebesar {nominal} telah disetujui.")
        elif action == "❎ Tolak":
            df_topup.loc[verifikasi.name, 'status'] = 'Gagal'
            print(Fore.RED + f"Top up untuk {username} sebesar {nominal} telah ditolak.")

        df_topup.to_csv('topup.csv', index=False)

    except (ValueError, IndexError, TypeError):
        print(Fore.RED + "Input tidak valid.")

def laporanpenjualan():
    judul("LAPORAN PENJUALAN DAN TOPUP")
    
    opsi = [
        inquirer.List(
            "pilih",
            message=Fore.YELLOW + "Pilih laporan yang ingin dilihat",
            choices=["1. Laporan Penjualan", "2. Laporan Top Up"],
        )
    ]
    
    answer = inquirer.prompt(opsi)
    pilihan = answer["pilih"]
    os.system("cls || clear")
    
    def laporanPenjualan():
        try:
            df = pd.read_csv("riwayat.csv")
        except FileNotFoundError:
            print(Fore.RED + "Belum ada data penjualan.")
            return
        
        if df.empty:
            print(Fore.RED + "Belum ada data penjualan.")
            return

        table = PrettyTable()
        table.field_names = ["No", "Username", "Nama Produk", "Jumlah", "Total", "Waktu"]
        
        for idx, row in df.iterrows():
            waktu_row = row["waktu"] if "waktu" in df.columns else "N/A"
            table.add_row([idx + 1, row["username"], row["nama_produk"], row["jumlah"], row["total"], waktu_row])
        judul("LAPORAN PENJUALAN")
        print(table)
        total_pemasukan = df["total"].sum()
        print(Fore.YELLOW + f"Total pemasukan: {total_pemasukan}")
        
    def laporanTopUp():
        try:
            df = pd.read_csv("topup.csv")
        except FileNotFoundError:
            print(Fore.RED + "Belum ada data top up.")
            return

        if df.empty:
            print(Fore.RED + "Belum ada data top up.")
            return

        table = PrettyTable()
        table.field_names = ["Username", "Jumlah Top Up", "Waktu Top Up", "Status"]

        for _, row in df.iterrows():
            user_row = row["username"] if "username" in df.columns else "N/A"
            jumlah_row = row["top_up"] if "top_up" in df.columns else "N/A"
            waktu_row = row["waktu"] if "waktu" in df.columns else "N/A"
            status_row = row["status"] if "status" in df.columns else "N/A"
            if pd.isna(status_row) or str(status_row).strip() == '':
                status_row = 'Pending'
            table.add_row([user_row, jumlah_row, waktu_row, status_row])
        judul("LAPORAN TOPUP")
        print(table)
        total_topup = df["top_up"].sum()
        print(Fore.YELLOW + f"Total jumlah top up masuk: {total_topup}")
        
    if "1" in pilihan:
        laporanPenjualan()
    else:
        laporanTopUp()
        
def hapususer():
    akun_cols = ["id", "username", "password", "role", "saldo"]
    try:
        df = pd.read_csv('akun.csv')
        for c in akun_cols:
            if c not in df.columns:
                raise ValueError("Struktur akun.csv tidak sesuai: kolom '" + c + "' Tidak ditemukan")
    except FileNotFoundError:
        print(Fore.RED + "File akun.csv tidak ditemukan.")
        return
    except ValueError as e:
        print(str(e))
        return

    if df.empty:
        print(Fore.RED + "Tidak ada data user.")
        return

    table = PrettyTable()
    table.field_names = df.columns.tolist()
    for _, row in df.iterrows():
        table.add_row(row.tolist())
    print(table)

    pilih_prompt = [
        inquirer.List("metode", message="Hapus berdasarkan", choices=["1. ID", "2. Username"])
    ]
    ans = inquirer.prompt(pilih_prompt)
    if not ans:
        return
    metode = ans["metode"]

    if metode.startswith("1"):
        try:
            id = input(Fore.YELLOW + "Masukkan ID user yang akan dihapus: ").strip()
            target_id = int(id)
        except ValueError:
            print(Fore.RED + "ID harus berupa angka.")
            return

        if target_id not in df['id'].values:
            print(Fore.RED + "ID user tidak ditemukan.")
            return

        if any((df['id'] == target_id) & (df['role'] == 'admin')):
            print(Fore.RED + "Akun admin tidak boleh dihapus.")
            return
        username = df.loc[df['id'] == target_id, 'username'].values[0]
        konfirmasi = input(Fore.YELLOW + f"Yakin hapus user '{username}' (ID {target_id})? [y/n]: ").strip().lower()
        if konfirmasi != 'y':
            print(Fore.GREEN + "Penghapusan dibatalkan.")
            return
        df_baru = df.loc[df['id'] != target_id].copy()
    else:
        username = input(Fore.YELLOW + "Masukkan username yang akan dihapus: ").strip()
        if username == "":
            print(Fore.RED + "Username tidak boleh kosong.")
            return
        if username not in df['username'].values:
            print(Fore.RED + "Username tidak ditemukan.")
            return
        if any((df['username'] == username) & (df['role'] == 'admin')):
            print(Fore.RED + "Akun admin tidak boleh dihapus.")
            return
        konfirmasi = input(Fore.YELLOW + f"Yakin hapus user '{username}'? [y/n]: ").strip().lower()
        if konfirmasi != 'y':
            print(Fore.GREEN + "Penghapusan dibatalkan.")
            return
        df_baru = df.loc[df['username'] != username].copy()
        
    try:
        df_baru['id'] = range(1, len(df_baru) + 1)
        df_baru.to_csv('akun.csv', index=False)
        print(Fore.GREEN + "User berhasil dihapus.")
    except Exception as e:
        print(Fore.RED + f"Gagal menghapus user: {e}")
    

def loginadmin(username):
    while True:
        os.system("cls || clear")
        menuuser = [
            inquirer.List("opsi",
                    message=Fore.WHITE + Back.BLUE + Style.BRIGHT + "SILAHKAN PILIH OPSI ADMIN",
                    choices=["➕. Tambah produk", "👀. Lihat produk", "🧵. Update produk", "🗑️.. Hapus produk", "✅. Verifikasi top up", "📜. Laporan penjualan & top up", "❌. Hapus user", "✈️. Keluar"],
                ),
        ]
        answer = inquirer.prompt(menuuser)
        menuuser = answer["opsi"]
        os.system("cls || clear")

        if "➕" in menuuser:
            judul("TAMBAH PRODUK")
            tambahproduk()
            input("Enter untuk kembali ke menu....")
        elif "👀" in menuuser:
            judul("LIHAT PRODUK")
            lihatproduk()
            input("Enter untuk kembali ke menu....")
        elif "🧵" in menuuser:
            judul("UPDATE PRODUK")
            updateproduk()
            input("\nEnter untuk kembali ke menu....")
        elif "🗑️" in menuuser:
            judul("HAPUS PRODUK")
            hapusproduk()
            input("Enter untuk kembali ke menu....")
        elif "✅" in menuuser:
            judul("VERIFIKASI TOP UP")
            verifikasitopup()
            input("Enter untuk kembali ke menu....")
        elif "📜" in menuuser:
            laporanpenjualan()
            input("Enter untuk kembali ke menu....")
        elif "❌" in menuuser:
            judul("HAPUS USER")
            hapususer()
            input("Enter untuk kembali ke menu....")
        else:
            break