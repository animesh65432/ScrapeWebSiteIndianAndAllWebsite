from selenium import webdriver
import os


def Get_Chrome_Options(use_scraperapi:bool,api_key:str):
    """Create Chrome options with stability and performance settings"""
    options = webdriver.ChromeOptions()
    
    # Detect GitHub Actions environment
    is_ci = os.getenv('GITHUB_ACTIONS') == 'true'

    if use_scraperapi:
        if not api_key:
            raise ValueError("ScraperAPI key not provided. Set SCRAPERAPI_KEY env var or pass scraperapi_key parameter")

        PROXY = "proxy-server.scraperapi.com:8001"
        options.add_argument(f'--proxy-server=http://{PROXY}')
        
       
        proxy_user = f"scraperapi.country_code=in"
        options.add_argument(f'--proxy-auth={proxy_user}:{api_key}')
        
        print(f"✅ ScraperAPI proxy configured: {PROXY}")

        if is_ci:
            print("ℹ️  Running in GitHub Actions with ScraperAPI proxy")
    
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
    
    # Network optimizations
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-web-security')  # For problematic sites
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-certificate-errors')
    
    # DNS optimization (helps with ERR_NAME_NOT_RESOLVED)
    if is_ci:
        options.add_argument('--dns-prefetch-disable')
        options.add_argument('--disable-features=NetworkService')
    
    # Cache settings
    options.add_argument('--disk-cache-size=0')
    options.add_argument('--aggressive-cache-discard')
    
    # User agent
    options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36')
    
    # Preferences for better stability
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
    
    # Exclude automation flags
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    
    return options
