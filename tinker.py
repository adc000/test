import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import string
from tkinter.filedialog import asksaveasfilename
import threading
import os
import subprocess
import requests
import webbrowser
import sys

import requests

URLS = [
    "https://toto-go.com",
    "https://todayzo.com",
    "https://lintoday.me"
]

CURRENT_VERSION = "v2.3.2"

urls = []
titletxt = ""
subjecttxt = ""

def check_urls():
    results = []
    has_failure = False

    for url in URLS:
        try:
            response = requests.head(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=3)
            results.append(f"✅ {url.replace('https://', '').replace('http://', '')} 접속 성공")
        except requests.RequestException:
            results.append(f"❌ {url.replace('https://', '').replace('http://', '')} 접속 실패!")
            has_failure = True

    return "\n".join(results), has_failure

def check_for_update():
    try:
        response = requests.get("https://api.github.com/repos/adc000/Hongbo/releases/latest")
        latest_version = response.json()["tag_name"]

        if CURRENT_VERSION != latest_version:
            messagebox.showinfo("업데이트 필요", f"최신 버전 {latest_version}이(가) 있습니다.")
            webbrowser.open("https://github.com/adc000/Hongbo/releases/tag/{}".format(latest_version))
            root.destroy()
            sys.exit()
    except requests.RequestException as e:
        messagebox.showerror("오류", f"업데이트 확인 중 오류가 발생했습니다: {e}")
        root.destroy()
        sys.exit()

# 메모장으로 파일 열기 함수
def open_in_notepad(file_path):
    if os.path.exists(file_path):
        subprocess.Popen(["notepad.exe", os.path.realpath(file_path)])
    else:
        messagebox.showerror("Error", "File not found!")

# 알림창 띄우기 함수
def show_notification(file_path):
    answer = messagebox.askyesno("홍보 끝", f"{os.path.realpath(file_path)} 파일을 확인하시겠습니까?")
    if answer:
        open_in_notepad(file_path)

def generate_random_string(length=30):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choices(characters, k=length))
    return random_string

def totogo(id, pw, s, cnt, driver, file_path, cnt_label):
    # 토토고
    driver.get("https://toto-go.com/")
    username = driver.find_element(By.NAME, "mb_id")
    password = driver.find_element(By.NAME, "mb_password")
    username.send_keys(id)
    password.send_keys(pw)

    login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-block.btn-lg.en")
    login_button.click()

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    for i in range(int(cnt)):
        driver.get("https://toto-go.com/promotion/write")

        title = driver.find_element(By.NAME, "wr_subject")
        title.send_keys("{0}{1}".format(titletxt, generate_random_string()))

        outer_iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src='https://toto-go.com/plugin/editor/smarteditor2/SmartEditor2Skin.html']"))
        )
        driver.switch_to.frame(outer_iframe)

        inner_iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe#se2_iframe"))
        )
        driver.switch_to.frame(inner_iframe)

        editable_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body[contenteditable='true']"))
        )

        editable_area.clear()
        editable_area.send_keys(f"{subjecttxt}")

        driver.switch_to.default_content()

        login_button = driver.find_element(By.ID, "btn_submit")
        login_button.click()

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("글 작성 완료. 현재 URL:", driver.current_url)
        urls.append(driver.current_url)
        file = open(file_path, "a", encoding="utf-8")
        file.write("{0} {1}\n".format(int(s) + i + 1, driver.current_url))
        file.close()
        cnt_label.config(text="{0}".format(i+1))
        if i+1 < int(cnt):
            time.sleep(30)

def todayzo(id, pw, s, cnt, driver, file_path, cnt_label):
    # 투데이존
    driver.get("https://todayzo.com/")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    username = driver.find_element(By.NAME, "mb_id")
    password = driver.find_element(By.NAME, "mb_password")
    username.send_keys(id)
    password.send_keys(pw)

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ol_submit"))
    )
    login_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    for i in range(int(cnt)):
        driver.get("https://todayzo.com/maple/write")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        title = driver.find_element(By.NAME, "wr_subject")
        title.send_keys(f"{titletxt}")
        subject = driver.find_element(By.NAME, "wr_content")
        subject.send_keys(f"{subjecttxt}")
        submit_button = driver.find_element(By.ID, "btn_submit")
        submit_button.click()
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        print("글 작성 완료. 현재 URL:", driver.current_url)
        urls.append(driver.current_url)
        file = open(file_path, "a", encoding="utf-8")
        file.write("{0} {1}\n".format(int(s) + i + 1, driver.current_url))
        file.close()
        cnt_label.config(text="{0}".format(i+1))

