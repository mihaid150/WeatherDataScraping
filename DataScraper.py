from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import html
from bs4 import BeautifulSoup

table_body = ""


def fetch_no_of_days(month, year):
    driver = configure_driver(month, year)
    dropdown_box = driver.find_element(By.ID, "wt-his-select")
    options = dropdown_box.find_elements(By.TAG_NAME, "option")
    return len(options)


def fetch_data_from_website(day, month, year):
    driver = configure_driver(month, year)
    first_day = get_firsts_day_data(driver)
    global table_body

    while True:
        # Find the dropdown box by its ID
        dropdown_box = driver.find_element(By.ID, "wt-his-select")

        # Find the option elements within the dropdown
        options = dropdown_box.find_elements(By.TAG_NAME, "option")

        # Click on the second option (change the index as needed)
        options[day - 1].click()

        # Wait for a specific element to be present (you can replace this with the element you expect)
        wait = WebDriverWait(driver, 30)
        wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@class='tb-scroll']")))

        # Get the updated content of the page
        page_content = driver.page_source
        page_text = html.unescape(page_content)
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(page_text, 'html.parser')
        # Find the table with ID "wt-his"
        table = soup.find('table', {'id': 'wt-his'})
        table_body = table.find('tbody')

        if day == 1 or first_day != table_body:
            break

    # Assuming you have already obtained the 'table_body' as in your previous code
    rows = table_body.find_all('tr')  # Find all table rows

    # Initialize an empty list to store the table data
    table_data = []

    # Iterate over the rows and extract the data from each cell
    for row in rows:
        # Find all the cell elements in this row
        hour = row.find('th')
        hour_text = hour.get_text(strip=True)
        if len(hour_text) > 5:
            hour_text = hour_text[:5]
        cells = row.find_all('td')

        # Extract data from each cell and append to the table_data list
        row_data = [hour_text] + [cell.get_text(strip=True)
                                      .replace('\xa0°C', ' °C').replace('\xa0km', ' km/h') for cell in cells]
        row_data.pop(1)
        # Append the row data to the table_data list
        table_data.append(row_data)

    # # Now 'table_data' contains all the rows of the table as a list of lists
    # # Each inner list represents a row, and its elements represent the cell data
    # for row in table_data:
    #     print(row)

    # Close the browser when done
    driver.quit()
    return table_data


def get_firsts_day_data(driver):
    dropdown_box = driver.find_element(By.ID, "wt-his-select")
    options = dropdown_box.find_elements(By.TAG_NAME, "option")
    options[0].click()
    wait = WebDriverWait(driver, 30)
    wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@class='tb-scroll']")))
    page_content = driver.page_source
    page_text = html.unescape(page_content)
    soup = BeautifulSoup(page_text, 'html.parser')
    table = soup.find('table', {'id': 'wt-his'})
    table_budy = table.find('tbody')
    return table_budy


def configure_driver(month, year):
    # Specify the path to the Microsoft Edge WebDriver executable
    edge_driver_path = '..\\msedgedriver.exe'  # Replace with the actual path

    # Create a Microsoft Edge WebDriver instance
    service = Service(edge_driver_path)
    driver = webdriver.Edge(service=service)

    # Navigate to the website
    driver.get(f"https://www.timeanddate.com/weather/romania/cluj-napoca/historic?month={month}&year={year}")
    return driver
