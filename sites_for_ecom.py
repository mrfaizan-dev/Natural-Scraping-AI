from bs4 import BeautifulSoup as bs

def parse_amazon(card_soup, base_url="https://www.amazon.com"):
    data = {}

    try:
        # 1. Product Title
        title_tag = card_soup.select_one('h2.a-size-base-plus span') or card_soup.select_one('h2 a span') or card_soup.select_one('span.a-text-normal')
        data['title'] = title_tag.get_text(strip=True) if title_tag else "N/A"

        # 2. Product Link (Dynamic Domain support for .ae, .sa, .com, etc.)
        link_tag = card_soup.select_one('a.a-link-normal.s-no-outline') or card_soup.select_one('h2 a.a-link-normal')
        if link_tag and 'href' in link_tag.attrs:
            href = link_tag['href']
            data['product_url'] = href if href.startswith('http') else f"{base_url}{href}"
        else:
            data['product_url'] = "N/A"

        # 3. Main Image URL
        img_tag = card_soup.select_one('img.s-image')
        data['image_url'] = img_tag['src'] if img_tag and 'src' in img_tag.attrs else "N/A"

        # 4. Price (Currency AED / SAR / USD automatically handled)
        price_offscreen = card_soup.select_one('span.a-price span.a-offscreen')
        
        if price_offscreen:
            data['price'] = price_offscreen.get_text(strip=True)
        else:
            price_symbol = card_soup.select_one('span.a-price-symbol')
            price_whole = card_soup.select_one('span.a-price-whole')
            price_fraction = card_soup.select_one('span.a-price-fraction')
            
            if price_whole:
                symbol = price_symbol.get_text(strip=True) if price_symbol else ""
                whole = price_whole.get_text(strip=True)
                fraction = price_fraction.get_text(strip=True) if price_fraction else ""
                data['price'] = f"{symbol}{whole}{fraction}"
            else:
                data['price'] = "N/A"

        # 5. Rating
        rating_tag = card_soup.select_one('i[data-cy="reviews-ratings-slot"] span.a-icon-alt') or card_soup.select_one('i.a-icon-star-small span.a-icon-alt')
        data['rating'] = rating_tag.get_text(strip=True) if rating_tag else "N/A"

        # 6. Total Reviews / Ratings Count
        reviews_tag = card_soup.select_one('span.s-underline-text')
        data['reviews'] = reviews_tag.get_text(strip=True).replace('(', '').replace(')', '') if reviews_tag else "N/A"

        # 7. Sales/Bought in past month
        sales_tags = card_soup.select('span.a-size-base.a-color-secondary')
        data['past_month_sales'] = "N/A"
        for tag in sales_tags:
            text = tag.get_text(strip=True)
            if 'bought' in text.lower() or 'تم شراء' in text:
                data['past_month_sales'] = text
                break

        # 8. Title Differentiators / Subtitle
        subtitle_tag = card_soup.select_one('span.title-differentiators')
        data['subtitle'] = subtitle_tag.get_text(strip=True) if subtitle_tag else "N/A"

        return data

    except Exception as e:
        return {
    "status": "error",
    "source": "Amazon",
    "error_type": type(e).__name__,
    "message": str(e)
}


