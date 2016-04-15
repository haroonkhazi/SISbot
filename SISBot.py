import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

def check_exists_by_id(id):
    try:
        driver.find_element_by_id(id)
    except NoSuchElementException:
        return False
    return True

def wait_until_exists(id, page):
    while True:
        try:
            WebDriverWait(driver, -1).until(EC.presence_of_element_located((By.ID, id)))
        except TimeoutException:
            print "Page took too long to respond"
            continue
        print "Success going to page: " + page
        break

def repeat_click_until_not(id, check, page):
    while True:
        try:
            if check_exists_by_id(check):
                print "No valid appointment, trying again"
                driver.find_element_by_id(id).click()
                time.sleep(0.1)
            else:
                print "Success going to page: "
                break
        except:
            print "Error, trying again"

def repeat_click_until(id, check, page):
    while True:
        try:
            if not check_exists_by_id(check):
                print "No valid appointment, trying again"
                driver.find_element_by_id(id).click()
                time.sleep(0.1)
            else:
                print "Success going to page: "
                break
        except:
            print "Error, trying again"

url = "https://sis.case.edu/psc/P90SCWR_1/EMPLOYEE/P90SCWR/c/SA_LEARNER_SERVICES_2.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ExactKeys=Y&EMPLID=3327742&TargetFrameName=None&PortalActualURL=https%3a%2f%2fsis.case.edu%2fpsc%2fP90SCWR_1%2fEMPLOYEE%2fP90SCWR%2fc%2fSA_LEARNER_SERVICES_2.SSR_SSENRL_CART.GBL%3fPage%3dSSR_SSENRL_CART%26Action%3dA%26ExactKeys%3dY%26EMPLID%3d3327742%26TargetFrameName%3dNone&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fsis.case.edu%2fpsp%2fP90SCWR_1%2f&PortalURI=https%3a%2f%2fsis.case.edu%2fpsc%2fP90SCWR_1%2f&PortalHostNode=HRMS&NoCrumbs=yes&PortalKeyStruct=yes"
userid = ""
pwd = ""

driver = webdriver.Firefox()
driver.get(url)

wait_until_exists("userid", "Log in")

driver.find_element_by_id("userid").send_keys(userid)
driver.find_element_by_id("pwd").send_keys(pwd)
driver.find_element_by_id("pwd").send_keys(Keys.RETURN)

wait_until_exists("SSR_DUMMY_RECV1$sels$2$$0", "Semester selection")

driver.find_element_by_id("SSR_DUMMY_RECV1$sels$2$$0").click()
driver.find_element_by_id("DERIVED_SSS_SCT_SSR_PB_GO").send_keys(Keys.RETURN)

wait_until_exists("SSR_REGFORM_VW$scroll$0", "Shopping cart")
    
for i in range(0, len(driver.find_elements_by_xpath("//table[@id='SSR_REGFORM_VW$scroll$0']/tbody/tr"))-2):
    elemid = "P_SELECT$" + str(i)
    if check_exists_by_id(elemid):
        driver.find_element_by_id(elemid).click()

driver.find_element_by_id("DERIVED_REGFRM1_LINK_ADD_ENRL").click()
time.sleep(1)

repeat_click_until_not("DERIVED_REGFRM1_LINK_ADD_ENRL", "ACE_DERIVED_SASSMSG_GROUP1", "Finish enrolling")

wait_until_exists("DERIVED_REGFRM1_SSR_PB_SUBMIT")

repeat_click_until("DERIVED_REGFRM1_SSR_PB_SUBMIT", "CW_DERIVED_SOC_CW_RQST_PERMISSION", "View results")

print
print "Success registering for classes!"
