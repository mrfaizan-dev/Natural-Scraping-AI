import os, time, random
from playwright.async_api import async_playwright, Error as pe
import asyncio
from seleniumbase import SB
import logging, uvicorn
from extract_main import ecommerece_extractor , real_estate_extractor
from pandas_save import process_and_save
import uuid
import nest_asyncio
from pydantic_v2_main import settings
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from scrp_retr import sp2
from scraping_retr_2 import scrape_heavy_sites

nest_asyncio.apply()

url_limit = 5

user_agents = [
    # Chrome 131 - Windows
    {
        "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "headers": {
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }
    },
    # Chrome 131 - macOS
    {
        "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "headers": {
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"'
        }
    },
    # Microsoft Edge 131 - Windows
    {
        "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "headers": {
            "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }
    },
    # Microsoft Edge 131 - macOS
    {
        "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "headers": {
            "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"'
        }
    },
    # Chrome 130 - Windows
    {
        "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "headers": {
            "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }
    },
    # Chrome 130 - macOS
    {
        "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "headers": {
            "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"'
        }
    },
    # Microsoft Edge 130 - Windows
    {
        "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
        "headers": {
            "sec-ch-ua": '"Microsoft Edge";v="130", "Chromium";v="130", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }
    },
    # Chrome 129 - Windows (Older but highly trusted)
    {
        "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "headers": {
            "sec-ch-ua": '"Chromium";v="129", "Not = A;Brand";v="99", "Google Chrome";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }
    },
    # Chrome 128 - macOS
    {
        "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "headers": {
            "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"'
        }
    },
    # Chrome 131 - Linux
    {
        "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "headers": {
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"'
        }
    }
]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
url_limit = 10
args = '--disable-blink-features=AutomationControlled,--no-first-run,--no-service-autorun,--password-store=basic,--start-maximized,--no-sandbox,--disable-dev-shm-usage'

async def engine(url, browser, semaphore , scrape_type, max_retries=2):
    def clean_ebay_url(long_url):
            
            parsed = urlparse(long_url)
            params = parse_qs(parsed.query)
    
            clean_params = {}
            if '_nkw' in params:
                clean_params['_nkw'] = params['_nkw'][0]  # Search query
            if '_pgn' in params:
                clean_params['_pgn'] = params['_pgn'][0]  # Page number
        
            new_query = urlencode(clean_params)
            clean_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', new_query, ''))
            return clean_url
    
    async with semaphore:
        for attempt in range(1, max_retries + 1):
            context = None
            try:
                ua_config = random.choice(user_agents)
                context = await browser.new_context(
                    user_agent=ua_config["ua"],
                    extra_http_headers=ua_config["headers"],
                    viewport={"width": 1280, "height": 800},
                                   
                    )
                                                                                                                                                                                                                                                                                                                                                                
                page = await context.new_page()
                if "ebay" in url:
                    url = clean_ebay_url(url)
                # try:
                #     async def route_bypass(route):
                #         req_type = route.request.resource_type
                #         if req_type in ["document", "script", "fetch", "xhr", "stylesheet" , "image"]:
                #             await route.continue_()
                #         else:
                #             await route.abort()
                #     await page.route("**/*" , route_bypass)
                # except Exception as e:
                #     logging.info(f"Route Intercept Error: {e}")
                
                logging.info(f"Attempt {attempt}/{max_retries} - Ready To Go To The Url: {url}")
                await page.goto(url, timeout=75000, wait_until="domcontentloaded")

                
                await asyncio.sleep(random.uniform(3.0 , 6.0))
                await page.mouse.move(random.randint(100, 600), random.randint(100, 600))
                await page.evaluate("window.scrollBy(0, window.innerHeight / 2);")
                await asyncio.sleep(random.uniform(1.0 , 2.0))
                
                web_data = await page.content()
                data_length = len(web_data) if web_data else 0
                
                # PERFECT CHECK: Extracts and proceeds only if data length > 25000
                if data_length > 25000:
                    logging.info(f"✅ Web Data Length okay ({data_length}). Proceeding to extract.")
                    if scrape_type.lower() == "ecommerce":
                        all_data = await ecommerece_extractor(web_data , url)
                    else:
                        all_data = await real_estate_extractor(web_data , url)
                    await context.close()
                    return {"status": "Success", "clean_data": all_data}
                else:
                    logging.info(f"⚠️ Web Data Length too short ({data_length}). Ready to retry...")

                    await context.close()
                    # Did not return here so that the retry loop continues
                    
            except Exception as e:
                logging.info(f"❌ Attempt {attempt} Error on Url: {e}")
                if context:
                    await context.close()
                # We will not return on error either so that the loop retries

            # If data was low or an error occurred, wait briefly before retrying
            if attempt < max_retries:
                await asyncio.sleep(random.uniform(2.5 , 3.5))

        logging.info(f"🚫 Max Retries Reached for URL: {url}. Now trying sp2 (fallback)...")
        try:
            web_data = await sp2(url)
            data_length = len(web_data) if web_data else 0
            
            if data_length > 25000:
                logging.info(f"✅ Data retrieved via sp2 fallback ({data_length}). Extracting data.")
                if scrape_type.lower() == "ecommerce":
                     all_data = await ecommerece_extractor(web_data , url)
                else:
                    all_data = await real_estate_extractor(web_data , url)
                return {"status": "Success", "clean_data": all_data}
            else:
                logging.info(f"⚠️ Data was low or failed even with sp2 fallback.")
                web_data = await scrape_heavy_sites(url)
                if web_data:
                    if scrape_type.lower() == "ecommerce":
                        all_data = await ecommerece_extractor(web_data , url)
                    else:
                        all_data = await real_estate_extractor(web_data , url)
                    return {"status": "Success", "clean_data": all_data}

        except Exception as e:
            logging.info(f"❌ sp2 Fallback Error on Url: {e}")

        return {"status": "Fail", "all_data": "Max retries reached and sp2 and sp3 fallback also failed."}


