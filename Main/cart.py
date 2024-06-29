import datetime
from Main.products import Products
from hakoniwa import Hakoniwa


class Cart:
    def __init__(self):
        self.products = {}
        self.carts = Hakoniwa("./TABLES/carts.json")
        self.product_list = Products().products

    def add(self, item, num):
        if item in self.products:
            self.products[item] += num
        else:
            self.products[item] = num

    def remove(self, item, num):
        print(item, num)
        print(self.products)
        if item in self.products:
            self.products[item] -= num
            if self.products[item] <= 0:
                del self.products[item]
    
    def get_cart(self):
        for product_no, quantity in self.products.items():
            print(f"{self.product_list[product_no]['product_id']}. {self.product_list[product_no]['name']} x {quantity}")

    def get_total(self):
        total = 0
        for product_no, quantity in self.products.items():
            total += self.product_list[product_no]['price'] * quantity
        return total
    
    def checkout(self, user_id):
        products = [{"pid":int(pid), "quantity":int(quantity)} for pid, quantity in self.products.items()]
        print(products)
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self.carts.insert({"uid": user_id, "products": products, "total": self.get_total(), "created_at": created_at}, "cart_id")
        self.carts._update_db()

    def get_user_cart(self, uid):
        carts_found = self.carts.find({"uid": uid})
        if carts_found:
            return carts_found
        raise Exception("No carts found.")