def parse_ebay(card_soup):
    data = {}
    try:
        # 1. Product Title (Support for both new 's-card' and old 's-item' layouts)
        title_tag = card_soup.select_one('.s-card__title, .s-item__title, h3.bsig__title__text, h3')
        title = "N/A"
        if title_tag:
            # "Opens in a new window" jaise hidden span texts ko remove karna
            for clipped in title_tag.select('.clipped, .LIGHT_WEIGHT'):
                clipped.decompose()
            title = title_tag.get_text(strip=True)
        
        # Faltu ya empty cards ko filter karna
        if "Shop on eBay" in title or title == "N/A" or not title:
            return None
        data['title'] = title

        # 2. Product Link
        link_tag = card_soup.select_one('a.s-card__link, a.s-item__link, a.bsig__title__wrapper, a[href*="/itm/"]')
        data['product_url'] = link_tag.get('href', "N/A") if link_tag else "N/A"

        # 3. Image URL
        img_tag = card_soup.select_one('div.s-item__image-wrapper img, img.brwrvr__item-card__image, img')
        if img_tag:
            data['image_url'] = img_tag.get('src') or img_tag.get('data-src') or "N/A"
        else:
            data['image_url'] = "N/A"

        # 4. Price (Extracting from new classes like .s-card__price)
        price_tag = card_soup.select_one('.s-card__price, .s-item__price, span.bsig__price')
        data['price'] = price_tag.get_text(strip=True) if price_tag else "N/A"

        # Initialize Default Variables
        condition = "N/A"
        sold_count = "N/A"
        delivery = "N/A"
        location = "N/A"
        
        # 5. Item Condition (e.g., Pre-Owned, Brand New)
        cond_tag = card_soup.select_one('span.su-styled-text.secondary.default, .s-item__subtitle, span.bsig__listingCondition')
        if cond_tag:
            condition = cond_tag.get_text(strip=True)
        
        # 6. Extracting Attributes dynamically (Shipping, Sold, Location from grid/list rows)
        attr_rows = card_soup.select('.s-card__attribute-row, .s-item__detail, .s-item__shipping, .s-item__hotness')
        for row in attr_rows:
            text = row.get_text(strip=True)
            text_lower = text.lower()
            
            if 'sold' in text_lower or 'almost gone' in text_lower:
                sold_count = text
            elif 'shipping' in text_lower or 'delivery' in text_lower or 'free' in text_lower:
                # Sirf tabhi assign karein agar pehle se set na ho
                if delivery == "N/A": 
                    delivery = text
            elif 'located in' in text_lower or 'from' in text_lower:
                location = text

        # 6.1 Naya Check: Specific target for "94+ sold" with new span classes
        specific_sold_tag = card_soup.select_one('.s-card__attribute-row span.su-styled-text.primary.bold.large')
        if specific_sold_tag:
            tag_text = specific_sold_tag.get_text(strip=True)
            if 'sold' in tag_text.lower() or '+' in tag_text:
                sold_count = tag_text

        # 7. Seller Info Extraction
        seller_name = "N/A"
        seller_rating = "N/A"
        
        for row in card_soup.select('.s-card__attribute-row'):
            spans = row.select('span.su-styled-text.primary.large')
            # Check karte hain ke kya 2 span hain aur dusre mein '%' (rating) hai
            if len(spans) >= 2 and '%' in spans[1].get_text(strip=True):
                seller_name = spans[0].get_text(strip=True)
                seller_rating = spans[1].get_text(strip=True)
                break

        # Saving all variables in data dictionary
        data['condition'] = condition
        data['sold_count'] = sold_count
        data['delivery'] = delivery
        data['location'] = location
        data['seller_name'] = seller_name      
        data['seller_rating'] = seller_rating  

        return data

    except Exception as e:
        return {
            "status": "error",
            "source": "Ebay",
            "error_type": type(e).__name__,
            "message": str(e)
        }



def parse_etsy(card_soup):
    data = {}

    try:
        # 1. Product Link
        link_tag = card_soup if card_soup.name == 'a' else card_soup.select_one('a.listing-link')
        data['product_url'] = link_tag['href'] if link_tag and 'href' in link_tag.attrs else "N/A"

        # 2. Product Title
        title_tag = card_soup.select_one('h3.v2-listing-card__title')
        data['title'] = title_tag.get_text(strip=True) if title_tag else "N/A"

        # 3. Main Image URL
        img_tag = card_soup.select_one('img.wt-image') or card_soup.select_one('img')
        data['image_url'] = img_tag.get('src') or img_tag.get('data-src') or "N/A" if img_tag else "N/A"

        # 4. Rating
        rating_tag = card_soup.select_one('span.clg-static-review-stars__rating-label') or \
                    card_soup.select_one('.inline-title-and-stars-wrap span.wt-text-title-small')
        data['rating'] = rating_tag.get_text(strip=True) if rating_tag else "N/A"

        # 5. Reviews Count
        reviews_tag = card_soup.select_one('span.clg-static-review-stars__review-count') or \
                    card_soup.select_one('.inline-title-and-stars-wrap p.wt-text-body-smaller')
        data['reviews'] = reviews_tag.get_text(strip=True).replace('(', '').replace(')', '') if reviews_tag else "N/A"

        # 6. Shop Name / Seller
        shop_tag = card_soup.select_one('p[data-seller-name-container] span[aria-hidden="true"]') or \
                card_soup.select_one('span.clickable-shop-name')
        data['shop_name'] = shop_tag.get_text(strip=True) if shop_tag else "N/A"

        # 7. Price
        currency_tag = card_soup.select_one('.currency-symbol')
        price_tag = card_soup.select_one('.currency-value')
        if price_tag:
            currency = currency_tag.get_text(strip=True) if currency_tag else "$"
            price = price_tag.get_text(strip=True)
            data['price'] = f"{currency}{price}"
        else:
            data['price'] = "N/A"

        # 8. Urgency / Extra Info
        urgency_tag = card_soup.select_one('.wt-text-brick')
        data['urgency'] = urgency_tag.get_text(strip=True).replace('\xa0', ' ') if urgency_tag else "N/A"

        return data

    except Exception as e:
        return {
    "status": "error",
    "source": "Etsy",
    "error_type": type(e).__name__,
    "message": str(e)
}


