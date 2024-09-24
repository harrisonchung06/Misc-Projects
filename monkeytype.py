from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import win32api
import win32con
from time import sleep

def press(*args):
    for i in args:
        win32api.keybd_event(vk[i], 0,0,0)
        sleep(0.01)
        win32api.keybd_event(vk[i],0 ,win32con.KEYEVENTF_KEYUP ,0)

#selenium setup
option = Options()
option.add_argument('--ignore-certificate-errors')
option.add_argument('--ignore-ssl-errors')
option.add_argument('--test-type')
driver = webdriver.Chrome(options = option)
driver.get("https://monkeytype.com/")
wait = WebDriverWait(driver, 10)

#vk codes
vk = {'spacebar':0x20,
           'a':0x41,
           'b':0x42,
           'c':0x43,
           'd':0x44,
           'e':0x45,
           'f':0x46,
           'g':0x47,
           'h':0x48,
           'i':0x49,
           'j':0x4A,
           'k':0x4B,
           'l':0x4C,
           'm':0x4D,
           'n':0x4E,
           'o':0x4F,
           'p':0x50,
           'q':0x51,
           'r':0x52,
           's':0x53,
           't':0x54,
           'u':0x55,
           'v':0x56,
           'w':0x57,
           'x':0x58,
           'y':0x59,
           'z':0x5A}

while True: 
    if (win32api.GetKeyState(0x26)):
        break

ck = False
while not(ck):
    ck = (driver.find_element(By.XPATH,"//*[@id='wpmChart']")).is_displayed()
    active_word_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "word.active")))  
    word = active_word_element.text
    for letter in word:
        if(ck):
            break
        #actuate the solenoid 
        press(letter)
    press('spacebar')
    
print('pausing')

while True:
    if (win32api.GetKeyState(0x28)):
        break

driver.quit()
print('closed')