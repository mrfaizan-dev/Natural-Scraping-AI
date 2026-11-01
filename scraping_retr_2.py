import asyncio
import nodriver as uc
import random
import html2text


async def scrape_heavy_sites(url):
    print(f"🚀 Launching stealth browser for: {url}")
    
    browser = await uc.start(
        headless=True,
    )
    
    try:
        page = await browser.get(url)
        print("⏳ Waiting for page to mimic human behavior...")
        await asyncio.sleep(random.uniform(5.0, 8.0))

        print("📜 Scrolling page...")
        await page.scroll_down(150)
        await asyncio.sleep(random.uniform(2.0, 4.0))

        content = await page.get_content()
        
        data_length = len(content) if content else 0
        
        if data_length > 50000:
            print(f"✅ Success! Data fetched. Length: {data_length}")
            return content
        else:
            print(f"⚠️ Content too short ({data_length}). Cloudflare challenged.")
            return None
            
    except Exception as e:
        print(f"❌ Error occurred: {e}")
    finally:
        browser.stop()

if __name__ == "__main__":
    url = "https://www.fiverr.com/gigs/rag-ai"
    html_output = asyncio.run(scrape_heavy_sites(url))
    print(html_output)