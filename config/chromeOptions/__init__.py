from selenium.webdriver.chrome.options import Options

def Get_Chrome_Options():
    chrome_options = Options()

    # Use stable headless mode
    chrome_options.add_argument("--headless")  

    # Disable GPU + use software rendering
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")

    # Must-haves for Linux stability
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Fix renderer crashes
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--disable-features=IsolateOrigins")
    chrome_options.add_argument("--disable-site-isolation-trials")

    # Prevent renderer crash due to debugging port
    # REMOVE THIS → it causes renderer to fail in headless
    # chrome_options.add_argument("--remote-debugging-port=9222")

    # Real browser UA
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    )

    return chrome_options
