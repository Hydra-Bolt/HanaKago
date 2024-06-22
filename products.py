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


    @property
    def products(self):
        return self.__current_products