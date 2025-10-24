import os
from time import sleep
from random import randint
from datetime import datetime
from urllib.parse import quote

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


# ============= CONFIG =============
EXCEL_PATH = r"D:\Projects\whatsapp-blast\birthdays.xlsx"
HBD_MESSAGE_FILE = r"D:\Projects\whatsapp-blast\hbdmessage.txt"
GROUP_MESSAGE_FILE = r"D:\Projects\whatsapp-blast\messagegroup.txt"
USER_DATA_DIR = r"D:\Projects\whatsapp-blast\chrome_user_data"
IMAGE_PATH = r""  # Optional: image for personal messages
DELAY = 20
TITLE = "Birthday Notification"

SEND_PERSONAL = True
SEND_TO_GROUP = True
GROUP_ID = "CBZnKzdPcW92qBvY6CM64Q"

# --- NEW CONFIG ---
HEADLESS = False  # ✅ Set True for headless (no browser UI)
# ==================================


# ============= CONSOLE COLORS =============
class style:
    GREEN = '\033[32m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    RESET = '\033[0m'


print(style.MAGENTA + "🎉 WhatsApp Birthday Notifier by Elvri\n" + style.RESET)
start_time = datetime.now()


# ============= READ EXCEL =============
print("📘 Reading Excel:", EXCEL_PATH)
df = pd.read_excel(EXCEL_PATH)

required_cols = {"name", "nik", "birthdate", "phone"}
if not required_cols.issubset(df.columns):
    raise Exception(f"Excel must have columns: {required_cols}")

df["birthdate"] = pd.to_datetime(df["birthdate"], errors="coerce")
today = datetime.today()
today_md = (today.month, today.day)

birthday_people = df[df["birthdate"].apply(lambda d: (d.month, d.day) == today_md if pd.notnull(d) else False)]

if birthday_people.empty:
    print(style.YELLOW + "No birthdays today 🎂" + style.RESET)
    exit()

print(style.GREEN + f"Found {len(birthday_people)} birthdays today!" + style.RESET)
print(birthday_people[["name", "phone"]])


# ============= READ MESSAGE TEMPLATES =============
if not os.path.exists(HBD_MESSAGE_FILE):
    raise Exception(f"Message file not found: {HBD_MESSAGE_FILE}")
if not os.path.exists(GROUP_MESSAGE_FILE):
    raise Exception(f"Group message file not found: {GROUP_MESSAGE_FILE}")

with open(HBD_MESSAGE_FILE, "r", encoding="utf8") as f:
    personal_template = f.read().strip()

with open(GROUP_MESSAGE_FILE, "r", encoding="utf8") as f:
    group_template = f.read().strip()


def generate_personal_message(name):
    return personal_template.replace("{name}", name)


def generate_group_message(names):
    joined_names = ", ".join(names)
    return group_template.replace("{names}", joined_names)


# ============= SELENIUM SETUP =============
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-infobars")

if HEADLESS:
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    print(style.CYAN + "🧠 Running in HEADLESS mode (no visible browser)" + style.RESET)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.get("https://web.whatsapp.com")


# ============= LOGIN DETECTION =============
print(style.YELLOW + "\n🔍 Checking WhatsApp Web login status..." + style.RESET)
try:
    WebDriverWait(driver, 60).until(lambda d: d.execute_script("return document.readyState") == "complete")

    logged_in = False
    max_wait_time = 30
    check_interval = 3
    waited = 0

    print(style.CYAN + f"⏳ Waiting for WhatsApp Web to be ready (max {max_wait_time}s)..." + style.RESET)
    while waited < max_wait_time:
        elements = driver.find_elements(By.CSS_SELECTOR, "div#side")
        if elements:
            logged_in = True
            break

        qr_code = driver.find_elements(By.CSS_SELECTOR, "canvas[aria-label='Scan me!']")
        if qr_code and waited == 0 and not HEADLESS:
            print(style.MAGENTA + "📱 QR code detected — please scan it with your phone." + style.RESET)

        sleep(check_interval)
        waited += check_interval
        print(style.YELLOW + f" ... waited {waited}s" + style.RESET)

    if logged_in:
        print(style.GREEN + "✅ Session found! Already logged in to WhatsApp Web.\n" + style.RESET)
    else:
        if HEADLESS:
            raise Exception("❌ Headless mode active, but WhatsApp session not found. Please login first in normal mode.")
        print(style.MAGENTA + "\n⚠️ Still not logged in after 30 seconds." + style.RESET)
        input(style.MAGENTA + "✅ Please log in manually, then press ENTER when chats are visible..." + style.RESET)

except Exception as e:
    print(style.RED + f"Error checking login status: {e}" + style.RESET)
    if not HEADLESS:
        input(style.MAGENTA + "Press ENTER after logging in manually..." + style.RESET)
    else:
        driver.quit()
        raise


# ============= SEND PERSONAL MESSAGES =============
failed = []

if SEND_PERSONAL:
    for i, row in birthday_people.iterrows():
        number = str(row["phone"]).strip()
        name = str(row["name"]).strip()

        if not number or number.lower() == "nan":
            continue

        msg = generate_personal_message(name)
        encoded_msg = quote(msg)

        print(style.YELLOW + f"\n🎈 Sending to {name} ({number})..." + style.RESET)
        try:
            driver.get(f"https://web.whatsapp.com/send?phone={number}&text={encoded_msg}")

            click_btn = WebDriverWait(driver, DELAY).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='wds-ic-send-filled']"))
            )
            sleep(1)
            click_btn.click()
            sleep(3)
            print(style.GREEN + f"✅ Message sent to {name}" + style.RESET)

            # Optional: send image
            if IMAGE_PATH:
                attach_btn = WebDriverWait(driver, DELAY).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='plus-rounded']"))
                )
                attach_btn.click()
                file_box = driver.find_element(By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']")
                file_box.send_keys(IMAGE_PATH)
                send_btn = WebDriverWait(driver, DELAY).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='wds-ic-send-filled']"))
                )
                send_btn.click()
                sleep(1)
                print(style.GREEN + f"📎 Image sent to {name}" + style.RESET)

        except TimeoutException:
            print(style.RED + f"❌ Timeout sending to {name} ({number})" + style.RESET)
            failed.append(f"{name} - {number}")
        except Exception as e:
            print(style.RED + f"❌ Failed to send to {name} ({number}): {e}" + style.RESET)
            failed.append(f"{name} - {number}")

        sleep(randint(3, 8))