def parse_aliexpress(card_soup):
    data = {}

    try:
        # 1. Product Link
        link_tag = card_soup if card_soup.name == 'a' else card_soup.select_one('a.search-card-item') or card_soup.select_one('a[href*="/item/"]')
        if link_tag and 'href' in link_tag.attrs:
            href = link_tag['href']
            data['product_url'] = f"https:{href}" if href.startswith('//') else href
        else:
            data['product_url'] = "N/A"

        # 2. Product Title
        title_tag = card_soup.select_one('h3[class*="titleText"]') or card_soup.select_one('div[class*="title--"]')
        data['title'] = title_tag.get_text(strip=True) if title_tag else "N/A"

        # 3. Main Image URL
        img_tag = card_soup.select_one('img[class*="images--item"]') or card_soup.select_one('img')
        if img_tag:
            img_src = img_tag.get('src') or img_tag.get('data-src') or ""
            data['image_url'] = f"https:{img_src}" if img_src.startswith('//') else (img_src if img_src else "N/A")
        else:
            data['image_url'] = "N/A"

        # 4. Sale Price
        price_container = card_soup.select_one('div[class*="us--price--"]')
        if price_container and price_container.get('aria-label'):
            data['price'] = price_container.get('aria-label')
        else:
            price_tag = card_soup.select_one('div[class*="price-sale"]')
            data['price'] = price_tag.get_text(strip=True) if price_tag else "N/A"

        # 5. Original Price
        orig_price_tag = card_soup.select_one('div[class*="price-original"]')
        data['original_price'] = orig_price_tag.get_text(strip=True) if orig_price_tag else "N/A"

        # 6. Discount Tag
        discount_tag = card_soup.select_one('span[class*="minDiscount"]')
        data['discount'] = discount_tag.get_text(strip=True) if discount_tag else "N/A"

        # 7. Star Rating
        rating_tag = card_soup.select_one('span[class*="starRating"]')
        data['rating'] = rating_tag.get_text(strip=True) if rating_tag else "N/A"

        # 8. Sold Count
        sold_tag = card_soup.select_one('span[class*="trade--"]')
        data['sold_count'] = sold_tag.get_text(strip=True) if sold_tag else "N/A"

        # 9. Special Buyer Tag / Offer
        promo_tag = card_soup.select_one('span[class*="tag--textStyle"]')
        data['promotion'] = promo_tag.get_text(strip=True) if promo_tag else "N/A"

        return data

    except Exception as e:
        return {
    "status": "error",
    "source": "AliExpress",
    "error_type": type(e).__name__,
    "message": str(e)
}


