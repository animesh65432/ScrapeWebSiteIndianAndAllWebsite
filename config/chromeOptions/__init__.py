from selenium.webdriver.chrome.options import Options

def Get_Chrome_Options():
    chrome_options = Options()

    chrome_options.page_load_strategy = 'eager'
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    

    # Headless mode
    chrome_options.add_argument("--headless=new")

    # Linux stability flags
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")


    # Disable GPU / Rasterization
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")

    # Prevent renderer crashes
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--disable-features=IsolateOrigins")
    chrome_options.add_argument("--disable-site-isolation-trials")

    # Add after existing arguments
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding") 
    chrome_options.add_argument("--disable-extensions")  # Blocks ad/tracking extensions[web:40]


    # Real browser user agent
    # Replace user-agent line
    # 
    chrome_options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    )


    return chrome_options
