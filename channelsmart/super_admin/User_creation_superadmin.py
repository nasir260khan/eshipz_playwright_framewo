import time
from threading import Thread
from selenium.webdriver.common.by import By
from selenium import webdriver
import json

with open("data_users.json", "r") as file:
    Users = json.load(file)
driver = webdriver.Firefox()
driver.get("http://bluedartstorageuat.z29.web.core.windows.net/auth/signin")
time.sleep(4)
driver.maximize_window()
driver.find_element(By.CLASS_NAME,'form-control').send_keys("superadminuat@gmail.com")
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
time.sleep(5)
for user in Users:
    try:
        button2=driver.find_element(By.XPATH,"/html[1]/body[1]/app-root[1]/app-admin[1]/div[1]/div[1]/app-esa-user[1]/div[1]/div[1]/button[1]/span[1]")
        button2.click()
        time.sleep(7)
        print("add user sucessfull")
        driver.find_element(By.XPATH,("//input[@formcontrolname='first_name']")).send_keys(user["first_name"])
        time.sleep(2)
        driver.find_element(By.XPATH,("//input[@formcontrolname='last_name']")).send_keys(user["last_name"])
        time.sleep(2)
        driver.find_element(By.XPATH,("//input[@formcontrolname='password']")).send_keys(user["password"])
        time.sleep(2)
        driver.find_element(By.XPATH,("//input[@formcontrolname='contact_number']")).send_keys(user["contact_number"])
        time.sleep(2)
        driver.find_element(By.XPATH,("//input[@formcontrolname='email_id']")).send_keys(user["email_id"])
        time.sleep(2)
        driver.find_element(By.XPATH,"/html[1]/body[1]/div[3]/div[2]/div[1]/mat-dialog-container[1]/app-dialog-modal[1]/mat-dialog-content[1]/form[1]/div[7]/mat-form-field[1]/div[1]/div[1]/div[1]").click()
        time.sleep(3)
        driver.find_element(By.XPATH,f"//span[normalize-space()='{user['region']}']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//span[text()='Add']").click()
        time.sleep(2)
        print("user created sucessfully")
        User_validation=driver.find_element(By.XPATH,"//h2[normalize-space()='Added User Successfully.']")
        if User_validation.is_displayed():
             print("User created sucessfull ")
        else:
                print("offers generation failed")
        time.sleep(3)
        driver.find_element(By.XPATH,"//*[@id='added-user-confirm']").click()
    except Exception as error:
        print(f"Error: {error}")
driver.quit()