def lintoday(id, pw, s, cnt, driver, file_path, cnt_label):
    # 린투데이
    driver.get("https://lintoday.me/")
    try:
        button = driver.find_element(By.CSS_SELECTOR, "button.hd_pops_reject.hd_pops_1")
        button.click()
    except Exception as e:
        print("에러 발생:", e)

    try:
        button = driver.find_element(By.CSS_SELECTOR, "button.hd_pops_reject.hd_pops_4")
        button.click()
    except Exception as e:
        print("에러 발생:", e)

    try:
        button = driver.find_element(By.CSS_SELECTOR, "button.hd_pops_reject.hd_pops_5")
        button.click()
    except Exception as e:
        print("에러 발생:", e)

    username = driver.find_element(By.NAME, "mb_id")
    password = driver.find_element(By.NAME, "mb_password")
    username.send_keys(id)
    password.send_keys(pw)
    login_button = driver.find_element(By.ID, "ol_submit")
    login_button.click()

    try:
        driver.get("https://lintoday.me/plugin/attendance/")
        attendance_button = driver.find_element(By.CLASS_NAME, "sat_form_btn")
        attendance_button.click()

        alert = driver.switch_to.alert
        print("Alert 텍스트:", alert.text)

        alert.accept()

    except Exception as e:
        print("에러 발생:", e)
    finally:
        print("done")


    for i in range(int(cnt)):
        driver.get("https://lintoday.me/bbs/write.php?bo_table=22")
        title = driver.find_element(By.NAME, "wr_subject")
        title.send_keys(f"{titletxt}")

        outer_iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src='https://lintoday.me/plugin/editor/smarteditor2/SmartEditor2Skin.html']"))
        )
        driver.switch_to.frame(outer_iframe)

        inner_iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe#se2_iframe"))
        )
        driver.switch_to.frame(inner_iframe)

        editable_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body[contenteditable='true']"))
        )

        editable_area.clear()
        editable_area.send_keys(f"{subjecttxt}")

        driver.switch_to.default_content()

        button = driver.find_element(By.XPATH, "//button[@accesskey='s']")
        button.click()

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        print("글 작성 완료. 현재 URL:", driver.current_url)
        urls.append(driver.current_url)
        file = open(file_path, "a", encoding="utf-8")
        file.write("{0} {1}\n".format(int(s) + i + 1, driver.current_url))
        file.close()
        cnt_label.config(text="{0}".format(i+1))

def run_test():
    thread = threading.Thread(target=test)
    thread.daemon = True
    thread.start()

