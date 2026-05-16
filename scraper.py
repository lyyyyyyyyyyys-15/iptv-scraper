import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def extract_m3u8_links(target_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # تشغيل مخفي تماماً يناسب السيرفر
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.set_capability("goog:loggingDims", {"performance": "ALL"})
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    print(f"🔄 Navigating to: {target_url}")
    driver.get(target_url)
    time.sleep(12) # وقت كافٍ لتحميل مشغل الفيديو والروابط

    logs = driver.get_log("performance")
    m3u8_urls = set()

    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if "Network.requestWillBeSent" in log["method"]:
            request_url = log["params"]["request"]["url"]
            if ".m3u8" in request_url:
                m3u8_urls.add(request_url)

    driver.quit()
    return list(m3u8_urls)

def save_to_m3u(urls, filename="playlist.m3u"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("#EXTM3U\n")
        for i, url in enumerate(urls, start=1):
            file.write(f"#EXTINF:-1, Channel {i}\n")
            file.write(f"{url}\n")
    print(f"✅ Saved {len(urls)} links to {filename}")

if __name__ == "__main__":
    # ضع هنا رابط موقع البث المستهدف
    SITE_URL = "https://example-streaming-site.com" 
    
    found_links = extract_m3u8_links(SITE_URL)
    save_to_m3u(found_links)
