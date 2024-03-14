import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


# Replace with your LinkedIn credentials
username = "dhakardinesh1997@gmail.com"
password = "Dha@9460.1"

# Open Chrome browser
driver = webdriver.Chrome()

# Navigate to LinkedIn
driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
username=driver.find_element(By.XPATH,"""//*[@id="username"]""")
username.send_keys("dhakardinesh1997@gmail.com")
password=driver.find_element(By.XPATH,"""//*[@id="password"]""")
password.send_keys("Dha@9460.1")
password.send_keys(Keys.ENTER)
# driver.get("https://www.linkedin.com/jobs")
# search_field=driver.find_element(By.XPATH,'//*[@id="jobs-search-box-keyword-id-ember25"]')
# search_field.send_keys("Software Engineer")
# search_field.send_keys(Keys.ENTER)
print("zoom out to 25% and increase tab length and press enter here")
a=input()

job_data = pd.DataFrame(columns=['Job Id', 'Job Title', 'Job Link', 'Company Name', 'Location', 'Connection Info'])


def get_job_cards():
    current_height = driver.execute_script("return document.body.scrollHeight")
    max_scrolls = 2
    for _ in range(max_scrolls):
        driver.execute_script(f"window.scrollTo(0, {current_height});")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == current_height:
            break
        current_height = new_height
    return driver.find_elements(By.CLASS_NAME, 'job-card-container')


def export_jobs(job_cards, job_data):
    for card in job_cards:
        card_html = card.get_attribute('outerHTML')
        soup = BeautifulSoup(card_html, 'html.parser')
        job_title = soup.find('a', class_='job-card-list__title').text.strip() \
            if soup.find('a', class_='job-card-list__title') else ""
        job_link = soup.find('a', class_='job-card-list__title')['href'] \
            if soup.find('a', class_='job-card-list__title') else ""
        company_name = soup.find('span', class_='job-card-container__primary-description').text.strip() \
            if soup.find('span', class_='job-card-container__primary-description') else ""
        location = soup.find('li', class_='job-card-container__metadata-item').text.strip() \
            if soup.find('li', class_='job-card-container__metadata-item') else ""
        connection_info = soup.find('div', class_='job-card-container__job-insight-text').text.strip() \
            if soup.find('div', class_='job-card-container__job-insight-text') else ""
        job_id = soup.find('div', class_='job-card-container')['data-job-id'] \
            if soup.find('div', class_='job-card-container')['data-job-id'] else ""

        temp_df = pd.DataFrame({'Job Id': [job_id],
                                'Job Title': [job_title],
                                'Job Link': [job_link],
                                'Company Name': [company_name],
                                'Location': [location],
                                'Connection Info': [connection_info]})
        job_data = pd.concat([job_data, temp_df], ignore_index=True)
    return job_data

j = 0

while True:
    driver.get(f'https://www.linkedin.com/jobs/search/?keywords=Software%20Engineer&origin=JOBS_HOME_SEARCH_BUTTON&refresh=true&start={25*j}')
    time.sleep(4)
    print(f"page: {j+1}")
    job_cards=get_job_cards()
    job_data=export_jobs(job_cards,job_data)
    job_data.to_csv(f"job_data_page{j+1}.csv")
    j += 1

import pandas as pd
import spacy

# Now you can load the model
nlp = spacy.load("en_core_web_sm")


# Function to extract experience from job description using NER
def extract_experience(text):
    doc = nlp(text)
    experience = []
    for ent in doc.ents:
        if ent.label_ == "DATE" and ("year" in ent.text.lower() or "yr" in ent.text.lower()):
            experience.append(ent.text)
    return experience

import pandas as pd
import os
if os.path.exists("job_data_desc_exp.csv"):
    df=pd.read_csv("job_data_desc_exp.csv")
else:
    df = pd.read_csv("job_data_desc.csv")
    df["Exp"]=None

# Read CSV file
import pandas as pd

# Assuming df is your DataFrame containing the CSV data

i = 0

# Process job descriptions and extract experience
for index, row in df.iterrows():
    i += 1
    job_title = row["Job Title"]

    # Check if 'Extracted Text' is not NaN
    if pd.notna(row['Extracted Text']):
        # Convert to string and check length
        if len(str(row['Extracted Text'])) > 10:
            job_description = str(row['Extracted Text'])
            experience = extract_experience(job_description)
            df.at[index, "Exp"] = ', '.join(experience)


df.to_csv("job_data_desc_exp.csv")