def test():
    s1 = 0
    if cnt_entry1.get() == "":
        s2 = 0
        print(cnt_entry1.get())
    else:
        s2 = int(cnt_entry1.get())

    if cnt_entry2.get() == "":
        s3 = s2
    else:
        s3 = s2 + int(cnt_entry2.get())

    if cnt_entry3.get() == "":
        s4 = s3
    else:
        s4 = s3 + int(cnt_entry3.get())
    inputs = {
        "세트 1": (id_entry1.get(), pw_entry1.get(), cnt_entry1.get(), cnt_label1, totogo, s1),
        "세트 2": (id_entry2.get(), pw_entry2.get(), cnt_entry2.get(), cnt_label2, todayzo, s2),
        "세트 3": (id_entry3.get(), pw_entry3.get(), cnt_entry3.get(), cnt_label3, todayzo, s3),
        "세트 4": (id_entry4.get(), pw_entry4.get(), cnt_entry4.get(), cnt_label4, lintoday, s4),
    }

    id_entry1.config(state="disabled")
    pw_entry1.config(state="disabled")
    cnt_entry1.config(state="disabled")

    id_entry2.config(state="disabled")
    pw_entry2.config(state="disabled")
    cnt_entry2.config(state="disabled")

    id_entry3.config(state="disabled")
    pw_entry3.config(state="disabled")
    cnt_entry3.config(state="disabled")

    id_entry4.config(state="disabled")
    pw_entry4.config(state="disabled")
    cnt_entry4.config(state="disabled")

    executed = False

    file_path = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("텍스트 파일", "*.txt")],
        title="파일 저장"
    )
    if not file_path:
        file_path = "./default.txt"

    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-logging")
    options.add_argument("--start-maximized")


    for set_name, (id_val, pw_val, cnt, cnt_label, action, s) in inputs.items():
        if id_val and pw_val and cnt:
            driver = webdriver.Chrome(service=service, options=options)
            action(id_val, pw_val, s, cnt, driver, file_path, cnt_label)
            file = open(file_path, "a", encoding="utf-8")
            file.write("\n")
            file.close()
            driver.quit()
            executed = True

    if not executed:
        messagebox.showerror("오류", "모든 세트가 비어 있습니다. 값을 입력해주세요.")
        driver.quit()
        return

    driver.quit()

    id_entry1.config(state="normal")
    pw_entry1.config(state="normal")
    cnt_entry1.config(state="normal")

    id_entry2.config(state="normal")
    pw_entry2.config(state="normal")
    cnt_entry2.config(state="normal")

    id_entry3.config(state="normal")
    pw_entry3.config(state="normal")
    cnt_entry3.config(state="normal")

    id_entry4.config(state="normal")
    pw_entry4.config(state="normal")
    cnt_entry4.config(state="normal")


    answer = messagebox.askyesno("홍보끝", "클립보드에 url들을 복사하시겠습니까?")
    if answer:
        root.clipboard_clear()
        for idx, url in enumerate(urls):
            root.clipboard_append("{0}. {1}\n".format(idx, url))

    import os
    show_notification(os.path.realpath(file_path))
    root.destroy()

root = tk.Tk()
root.title("홍보 자동화 툴")

root.withdraw()

