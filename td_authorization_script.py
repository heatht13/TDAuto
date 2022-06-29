from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
from urllib import parse
import credentials

userID = credentials.user_id
userPass = credentials.user_password
body = r"https://auth.tdameritrade.com/auth?"
#lvl1 app's consumer key
consumer_key = credentials.consumer_key
suffix = "@AMER.OAUTHAP"
payload = {
    "response_type" : "code",
    "redirect_uri" : "http://localhost",
    "client_id" : consumer_key + suffix
}
request = requests.get(body, params = payload)
request.url

options = Options()
#options.add_argument("--headless")
#options.add_argument("--start-maximized")
service = Service("C:\\Users\\Heath\\OneDrive\\Documents\\Side\\chromedriver_win32\\chromedriver")

driver = webdriver.Chrome(service = service, options = options)
driver.get(request.url)

username = driver.find_element(By.NAME, "su_username")
username.send_keys(userID)
password = driver.find_element(By.NAME, "su_password")
password.send_keys(userPass)
button = driver.find_element(By.NAME, "authorize")
button.submit()

summary = driver.find_element(By.TAG_NAME, 'summary')
summary.click()
security = driver.find_element(By.NAME, 'init_secretquestion')
#print(security.get_attribute('value'))
security.click()

question = driver.find_element(By.XPATH, "/html/body/form[1]/main/div[@class='row description']/p[2]")
if('Question: In what city was your high school? (Enter full name of city only.)' == question.text):
    answer = driver.find_element(By.NAME, 'su_secretquestion')
    answer.send_keys(credentials.answer1)
    button = driver.find_element(By.NAME, 'authorize')
    button.submit()
elif('Question: What is your best friend\'s first name?' == question.text):
    answer = driver.find_element(By.NAME, 'su_secretquestion')
    answer.send_keys(credentials.answer2)
    button = driver.find_element(By.NAME, 'authorize')
    button.submit()
elif('Question: What was the name of your first pet?' == question.text):
    answer = driver.find_element(By.NAME, 'su_secretquestion')
    answer.send_keys(credentials.answer3)
    button = driver.find_element(By.NAME, 'authorize')
    button.submit()
elif('Question: What was the last name of your favorite teacher in your final year of high school?' == question.text):
    answer = driver.find_element(By.NAME, 'su_secretquestion')
    answer.send_keys(credentials.answer4)
    button = driver.find_element(By.NAME, 'authorize')
    button.submit()
else:
    print(f'Question Not Found: {question.text}')

trust = driver.find_element(By.XPATH, "/html/body/form[1]/main/fieldset/div[@id='stepup_trustthisdevice0']/div[1]/label[1]")
#print(trust.get_attribute('class'))
trust.click()
button = driver.find_element(By.NAME, 'authorize')
button.submit()

allow = driver.find_element(By.NAME, 'su_authorization')
allow.submit()

urlCode = driver.current_url
driver.close()
print(urlCode)
authorizationCode = parse.unquote(urlCode.strip('https://localhost/?code='))
print(authorizationCode)

file = open('authorization_code.txt', 'w')
file.write(authorizationCode)
file.close()


