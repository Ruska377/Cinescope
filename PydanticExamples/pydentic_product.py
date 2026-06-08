from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool

product_1 = Product(name="CocaCola", price=123, in_stock=True)

json_data = product_1.model_dump_json()
print(json_data)

new_product = Product.model_validate_json(json_data)
print(new_product)
