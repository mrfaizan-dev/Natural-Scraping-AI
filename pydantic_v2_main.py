from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field , BaseModel ,ConfigDict
from typing import List , Optional , Any
import time , datetime


class Settings(BaseSettings):
    # Field ka use karke default bata dein (jo blank hoga)
    proxy_server: str = Field(default="") 
    proxy_username: str = Field(default="")
    proxy_password: str = Field(default="")

    db_url: str = Field(default="")
    redis_url: str = Field(default="redis://localhost:6379/0")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()


class Product(BaseModel):
    # ConfigDict(extra='allow') ensures extra scraped fields aren't dropped
    model_config = ConfigDict(extra='allow')

    title: Optional[Any] = None
    price: Optional[Any] = None
    original_price: Optional[Any] = None
    discount: Optional[Any] = None
    extra_discount: Optional[Any] = None
    rating: Optional[Any] = None
    reviews: Optional[Any] = None
    seller: Optional[Any] = None
    shop_name: Optional[Any] = None
    delivery: Optional[Any] = None
    condition: Optional[Any] = None
    sold_count: Optional[Any] = None
    past_month_sales: Optional[Any] = None
    location: Optional[Any] = None
    urgency: Optional[Any] = None
    promotion: Optional[Any] = None
    subtitle: Optional[Any] = None
    description: Optional[Any] = None
    is_express: Optional[Any] = None
    image_url: Optional[Any] = None
    product_url: Optional[Any] = None
    source: Optional[Any] = None


class RealEstate(BaseModel):
    # ConfigDict(extra='allow') ensures extra scraped fields aren't dropped
    model_config = ConfigDict(extra='allow')

    title: Optional[Any] = None
    price: Optional[Any] = None
    property_type: Optional[Any] = None
    bedrooms: Optional[Any] = None
    bathrooms: Optional[Any] = None
    area_size: Optional[Any] = None
    location: Optional[Any] = None
    address: Optional[Any] = None
    agent_or_agency: Optional[Any] = None
    phone: Optional[Any] = None
    description: Optional[Any] = None
    image_url: Optional[Any] = None
    property_url: Optional[Any] = None
    source: Optional[Any] = None