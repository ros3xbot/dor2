from api_request import get_package, send_api_request
from ui import clear_screen, pause, console, _c, RICH_OK
from auth_helper import AuthInstance

try:
    from rich.table import Table
    from rich.panel import Panel
    from rich.align import Align
    from rich.box import ROUNDED
except ImportError:
    pass

# Fetch my packages
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
        panel = Panel(
            Align.center(f"[{_c('text_sub')}]Fetching my packages...[/]"),
            title=f"[{_c('text_title')}]My Packages[/]",
            border_style=_c("border_primary"),
            box=ROUNDED
        )
        console.print(panel)
    else:
        print("Fetching my packages...")

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
    clear_screen()
    if RICH_OK:
        table = Table(
            title=f"[{_c('text_title')}]My Packages[/]",
            show_header=True, header_style=_c("text_sub"), box=ROUNDED
        )
        table.add_column("No", style=_c("text_number"), width=4)
        table.add_column("Name", style=_c("text_body"))
        table.add_column("Quota Code", style=_c("text_sub"))
        table.add_column("Family Code", style=_c("text_sub"))
        table.add_column("Group Code", style=_c("text_sub"))
    else:
        print("===============================")
        print("My Packages")
        print("===============================")

    for num, quota in enumerate(quotas, 1):
        quota_code = quota["quota_code"] # Can be used as option_code
        group_code = quota["group_code"]
        name = quota["name"]
        family_code = "N/A"

        # Info loading detail per paket
        if RICH_OK:
            console.print(f"[{_c('text_sub')}]Fetching package no. {num} details...[/]")
        else:
            print(f"fetching package no. {num} details...")

        package_details = get_package(api_key, tokens, quota_code)
        if package_details:
            family_code = package_details["package_family"]["package_family_code"]

        if RICH_OK:
            table.add_row(
                str(num),
                name,
                quota_code,
                family_code,
                group_code
            )
        else:
            print("===============================")
            print(f"Package {num}")
            print(f"Name: {name}")
            print(f"Quota Code: {quota_code}")
            print(f"Family Code: {family_code}")
            print(f"Group Code: {group_code}")
            print("===============================")

    if RICH_OK:
        panel = Panel(
            Align.center(table),
            title=f"[{_c('text_title')}]My Packages[/]",
            border_style=_c("border_info"),
            box=ROUNDED
        )
        console.print(panel)
    pause()