# ============= SEND TO GROUP (ONCE ONLY) =============
if SEND_TO_GROUP and GROUP_ID:
    try:
        print(style.CYAN + f"\n📢 Sending message to group via GROUP ID..." + style.RESET)

        group_url = f"https://web.whatsapp.com/accept?code={GROUP_ID}"
        driver.get(group_url)
        sleep(10)

        group_msg = generate_group_message(birthday_people["name"].tolist())

        msg_box = WebDriverWait(driver, DELAY).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='textbox' and contains(@aria-label, 'Type to group')]"))
        )

        driver.execute_script("arguments[0].focus();", msg_box)
        sleep(1)

        driver.execute_script("""
            const el = arguments[0];
            const text = arguments[1];
            el.focus();
            const dt = new DataTransfer();
            dt.setData('text/plain', text);
            const pasteEvent = new ClipboardEvent('paste', {
                bubbles: true,
                cancelable: true,
                clipboardData: dt
            });
            el.dispatchEvent(pasteEvent);
        """, msg_box, group_msg)

        sleep(1.5)
        msg_box.send_keys(Keys.ENTER)
        sleep(3)

        print(style.GREEN + "✅ Group message sent successfully!" + style.RESET)

    except TimeoutException:
        print(style.RED + "❌ Timeout — group chat did not load properly." + style.RESET)
    except Exception as e:
        print(style.RED + f"❌ Failed to send message to group: {e}" + style.RESET)


# ============= SUMMARY =============
driver.quit()
end_time = datetime.now()
elapsed = end_time - start_time

print(style.CYAN + f"\nDone in {elapsed}" + style.RESET)

if failed:
    print(style.RED + f"\nFailed to send to {len(failed)} contacts:" + style.RESET)
    for f in failed:
        print(" -", f)
