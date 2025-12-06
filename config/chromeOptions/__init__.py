from selenium import webdriver


def Get_Chrome_Options():
    """Create Chrome options with stability and performance settings"""
    options = webdriver.ChromeOptions()
    
    # Essential stability flags
    options.add_argument('--headless=new')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-software-rasterizer')
    
    # Performance optimization
    options.add_argument('--disable-background-networking')
    options.add_argument('--disable-background-timer-throttling')
    options.add_argument('--disable-backgrounding-occluded-windows')
    options.add_argument('--disable-renderer-backgrounding')
    options.add_argument('--disable-breakpad')
    
    # Prevent crashes
    options.add_argument('--disable-crash-reporter')
    options.add_argument('--disable-hang-monitor')
    options.add_argument('--disable-prompt-on-repost')
    
    # Network optimizations for slow sites
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Increase timeout tolerance
    options.add_argument('--disk-cache-size=0')  # Disable disk cache
    options.add_argument('--aggressive-cache-discard')
    
    # Set user agent
    options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36')
    
    # Add preferences for better stability
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2,  # Don't load images (faster)
            'plugins': 2,
            'popups': 2,
            'geolocation': 2,
            'notifications': 2,
            'media_stream': 2,
        }
    }
    options.add_experimental_option('prefs', prefs)
    
    return options
