import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def verify_match_page_text(main_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        print(f"🔄 1. جاري الدخول إلى الصفحة الرئيسية: {main_url}")
        driver.get(main_url)
        time.sleep(5) 

        main_window = driver.current_window_handle

        print("🔍 2. جاري البحث عن أول رابط مباراة متاح...")
        # استخراج جميع الروابط في الصفحة
        all_links = driver.find_elements(By.TAG_NAME, "a")
        target_match_url = None

        for elem in all_links:
            href = elem.get_attribute("href")
            # تصفية الروابط لضمان اختيار رابط مباراة داخلي (يحتوي عادة على match أو id)
            if href and main_url in href and href != main_url and ("match" in href or "live" in href or "go" in href):
                target_match_url = href
                break

        # إذا لم يجد رابط مخصص، سيأخذ أول رابط مختلف عن الصفحة الرئيسية كخطة بديلة
        if not target_match_url:
            for elem in all_links:
                href = elem.get_attribute("href")
                if href and main_url in href and href != main_url:
                    target_match_url = href
                    break

        if not target_match_url:
            print("❌ لم يتم العثور على أي روابط للانتقال إليها.")
            driver.quit()
            return

        print(f"🎯 الرابط الذي سيتم دخوله وفحصه: {target_match_url}")

        print("🔄 3. جاري الانتقال إلى الصفحة والتعامل مع النوافذ الإعلانية...")
        driver.get(target_match_url)
        time.sleep(8) # وقت كافٍ لتحميل النصوص وإغلاق الإعلانات الخلفية

        # إغلاق النوافذ الإعلانية المنبثقة إن وجدت لضمان ثبات المتصفح
        all_windows = driver.window_handles
        if len(all_windows) > 1:
            print(f"⚠️ تم رصد وإغلاق {len(all_windows) - 1} نافذة إعلانية منبثقة.")
            for window in all_windows:
                if window != main_window:
                    driver.switch_to.window(window)
                    driver.close()
            driver.switch_to.window(main_window)

        print("📝 4. جاري استخراج النصوص الظاهرة في الصفحة وحفظها...")
        # سحب النص المقروء بالكامل من جسم الصفحة (Body)
        visible_text = driver.find_element(By.TAG_NAME, "body").text

        # حفظ النصوص المستخرجة في ملف txt
        with open("match_page_text.txt", "w", encoding="utf-8") as file:
            file.write(f"--- معلومات الفحص ---\n")
            file.write(f"رابط الصفحة المستهدفة: {target_match_url}\n")
            file.write(f"تاريخ ووقت الفحص: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"-----------------------\n\n")
            file.write(visible_text)
        
        print("✅ تم حفظ محتوى الصفحة النصي بنجاح في ملف: match_page_text.txt")

    except Exception as e:
        print(f"❌ حدث خطأ أثناء التنفيذ: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    # استبدل هذا برابط الموقع الذي تريد اختباره
    TARGET_SITE = "https://www.yallaschool.live/" 
    verify_match_page_text(TARGET_SITE)
