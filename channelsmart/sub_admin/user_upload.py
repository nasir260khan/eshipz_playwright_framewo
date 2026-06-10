import time
from selenium.webdriver.common.by import By
from selenium import webdriver
##from selenium.webdriver.firefox.remote_connection import FirefoxRemoteConnection
##from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Firefox()
driver.get("http://bluedartstorageuat.z29.web.core.windows.net/auth/signin")
driver.maximize_window()
time.sleep(4)
driver.find_element(By.CLASS_NAME,'form-control').send_keys("subadminuat@gmail.com")
print("email id passed")
driver.find_element(By.CLASS_NAME,'ng-pristine').send_keys("password")
print("password passed")
time.sleep(3)
button=driver.find_element(By.XPATH,"//button[text()='Sign In']")
button.click()
time.sleep(3)
print("login passed")
driver.maximize_window()
time.sleep(3)
button1=driver.find_element(By.XPATH,"//span[text()='Users']")
button1.click()
time.sleep(5)
button4=driver.find_element(By.XPATH,"/html[1]/body[1]/app-root[1]/app-admin[1]/div[1]/div[1]/app-esa-user[1]/div[1]/button[1]/span[1]")
button4.click()
time.sleep(5)
file_input=driver.find_element(By.XPATH,"//*[@id='file']")
file_input.send_keys("C:\\Users\\eshipz\\Downloads\\esa_template (10).csv")
time.sleep(6)
driver.find_element(By.XPATH,"//*[@id='exampleModal']/div/div/div[3]/button[2]").click()
time.sleep(10)
Usercreation_validation=driver.find_element(By.XPATH,"//h2[normalize-space()='Uploaded Successfully.']")
if Usercreation_validation.is_displayed():
    print("user created sucessfull ")
else:
    print("user creation  failed")
time.sleep(3)
