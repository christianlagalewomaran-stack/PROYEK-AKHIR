from prettytable import PrettyTable
from colorama import Fore, Style, Back, init
import pandas as pd
import inquirer
import os

pesanan = {}
init(autoreset=True)

garis2 = "="*55
def judul(teks):
    print(Fore.MAGENTA + Back.WHITE + Style.BRIGHT + garis2)
    print(Fore.MAGENTA + Back.WHITE + Style.BRIGHT + teks.center(55))
    print(Fore.MAGENTA + Back.WHITE + Style.BRIGHT + garis2)

garis1 = "^"*55
def info(teks):
    print(Fore.MAGENTA + Back.WHITE + Style.BRIGHT + garis1)
    print(Fore.MAGENTA + Back.WHITE + Style.BRIGHT + teks.center(55))
    print(Fore.MAGENTA + Back.WHITE + Style.BRIGHT + garis1)

def lihatproduk():
    try:
        df = pd.read_csv('produk.csv')
        df.columns = df.columns.str.strip()
    except FileNotFoundError:
        print(Fore.RED + "File tidak ditemukan.")
        return None
    opsi = [
        inquirer.List("opsi",
                    message=Fore.YELLOW + "PILIH GENDER",
                    choices=[Fore.BLUE + "👨. Pria", Fore.MAGENTA +  "👧. Wanita", Fore.GREEN +  "👥. Unisex"],
                ),
    ]
    answer = inquirer.prompt(opsi)
    gender = answer["opsi"]
    if "👨" in gender:
        gender = "Pria"
    elif "👧" in gender:
        gender = "Wanita"
    else:
        gender = "Unisex"
    
    os.system("cls || clear")
    
    pilih = [
        inquirer.List("opsi",
                    message=Fore.YELLOW + "PILIH KATEGORI",
                    choices=[Fore.GREEN + "👕. Atasan", Fore.CYAN + "👖. Bawahan", Fore.MAGENTA + "👟. Sepatu", Fore.BLUE + "⌚. Pelengkap"],
                ),
    ]
    answer = inquirer.prompt(pilih)
    kategori = answer["opsi"]
    if "👕" in kategori:
        kategori = "Atasan"
    elif "👖" in kategori:
        kategori = "Bawahan"
    elif "👟" in kategori:
        kategori = "Sepatu"
    else:
        kategori = "Pelengkap"
    os.system("cls || clear")
    filtered_df = df[(df["gender"] == gender) & (df["kategori"] == kategori)]
    if filtered_df.empty:
        print(Fore.RED + "Produk tidak ditemukan")
        return None
    table = PrettyTable()
    table.field_names = filtered_df.columns.tolist()
    for i, j in filtered_df.iterrows():
        table.add_row(j.tolist())
    print(table)
    return filtered_df