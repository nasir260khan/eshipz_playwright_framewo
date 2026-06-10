import time
from threading import Thread
from selenium.webdriver.common.by import By
from selenium import webdriver
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
button1=driver.find_element(By.XPATH,"//span[text()='Shipments']")
button1.click()
driver.find_element(By.XPATH,"//*[@id='mat-input-4']").send_keys("53451982290")
time.sleep(3)
driver.find_element(By.XPATH, "/html/body/app-root/app-admin/div/div/app-esa-shipments/div[1]/div[4]/button").click()
time.sleep(3)