import pandas as pd
import numpy as np
import re
import os
import time
import uuid
import shutil
import glob
from sqlalchemy import create_engine
from pydantic_v2_main import settings
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def cleanup_old_folders(base_dir="user_downloads", max_age_seconds=600):
    """10 minute se purane user folders ko automatically delete karega taake space bache."""
    if not os.path.exists(base_dir):
        return
    
    now = time.time()
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)
        if os.path.isdir(folder_path):
            if os.stat(folder_path).st_mtime < now - max_age_seconds:
                try:
                    shutil.rmtree(folder_path) 
                    print(f"🗑️ Cleaned up old user folder: {folder_path}")
                except Exception:
                    pass

def clean_text_advanced(val):
    """Uses Regex and Numpy to perfectly clean scraped text."""
    if pd.isna(val) or val is None or str(val).strip().lower() in ["nan", "none", "null", ""]:
        return "N/A"
    
    val_str = str(val).strip()
    clean_str = re.sub(r'\s+', ' ', val_str) 
    
    return clean_str if clean_str else "N/A"

def process_and_save(raw_results, user_id=None):
    """
    Data ko unique user folder me save karega taake mix na ho, aur Database me bhi bhejega.
    """
    base_dir = "user_downloads"
    cleanup_old_folders(base_dir, max_age_seconds=600) 
    
    # Agar user_id nahi mili to nayi bana dega (Folder creation)
    if not user_id:
        user_id = str(uuid.uuid4())
        
    user_folder = os.path.join(base_dir, str(user_id))
    os.makedirs(user_folder, exist_ok=True)
    
    all_products = []
    
    # 1. Flatten the Mixed Data
    for result in raw_results:
        if isinstance(result, dict) and result.get("status") == "Success":
            clean_data_dict = result.get("clean_data", {})
            products = clean_data_dict.get("Clean_Data", [])
            
            if isinstance(products, dict) and "error" not in products:
                all_products.append(products)
            elif isinstance(products, list):
                valid_prods = [p for p in products if isinstance(p, dict) and "error" not in p]
                all_products.extend(valid_prods)

    if not all_products:
        print("⚠️ No valid product or property data extracted. Files not saved.")
        return None, None, None

    df = pd.DataFrame(all_products)
    df.replace([r'^\s*$', "None", "null"], np.nan, regex=True, inplace=True)
    
    for col in df.columns:
        df[col] = df[col].apply(clean_text_advanced)

    preferred_order = [
        'title', 'price', 'original_price', 'discount', 'extra_discount', 
        'property_type', 'bedrooms', 'bathrooms', 'area_size', 
        'rating', 'reviews', 'sold_count', 'past_month_sales', 'is_express', 
        'delivery', 'condition', 'shop_name', 'location', 'address', 
        'agent_or_agency', 'phone', 'urgency', 'promotion', 'subtitle', 
        'description', 'image_url', 'product_url', 'property_url', 'source'
    ]
    
    existing_cols = df.columns.tolist()
    ordered_cols = [c for c in preferred_order if c in existing_cols]
    remaining_cols = [c for c in existing_cols if c not in ordered_cols]
    df = df[ordered_cols + remaining_cols]

    # --- 2. POSTGRESQL DATABASE SAVING LOGIC ---
    if settings.db_url:
        try:
            engine = create_engine(settings.db_url)
            df.to_sql('scraped_products', con=engine, if_exists='append', index=False)
            print("🐘 ✅ Data PostgreSQL database me successfully save ho gaya!")
        except Exception as e:
            print(f"⚠️ Database me save karte waqt error aaya: {e}")
    # --------------------------------------------

    # 3. Generate Filenames inside the User's Folder
    file_prefix = str(uuid.uuid4())[:5].upper()
    csv_filename = os.path.join(user_folder, f"VIP_Data_{file_prefix}.csv")
    excel_filename = os.path.join(user_folder, f"VIP_Data_{file_prefix}.xlsx")

    # 4. Save Base CSV
    df.to_csv(csv_filename, index=False, encoding="utf-8-sig")

    # 5. Advanced VIP Excel Creation
    with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Pro Data')
        
        workbook = writer.book
        worksheet = writer.sheets['Pro Data']
        
        # VIP STYLING CONFIGURATION
        header_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
        header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF") 
        data_font = Font(name="Segoe UI", size=10)
        zebra_fill = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")
        
        thin_border = Border(
            left=Side(style='thin', color='D9D9D9'), right=Side(style='thin', color='D9D9D9'),
            top=Side(style='thin', color='D9D9D9'), bottom=Side(style='thin', color='D9D9D9')
        )

        worksheet.row_dimensions[1].height = 28
        for col_num in range(1, len(df.columns) + 1):
            cell = worksheet.cell(row=1, column=col_num)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = thin_border
            cell.value = str(cell.value).replace("_", " ").title()

        for row_num in range(2, len(df) + 2):
            is_even = (row_num % 2 == 0)
            worksheet.row_dimensions[row_num].height = 55 
            
            for col_num, col_name in enumerate(df.columns, start=1):
                cell = worksheet.cell(row=row_num, column=col_num)
                cell.font = data_font
                cell.border = thin_border
                
                if is_even:
                    cell.fill = zebra_fill
                
                if col_name == "title":
                    cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True, indent=1)
                elif col_name in ["product_url", "property_url", "image_url"]:
                    url_val = str(cell.value).strip()
                    if url_val and url_val.upper() != "N/A":
                        cell.hyperlink = url_val
                        if col_name == "product_url":
                            cell.value = "View Product"
                        elif col_name == "property_url":
                            cell.value = "View Property"
                        else:
                            cell.value = "View Image"
                        cell.font = Font(name="Segoe UI", size=10, color="0563C1", underline="single")
                    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

                elif col_name in ["subtitle", "promotion", "description"]:
                    cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True, indent=1)
                else:
                    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        for col_num, col_name in enumerate(df.columns, start=1):
            col_letter = get_column_letter(col_num)
            
            if col_name == "title":
                worksheet.column_dimensions[col_letter].width = 65 
            elif col_name in ["product_url", "property_url", "image_url"]:
                worksheet.column_dimensions[col_letter].width = 18 
            elif col_name in ["price", "discount", "original_price", "extra_discount"]:
                worksheet.column_dimensions[col_letter].width = 16
            elif col_name in ["rating", "reviews", "is_express", "sold_count", "bedrooms", "bathrooms"]:
                worksheet.column_dimensions[col_letter].width = 14
            elif col_name in ["shop_name", "location", "address", "agent_or_agency", "delivery", "condition"]:
                worksheet.column_dimensions[col_letter].width = 22
            else:
                worksheet.column_dimensions[col_letter].width = 18 

        worksheet.freeze_panes = "A2"

        full_range = f"A1:{get_column_letter(len(df.columns))}{len(df) + 1}"
        worksheet.auto_filter.ref = full_range

    print(f"✅ Data securely saved for User in: {user_folder}")
    
    return csv_filename, excel_filename, user_folder

if __name__ == "__main__":
    pass


