from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone
import json

load_dotenv()

app = FirecrawlApp()

class Product(BaseModel):
	"""Schema for creating a new product"""

	url: str = Field(description="The URL of the product")
	name: str = Field(description="The product name/title")
	price: float = Field(description="The current price of the product")
	currency: str = Field(description="Currency code (USD, EUR, etc)")
	main_image_url: str = Field(description="The URL of the main image of the product")


def scrape_product(url: str):
	extracted_data = app.scrape_url(
		url,
		formats=['extract'],
		extract={
			'prompt': "Extract the product's name, price, currency, and image",
			'schema': Product.model_json_schema(),
		}
	)

	now = datetime.now(timezone('America/Chicago'))
	timestamp_str = now.strftime('%Y-%m-%d %H-%M')

	if hasattr(extracted_data, 'extract') and isinstance(extracted_data.extract, dict):
		# Access the dictionary within the response object
		product_dict = extracted_data.extract

		# Add the timestamp to this dictionary. Using 'scrape_timestamp'
		# as the key name since 'time' is not in your schema above.
		product_dict['time'] = timestamp_str

		# Return the dictionary containing the product data + timestamp
		return product_dict
	else:
		# Handle cases where the expected data structure wasn't returned
		print("Warning: Could not find '.extract' dictionary in the response object.")
		print(f"Received object type: {type(extracted_data)}")
		# Return None to indicate failure to get the data in the expected format
		return None

	# Add the scraping date to the extracted data
#	extracted_data["timestamp"] = timestamp

	return extracted_data

if __name__ == "__main__":
	product = "https://www.amazon.com/gp/product/B002U21ZZK"

	result = scrape_product(product)
	pretty_json_string = json.dumps(result, indent=4, sort_keys=True)
	print(pretty_json_string)


