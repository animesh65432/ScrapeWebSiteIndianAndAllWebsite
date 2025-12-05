from selenium import webdriver

def Get_Chrome_Options():
    """Create Chrome options with stability settings"""
    options = webdriver.ChromeOptions()
    
    # Essential stability flags
    options.add_argument('--headless=new')  # Use new headless mode
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-software-rasterizer')
    
    # Memory optimization
    options.add_argument('--disable-background-networking')
    options.add_argument('--disable-background-timer-throttling')
    options.add_argument('--disable-backgrounding-occluded-windows')
    options.add_argument('--disable-renderer-backgrounding')
    
    # Prevent crashes
    options.add_argument('--disable-crash-reporter')
    options.add_argument('--disable-hang-monitor')
    
    # Set user agent to avoid detection
    options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
    
    return options