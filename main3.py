import requests
import random
import string
import sys
import os
import time
from datetime import datetime

# --- COLORS ---
R, G, Y, B, P, C, W, N = '\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;34m', '\033[1;35m', '\033[1;36m', '\033[1;37m', '\033[0m'

# --- CONFIG ---
EXPIRY_URL = "https://raw.githubusercontent.com/ramsiya0ram-hue/Piczio-connection/refs/heads/main/piczio%20contro.txt" 
API_KEY = "gAAAAABkrjh_9CibQaJvdxQtJdQIlM-ILat3XU3sI4DNcMmtW2zTs-5-1LpEOmTaLNgvUHZu4mp1WEcdHSHsOYE5tf80QWAvYQ=="
BASE_URL = "https://piczio.app/api/v1"

FIXED_FOLLOW_LIST = [24, 38946] 
FIXED_POST_IDS = [554401, 169801]

DEVICES = [
    {"brand": "Realme", "model": "RMX3933", "name": "realme RMX3933"},
    {"brand": "Xiaomi", "model": "Redmi Note 12", "name": "Redmi Note 12 5G"},
    {"brand": "Samsung", "model": "SM-G991B", "name": "Samsung Galaxy S21"},
    {"brand": "Vivo", "model": "V2250", "name": "Vivo Y100"}
]

# --- UI FUNCTIONS ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    logo = f"""
{P}  __  __           _     _ _              ______                      
{P} |  \/  |         | |   | (_)            |___  /                      
{C} | \  / | ___   __| | __| |_ _ __   __ _    / /  ___  _ __   ___      
{C} | |\/| |/ _ \ / _` |/ _` | | '_ \ / _` |  / /  / _ \| '_ \ / _ \     
{G} | |  | | (_) | (_| | (_| | | | | | (_| | / /__| (_) | | | |  __/     
{G} |_|  |_|\___/ \__,_|\__,_|_|_| |_|\__, |/_____|\___/|_| |_|\___|     
{W}                                    __/ |                             
{W}      {R}MODDED BY @MODDING_ZONEE{W}     |___/      {Y}VERSION: 1.6.6{N}
{G}====================================================================={N}
    """
    print(logo)

def loading_animation(text):
    sys.stdout.write(f"{Y}[+] {text}")
    for _ in range(3):
        time.sleep(0.5)
        sys.stdout.write(".")
        sys.stdout.flush()
    print(f"{N}")

# --- HELPER FUNCTIONS ---
def get_random_ip(): return f"{random.randint(10, 192)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
def get_random_imei(): return ''.join(random.choices(string.digits, k=15))
def get_random_string(length=8): return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
def generate_device_token(): return "f" + get_random_string(10) + ":" + get_random_string(140)

def check_expiry():
    loading_animation("Checking License")
    try:
        res = requests.get(EXPIRY_URL, timeout=10)
        exp = datetime.strptime(res.text.strip(), "%Y-%m-%d").date()
        if datetime.now().date() > exp:
            print(f"{R}[!] EXPIRED! Contact @MODDING_ZONEE{N}"); sys.exit()
        print(f"{G}[✓] Access Granted!{N}\n")
    except: 
        print(f"{R}[!] License Error!{N}"); sys.exit()

def run_automation():
    banner()
    check_expiry()
    
    # --- CUSTOM INPUTS ---
    print(f"{Y}--- TARGET CONFIGURATION ---{N}")
    custom_f = input(f"{C}[+] Enter Follow IDs (Contact Admin): {W}")
    custom_p = input(f"{C}[+] Enter Post IDs (Contact Admin): {W}")

    final_follow = FIXED_FOLLOW_LIST.copy()
    if custom_f:
        final_follow.extend([int(i.strip()) for i in custom_f.split(',') if i.strip().isdigit()])

    final_posts = FIXED_POST_IDS.copy()
    if custom_p:
        final_posts.extend([int(i.strip()) for i in custom_p.split(',') if i.strip().isdigit()])

    device = random.choice(DEVICES)
    ip, imei = get_random_ip(), get_random_imei()
    
    print(f"\n{G}[#] Spoofer Active: {W}{device['name']} | IP: {ip}{N}")
    target_email = input(f"{C}[+] Enter Target Gmail: {W}")

    headers = {"api-key": API_KEY, "user-agent": "okhttp/5.1.0", "content-type": "application/json; charset=UTF-8"}
    fake_phone = "9" + "".join(random.choices(string.digits, k=9))

    # OTP Logic
    loading_animation("Sending OTP to Gmail")
    requests.post(f"{BASE_URL}/auth/check-user", headers=headers, json={"country_code": "+91", "phone_number": fake_phone})
    requests.post(f"{BASE_URL}/auth/send-otp", headers=headers, json={"country_code": "+91", "phone_number": fake_phone, "email": target_email})

    otp = input(f"\n{P}[?] Enter Received OTP: {W}")
    v_res = requests.post(f"{BASE_URL}/auth/verify-otp", headers=headers, json={"country_code": "+91", "phone_number": fake_phone, "otp": otp})
    
    if v_res.json().get("code") == 1:
        print(f"{G}[✓] OTP Verified!{N}")
        loading_animation("Creating Modded Account")
        
        payload = {
            "app_version": "1.6.6", "login_type": "S", "os_version": "35", "device_type": "A",
            "ip_address": ip, "uu_id_number": f"{get_random_string(8)}-{get_random_string(4)}-4555-a888-{get_random_string(12)}",
            "api_version": "v1", "country_code": "+91", "password": "User@123", 
            "device_name": device['name'], "referred_by_code": "", "model_name": device['brand'],
            "imei_number": imei, "device_token": generate_device_token(),
            "phone_number": fake_phone, "email": target_email, "fullname": "Modding Zone User", "username": f"mz_{get_random_string(5)}", "social_key": ""
        }
        
        final_res = requests.post(f"{BASE_URL}/auth/signup", headers=headers, json=payload).json()
        token = final_res.get('data', {}).get('token')

        if token:
            print(f"{G}[✓] Account Securely Created!{N}\n")
            auth_headers = headers.copy()
            auth_headers["authorization"] = f"TOKEN {token}"
            
            # --- FOLLOW EXECUTION ---
            print(f"{B}[>] Injecting Follow Requests...{N}")
            for tid in final_follow:
                requests.post(f"{BASE_URL}/auth/follow-following/add-follow-request", headers=auth_headers, json={"instance_id": tid})
                print(f"    {W}Account -> {C}{tid} {G}[DONE]{N}")
                time.sleep(0.5)

            # --- POST BOOSTING ---
            print(f"\n{B}[>] Boosting Posts (Likes + Views)...{N}")
            for pid in final_posts:
                requests.post(f"{BASE_URL}/post/post-like", headers=auth_headers, json={"post": pid})
                requests.post(f"{BASE_URL}/post/update-post-view", headers=auth_headers, json={"post": pid})
                print(f"    {W}PostID -> {C}{pid} {G}[BOOSTED]{N}")
                time.sleep(0.5)
            
            print(f"\n{G}=====================================================")
            print(f"{Y}   SUCCESSFULLY COMPLETED BY @MODDING_ZONEE")
            print(f"{G}====================================================={N}")
        else:
            print(f"{R}[!] Signup Failed! API might be blocked.{N}")
    else:
        print(f"{R}[!] Invalid OTP! Execution Stopped.{N}")

if __name__ == "__main__":
    try:
        run_automation()
    except KeyboardInterrupt:
        print(f"\n{R}[!] Stopped by User.{N}")
        sys.exit()
