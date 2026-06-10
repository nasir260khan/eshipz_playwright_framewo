import time
from threading import Thread
from selenium.webdriver.common.by import By
from selenium import webdriver
import json

with open("data_report.json", "r") as file:
    reports = json.load(file)
driver = webdriver.Firefox()
driver.get("http://bluedartstorageuat.z29.web.core.windows.net/auth/signin")
#time.sleep(4)
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
button1=driver.find_element(By.XPATH,"//span[text()='Reports']")
button1.click()
print("passed on report")
for report in reports:
    try:
        driver.find_element(By.XPATH, "//input[@formcontrolname='fromday']").send_keys(report["start_date"])
        driver.find_element(By.XPATH,"//input[@formcontrolname='today']").send_keys(report["end_date"])
        driver.find_element(By.XPATH,"//input[@formcontrolname='email_id']").send_keys(report["email_id"])
        time.sleep(2)
        button4=driver.find_element(By.XPATH,"//button[@class='btn btn-block btn-primary']")
        button4.click()
        print("mail received sucessfull")
        time.sleep(5)
        report_validation=driver.find_element(By.XPATH,"//h2[normalize-space()='Generated Report Shared To Your Email.']")
        if report_validation.is_displayed():
            print("report sucessfully generated")
        else:
            print("reports generation failed")
        driver.find_element(By.XPATH,"//*[@id='generated-report-confirm']").click()
    except Exception as error:
             print(f"Error: {error}")

driver.quit()




