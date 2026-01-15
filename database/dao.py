from database.DB_connect import DBConnect
from model.product import Product
from model.sale import Sale


class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def read_categories():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """
                select *
                from category c 
        """
        cursor.execute(query)

        for row in cursor:
            result[row["id"]] = row["category_name"]

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_products(c):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select *
                from product p 
                where p.category_id = %s 
        """
        cursor.execute(query, (c,))

        for row in cursor:
            product = Product(**row)
            result.append(product)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_sales(list_products, dict_products, start, end):
        conn = DBConnect.get_connection()

        result = []
        tuple_product = tuple(p.id for p in list_products)

        cursor = conn.cursor(dictionary=True)
        query = f"""
                select oi.product_id, count(*) as n_ordini
                from `order` o , order_item oi 
                where o.id = oi.order_id
                and oi.product_id in {tuple_product}
                and o.order_date between %s and %s
                group by oi.product_id  
            """
        cursor.execute(query, (start, end))

        for row in cursor:
            product = dict_products[row["product_id"]]
            sale = Sale(product, row["n_ordini"])
            result.append(sale)

        cursor.close()
        conn.close()
        return result