def parse_daraz(card_soup):
    data = {}

    try:
        # 1. Product Link (Auto-fixes '//' relative URLs)
        link_tag = card_soup if card_soup.name == 'a' else card_soup.select_one('a[href*="/products/"]') or card_soup.select_one('a[href]')
        if link_tag and 'href' in link_tag.attrs:
            href = link_tag['href']
            data['product_url'] = f"https:{href}" if href.startswith('//') else href
        else:
            data['product_url'] = "N/A"

        # 2. Product Title
        title_tag = card_soup.select_one('a[title]') or card_soup.select_one('a[href*="/products/"]')
        if title_tag:
            data['title'] = title_tag.get('title') or title_tag.get_text(strip=True)
        else:
            data['title'] = "N/A"

        # 3. Main Image URL
        img_tag = card_soup.select_one('img[type="product"]') or card_soup.select_one('img')
        if img_tag:
            img_src = img_tag.get('src') or img_tag.get('data-src') or ""
            data['image_url'] = f"https:{img_src}" if img_src.startswith('//') else (img_src if img_src else "N/A")
        else:
            data['image_url'] = "N/A"

        # 4. Price
        price_tag = card_soup.select_one('span.ooOxS') or card_soup.select_one('span[class*="ooOxS"]')
        data['price'] = price_tag.get_text(strip=True) if price_tag else "N/A"

        # 5. Discount Tag
        discount_tag = card_soup.select_one('span.IcOsH') or card_soup.select_one('span[class*="IcOsH"]')
        data['discount'] = discount_tag.get_text(strip=True) if discount_tag else "N/A"

        # 6. Reviews Count (e.g. "30" or "396")
        reviews_tag = card_soup.select_one('span.qzqFw') or card_soup.select_one('span[class*="qzqFw"]')
        data['reviews'] = reviews_tag.get_text(strip=True).replace('(', '').replace(')', '') if reviews_tag else "N/A"

        # 7. Sold Count (e.g. "206 sold")
        data['sold_count'] = "N/A"
        for span in card_soup.select('span'):
            text = span.get_text(strip=True)
            if 'sold' in text.lower():
                data['sold_count'] = text
                break

        # 8. Seller Location (e.g. "Sindh")
        location_tag = card_soup.select_one('span.oa6ri') or card_soup.select_one('span[class*="oa6ri"]')
        data['location'] = location_tag.get_text(strip=True) if location_tag else "N/A"

        # 9. Coins / Special Savings Tag
        promo_tag = card_soup.select_one('span.ic-dynamic-badge')
        data['promotion'] = promo_tag.get_text(strip=True) if promo_tag else "N/A"

        return data

    except Exception as e:
        return {
    "status": "error",
    "source": "Daraz",
    "error_type": type(e).__name__,
    "message": str(e)
}

def parse_noon(card_soup, base_url="https://www.noon.com"):
    data = {}

    try:
        # 1. Product Link (Dynamic domain support for UAE, KSA, Egypt)
        link_tag = card_soup if card_soup.name == 'a' else card_soup.select_one('a[class*="productBoxLink"]') or card_soup.select_one('a[href*="/p/"]')
        if link_tag and 'href' in link_tag.attrs:
            href = link_tag['href']
            data['product_url'] = href if href.startswith('http') else f"{base_url}{href}"
        else:
            data['product_url'] = "N/A"

        # 2. Product Title (Using Data-QA attribute for 100% accuracy)
        title_tag = card_soup.select_one('[data-qa="product-box-name"]') or card_soup.select_one('h2[class*="title"]')
        if title_tag:
            data['title'] = title_tag.get('title') or title_tag.get_text(strip=True)
        else:
            data['title'] = "N/A"

        # 3. Main Image URL
        img_tag = card_soup.select_one('img[class*="productImage"]') or card_soup.select_one('[data-qa*="productImagePLP"] img') or card_soup.select_one('img')
        if img_tag:
            data['image_url'] = img_tag.get('src') or img_tag.get('data-src') or "N/A"
        else:
            data['image_url'] = "N/A"

        # 4. Price (Extracting just the amount since Noon uses custom font for currency)
        price_tag = card_soup.select_one('strong[class*="amount"]') or card_soup.select_one('[data-qa="product-box-price"] strong')
        data['price'] = price_tag.get_text(strip=True) if price_tag else "N/A"

        # 5. Rating (e.g., "5.0")
        rating_tag = card_soup.select_one('div[class*="textCtr"]') or card_soup.select_one('div[class*="starContainer"] + div')
        data['rating'] = rating_tag.get_text(strip=True) if rating_tag else "N/A"

        # 6. Reviews Count (e.g., "5")
        reviews_tag = card_soup.select_one('div[class*="countCtr"] span')
        data['reviews'] = reviews_tag.get_text(strip=True) if reviews_tag else "N/A"

        # 7. Delivery / Nudge (e.g., "Free Delivery")
        delivery_tag = card_soup.select_one('div[class*="nudgeText"]')
        data['delivery'] = delivery_tag.get_text(strip=True) if delivery_tag else "N/A"

        # 8. Standard Discount (e.g., "40% Off")
        discount_tag = card_soup.select_one('span[class*="discount_"]')
        data['discount'] = discount_tag.get_text(strip=True) if discount_tag else "N/A"

        # 9. Extra Discount (e.g., "Extra 10% off")
        extra_discount = card_soup.select_one('span[class*="discountText"]')
        data['extra_discount'] = extra_discount.get_text(strip=True) if extra_discount else "N/A"

        # 10. Noon Express Delivery Check (Yes/No flag)
        express_tag = card_soup.select_one('img[alt="noon-express"]')
        data['is_express'] = "Yes" if express_tag else "No"

        return data

    except Exception as e:
        return {
    "status": "error",
    "source": "Noon",
    "error_type": type(e).__name__,
    "message": str(e)
}

