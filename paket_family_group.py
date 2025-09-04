import json
from api_request import send_api_request, get_family
from ui import clear_screen, show_package_details

# Kumpulan Family Code yang akan ditampilkan di submenu
family_codes_grouped = {
    "1": {"name": "Xta Unlimited Turbo", "code": "08a3b1e6-8e78-4e45-a540-b40f06871cfe"},
    "2": {"name": "Special For You", "code": "6fda76ee-e789-4897-89fb-9114da47b805"},
    "3": {"name": "Edukasi", "code": "5d63dddd-4f90-4f4c-8438-2f005c20151f"},
    "4": {"name": "Xtra Combo Flex", "code": "4a1acab0-da54-462c-84b1-25fd0efa9318"},
    "5": {"name": "Xtra Combo Old", "code": "364d5764-77d3-41b8-9c22-575b555bf9df"},
    "6": {"name": "Bonus XCP", "code": "45c3a622-8c06-4bb1-8e56-bba1f3434600"},
    "7": {"name": "Xtra Combo Plus V1 & V2", "code": "23b71540-8785-4abe-816d-e9b4efa48f95"},
}

def show_family_group_menu(api_key: str, tokens: dict):
    in_group_menu = True
    while in_group_menu:
        clear_screen()
        print("--------------------------")
        print("Pilih Kategori Family Code")
        print("--------------------------")
        for key, value in family_codes_grouped.items():
            print(f"{key}. {value['name']}")
        print("99. Kembali ke menu utama")
        print("--------------------------")

        choice = input("Pilih kategori (nomor): ").strip()
        if choice == "99":
            in_group_menu = False
            return

        selected_family = family_codes_grouped.get(choice)
        if not selected_family:
            print("Kategori tidak ditemukan. Silakan pilih nomor yang benar.")
            continue

        family_code = selected_family["code"]
        show_packages_by_family(api_key, tokens, family_code)


def show_packages_by_family(api_key: str, tokens: dict, family_code: str):
    """
    Fungsi ini memanggil paket berdasarkan family code, sama seperti paket_custom_family.py
    """
    packages = []

    data = get_family(api_key, tokens, family_code)
    if not data:
        print("Gagal mendapatkan data paket.")
        input("Tekan Enter untuk kembali...")
        return

    in_package_menu = True
    while in_package_menu:
        clear_screen()
        print("--------------------------")
        print("Paket Tersedia")
        print("--------------------------")
        family_name = data['package_family']["name"]
        print(f"Family Name: {family_name}")

        package_variants = data["package_variants"]
        option_number = 1
        variant_number = 1

        for variant in package_variants:
            variant_name = variant["name"]
            print(f" Variant {variant_number}: {variant_name}")
            for option in variant["package_options"]:
                option_name = option["name"]

                packages.append({
                    "number": option_number,
                    "name": option_name,
                    "price": option["price"],
                    "code": option["package_option_code"]
                })

                print(f"{option_number}. {option_name} - Rp {option['price']}")
                option_number += 1
            variant_number += 1

        print("99. Kembali ke menu sebelumnya")
        pkg_choice = input("Pilih paket (nomor): ").strip()
        if pkg_choice == "99":
            in_package_menu = False
            return

        selected_pkg = next((p for p in packages if p["number"] == int(pkg_choice)), None)
        if not selected_pkg:
            print("Paket tidak ditemukan. Silakan masukan nomor yang benar.")
            input("Tekan Enter untuk melanjutkan...")
            continue

        is_done = show_package_details(api_key, tokens, selected_pkg["code"])
        if is_done:
            in_package_menu = False
            return