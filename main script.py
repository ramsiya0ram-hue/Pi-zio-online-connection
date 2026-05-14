import requests
import random
import string
import sys
from datetime import datetime

# --- COLORS DEFINITION ---
R = '\033[1;31m'  # Red
G = '\033[1;32m'  # Green
Y = '\033[1;33m'  # Yellow
B = '\033[1;34m'  # Blue
P = '\033[1;35m'  # Purple
C = '\033[1;36m'  # Cyan
W = '\033[1;37m'  # White
N = '\033[0m'     # Reset

# --- ONLINE EXPIRY CONFIG ---
# अपनी GitHub Raw लिंक यहाँ डालें। फाइल में तारीख इस तरह लिखें: 2026-05-30
EXPIRY_URL = "https://raw.githubusercontent.com/ramsiya0ram-hue/Piczio-connection/refs/heads/main/piczio%20contro.txt" 

# --- CONFIGURATION ---
API_KEY = "gAAAAABkrjh_9CibQaJvdxQtJdQIlM-ILat3XU3sI4DNcMmtW2zTs-5-1LpEOmTaLNgvUHZu4mp1WEcdHSHsOYE5tf80QWAvYQ=="
BASE_URL = "https://piczio.app/api/v1"

# इन आईडी को फॉलो किया जाएगा
FOLLOW_LIST = [40181, 24, 38946] 

# पोस्ट आईडीज़
POST_IDS = [337077, 337090, 337103] # अपनी पूरी लिस्ट यहाँ डालें

# नकली पहचान डेटा
FIRST_NAMES = ["Amit", "Rahul", "Sandeep", "Deepak", "Vivek", "Arjun", "Aditya", "Rohan", "Priya", "Anjali"]
LAST_NAMES = ["Kumar", "Singh", "Sharma", "Verma", "Yadav", "Gupta"]

def check_expiry():
    """ऑनलाइन तारीख चेक करने के लिए फंक्शन"""
    try:
        print(f"{Y}[*] Checking License Status...{N}")
        response = requests.get(EXPIRY_URL, timeout=10)
        online_date_str = response.text.strip()
        
        # ऑनलाइन तारीख को Python Date ऑब्जेक्ट में बदलना
        expiry_date = datetime.strptime(online_date_str, "%Y-%m-%d").date()
        today = datetime.now().date()

        if today > expiry_date:
            print(f"\n{R}╔══════════════════════════════════════════════╗")
            print(f"║  {W}❌ SCRIPT EXPIRED!                          {R}║")
            print(f"║  {Y}Expired On: {W}{online_date_str}              {R}║")
            print(f"║  {C}Contact: @Modding_Zonee to renew license    {R}║")
            print(f"╚══════════════════════════════════════════════╝{N}")
            sys.exit()
        else:
            print(f"{G}[✓] License Active ✅  Expires: Next Update")
    except Exception as e:
        print(f"{R}[!] Online License Verification Failed!{N}")
        print(f"{Y}[!] Please check your internet connection or URL.{N}")
        sys.exit()

def banner():
    print(f"""
{C}╔══════════════════════════════════════════════════════╗
{C}║  {Y}☠️  MODDING ZONE MEGA AUTOMATION  ☠️  {C}║
{C}║  {W}Developer: {G}@Modding_Zonee                    {C}║
{C}╚══════════════════════════════════════════════════════╝{N}
    """)

def generate_real_identity():
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    fullname = f"{first} {last}"
    username = f"{first.lower()}{random.choice(['_', '.'])}{last.lower()}{random.randint(100, 999)}"
    return fullname, username

def get_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_device_token():
    return "f" + get_random_string(10) + ":" + get_random_string(140)

def run_automation():
    # सबसे पहले एक्सपायरी चेक होगी
    check_expiry()
    
    banner()
    fullname, username = generate_real_identity()
    print(f"{Y}[!] Generating Profile: {W}{fullname} (@{username})")
    
    target_email = input(f"{C}[+] Enter Gmail ID for OTP: {W}")

    headers = {
        "api-key": API_KEY, 
        "user-agent": "okhttp/5.1.0", 
        "content-type": "application/json; charset=UTF-8"
    }
    fake_phone = "9" + "".join(random.choices(string.digits, k=9))

    print(f"{Y}[*] Sending OTP to {target_email}...{N}")
    requests.post(f"{BASE_URL}/auth/check-user", headers=headers, json={"country_code": "+91", "phone_number": fake_phone})
    requests.post(f"{BASE_URL}/auth/send-otp", headers=headers, json={"country_code": "+91", "phone_number": fake_phone, "email": target_email})

    otp_code = input(f"{C}[+] Enter Received OTP: {W}")
    v_res = requests.post(f"{BASE_URL}/auth/verify-otp", headers=headers, json={"country_code": "+91", "phone_number": fake_phone, "otp": otp_code})
    
    if v_res.json().get("code") == 1:
        print(f"{G}[✓] OTP Verified! Creating Account...{N}")
        signup_payload = {
            "app_version": "1.6.6", "login_type": "S", "os_version": "35", "device_type": "A",
            "device_token": generate_device_token(),
            "uu_id_number": f"{get_random_string(8)}-{get_random_string(4)}-4555-a888-{get_random_string(12)}",
            "password": "User@123", "country_code": "+91",
            "phone_number": fake_phone, "email": target_email, "username": username, "fullname": fullname
        }
        
        final_res = requests.post(f"{BASE_URL}/auth/signup", headers=headers, json=signup_payload).json()
        token = final_res.get('data', {}).get('token')

        if token:
            print(f"{G}[✓] Account Created Successfully!{N}")
            auth_headers = headers.copy()
            auth_headers["authorization"] = f"TOKEN {token}"
            
            # Follow Loop
            print(f"{P}[>] Following Targeted Profiles...{N}")
            for target_id in FOLLOW_LIST:
                requests.post(f"{BASE_URL}/auth/follow-following/add-follow-request", headers=auth_headers, json={"instance_id": target_id})
                print(f"    {W}[Followed] ID {target_id}")

            # Engagement Loop
            print(f"{P}[>] Boosting {len(POST_IDS)} Posts (Likes + Views)...{N}")
            for i, p_id in enumerate(POST_IDS, start=1):
                try:
                    requests.post(f"{BASE_URL}/post/post-like", headers=auth_headers, json={"post": p_id}, timeout=10)
                    requests.post(f"{BASE_URL}/post/update-post-view", headers=auth_headers, json={"post": p_id}, timeout=10)
                    print(f"    {B}[{i}] {W}Post {p_id}: {G}Done ✓{N}")
                except:
                    print(f"    {R}[{i}] Post {p_id}: Failed ✘{N}")
            
            print(f"\n{G}══════════════════════════════════════════════════")
            print(f"{Y}DONE BY ☠️ MODDING ZONE ☠️")
            print(f"{W}Account: {C}{username} {W}| Status: {G}Fully Optimized")
            print(f"{G}══════════════════════════════════════════════════{N}")
        else:
            print(f"{R}[!] Signup Failed: {final_res.get('message')}{N}")
    else:
        print(f"{R}[!] OTP Verification Failed!{N}")

if __name__ == "__main__":
    try:
        run_automation()
    except KeyboardInterrupt:
        print(f"\n\n{R}[!] STOPPED BY USER: ☠️ MODDING ZONE ☠️ (@Modding_Zonee){N}")
        sys.exit()
    except Exception as e:
        print(f"\n\n{R}[!] ERROR: Please contact @Modding_Zonee")
        print(f"{Y}Message: {W}{e}{N}")
