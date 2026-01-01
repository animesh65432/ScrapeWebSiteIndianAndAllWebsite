from selenium import webdriver
import os
import shutil


def Get_Chrome_Options():
    """Create Chrome options with stability and performance settings"""
    options = webdriver.ChromeOptions()

    chrome_path = shutil.which("google-chrome")
    print(f"[DEBUG] google-chrome path: {chrome_path}")

    if not chrome_path:
        raise RuntimeError("google-chrome binary not found")

    options.binary_location = chrome_path
    print(f"[DEBUG] Using Chrome binary: {options.binary_location}")
    
    # Detect GitHub Actions environment
    is_ci = os.getenv('GITHUB_ACTIONS') == 'true'

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
