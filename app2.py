from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import csv
import parameters


writer = csv.writer(open(parameters.file_name, 'w'))


writer.writerow(['Name','Job Title','Education','Profile_URL '])

empty=""
def validate_field(field):
    if field == "":
        return 'No results'
    if field == None:
        return "None"
    else:
        return field 


options = webdriver.ChromeOptions()
#options.add_argument("headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

try:
    driver.implicitly_wait(10)
    driver.get('https://www.linkedin.com')
    username=driver.find_element_by_id('session_key') #locating the email form using the class name
    username.send_keys('xxxxx) # here we input the username 
    
    password=driver.find_element_by_id('session_password') #locating the password form using the class name
    password.send_keys('xxxxxx') # here we input the password for linked in 
   
    log_in_button=driver.find_element_by_class_name('sign-in-form__submit-button') #locating submit button by class name
    log_in_button.click()
    
    
    driver.get('https://www.google.com') #navigating to google
    search_gog=driver.find_element_by_name('q')
    search_gog.send_keys('site:linkedin.com/in/ AND "data analyst" AND "California"')
    search_gog.send_keys(Keys.RETURN)
    
    
    for x in range(3):
        current=driver.current_url
        list_links = [link.get_attribute('href') for link in driver.find_elements_by_xpath("//div[@class='g']//div[@class='r']/a[contains(@href, 'https://www.linkedin.com')]")]
    
        for link in list_links:
            driver.get(link)
            sel=Selector(text=driver.page_source)
            name = sel.xpath('//*[starts-with(@class, "inline t-24 t-black t-normal break-words")]/text()').extract_first()
            if name:
                name=name.strip()
            job_title= sel.xpath('//*[starts-with(@class, "mt1 t-18 t-black t-normal break-words")]/text()').extract_first()
            if job_title:
                job_title=job_title.strip()

            education = sel.xpath('//*[starts-with(@class, "pv-profile-section-pager ember-view")]/text()').extract_first()
            if education:
                education=education.strip()
            
            name=validate_field(name)
            job_title=validate_field(job_title)
            education=validate_field(education)

            
            writer.writerow([name.encode('utf-8'),
                 job_title.encode('utf-8'),
                 education.encode('utf-8'),
                 link.encode('utf-8')])
                 
        driver.get(current)
        next_links = driver.find_elements_by_link_text("Next") 
        if len(next_links):
            print('Found "Next" link')
            next_links[0].click()
        else:
            print('There is no "Next" link')

finally:
    input('pausing (hit enter to terminate) ...')
    driver.quit()










 
 
 



