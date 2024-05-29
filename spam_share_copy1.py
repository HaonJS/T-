import requests
import re
import sys
from bs4 import BeautifulSoup as bs
import os

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')
    print_banner()

def get_user_cookie(user_email, user_password):
    url = 'https://mbasic.facebook.com'
    xurl = url + '/login.php'
    user_agent = "Mozilla/5.0 (Linux; Android 4.1.2; GT-I8552 Build/JZO54K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    req = requests.Session()
    req.headers.update({
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en_US',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user_agent
    })
    with req.get(url) as response_body:
        inspect = bs(response_body.text, 'html.parser')
        lsd_key = inspect.find('input', {'name': 'lsd'})['value']
        jazoest_key = inspect.find('input', {'name': 'jazoest'})['value']
        m_ts_key = inspect.find('input', {'name': 'm_ts'})['value']
        li_key = inspect.find('input', {'name': 'li'})['value']
        try_number_key = inspect.find('input', {'name': 'try_number'})['value']
        unrecognized_tries_key = inspect.find('input', {'name': 'unrecognized_tries'})['value']
        bi_xrwh_key = inspect.find('input', {'name': 'bi_xrwh'})['value']
        data = {
            'lsd': lsd_key, 'jazoest': jazoest_key,
            'm_ts': m_ts_key, 'li': li_key,
            'try_number': try_number_key,
            'unrecognized_tries': unrecognized_tries_key,
            'bi_xrwh': bi_xrwh_key, 'email': user_email,
            'pass': user_password, 'login': "submit"
        }
        response_body2 = req.post(xurl, data=data, allow_redirects=True, timeout=300)
        cookie = req.cookies.get_dict()

        if 'c_user' in cookie:
            return cookie
        else:
            return None

header = {
    "authority": "graph.facebook.com",
    "cache-control": "max-age=0",
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.66 Safari/537.36"
}
ses = requests.Session()

def login(user_email, user_password):
    cookie = get_user_cookie(user_email, user_password)
    if not cookie:
        print("Failed to obtain cookie. Please check your credentials.")
        sys.exit(1)

    try:
        get_tok = requests.get('https://business.facebook.com/business_locations', headers={
            "user-agent": "Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36",
            "referer": "https://www.facebook.com/",
            "host": "business.facebook.com",
            "origin": "https://business.facebook.com",
            "upgrade-insecure-requests": "1",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "content-type": "text/html; charset=utf-8"
        }, cookies=cookie)
        tokenz = re.search("(EAAG\w+)", get_tok.text).group(1)
        if tokenz:
            print("\n[ Successfully Logged In ]\n")
        coki = {"cookie": "; ".join([f"{k}={v}" for k, v in cookie.items()])}
    except Exception as e:
        print("Invalid cookie")
        sys.exit(1)
        

    idt = input("Enter the link » ")
    limit = int(input("Enter the limit » "))
    print("\n\t\tPress Ctrl+C to stop\n")
    token = tokenz

    try:
        for x in range(limit):
            x += 1
            response = ses.post(
                f"https://graph.facebook.com/v13.0/me/feed?link={idt}&published=0&access_token={token}",
                headers=header, cookies=coki).json()
            if "id" in response:
                sys.stdout.write(f"\r [+] DONE {x}/{limit}")
                sys.stdout.flush()
            else:
                print(" Failed, your account might be flagged as spam")
                sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("[!] Unable to connect to the internet!")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[!] Process interrupted by user.")
        sys.exit(0)

def print_banner():
    banner = (
    "╔════════════════════════════════╗\n"
    "║          FACEBOOK TOOL         ║\n"
    "║      Simple Facebook Tool      ║\n"
    "║      Author : Jessica          ║\n"
    "║      Facebook: Jessica         ║\n"
    "╚════════════════════════════════╝\n"
    )
    print(banner)

def another_session(user_email, user_password):
    while True:
        choice = input("\nDo you want another session? (Y/n): ").strip().lower()
        if choice == 'y':
            same_account = input("\nDo you want the same account? (Y/n): ").strip().lower()
            if same_account == 'y':
                clear_screen()
                print("\nUser email:", user_email)
                print("User password:", user_password)
                login(user_email, user_password)
            elif same_account == 'n':
                clear_screen()
                return True
            else:
                print("Invalid input. Please enter 'Y' or 'n'.")
        elif choice == 'n':
            print("Exiting the program.")
            sys.exit(0)
        else:
            print("Invalid input. Please enter 'Y' or 'n'.")

def main_menu():
    while True:
        print("\n1. SpamShare")
        print("2. Exit")
        choice = input("\nChoose an option: ").strip()
        clear_screen()
        
        if choice == '1':
            print("FACEBOOK SHARE TOOL")
            while True:
                user_email = input("\n⟨ Enter your UID/Email/Number/Name ⟩: ")
                user_password = input("⟨ Enter your Password ⟩: ")
              
                login(user_email, user_password)
                if not another_session(user_email, user_password):
                    break
        elif choice == '2':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please select 1 or 2.")

if __name__ == "__main__":
    os.system('clear' if os.name == 'posix' else 'cls')
    print_banner()
    main_menu()