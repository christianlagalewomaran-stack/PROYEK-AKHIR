from prettytable import PrettyTable
from data import judul
import pandas as pd
import inquirer
import os

pesanan = {}

def lihatsaldo(username):
    try:
        df = pd.read_csv('akun.csv')
    except FileNotFoundError:
        print("File tidak ditemukan.")
        return
    saldo = "Tidak ditemukan."
    for i, j in df.iterrows():
        if j["username"] == username:
            saldo = j["saldo"]
    print(f"Saldo anda: {saldo}")

def lihatproduk():
    try:
        df = pd.read_csv('produk.csv')
    except FileNotFoundError:
        print("File tidak ditemukan.")
        return
    gender = input("pilih gender(pria/wanita/unisex): ")
    kategori = input("pilih kategori(atasan/bawahan/sepatu/pelengkap): ")
    df = df[(df["gender"] == gender) & (df["kategori"] == kategori)]
    if df.empty:  
        print("produk tidak ditemukan")
        return
    table = PrettyTable()
    table.field_names = df.columns.tolist()
    for i, j in df.iterrows():
        table.add_row(j.tolist())
    print(table)

def tambahpesanan():
    global pesanan
    try:
        df = pd.read_csv('produk.csv')
    except FileNotFoundError:
        print("File tidak ditemukan.")
        return

    lihatproduk()
    try:
        pesan_id = int(input("masukkan ID pesanan anda (1-12): "))
    except ValueError:
        print("Input harus berupa angka.")
        return

    if pesan_id < 1 or pesan_id > 12:
        print("ID produk tidak valid. Harus antara 1-12.")
        return

    produk = df[df['id'] == pesan_id]
    if produk.empty:
        print("Produk tidak ditemukan.")
        return

    stok = produk['stok'].values[0]
    if stok <= 0:
        print("Stok produk habis.")
        return

    nama = produk['nama'].values[0]
    harga = produk['harga'].values[0]
    kategori = produk['kategori'].values[0]
    gender = produk['gender'].values[0]

    try:
        jumlah_input = int(input(f"Masukkan jumlah untuk '{nama}' (stok tersedia: {stok}): "))
    except ValueError:
        print("Input jumlah harus berupa angka.")
        return

    if jumlah_input <= 0:
        print("Jumlah harus lebih dari 0.")
        return

    if jumlah_input > stok:
        print("Jumlah melebihi stok tersedia.")
        return

    produk_ada = False
    for key, item in pesanan.items():
        if item['id'] == pesan_id:
            item['jumlah'] += jumlah_input
            produk_ada = True
            break

    if not produk_ada:
        pesanan_len = len(pesanan) + 1
        pesanan[pesanan_len] = {
            'id': pesan_id,
            'nama': nama,
            'kategori': kategori,
            'harga': harga,
            'gender': gender,
            'jumlah': jumlah_input
        }

    os.system("cls || clear")
    table = PrettyTable()
    table.field_names = ["No", "Nama Produk", "Kategori", "Harga", "Gender", "Jumlah"]
    for no, item in pesanan.items():
        table.add_row([no, item['nama'], item['kategori'], item['harga'], item['gender'], item['jumlah']])
    print(table)
    print(f"Pesanan '{nama}' telah ditambahkan.")

def hapuspesanan():
    print("hapus pesanan")

def konfirmasipesanan(username):
    print("konfirmasi pesanan")

def historipembelian():
    print("histori")

def topup():
    print("top up")
    
def loginuser(username):
    while True:
        os.system("cls || clear")
        menuuser = [
            inquirer.List("opsi",
                    message="SILAHKAN PILIH OPSI",
                    choices=["1.lihat saldo", "2.lihat produk", "3.tambah pesanan", "4.hapus pesanan", "5.konfirmasi pesanan", "6.histori pembelian", "7.top up saldo", "8.keluar"],
                ),
        ]
        answer = inquirer.prompt(menuuser)
        menuuser = answer["opsi"]
        os.system("cls || clear")

        if "1" in menuuser:
            judul("LIHAT SALDO")
            lihatsaldo(username)
            input("enter untuk kembali ke menu....")
        elif "2" in menuuser:
            judul("LIHAT PRODUK")
            lihatproduk()
            input("enter untuk kembali ke menu....")
        elif "3" in menuuser: 
            judul("TAMBAH PESANAN")
            tambahpesanan()
            input("enter untuk kembali ke menu....")
        elif "4" in menuuser: 
            judul("HAPUS PESANAN")
            hapuspesanan()
            input("enter untuk kembali ke menu....")
        elif "5" in menuuser:
            judul("KONFIRMASI PESANAN")
            konfirmasipesanan(username)
            input("enter untuk kembali ke menu....")
        elif "6" in menuuser: 
            judul("HISTORI PEMBELIAN")
            historipembelian()
            input("enter untuk kembali ke menu....")
        elif "7" in menuuser:
            judul("TOP UP SALDO")
            topup()
            input("enter untuk kembali ke menu....")
        else:
            break