if os.path.exists("./README.txt"):
    with open("./README.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    if lines:
        title = lines[0].strip()
        content = "".join(lines[1:]).strip()
        if messagebox.askyesno(f"{title} 업데이트", f"{content}\n\n다시 보지 않으려면 예를 누르세요."):
            os.remove("./README.txt")

check_for_update()

while True:
    result_string, has_failure = check_urls()
    if has_failure:
        response = messagebox.askyesnocancel("접속 확인 결과", f"{result_string}\n\n일부 사이트에 접속이 불가능합니다.\n재시도(예) / 무시(아니오) / 취소(프로그램 종료)",
                                            icon="warning")
        if response is None:
            root.quit()
            sys.exit()
        elif response is False:
            break
        else:
            continue
    else:
        messagebox.showinfo("접속 확인 결과", f"{result_string}\n\n모든 사이트에 접속이 정상적입니다.",
                            icon="info")
        break

root.deiconify()

entries = []

tk.Label(root, text="toto-go.com").grid(row=0, column=0, columnspan=4, padx=5, pady=5)
tk.Label(root, text="ID").grid(row=1, column=0, padx=5, pady=5, sticky="e")
id_entry1 = tk.Entry(root, width=30)
id_entry1.grid(row=1, column=2, padx=5, pady=5)
entries.append(id_entry1)

tk.Label(root, text="PW").grid(row=2, column=0, padx=5, pady=5, sticky="e")
pw_entry1 = tk.Entry(root, width=30)
pw_entry1.grid(row=2, column=2, padx=5, pady=5)
entries.append(pw_entry1)

tk.Label(root, text="CNT").grid(row=3, column=0, padx=5, pady=5, sticky="e")
cnt_label1 = tk.Label(root, text="0")
cnt_label1.grid(row=3, column=1, padx=5, pady=5, sticky="w")
cnt_entry1 = tk.Entry(root, width=30)
cnt_entry1.grid(row=3, column=2, padx=5, pady=5)
entries.append(cnt_entry1)


tk.Label(root, text="todayzo.com").grid(row=4, column=0, columnspan=4, padx=5, pady=5)
tk.Label(root, text="ID1").grid(row=5, column=0, padx=5, pady=5, sticky="e")
id_entry2 = tk.Entry(root, width=30)
id_entry2.grid(row=5, column=2, padx=5, pady=5)
entries.append(id_entry2)

tk.Label(root, text="PW1").grid(row=6, column=0, padx=5, pady=5, sticky="e")
pw_entry2 = tk.Entry(root, width=30)
pw_entry2.grid(row=6, column=2, padx=5, pady=5)
entries.append(pw_entry2)

tk.Label(root, text="CNT").grid(row=7, column=0, padx=5, pady=5, sticky="e")
cnt_label2 = tk.Label(root, text="0")
cnt_label2.grid(row=7, column=1, padx=5, pady=5, sticky="w")
cnt_entry2 = tk.Entry(root, width=30)
cnt_entry2.grid(row=7, column=2, padx=5, pady=5)
entries.append(cnt_entry2)


tk.Label(root, text="todayzo.com").grid(row=8, column=0, columnspan=4, padx=5, pady=5)
tk.Label(root, text="ID2").grid(row=9, column=0, padx=5, pady=5, sticky="e")
id_entry3 = tk.Entry(root, width=30)
id_entry3.grid(row=9, column=2, padx=5, pady=5)
entries.append(id_entry3)

tk.Label(root, text="PW2").grid(row=10, column=0, padx=5, pady=5, sticky="e")
pw_entry3 = tk.Entry(root, width=30)
pw_entry3.grid(row=10, column=2, padx=5, pady=5)
entries.append(pw_entry3)

tk.Label(root, text="CNT").grid(row=11, column=0, padx=5, pady=5, sticky="e")
cnt_label3 = tk.Label(root, text="0")
cnt_label3.grid(row=11, column=1, padx=5, pady=5, sticky="w")
cnt_entry3 = tk.Entry(root, width=30)
cnt_entry3.grid(row=11, column=2, padx=5, pady=5)
entries.append(cnt_entry3)


tk.Label(root, text="lintoday.me").grid(row=12, column=0, columnspan=4, padx=5, pady=5)
tk.Label(root, text="ID").grid(row=13, column=0, padx=5, pady=5, sticky="e")
id_entry4 = tk.Entry(root, width=30)
id_entry4.grid(row=13, column=2, padx=5, pady=5)
entries.append(id_entry4)

tk.Label(root, text="PW").grid(row=14, column=0, padx=5, pady=5, sticky="e")
pw_entry4 = tk.Entry(root, width=30)
pw_entry4.grid(row=14, column=2, padx=5, pady=5)
entries.append(pw_entry4)

tk.Label(root, text="CNT").grid(row=15, column=0, padx=5, pady=5, sticky="e")
cnt_label4 = tk.Label(root, text="0")
cnt_label4.grid(row=15, column=1, padx=5, pady=5, sticky="w")
cnt_entry4 = tk.Entry(root, width=30)
cnt_entry4.grid(row=15, column=2, padx=5, pady=5)
entries.append(cnt_entry4)

submit_button = tk.Button(root, text="실행", command=run_test)
submit_button.grid(row=17, column=0, columnspan=4, pady=20)

if os.path.exists("./title.txt"):
    with open("./title.txt", "r", encoding="utf-8") as file:
        titletxt = file.readline().strip()
        print(titletxt)

if os.path.exists("./subject.txt"):
    with open("./subject.txt", "r", encoding="utf-8") as file:
        subjecttxt = file.read().strip()
        print(subjecttxt)

if os.path.exists("./mydata.txt"):
    with open("./mydata.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        print(lines)
        for i, line in enumerate(lines[:12]):
            entries[i].delete(0, tk.END)
            entries[i].insert(0, line.strip())
elif os.path.exists("./data.txt"):
    with open("./data.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        print(lines)
        for i, line in enumerate(lines[:12]):
            entries[i].delete(0, tk.END)
            entries[i].insert(0, line.strip())

root.mainloop()