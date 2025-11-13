from prettytable import PrettyTable
import pandas as pd
import inquirer
import os

pesanan = {}

garis2 = "="*50
def judul(teks):
    print(garis2)
    print(teks.center(50))
    print(garis2)

garis1 = "^"*50
def info(teks):
    print(garis1)
    print(teks.center(50))
    print(garis1)

def lihatproduk():
    try:
        df = pd.read_csv('produk.csv')
        df.columns = df.columns.str.strip()
    except FileNotFoundError:
        print("File tidak ditemukan.")
        return None
    opsi = [
        inquirer.List("opsi",
                    message="PILIH GENDER",
                    choices=["1. pria", "2. wanita", "3. unisex"],
                ),
    ]
    answer = inquirer.prompt(opsi)
    gender = answer["opsi"]
    if "1" in gender:
        gender = "pria"
    elif "2" in gender:
        gender = "wanita"
    else:
        gender = "unisex"
    
    os.system("cls || clear")
    
    pilih = [
        inquirer.List("opsi",
                    message="PILIH KATEGORI",
                    choices=["1. atasan", "2. bawahan", "3. sepatu", "4. pelengkap"],
                ),
    ]
    answer = inquirer.prompt(pilih)
    kategori = answer["opsi"]
    if "1" in kategori:
        kategori = "atasan"
    elif "2" in kategori:
        kategori = "bawahan"
    elif "3" in kategori:
        kategori = "sepatu"
    else:
        kategori = "pelengkap"
    os.system("cls || clear")
    filtered_df = df[(df["gender"] == gender) & (df["kategori"] == kategori)]
    if filtered_df.empty:
        print("produk tidak ditemukan")
        return None
    table = PrettyTable()
    table.field_names = filtered_df.columns.tolist()
    for i, j in filtered_df.iterrows():
        table.add_row(j.tolist())
    print(table)
    return filtered_df