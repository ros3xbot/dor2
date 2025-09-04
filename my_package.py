from api_request import get_package, send_api_request
from ui import clear_screen, pause, console, _c, RICH_OK
from auth_helper import AuthInstance

try:
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
    else:
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
        name = quota.get("name", "N/A")
        family_code = "N/A"
        description = "-"

        if RICH_OK:
            console.print(f"[{_c('text_sub')}]Fetching package no. {num} details...[/]")
        else : {name}\n"
            f"Family Code : {family_code}\n"
            f"Description : {description}"
        )

        if RICH_OK:
            console.print(Panel(text, title=f"Paket {num}", border_style=_c("border_info"), box=ROUNDED))
        else:
            print("===============================")
            print(text)
            print("===============================")

    pause()