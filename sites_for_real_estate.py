from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse

def parse_zameen(card_soup, base_url="https://www.zameen.com"):
    data = {}
    try:
        # 1. Property Link & Title (from main anchor tag)
        link_tag = card_soup.select_one('a.d870ae17') or card_soup.select_one('a[href*="/Property/"]')
        if link_tag and 'href' in link_tag.attrs:
            href = link_tag['href']
            data['property_url'] = href if href.startswith('http') else f"{base_url}{href}"
        else:
            data['property_url'] = "N/A"

        # Title extraction from title attribute or h2 heading
        title_tag = card_soup.select_one('h2._36dfb99f') or link_tag
        if title_tag:
            data['title'] = title_tag.get('title') or title_tag.get_text(strip=True)
        else:
            data['title'] = "N/A"

        # 2. Price Extraction
        price_tag = card_soup.select_one('span.dc381b54') or card_soup.select_one('div._2923a568')
        data['price'] = price_tag.get_text(strip=True) if price_tag else "N/A"

        # 3. Location Extraction
        loc_tag = card_soup.select_one('div.db1aca2f')
        data['location'] = loc_tag.get_text(strip=True) if loc_tag else "N/A"

        # 4. Bedrooms, Bathrooms & Area (from features container)
        beds, baths, area = "N/A", "N/A", "N/A"
        
        # Bedrooms
        bed_tag = card_soup.select_one('span._5ca8f903:has(svg g[data-name="Icon awesome-bed"]) span._6d9b9b83') or card_soup.select_one('span[aria-label="Beds"]')
        if bed_tag:
            beds = bed_tag.get_text(strip=True)
        
        # Bathrooms
        bath_tag = card_soup.select_one('span._5ca8f903:has(svg g[data-name="Icon awesome-bath"]) span._6d9b9b83') or card_soup.select_one('span[aria-label="Baths"]')
        if bath_tag:
            baths = bath_tag.get_text(strip=True)

        # Area Size
        area_tag = card_soup.select_one('span._5ca8f903:has(svg path[d*="M10.4"]) span._6d9b9b83') or card_soup.select_one('span[aria-label="Area"]')
        if area_tag:
            area = area_tag.get_text(strip=True)

        data['bedrooms'] = beds
        data['bathrooms'] = baths
        data['area_size'] = area

        # 5. Image URL
        img_tag = card_soup.select_one('picture.a659dd2e img') or card_soup.select_one('img.fd6eb59d')
        if img_tag:
            data['image_url'] = img_tag.get('src') or img_tag.get('data-src') or "N/A"
        else:
            data['image_url'] = "N/A"

        # 6. Agency / Agent details if available
        agency_tag = card_soup.select_one('div.f87f8bd9 img')
        data['agent_or_agency'] = agency_tag.get('alt') or "Zameen Verified Agency" if agency_tag else "N/A"

        return data

    except Exception as e:
        return {
            "status": "error",
            "source": "Zameen",
            "error_type": type(e).__name__,
            "message": str(e)
        }

def parse_dubizzle(card_soup, base_url="https://www.dubizzle.com"):
    data = {}
    try:
        # 1. Property Link & Title
        link_tag = card_soup.select_one('a[data-testid="listing-1"]') or card_soup.select_one('a[href*="/property-for-sale/"]')
        if link_tag and 'href' in link_tag.attrs:
            href = link_tag['href']
            data['property_url'] = href if href.startswith('http') else f"{base_url}{href}"
        else:
            data['property_url'] = "N/A"

        # Title / Subheading extraction
        title_tag = card_soup.select_one('h2[data-testid="subheading-text"]') or card_soup.select_one('img.property')
        if title_tag and title_tag.name == 'img':
            data['title'] = title_tag.get('alt', "N/A")
        elif title_tag:
            data['title'] = title_tag.get_text(strip=True)
        else:
            data['title'] = "N/A"

        # 2. Price Extraction
        price_tag = card_soup.select_one('div[data-testid="listing-price"]')
        data['price'] = f"AED {price_tag.get_text(strip=True)}" if price_tag else "N/A"

        # 3. Location Extraction
        loc_tag = card_soup.select_one('h3[data-testid="listing-location"] span')
        data['location'] = loc_tag.get_text(strip=True) if loc_tag else "N/A"

        # 4. Bedrooms, Bathrooms & Area Size
        bed_tag = card_soup.select_one('div[data-testid="listing-bedrooms"]')
        data['bedrooms'] = bed_tag.get_text(strip=True) if bed_tag else "N/A"

        bath_tag = card_soup.select_one('div[data-testid="listing-bathrooms"]')
        data['bathrooms'] = bath_tag.get_text(strip=True) if bath_tag else "N/A"

        # Built-up & Plot size extraction
        size_tag = card_soup.select_one('h3[data-testid="listing-size"]')
        data['area_size'] = size_tag.get_text(strip=True) if size_tag else "N/A"

        # 5. Image URL
        img_tag = card_soup.select_one('img.property[src*="dbz-images.dubizzle.com"]') or card_soup.select_one('img.property')
        if img_tag:
            data['image_url'] = img_tag.get('src') or img_tag.get('data-src') or "N/A"
        else:
            data['image_url'] = "N/A"

        data['agent_or_agency'] = "Dubizzle Verified Listing"

        return data

    except Exception as e:
        return {
            "status": "error",
            "source": "Dubizzle",
            "error_type": type(e).__name__,
            "message": str(e)
        }

