import time
from threading import Thread
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
import json

with open("data_pickupuser.json", "r") as file:
  pickup_user = json.load(file)

driver = webdriver.Firefox()
driver.get("http://bluedartstorageuat.z29.web.core.windows.net/auth/signin")
time.sleep(4)
driver.maximize_window()
driver.find_element(By.CLASS_NAME,'form-control').send_keys("channelsmart@eshipz.com")
print("email id passed")
driver.find_element(By.CLASS_NAME,'ng-pristine').send_keys("password")
print("password passed")
button=driver.find_element(By.XPATH,"//button[text()='Sign In']")
button.click()
time.sleep(3)
print("login passed")
driver.maximize_window()
time.sleep(3)
button1=driver.find_element(By.XPATH,"//span[text()='Users']")
button1.click()
time.sleep(2)
for user in pickup_user:
    try:
        button2=driver.find_element(By.XPATH,"/html[1]/body[1]/app-root[1]/app-admin[1]/div[1]/div[1]/app-esa-user[1]/div[1]/div[1]/button[1]")
        button2.click()
        time.sleep(2)
        driver.find_element(By.XPATH,("//input[@formcontrolname='first_name']")).send_keys(user["first_name"])
        driver.find_element(By.XPATH,("//input[@formcontrolname='last_name']")).send_keys(user["last_name"])
        driver.find_element(By.XPATH,("//input[@formcontrolname='email_id']")).send_keys(user["email_id"])
        driver.find_element(By.XPATH,("//input[@formcontrolname='contact_number']")).send_keys(user["contact_number"])
        driver.find_element(By.XPATH,("//input[@formcontrolname='password']")).send_keys(user["password"])
        time.sleep(4)
        driver.find_element(By.XPATH,"//*[@id='mat-select-value-5']/span").click()
        time.sleep(2)
        driver.find_element(By.XPATH, f"//span[normalize-space()='{user['services']}']").click()
        time.sleep(2)
        element3=driver.find_element(By.XPATH,"(//h2[normalize-space()='Add Pickup User'])[1]")
        time.sleep(1)
        actions = ActionChains(driver)
        actions.move_to_element(element3).click().perform()
        time.sleep(1)
        driver.find_element(By.XPATH,"//*[@id='mat-dialog-0']/app-dialog-modal/mat-dialog-actions/button[2]/span[1]").click()
        time.sleep(5)
        Pickupusercreation_validation1 = driver.find_element(By.XPATH,"//h2[normalize-space()='Added User Successfully.']")
        if Pickupusercreation_validation1.is_displayed():
            print("user created sucessfull ")
        else:
            print("user creation  failed")
        time.sleep(3)
        driver.find_element(By.ID,"added-user-confirm").click()
        time.sleep(3)
        driver.find_element(By.XPATH,"/html/body/app-root/app-admin/div/div/app-esa-user/div[1]/button/span[1]").click()
        time.sleep(2)
        file_input=driver.find_element(By.XPATH,"//*[@id='file']")
        file_input.send_keys("C:\\Users\\eshipz\\Downloads\\pickup_template (8).csv")
        time.sleep(6)
        driver.find_element(By.XPATH,"//*[@id='exampleModal']/div/div/div[3]/button[2]").click()
        time.sleep(3)
        Pickupusercreation_validation=driver.find_element(By.XPATH,"//h2[normalize-space()='Uploaded Successfully.']")
        if Pickupusercreation_validation.is_displayed():
         print("user created sucessfull ")
        else:
              print("user creation  failed")
        time.sleep(3)
    except Exception as error:
        print(f"Error: {error}")
driver.quit()
