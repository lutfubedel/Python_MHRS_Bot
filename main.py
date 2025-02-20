from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from dotenv import load_dotenv
import os

def select_item(button_xpath, li_xpath_list, item_to_search):
    time.sleep(2)
    button = driver.find_element(By.XPATH, button_xpath)
    button.click()

    time.sleep(1)
    list_items = driver.find_elements(By.XPATH, li_xpath_list)
    print(len(list_items))
    # Listeyi döngü ile tarayın
    for item in list_items:
        # Her bir öğeyi kontrol et
        if item_to_search in item.text:
            print(f"Eşleşen öğe bulundu: {item.text}")
            # Eşleşen öğeyi tıklayın
            item.click()
            break
    else:
        print("Eşleşen öğe bulunamadı!")

def click_button(button_xpath, wait_time):
    time.sleep(wait_time)
    button = driver.find_element(By.XPATH, button_xpath)
    button.click()

def click_ESC():
    time.sleep(5)
    # ESC tuşuna basma işlemi
    action = ActionChains(driver)
    action.send_keys(Keys.ESCAPE).perform()

def search_for_appointment():
    load_dotenv()
    tc_no = os.getenv("TC_NO")
    password = os.getenv("PASSWORD")

    edge_options = Options()
    edge_options.add_argument("--headless")

    global driver
    driver = webdriver.Edge(options=edge_options)

    driver.get("https://mhrs.gov.tr/vatandas/#/")
    time.sleep(5)

    username_box = driver.find_element(By.ID, "LoginForm_username")
    password_box = driver.find_element(By.ID, "LoginForm_password")
    username_box.send_keys(tc_no)
    password_box.send_keys(password)
    
    click_button('//*[@id="vatandasApp"]/div[2]/div[2]/div[2]/form/div[4]/div/div/span/button', 2)
    click_ESC()
    
    click_button("//div[contains(@class, 'ant-card randevu-card-dissiz hasta-randevu-card mb-16 mr-16')]//div[contains(@class, 'randevu-turu-grup-article')]",2)
    click_button("//button[span[text()='Genel Arama']]",2)
    
    il = "BURSA"
    ilce = "YILDIRIM"
    klinik = "Beyin ve Sinir Cerrahisi"
    hastane = "-FARK ETMEZ-"
    muayene_yeri = "-FARK ETMEZ-"
    hekim = "-FARK ETMEZ-"

    select_item("//span[text()='İl Seçiniz']", '//ul[@class="ant-select-tree"]//li', il)
    select_item('//*[@id="randevuAramaForm_ilce"]/div/div/div[1]', '//li[@role="option"]', ilce)
    select_item("//span[text()='Klinik Seçiniz']", '//li[@role="treeitem"]', klinik)
    select_item("//span[text()='-FARK ETMEZ-']", '//li[@role="treeitem"]', hastane)
        
    if (hastane != "-FARK ETMEZ-"):
        select_item('//*[@id="vatandasApp"]/section/main/div/div[1]/div/div[2]/div/div[3]/div/div[2]/form/div[7]/div[2]/div/span/span/span/span[1]/span', '//*[@id="rc-tree-select-list_4"]/ul/li', muayene_yeri)
        select_item('//*[@id="vatandasApp"]/section/main/div/div[1]/div/div[2]/div/div[3]/div/div[2]/form/div[8]/div[2]/div/span/span/span/span[1]/span', '//*[@id="rc-tree-select-list_5"]/ul/li', hekim)
    
    while True:
        click_button('//*[@id="vatandasApp"]/section/main/div/div[1]/div/div[2]/div/div[3]/div/div[2]/form/div[10]/div/div/span/div/button[1]', 2)
        click_ESC()
        
        list_data = []
        try:
            container = driver.find_element(By.CLASS_NAME, "ant-spin-container")
            list_items = container.find_elements(By.CLASS_NAME, "ant-list-item")
            
            if list_items:
                print("Liste Elemanları:")
                for item in list_items:
                    list_data.append(item.text)
                    print("-", item.text)
                break  # Eğer liste boş değilse döngüden çık
            else:
                empty_text = container.find_element(By.CLASS_NAME, "ant-list-empty-text").text
                list_data.append(empty_text)
                click_button('//*[@id="vatandasApp"]/section/main/div/div[1]/div/div[1]/div/div/div/div', 2)
                print(empty_text)
                time.sleep(5)  # Yeni arama için bekleme süresi
        
        except Exception as e:
            print("Hata:", e)
        
    time.sleep(5)
    driver.quit()
    return list_data





