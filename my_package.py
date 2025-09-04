from api_request import get_package, send_api_request
from ui import clear_screen, pause, console, _c, RICH_OK
from auth_helper import AuthInstance

try:
    from rich.table import Table
    from rich.panel import Panel
    from rich.box import ROUNDED
except ImportError:
    pass

def fetch_my_packages():
    api_key = AuthInstance.api_key
    tokens = AuthInstance.get_active_tokens()
    if not tokens:
        if RICH_OK:
            console.print(f"[{_c('text_err')}]No active user tokens found.[/]")
        else:
            print("No active user tokens found.")
        pause()
        return None
        
    id_token = tokens.get("id_token")
    path = "api/v8/packages/quota-details"
    payload = {
        "is_enterprise": False,
        "lang": "en",
        "family_member_id": ""
    }

    clear_screen()
    if RICH_OK:
        console.print(f"[{_c('text_title')}]My Packages[/]")
        table = Table(
            show_header=True, header_style=_c("text_sub"), box=ROUNDED
        )
        table.add_column("No", style=_c("text_number"), width=4)
        table.add_column("Name", style=_c("text_body"))
        table.add_column("Quota Code", style=_c("text_sub"))
        table.add_column("Group Code", style=_c("text_sub"))
        table.add_column("Family Code", style=_c("text_sub"))
        # Info utama di tabel
        rows = []
    else:
        print("===============================")
        print("My Packages")
        print("===============================")

    res = send_api_request(api_key, path, payload, id_token, "POST")
    if res.get("status") != "SUCCESS":
        if RICH_OK:
            console.print(f"[{_c('text_err')}]Failed to fetch packages[/]")
            console.print(f"[{_c('text_warn')}]Response: {res}[/]")
        else:
            print("Failed to fetch packages")
            print("Response:", res)
        pause()
        return None

    quotas = res["data"]["quotas"]

    for num, quota in enumerate(quotas, 1):
        quota_code = quota.get("quota_code", "N/A")
        group_code = quota.get("group_code", "N/A")
        name = quota.get("name", "N/A")
        family_code = "N/A"
        family_detail = "-"

        if RICH_OK:
            console.print(f"[{_c('text_sub')}]Fetching package no. {num} details...[/]")
        else:
            print(f"fetching package no. {num} details...")

        package_details = get_package(api_key, tokens, quota_code)
        if package_details and "package_family" in package_details:
            family_obj = package_details["package_family"]
            family_code = family_obj.get("package_family_code", "N/A")
            family_detail = "\n".join([f"{k}: {v}" for k, v in family_obj.items()])
        else:
            family_detail = "-"

        if RICH_OK:
            table.add_row(
                str(num),
                name,
                quota_code,
                group_code,
                family_code
            )
            rows.append((num, family_detail))
        else:
            print("===============================")
            print(f"Package {num}")
            print(f"Name: {name}")
            print(f"Quota Code: {quota_code}")
            print(f"Group Code: {group_code}")
            print(f"Family Code: {family_code}")
            print("Family Detail:")
            print(family_detail)
            print("===============================")

    # Tampilkan tabel utama dan detail family terpisah di bawahnya
    if RICH_OK:
        console.print(table)
        for num, family_detail in rows:
            # Family detail bukan dalam tabel!
            if family_detail and family_detail != "-":
                console.print(Panel(family_detail, title=f"Family Detail Paket {num}", border_style=_c("border_info"), box=ROUNDED))
            else:
                console.print(Panel("Tidak ada detail family.", title=f"Family Detail Paket {num}", border_style=_c("border_warn"), box=ROUNDED))
    pause()