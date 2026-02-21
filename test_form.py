import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


BASE_URL = "https://the-internet.herokuapp.com/login"


def test_successful_login(driver):
    driver.get(BASE_URL)

    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    flash = driver.find_element(By.ID, "flash").text
    assert "You logged into a secure area!" in flash


def test_unsuccessful_login(driver):
    driver.get(BASE_URL)

    driver.find_element(By.ID, "username").send_keys("wrong_user")
    driver.find_element(By.ID, "password").send_keys("wrong_pass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    flash = driver.find_element(By.ID, "flash").text
    assert "Your username is invalid!" in flash or "Your password is invalid!" in flash