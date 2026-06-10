import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
import json

with open("data_offers.json", "r") as file:
    offers = json.load(file)

driver = webdriver.Chrome()
driver.get("http://bluedartstorageuat.z29.web.core.windows.net/auth/signin")
# driver.get("http://channelsmart.eshipz.com/auth/signin")
driver.maximize_window()
driver.find_element(By.CLASS_NAME,'form-control').send_keys("superadminuat@gmail.com")
# driver.find_element(By.CLASS_NAME,'form-control').send_keys("bdadmin@channelsmart.com")
driver.find_element(By.CLASS_NAME,'ng-pristine').send_keys("password")
button=driver.find_element(By.XPATH,"//button[text()='Sign In']")
button.click()
time.sleep(5)
print("login passed")
driver.maximize_window()
button1=driver.find_element(By.XPATH,"//span[text()='Offers']")
button1.click()
time.sleep(3)

for offer in offers:
    try:
        button2 = driver.find_element(By.XPATH, "/html[1]/body[1]/app-root[1]/app-admin[1]/div[1]/div[1]/app-offers[1]/div[1]/div[1]/button[1]/span[1]")
        button2.click()
        time.sleep(3)
        driver.find_element(By.XPATH,("//input[@formcontrolname='offer_code']")).send_keys(offer["offer_code"])
        time.sleep(3)
        driver.find_element(By.XPATH,("//input[@formcontrolname='offer_description']")).send_keys(offer["offer_description"])
        time.sleep(3)
        driver.find_element(By.XPATH,("//input[@formcontrolname='bd_packtype']")).send_keys(offer["package_value"])
        time.sleep(3)
        driver.find_element(By.XPATH,("//input[@formcontrolname='start_date']")).send_keys(offer["start_date"])
        time.sleep(3)
        driver.find_element(By.XPATH,("//input[@formcontrolname='end_date']")).send_keys(offer["end_date"])
        time.sleep(3)
        driver.find_element(By.XPATH,("//input[@formcontrolname='created_by']")).send_keys(offer["created_by"])
        time.sleep(3)
        driver.find_element(By.XPATH,"/html[1]/body[1]/div[3]/div[2]/div[1]/mat-dialog-container[1]/app-offer-modal[1]/mat-dialog-content[1]/form[1]/div[7]/mat-form-field[1]/div[1]/div[1]/div[1]").click()
        time.sleep(3)
        driver.find_element(By.XPATH,f"//span[normalize-space()='{offer['offer_regions']}']").click()
        time.sleep(3)
        element1=driver.find_element(By.XPATH,"/html[1]/body[1]/div[3]/div[2]/div[1]/mat-dialog-container[1]/app-offer-modal[1]/mat-dialog-content[1]/form[1]/div[8]/mat-form-field[1]/div[1]/div[1]/div[1]")
        time.sleep(3)
        actions = ActionChains(driver)
        actions.move_to_element(element1).click().perform()
        time.sleep(3)
        driver.find_element(By.XPATH,"/html[1]/body[1]/div[3]/div[2]/div[1]/mat-dialog-container[1]/app-offer-modal[1]/mat-dialog-content[1]/form[1]/div[8]/mat-form-field[1]/div[1]/div[1]/div[1]").click()
        time.sleep(3)
        driver.find_element(By.XPATH,f"//span[normalize-space()='{offer['services']}']").click()
        time.sleep(3)
        element2=driver.find_element(By.XPATH,"/html[1]/body[1]/div[3]/div[2]/div[1]/mat-dialog-container[1]/app-offer-modal[1]/mat-dialog-content[1]")
        time.sleep(3)
        actions = ActionChains(driver)
        actions.move_to_element(element2).click().perform()
        time.sleep(3)
        driver.find_element(By.XPATH,"(//span[normalize-space()='Add'])[1]").click()
        time.sleep(3)
        Offers_validation=driver.find_element(By.XPATH,"//h2[normalize-space()='Offer Added Successfully.']")
        if Offers_validation.is_displayed():
            print("offers created sucessfull")
        else:
            print("offers generation failed")
        time.sleep(3)
        confirm_button = driver.find_element(By.ID, "offer-added-confirm")
        confirm_button.click()
        time.sleep(3)
    except Exception as error:
        print(f"Error: {error}")

driver.quit()