def parse_walmart(card_soup):
    data = {}

    try:
        # 1. Product Title
        title_elem = card_soup.find(attrs={"data-automation-id": "product-title"})
        data['title'] = title_elem.get_text(strip=True) if title_elem else "N/A"

        # 2. Current Price (Walmart dollar aur cents ko alag span mein rakhta hai, isliye hum unhe combine karenge)
        price_elem = card_soup.find(attrs={"data-testid": "ugpp-main-price"})
        if price_elem:
            # ".fw7 span" se hum '$', 'Dollar', aur 'Cents' ke teen spans nikalenge (Jaise: $, 10, 97 -> $10.97)
            price_spans = price_elem.select(".fw7 span")
            if len(price_spans) >= 3:
                data['price'] = f"{price_spans[0].get_text(strip=True)}{price_spans[1].get_text(strip=True)}.{price_spans[2].get_text(strip=True)}"
            else:
                data['price'] = price_elem.get_text(strip=True)
        else:
            data['price'] = "N/A"

        # 3. Original Price / Was Price / Range Price
        was_price_elem = card_soup.find(attrs={"data-testid": "ugpp-was-price"})
        range_price_elem = card_soup.find(attrs={"data-testid": "ugpp-range-price"})
        
        if was_price_elem:
            data['original_price'] = was_price_elem.get_text(strip=True)
        elif range_price_elem:
            data['original_price'] = range_price_elem.get_text(strip=True) # Ex: "Options from $10.97 – $21.94"
        else:
            data['original_price'] = "N/A"

        # 4. Rating
        rating_elem = card_soup.find(attrs={"data-testid": "rating-container"})
        if rating_elem:
            rating_text = rating_elem.find("span", string=lambda x: x and "out of 5" in x.lower())
            data['rating'] = rating_text.get_text(strip=True) if rating_text else "N/A"
        else:
            fallback_rating = card_soup.find("span", string=lambda x: x and "out of 5" in x.lower())
            data['rating'] = fallback_rating.get_text(strip=True) if fallback_rating else "N/A"

        # 5. Reviews Count
        reviews_elem = card_soup.find(attrs={"data-testid": "product-reviews"})
        data['reviews'] = reviews_elem.get_text(strip=True) if reviews_elem else "N/A"

        # 6. Image URL
        img_elem = card_soup.find("img", attrs={"data-testid": "productTileImage"})
        data['image_url'] = img_elem.get("src") if img_elem else "N/A"

        # 7. Product Link (href) - PERFECTLY EXTRACTED
        link_elem = card_soup.find("a", href=True)
        if link_elem:
            href = link_elem.get("href")
            # Agar link aadhi (relative) ho, toh uske aage base URL add kar do
            if href.startswith("/"):
                data['product_url'] = f"https://www.walmart.com{href}"
            else:
                data['product_url'] = href
        else:
            data['product_url'] = "N/A"

        return data

    except Exception as e:
        return {
            "status": "error",
            "source": "Walmart",
            "error_type": type(e).__name__,
            "message": str(e)
        }