def main(urls: list[str] , scrape_for: str):
    all_final_results = []
    with SB(uc=True, headless=True, chromium_arg=args) as sb:
        sb.activate_cdp_mode()
        endpoint_url = sb.get_endpoint_url()
        
        # 2. Captured SeleniumBase's event loop
        loop = sb.driver.cdp.loop  # type: ignore
        
        for i in range(0, len(urls), url_limit):
            batch = urls[i:i + url_limit]
            logging.info(f"Starting batch of {len(batch)} URLs")
            
            async def run_batch():
                async with async_playwright() as p:
                    browser = await p.chromium.connect_over_cdp(endpoint_url)

                    semaphore = asyncio.Semaphore(url_limit)
                    tasks = [engine(url, browser , semaphore , scrape_for) for url in batch]
                    return await asyncio.gather(*tasks)
            
            # 3. Executed Playwright tasks on SeleniumBase's loop
            results = loop.run_until_complete(run_batch())
            all_final_results.extend(results)
            
            if i + url_limit < len(urls):
                logging.info("Batch complete. Waiting 15 seconds before next batch...")
                time.sleep(15)
                
    logging.info("All URLs scraped. Proceeding to save user data securely...")
    
    user_session_id = str(uuid.uuid4()) 
    csv_file, excel_file, user_folder = process_and_save(all_final_results, user_id=user_session_id)
    
    if csv_file and excel_file:
        logging.info(f"✅ User Data Ready! Folder: {user_folder}")
        return {
            "status": "Success",
            "user_session_id": user_session_id,
            "download_folder": user_folder,
            "csv_file_path": csv_file,
            "excel_file_path": excel_file,
            "raw_data": all_final_results
        }
    
    return {"status": "Fail", "message": "No data saved", "raw_data": all_final_results}



if __name__ == "__main__":
    main(["https://www.upwork.com/freelance-jobs/artificial-intelligence/"] , scrape_for="ecommerce")
    
    # 4. Completely removed asyncio.run from here, called main() directly
#     main(["https://www.walmart.com/search?q=shampoo",
# "https://www.amazon.com/s?k=watch",
# "https://www.ebay.com/sch/i.html?_nkw=pc&_sacat=0&_from=R40&_trksid=p2334524.m570.l1313&_odkw=0pc&_osacat=0"

# , "https://www.etsy.com/search?q=Embroidered+clothing",
# "https://www.daraz.pk/catalog/?spm=a2a0e.tm80335142.search.d_go&q=shoes"] , scrape_for="ecommerce"

# )