def parse_property_finder(card_soup, base_url="https://www.propertyfinder.ae"):
    data = {}
    try:
        # 1. Property Link & Title
        link_tag = card_soup.select_one('a[data-testid="link"]') or card_soup.select_one('a[href*="/plp/rent/"]')
        if link_tag and 'href' in link_tag.attrs:
            href = link_tag['href']
            data['property_url'] = href if href.startswith('http') else f"{base_url}{href}"
        else:
            data['property_url'] = "N/A"

        # Title extraction from heading or image alt
        title_tag = card_soup.select_one('h3.styles-module_content__title__maprN') or card_soup.select_one('img[data-testid="gallery-picture"]')
        if title_tag and title_tag.name == 'img':
            data['title'] = title_tag.get('alt', "N/A")
        elif title_tag:
            data['title'] = title_tag.get_text(strip=True)
        else:
            data['title'] = "N/A"

        # 2. Price Extraction
        price_tag = card_soup.select_one('div[data-testid="property-card-price"]')
        data['price'] = price_tag.get_text(strip=True) if price_tag else "N/A"

        # 3. Location Extraction
        loc_tag = card_soup.select_one('div[data-testid="property-card-location"]')
        data['location'] = loc_tag.get_text(strip=True) if loc_tag else "N/A"

        # 4. Bedrooms, Bathrooms & Area Size
        bed_tag = card_soup.select_one('p[data-testid="property-card-spec-bedroom"]')
        data['bedrooms'] = bed_tag.get_text(strip=True) if bed_tag else "N/A"

        bath_tag = card_soup.select_one('p[data-testid="property-card-spec-bathroom"]')
        data['bathrooms'] = bath_tag.get_text(strip=True) if bath_tag else "N/A"

        area_tag = card_soup.select_one('p[data-testid="property-card-spec-area"]')
        data['area_size'] = area_tag.get_text(strip=True) if area_tag else "N/A"

        # 5. Image URL
        img_tag = card_soup.select_one('img[data-testid="gallery-picture"]')
        if img_tag:
            data['image_url'] = img_tag.get('src') or img_tag.get('data-src') or "N/A"
        else:
            data['image_url'] = "N/A"

        # 6. Agent / Agency details
        agent_tag = card_soup.select_one('h3.styles-module_agent-info__name__6J1tN')
        data['agent_or_agency'] = agent_tag.get_text(strip=True) if agent_tag else "Property Finder Agent"

        return data

    except Exception as e:
        return {
            "status": "error",
            "source": "PropertyFinder",
            "error_type": type(e).__name__,
            "message": str(e)
        }


