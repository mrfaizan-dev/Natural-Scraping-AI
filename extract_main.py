import time, os, random
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import asyncio, logging
from bs4 import BeautifulSoup as bs

from sites_for_ecom import (
    parse_amazon, 
    parse_ebay, 
    parse_etsy, 
    parse_aliexpress, 
    parse_daraz, 
    parse_noon, 
    parse_walmart
)

from sites_for_real_estate import (
    parse_zameen, 
    parse_dubizzle, 
    parse_property_finder, 
    parse_rightmove,
    parse_zillow
    )

from pydantic_v2_main import Product , RealEstate


def validate_property(raw_data, source_name=None):
    if not raw_data or not isinstance(raw_data, dict):
        return None
    
    if raw_data.get("status") == "error":
        return raw_data
    
    if source_name and "source" not in raw_data:
        raw_data["source"] = source_name

    title = str(raw_data.get("title", "")).strip()
    url = str(raw_data.get("property_url", "")).strip()

    if (not title or title.lower() in ["n/a", "none", "nan"]) and (not url or url.lower() in ["n/a", "none", "nan"]):
        return None

    try:
        return RealEstate(**raw_data).model_dump()
    except Exception as e:
        logging.error(f"Pydantic RealEstate Validation Error: {e}")
        return raw_data


def validate_product(raw_data, source_name=None):
    if not raw_data or not isinstance(raw_data, dict):
        return None
    
    if raw_data.get("status") == "error":
        return raw_data
    
    if source_name and "source" not in raw_data:
        raw_data["source"] = source_name

    # Check if this is a valid product card and not a header/footer dummy link
    title = str(raw_data.get("title", "")).strip()
    url = str(raw_data.get("product_url", "")).strip()

    if (not title or title.lower() in ["n/a", "none", "nan", "shop on ebay"]) and ("mobile-apps" in url or not url or url.lower() in ["n/a", "none", "nan"]):
        return None

    try:
        return Product(**raw_data).model_dump()
    except Exception as e:
        logging.error(f"Pydantic Validation Error: {e}")
        return raw_data


async def ecommerece_extractor(html_content, url):
    try:
        soup = bs(html_content, 'html.parser')


        if 'ebay' in url:
                # URL ko process karne se pehle clean/short karein
                clean_url = url
                
                # 'or' ki jagah comma (,) use kiya hai taake naye aur purane dono designs (s-item aur s-card) ke cards ek sath pick ho sakein
                cards = soup.select('li.s-item, li.s-card, div.s-card, div.s-item__wrapper, div.brwrvr__item-card')
                
                products = []
                for card in cards:
                    parsed_data = parse_ebay(card)
                    validated = validate_product(parsed_data, "eBay")
                    if validated:
                        products.append(validated)
                        
                return {"Clean_Data": products}
        
        elif 'amazon' in url:
                    
                    parsed_url = urlparse(url)
                    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                    
                    cards = soup.select('div[data-component-type="s-search-result"]') or soup.select('div.s-result-item[data-asin]')
                    data = []
                    for card in cards:
                        v = validate_product(parse_amazon(card, base_url=base_url), "Amazon")
                        if v:
                            data.append(v)
                        
                    return {"Clean_Data": data}

        elif 'etsy' in url:
            cards = soup.select('div.v2-listing-card') or soup.select('a.listing-link')
            data = []
            for card in cards:
                v = validate_product(parse_etsy(card), "Etsy")
                if v:
                    data.append(v)
            return {"Clean_Data": data}

        elif 'aliexpress' in url:
            cards = soup.select('a.search-card-item') or soup.select('div[class*="search-card-item"]')
            data = []
            for card in cards:
                v = validate_product(parse_aliexpress(card), "AliExpress")
                if v:
                    data.append(v)
            return {"Clean_Data": data}

        elif 'daraz' in url:
            cards = (
                soup.select('div[data-qa-locator="product-item"]') or 
                soup.select('div.gridItem--1_jI6') or 
                soup.select('div.c2pr38') or 
                soup.select('div[data-tracking="product-card"]') or
                soup.select('div.c1_634')
            )
            data = []
            for card in cards:
                v = validate_product(parse_daraz(card), "Daraz")
                if v:
                    data.append(v)
            return {"Clean_Data": data}
        
        elif 'noon' in url:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            cards = soup.select('a[class*="productBoxLink"]') or soup.select('div[class*="productContainer"]')
            data = []
            for card in cards:
                v = validate_product(parse_noon(card, base_url=base_url), "Noon")
                if v:
                    data.append(v)
            return {"Clean_Data": data}

        elif 'walmart' in url:
            cards = soup.select('div[data-automation-id="search-result-grid-item"]') or soup.select('div[data-item-id]')
            data = []
            for card in cards:
                v = validate_product(parse_walmart(card), "Walmart")
                if v:
                    data.append(v)
            return {"Clean_Data": data}
        
        else:
            return {"error": "Unsupported Domain", "url": url}

    except Exception as e:
        logging.info(f"Extracting Error: {e}")
        return {"error": str(e)}


async def real_estate_extractor(html_content, url):
    try:
        soup = bs(html_content, 'html.parser')

        if 'zameen.com' in url:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            cards = soup.select('article._5b98ebdf') or soup.select('div[role="article"]')
            data = []
            for card in cards:
                parsed_data = parse_zameen(card, base_url=base_url)
                validated = validate_property(parsed_data, "Zameen")
                if validated:
                    data.append(validated)
            return {"Clean_Data": data}

        elif 'dubizzle.com' in url:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            cards = soup.select('div[id^="listing-card-"]') or soup.select('div.property-lpv-card-1')
            data = []
            for card in cards:
                parsed_data = parse_dubizzle(card, base_url=base_url)
                validated = validate_property(parsed_data, "Dubizzle")
                if validated:
                    data.append(validated)
            return {"Clean_Data": data}

        elif 'propertyfinder.ae' in url:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            cards = soup.select('div[data-testid="gallery-item"]') or soup.select('div[data-testid="property-card"]')
            data = []
            for card in cards:
                parsed_data = parse_property_finder(card, base_url=base_url)
                validated = validate_property(parsed_data, "PropertyFinder")
                if validated:
                    data.append(validated)
            return {"Clean_Data": data}

        elif 'rightmove.co.uk' in url:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            cards = soup.select('div.propertyCard') or soup.select('div[data-testid="property-card"]') or [soup]
            data = []
            for card in cards:
                parsed_data = parse_rightmove(card, base_url=base_url)
                validated = validate_property(parsed_data, "Rightmove")
                if validated:
                    data.append(validated)
            return {"Clean_Data": data}

        elif 'zillow.com' in url:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            # Zillow property card containers / articles selector
            cards = soup.select('article[data-test="property-card"]') or soup.select('div.property-card-data') or [soup]
            data = []
            for card in cards:
                parsed_data = parse_zillow(card, base_url=base_url)
                validated = validate_property(parsed_data, "Zillow")
                if validated:
                    data.append(validated)
            return {"Clean_Data": data}

        else:
            return {"error": "Unsupported Real Estate Domain", "url": url}

    except Exception as e:
        logging.info(f"Real Estate Extracting Error: {e}")
        return {"error": str(e)}



