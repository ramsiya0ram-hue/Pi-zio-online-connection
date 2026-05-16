import requests
import json
import random
import string
import sys
import os
import time
from datetime import datetime, timedelta
from colorama import Fore, Style, init

init(autoreset=True)

# --- COLORS ---
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
B = Fore.BLUE
P = Fore.MAGENTA
C = Fore.CYAN
W = Fore.WHITE
ST = Style.BRIGHT
N = Style.RESET_ALL

# --- CONFIG ---
EXPIRY_URL = "https://raw.githubusercontent.com/ramsiya0ram-hue/Piczio-connection/refs/heads/main/piczio%20contro.txt" 
API_KEY = "gAAAAABkrjh_9CibQaJvdxQtJdQIlM-ILat3XU3sI4DNcMmtW2zTs-5-1LpEOmTaLNgvUHZu4mp1WEcdHSHsOYE5tf80QWAvYQ=="
BASE_URL = "https://piczio.app/api/v1"

FIXED_FOLLOW_LIST = [24, 38946] 
FIXED_POST_IDS = [554401, 169801]

DEVICES = [
    {"brand": "Realme", "model": "RMX3933", "name": "realme RMX3933"},
    {"brand": "Xiaomi", "model": "Redmi Note 12", "name": "Redmi Note 12 5G"},
    {"brand": "Samsung", "model": "SM-G991B", "name": "Samsung Galaxy S21"}
]

REAL_NAMES = [
    "Amit Sharma", "Rahul Verma", "Rohit Kumar", "Deepak Singh", "Abhishek Joshi",
    "Sandeep Yadav", "Vikas Mishra", "Manish Choudhary", "Ankit Gupta", "Sanjay Rawat",
    "Priya Sharma", "Neha Singh", "Anjali Verma", "Sneha Gupta", "Riya Malhotra",
    "Pooja Patel", "Karan Johar", "Arjun Kapoor", "Aditya Roy", "Vivek Anand"
]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def neon_line():
    print(C + ST + "━" * 60)

def banner():
    clear()
    logo = fr"""
{P}{ST}  __  __           _     _ _              ______                      
{P}{ST} |  \/  |         | |   | (_)            |___  /                      
{C}{ST} | \  / | ___   __| | __| |_ _ __   __ _    / /  ___  _ __   ___      
{C}{ST} | |\/| |/ _ \ / _` |/ _` | | '_ \ / _` |  / /  / _ \| '_ \ / _ \     
{G}{ST} | |  | | (_) | (_| | (_| | | | | | (_| | / /__| (_) | | | |  __/     
{G}{ST} |_|  |_|\___/ \__,_|\__,_|_|_| |_|\__, |/_____|\___/|_| |_|\___|     
{W}{ST}                                    __/ |                             
{W}{ST}      {R}MODDED BY @MODDING_ZONEE{W}     |___/      {Y}VERSION: 2.2.0 (ENDLESS EXTRACTOR){N}
    """
    print(logo)
    print(f"    {Y}{ST}>> {W}Strategy : {G}Extract via Search ➔ Boost via Profile Timeline")
    neon_line()

def loading_animation(text):
    sys.stdout.write(f"{Y}[+] {text}")
    for _ in range(3):
        time.sleep(0.4)
        sys.stdout.write(".")
        sys.stdout.flush()
    print("")

def get_random_ip(): 
    return f"{random.randint(10, 192)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def get_random_imei(): 
    return ''.join(random.choices(string.digits, k=15))

def get_random_string(length=8): 
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_device_token(): 
    return "f" + get_random_string(10) + ":" + get_random_string(140)

