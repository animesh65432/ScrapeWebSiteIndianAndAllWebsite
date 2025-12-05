from selenium.webdriver.chrome.options import Options

def Get_Chrome_Options():
    chrome_options = Options()

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

    # Real browser user agent
    chrome_options.add_argument(
       "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
       "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    )

    return chrome_options
