from dataclasses import dataclass
from model.product import Product

@dataclass
class Sale:
    product: Product
    n_ordini : int