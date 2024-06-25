from hakoniwa import Hakoniwa


class Products:
    def __init__(self):
        self.__current_products = self.__getProducts()

    def add(self, item):
        self.__current_products.insert(item)
        self.updateProducts()

    def remove(self, item):
        self.__current_products.delete(item)
        self.updateProducts()
    
    def updateProducts(self):
        self.__current_products._update_db()
        self.__current_products = self.__getProducts()

    def __getProducts(self):
        return Hakoniwa("./TABLES/products.json")
    
    def pretty_print(self, products_per_row=3):
        # Define the maximum lengths for each field
        products = self.products
        max_name_length = max(len(product['name']) for product in products)
        max_price_length = max(len(f"Rs{product['price']}") for product in products)
        max_id_length = max(len(str(product['product_id'])) for product in products)
        
        # Calculate the width for each product box
        box_width = max_name_length + max_price_length + max_id_length + 14  # 14 for padding and labels
        
        # Split the products into rows of fixed length
        rows = [products[i:i + products_per_row] for i in range(0, len(products), products_per_row)]
        
        for row in rows:
            # Print the top border for each row
            print("+" + ("-" * box_width + "+") * len(row))
            
            # Print the name line for each product in the row
            for product in row:
                name_line = f" ID: {product['product_id']:<{max_id_length}} Name: {product['name']} "
                print(f"|{name_line.ljust(box_width)}|", end='')
            print()  # Newline after the row
            
            # Print the price line for each product in the row
            for product in row:
                price_line = f" Price: Rs{product['price']:<{max_price_length}} "
                print(f"|{price_line.ljust(box_width)}|", end='')
            print()  # Newline after the row
            
            # Print the bottom border for each row
            print("+" + ("-" * box_width + "+") * len(row))

    @property
    def products(self):
        return self.__current_products.data_records