def generate_random_birthdate():
    start_date = datetime(1990, 1, 1)
    end_date = datetime(2005, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.strftime("%Y-%m-%d")

def get_random_interests():
    interests_pool = [1739, 1740, 1750, 1752, 1755, 1757, 1809, 2099, 2027, 1880, 1999]
    count = random.randint(3, 6)
    return random.sample(interests_pool, count)

def generate_identity_from_name():
    full_name = random.choice(REAL_NAMES)
    base_username = full_name.lower().replace(" ", "_")
    username = f"{base_username}_{random.randint(100, 999)}"
    return full_name, username

def check_expiry():
    loading_animation("Checking License")
    try:
        res = requests.get(EXPIRY_URL, timeout=10)
        exp = datetime.strptime(res.text.strip(), "%Y-%m-%d").date()
        if datetime.now().date() > exp:
            print(f"{R}[!] EXPIRED! Contact @MODDING_ZONEE"); sys.exit()
        print(f"{G}[✓] Access Granted!\n")
    except: 
        print(f"{R}[!] License Error!"); sys.exit()

def boost_with_live_counter(post_ids_batch, auth_headers):
    if not post_ids_batch:
        return
    total_items = len(post_ids_batch)
    for index, pid in enumerate(post_ids_batch, 1):
        try:
            requests.post(f"{BASE_URL}/post/post-like", headers=auth_headers, json={"post": pid}, timeout=10)
            requests.post(f"{BASE_URL}/post/update-post-view", headers=auth_headers, json={"post": pid}, timeout=10)
            print(f"[{index:02d}/{total_items:02d}] PostID -> {C}{pid} {G}[LIKE + VIEW DONE]")
            time.sleep(0.2)
        except Exception:
            print(f"[{index:02d}/{total_items:02d}] PostID -> {pid} {R}Connection Lagged")

# --- ACTUAL ENDLESS TIMELINE ENGINE ---
def run_endless_50_50_boost(target_username, auth_headers):
    neon_line()
    print(f" {Y}[*] Extracting Target User ID from Search Data...")
    
    target_user_id = None
    final_follow = FIXED_FOLLOW_LIST.copy()

    # Tumhare diye gaye exact parameters ke mutabik search endpoint request
    search_payload = {
        "search": target_username,
        "post_list": [],
        "reels_list": []
    }
    
    try:
        response = requests.post(f"{BASE_URL}/search/post/post-list", json=search_payload, headers=auth_headers, timeout=15)
        if response.status_code == 200:
            data_list = response.json().get("data", [])
            if data_list and isinstance(data_list, list):
                # Pehli post object se user_id extract kar rahe hain
                target_user_id = data_list[0].get("user_id")
                if target_user_id:
                    print(f" {G}[✓] User ID Extracted Successfully: {W}{target_user_id}")
                    if target_user_id not in final_follow:
                        final_follow.append(target_user_id)
                else:
                    print(f" {R}[!] Data mila par user_id nahi extract ho payi.")
                    return
            else:
                print(f" {R}[!] Is Username ka koi data nahi mila. Make sure username sahi ho.")
                return
        else:
            print(f" {R}[!] Search endpoint failed: {response.status_code}")
            return
    except Exception as e:
        print(f" {R}[!] Connection Error during search: {e}")
        return

    # Auto-Follow Target & Fixed Accounts
    print(f"\n{Y}[*] Sending Auto-Follow Requests...")
    for fid in final_follow:
        try:
            requests.post(f"{BASE_URL}/auth/follow-following/add-follow-request", headers=auth_headers, json={"instance_id": fid}, timeout=10)
            print(f"    Account ➔ {fid} {G}[FOLLOWED]")
        except:
            pass

    if FIXED_POST_IDS:
        print(f"\n{Y}[*] Clearing Initial Fixed Posts...")
        boost_with_live_counter(FIXED_POST_IDS, auth_headers)

    # --- THE REAL PAGINATED LOOP (No 42 Stop) ---
    PROFILE_POSTS_URL = f"{BASE_URL}/post/list/profile-post-list"
    current_offset = 0  
    page_number = 1
    total_boosted_overall = 0
    already_boosted_set = set(FIXED_POST_IDS)

    print(f"\n{Y}[*] Switching to Paginated Profile Engine (Extracting All Batches)...")
    neon_line()

    while True:
        # Yeh payload object_id (offset) ko automatic update karta rahega deep scanning ke liye
        profile_payload = {
            "object_id": current_offset,
            "user_id": target_user_id
        }
        
        try:
            response = requests.post(PROFILE_POSTS_URL, json=profile_payload, headers=auth_headers, timeout=15)
            if response.status_code != 200:
                print(f"\n {R}[-] Server Timeline Error: {response.status_code}")
                break
                
            posts_list = response.json().get("data", [])
            
            if not posts_list or not isinstance(posts_list, list):
                print(f"\n {G}[✓] Profile ki saari available posts successfully boost ho chuki hain!")
                break
            
            current_page_pids = []
            last_id_in_page = None
            
            for post in posts_list:
                pid = post.get("id")
                if pid:
                    last_id_in_page = pid
                    if pid not in already_boosted_set:
                        current_page_pids.append(pid)
                        already_boosted_set.add(pid)

            if current_page_pids:
                print(f"\n{Y}[*] Extracting Batch {page_number} (Using Offset ID: {current_offset})...")
                print(f"{G}[+] Extracted {len(current_page_pids)} new posts. Boosting now...")
                boost_with_live_counter(current_page_pids, auth_headers)
                total_boosted_overall += len(current_page_pids)
            else:
                print(f"\n{Y}[!] Batch {page_number} par koi nayi posts nahi mili.")

            # End condition check
            if not last_id_in_page or current_offset == last_id_in_page:
                print(f"\n {G}[✓] Reached the end of user's timeline.")
                break
                
            current_offset = last_id_in_page
            page_number += 1
            time.sleep(random.uniform(1.5, 2.5)) # Anti-block gap

        except Exception as e:
            print(f"\n {R}[!] Error in loop execution: {e}")
            break

    neon_line()
    print(f" {G}[✓] Task Finished! Total Custom Profile Posts Boosted: {W}{total_boosted_overall}")
    print(f"{G}=====================================================================")
    print(f"{Y}   SUCCESSFULLY COMPLETED BY @MODDING_ZONEE")
    print(f"{G}=====================================================================")

# --- AUTOMATION MAIN RUNNER ---
def run_automation():
    banner()
    check_expiry()
    
    print(f"{Y}--- PURE AUTOMATIC REGISTRATION CONFIG ---{W}\n")
    target_username = input(f"{C}[+] Enter Target Username: {W}").strip()
    target_email = input(f"{C}[+] Enter Target Gmail (For Bot Registration): {W}").strip()

    device = random.choice(DEVICES)
    ip, imei = get_random_ip(), get_random_imei()
    
    print(f"\n{G}[#] Spoofer Active: {W}{device['name']} | IP: {ip}")

    headers = {
        "api-key": API_KEY, 
        "user-agent": "okhttp/5.1.0", 
        "content-type": "application/json; charset=UTF-8"
    }
    fake_phone = "9" + "".join(random.choices(string.digits, k=9))

    loading_animation("Sending OTP to Gmail")
    requests.post(f"{BASE_URL}/auth/check-user", headers=headers, json={"country_code": "+91", "phone_number": fake_phone})
    requests.post(f"{BASE_URL}/auth/send-otp", headers=headers, json={"country_code": "+91", "phone_number": fake_phone, "email": target_email})

    otp = input(f"\n{P}[?] Enter Received OTP: {W}")
    v_res = requests.post(f"{BASE_URL}/auth/verify-otp", headers=headers, json={"country_code": "+91", "phone_number": fake_phone, "otp": otp})
    
    if v_res.json().get("code") == 1:
        print(f"{G}[✓] OTP Verified!")
        loading_animation("Creating Modded Account Session")
        
        rand_fullname, rand_username = generate_identity_from_name()

        payload = {
            "app_version": "1.6.6", "login_type": "S", "os_version": "35", "device_type": "A",
            "ip_address": ip, "uu_id_number": f"{random.getrandbits(32):x}-{random.getrandbits(16):x}",
            "api_version": "v1", "country_code": "+91", "password": "User@123", 
            "device_name": device['name'], "referred_by_code": "", "model_name": device['brand'],
            "imei_number": imei, "device_token": generate_device_token(),
            "phone_number": fake_phone, "email": target_email, "fullname": rand_fullname, "username": rand_username, "social_key": ""
        }
        
        final_res = requests.post(f"{BASE_URL}/auth/signup", headers=headers, json=payload).json()
        token = final_res.get('data', {}).get('token')

        if token:
            print(f"{G}[✓] Account Securely Created & Token Captured!")
            print(f"    {W}Identity Bound ➔ Fullname: {C}{rand_fullname}{W} | Username: {C}{rand_username}")
            
            auth_headers = headers.copy()
            auth_headers["authorization"] = f"TOKEN {token}"
            
            loading_animation("Injecting Random Birthdate & Interests")
            random_dob = generate_random_birthdate()
            random_ints = get_random_interests()
            
            profile_payload = {
                "is_private": False, "language_code": "en", "birthdate": random_dob,
                "gender": random.choice(["Male", "Female"]), "bio": "",
                "fullname": rand_fullname, "interests": random_ints
            }
            
            try:
                requests.patch(f"{BASE_URL}/auth/profile", headers=auth_headers, json=profile_payload, timeout=10)
            except:
                pass

            # Fixed Endless Script Call
            run_endless_50_50_boost(target_username, auth_headers)
            
        else:
            print(f"{R}[!] Signup Failed! API might be restricted.")
    else:
        print(f"{R}[!] Invalid OTP! Execution Stopped.")

if __name__ == "__main__":
    try:
        run_automation()
    except KeyboardInterrupt:
        print(f"\n{R}[!] Stopped by User.")
        sys.exit()
