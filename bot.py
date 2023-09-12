from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
import os
import tempfile

# Define the paths to your files
weblinks_file_path = 'D:/bot final - Copy/bot/weblinks.txt'
proxy_file_path = 'D:/bot final - Copy/bot/proxy.txt'
user_agents_file_path = 'D:/bot final - Copy/bot/user_agents.txt'

# Read user-agents from the txt file
with open(user_agents_file_path, 'r') as user_agents_file:
    user_agents = user_agents_file.read().splitlines()

# Shuffle the list of user-agents
random.shuffle(user_agents)

# Define a global variable to keep track of the used proxies
used_proxies = set()

def main():
    # Read website links from the txt file
    with open(weblinks_file_path, 'r') as links_file:
        links = links_file.read().splitlines()

    # Read proxy addresses from the txt file
    with open(proxy_file_path, 'r') as proxies_file:
        proxies = proxies_file.read().splitlines()

    for link in links:
        for proxy in proxies:
            try:
                if proxy not in used_proxies:
                    used_proxies.add(proxy)
                    # Choose the next user-agent in the shuffled list
                    user_agent = get_next_user_agent()
                    # Create a temporary directory for Chrome user data
                    temp_dir = tempfile.mkdtemp()
                    user_data_dir = os.path.join(temp_dir, 'UserData')
                    search_and_click_first_result(link, proxy, user_agent, user_data_dir)
            except Exception as e:
                print(f"An error occurred with proxy {proxy}: {e}")
                remove_proxy(proxy)
                continue

def get_next_user_agent():
    if user_agents:
        print("user_agents has been picked")
        return user_agents.pop(0)
    else:
        # If the user agent list is empty, you can add a default user agent or handle it as needed.
        # For example, you can add a common user agent.
        return 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
                
def search_and_click_first_result(link, proxy, user_agent, user_data_dir):
    options = webdriver.ChromeOptions()
    print(user_agent)
    options.add_argument(f'--proxy-server={proxy}')
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument(f'--user-data-dir={user_data_dir}')
    options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation control flag
    
    # Open Chrome with the specified options
    driver = uc.Chrome(options=options)
    try:
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        # Paste the link in the search box
        search_box.send_keys(link)
        search_box.send_keys(Keys.RETURN)
        # You might want to add a delay here to wait for the search results to load
        time.sleep(20)  # Adjust the delay as needed
        try:
            # Check if the user agent indicates a mobile device
            is_mobile = "iPhone" in user_agent or "Android" in user_agent
            if is_mobile:
                print('mobil device')
                # Mobile device
                first_result = driver.find_element(By.CSS_SELECTOR, "h3.LC20lb.MBeuO.DKV0Md")
            else:
                # Desktop device
                first_result = driver.find_element(By.CSS_SELECTOR, "h3.LC20lb.MBeuO.DKV0Md")
            first_result.click()
            # You might want to add a delay here to ensure the clicked page loads
            time.sleep(20)  # Adjust the delay as needed

            # Scroll down the page
            smooth_scroll_down(driver)

            # Click on all h2 tags with classname "post-title"
            h2_tags = driver.find_elements(By.CSS_SELECTOR, "h2.post-title")
            for h2_tag in h2_tags:
                # Open each h2 tag link in a new tab
                h2_tag_link = h2_tag.find_element(By.TAG_NAME, "a")
                h2_tag_link.send_keys(Keys.CONTROL + Keys.RETURN)

            # Switch to the newly opened tabs and scroll down each tab
            tabs = driver.window_handles
            for tab in tabs[1:]:
                driver.switch_to.window(tab)
                smooth_scroll_down(driver)
                smooth_scroll_up(driver)  # Scroll up in the new tab
                driver.close()

            # Switch back to the original tab
            driver.switch_to.window(tabs[0])
            # Scroll down the original tab
            smooth_scroll_down(driver)
            smooth_scroll_up(driver)  # Scroll up in the original tab

        except Exception as e:
            print("An error occurred while clicking the result:", e)

    except Exception as e:
        print("An error occurred while finding the search box:", e)
        remove_proxy(proxy)
    
    # Close the browser after handling the result
    driver.quit()
    remove_proxy(proxy)  # Remove the used proxy from the file

def remove_proxy(proxy):
    with open(proxy_file_path, 'r') as proxies_file:
        lines = proxies_file.readlines()
    with open(proxy_file_path, 'w') as proxies_file:
        for line in lines:
            if line.strip() != proxy:
                proxies_file.write(line)

def smooth_scroll_down(driver):
    scroll_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    current_scroll = 0
    while current_scroll < scroll_height:
        current_scroll += random.uniform(50, 100)  # Scroll by a random amount
        driver.execute_script(f"window.scrollTo(0, {current_scroll});")
        time.sleep(random.uniform(0.1, 0.5))  # Add randomness to scroll time

def smooth_scroll_up(driver):
    scroll_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    current_scroll = scroll_height
    while current_scroll > 0:
        current_scroll -= random.uniform(50, 100)  # Scroll by a random amount
        if current_scroll < 0:
            current_scroll = 0
        driver.execute_script(f"window.scrollTo(0, {current_scroll});")
        time.sleep(random.uniform(0.1, 0.5))  # Add randomness to scroll time

if __name__ == "__main__":
    main()
