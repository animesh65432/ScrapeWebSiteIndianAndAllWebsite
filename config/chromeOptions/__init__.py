from selenium.webdriver.chrome.options import Options

def Get_Chrome_Options():
    chrome_options = Options()
    
    # Use modern stable headless mode
    chrome_options.add_argument("--headless=new")

    # Stability flags for Linux
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-setuid-sandbox")
    
    # Prevent Selenium detection
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Important: prevents timeout error
    chrome_options.add_argument("--remote-debugging-port=9222")

    # Fix for many "page_source timeout" issues
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    
    # Add user agent
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )

    return chrome_options