def parse_rightmove(card_soup, base_url="https://www.rightmove.co.uk"):
    data = {}
    try:
        # 1. Property Link & Title
        link_tag = card_soup.select_one('a[data-monitor-testid="propertyCard-img-link"]') or card_soup.select_one('a[href*="/properties/"]')
        if link_tag and 'href' in link_tag.attrs:
            href = link_tag['href']
            data['property_url'] = href if href.startswith('http') else f"{base_url}{href}"
        else:
            data['property_url'] = "N/A"

        # Property Type or Title (e.g. Maisonette)
        type_tag = card_soup.select_one('span.PropertyInformation_propertyType__u8e76')
        addr_tag = card_soup.select_one('address.PropertyAddress_address__LYRPq')
        
        prop_type = type_tag.get_text(strip=True) if type_tag else "Property"
        address = addr_tag.get_text(strip=True) if addr_tag else "N/A"
        data['title'] = f"{prop_type} at {address}"

        # 2. Price Extraction
        price_tag = card_soup.select_one('div.PropertyPrice_price__VL65t')
        qualifier_tag = card_soup.select_one('div.PropertyPrice_priceQualifier__U1Qu7')
        
        price = price_tag.get_text(strip=True) if price_tag else "N/A"
        qualifier = qualifier_tag.get_text(strip=True) if qualifier_tag else ""
        data['price'] = f"{qualifier} {price}".strip()

        # 3. Location Extraction
        data['location'] = address

        # 4. Bedrooms, Bathrooms
        bed_tag = card_soup.select_one('span.PropertyInformation_bedroomsCount___2b5R')
        data['bedrooms'] = bed_tag.get_text(strip=True) if bed_tag else "N/A"

        bath_tag = card_soup.select_one('span[aria-label*="in property"]') # Fallback or select bath count container
        if not bath_tag:
            bath_container = card_soup.select_one('div.PropertyInformation_bathContainer__ut8VY span')
            data['bathrooms'] = bath_container.get_text(strip=True) if bath_container else "1"
        else:
            data['bathrooms'] = bath_tag.get_text(strip=True)

        data['area_size'] = "N/A"

        # 5. Image URL (Rightmove cards mein image background ya alag element me hoti hai, fallback handle kiya hai)
        img_tag = card_soup.select_one('img.EstateAgent_estateAgentLogo__v5fOg')
        data['image_url'] = "N/A" # Main image card background se hoti hai, fallback agency logo ya N/A

        # 6. Agent / Agency details
        marketed_tag = card_soup.select_one('span[data-testid="marketed-by-text"]')
        data['agent_or_agency'] = marketed_tag.get_text(strip=True) if marketed_tag else "Rightmove Partner Agent"

        return data

    except Exception as e:
        return {
            "status": "error",
            "source": "Rightmove",
            "error_type": type(e).__name__,
            "message": str(e)
        }


def parse_zillow(card_soup, base_url="https://www.zillow.com"):
    data = {}
    try:
        # 1. Property Link & Title
        link_tag = card_soup.select_one('a[data-testid="property-card-address-link"]') or card_soup.select_one('a[data-testid="carousel-photo"]')
        if link_tag and 'href' in link_tag.attrs:
            href = link_tag['href']
            data['property_url'] = href if href.startswith('http') else f"{base_url}{href}"
        else:
            data['property_url'] = "N/A"

        # Title from Image Alt or Address
        img_tag = card_soup.select_one('img[data-c11n-component="Image"]') or card_soup.select_one('img')
        addr_tag = card_soup.select_one('address')
        
        address = addr_tag.get_text(strip=True) if addr_tag else "N/A"
        img_alt = img_tag.get('alt', "Zillow Property") if img_tag else "Zillow Property"
        
        data['title'] = img_alt if img_alt != "Zillow Property" else address

        # 2. Price Extraction
        price_tag = card_soup.select_one('span[data-testid="property-card-price"]') or card_soup.select_one('span.srp-bueOgM')
        data['price'] = price_tag.get_text(strip=True) if price_tag else "N/A"

        # 3. Location Extraction
        data['location'] = address

        # 4. Bedrooms, Bathrooms & Area Size
        beds, baths, area = "N/A", "N/A", "N/A"
        details_list = card_soup.select('ul[data-testid="property-card-details"] li')
        
        if len(details_list) >= 3:
            beds = details_list[0].get_text(strip=True)
            baths = details_list[1].get_text(strip=True)
            area = details_list[2].get_text(strip=True)
        else:
            # Fallback text check
            for li in details_list:
                text = li.get_text(strip=True).lower()
                if 'bd' in text:
                    beds = text
                elif 'ba' in text:
                    baths = text
                elif 'sqft' in text or 'sq ft' in text:
                    area = text

        data['bedrooms'] = beds
        data['bathrooms'] = baths
        data['area_size'] = area

        # 5. Image URL
        if img_tag:
            data['image_url'] = img_tag.get('src') or img_tag.get('data-src') or "N/A"
        else:
            data['image_url'] = "N/A"

        # 6. Broker / Agency Details
        broker_tag = card_soup.select_one('div.c11n_property-card__data-area') or card_soup.select_one('div[class*="srp-fzoNvt"]')
        data['agent_or_agency'] = broker_tag.get_text(strip=True) if broker_tag else "Zillow Real Estate Partner"

        return data

    except Exception as e:
        return {
            "status": "error",
            "source": "Zillow",
            "error_type": type(e).__name__,
            "message": str(e)
        }

