import streamlit as st
import mysql.connector
import datetime
from connection import create_connection
import pandas as pd
class Retailer:
    def __init__(self, username, password, address, area_id, phone, email=None, retailer_id=None):
        self.retailer_id = retailer_id
        self.username = username
        self.password = password
        self.address = address
        self.area_id = area_id
        self.phone = phone
        self.email = email
 
class Order:
    def __init__(self, retailer_code, order_date, approved, status, total_amount):
        self.retailer_code = retailer_code
        self.order_date = order_date
        self.approved = approved
        self.status = status
        self.total_amount = total_amount

class Product:
    def __init__(self, name, description, price, unit, category, quantity=None):
        self.name = name
        self.description = description
        self.price = price
        self.unit = unit
        self.category = category
        self.quantity = quantity if quantity is not None else 0

    def update(self, new_name, new_price):
        connection = create_connection()
        cursor = connection.cursor()
        update_query = f"""
        UPDATE products SET pro_name = '{new_name}', pro_price = {new_price} 
        WHERE pro_id = {self.product_id}
        """
        cursor.execute(update_query)
        connection.commit()
        cursor.close()
        connection.close()

class SupplyChain:
    def __init__(self):
        pass  
    def add_product(self, product):
        name = product.name
        description = product.description
        price = product.price
        unit = self.get_unit_id(product.unit)
        category = product.category
        quantity = product.quantity

        connection = create_connection()
        if connection is None:
            return False

        cursor = connection.cursor()
        print(f"Inserting product: {name}, {description}, {price}, {unit}, {category}, {quantity}")

        add_query = """
        INSERT INTO products (pro_name, pro_desc, pro_price, unit, pro_cat, quantity)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(add_query, (name, description, price, unit, category, quantity))
            connection.commit()
            print("Product added successfully!")
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return False
        finally:
            cursor.close()
            connection.close()

        return True
    def get_unit_id(self, unit_name):
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM unit WHERE unit_details = %s", (unit_name,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result:
            return result[0]
        else:
            print(f"Error: The unit '{unit_name}' does not exist in the 'unit' table.")
            return None
    def update_product(self, product_id, name, description, price, unit, category, quantity):
        unit = int(unit)
        category = int(category)
        quantity = int(quantity)
        price = float(price)
        product_id=int(product_id)
        connection = create_connection()
        if connection is None:
            return False

        cursor = connection.cursor()
        update_query = """
        UPDATE products 
        SET pro_name = %s, pro_desc = %s, pro_price = %s, quantity = %s
        WHERE pro_id = %s
        """
        try:
            cursor.execute(update_query, (name, description, price, quantity, product_id))
            connection.commit()
            print(f"Product with ID {product_id} updated successfully!")
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return False
        finally:
            cursor.close()
            connection.close()

        return True 
    def update_order(self, order_id, retailer_code, order_quantity, order_date):
        order_id = int(order_id)
        retailer_code = int(retailer_code)
        order_quantity = float(order_quantity)
        order_date = order_date
        update_query = """
        UPDATE orders
        SET retailer_id = %s, total_amount = %s, date = %s
        WHERE order_id = %s
        """
        connection = create_connection() 
        cursor = connection.cursor()
        try:
            cursor.execute(update_query, (retailer_code, order_quantity, order_date, order_id))
            connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()
            connection.close()
    def add_order(self, retailer_id, order_date, approved, status, total_amount):
        retailer_id = int(retailer_id)
        order_date = order_date.strftime('%Y-%m-%d') if isinstance(order_date, datetime.date) else order_date
        approved = int(approved)
        status = int(status) 
        total_amount = float(total_amount)

        insert_query = """
        INSERT INTO orders (date, retailer_id, approved, status, total_amount)
        VALUES (%s, %s, %s, %s, %s)
        """
        connection = create_connection() 
        cursor = connection.cursor()

        try:
            cursor.execute(insert_query, (order_date, retailer_id, approved, status, total_amount))
            connection.commit()
            return True  
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False 
        finally:
            cursor.close()
            connection.close()

    def add_retailer(self, username, password, address, area_id, phone, email=None):
        area_id = int(area_id)
        connection = create_connection()
        if connection is None:
            return False
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO retailer (username, password, address, area_id, phone, email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(insert_query, (username, password, address, area_id, phone, email))
            connection.commit()
            print(f"Retailer '{username}' added successfully!")
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return False
        finally:
            cursor.close()
            connection.close()

        return True

    def update_retailer(self, retailer_id, username, password, address, area_id, phone, email):
        retailer_id = int(retailer_id)
        area_id = int(area_id)
        connection = create_connection()
        if connection is None:
            return False
        cursor = connection.cursor()
        update_query = """
        UPDATE retailer
        SET username = %s, password = %s, address = %s, area_id = %s, phone = %s, email = %s
        WHERE retailer_id = %s
        """
        try:
            cursor.execute(update_query, (username, password, address, area_id, phone, email, retailer_id))
            connection.commit()
            print(f"Retailer with ID {retailer_id} updated successfully!")
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return False
        finally:
            cursor.close()
            connection.close()

        return True

    def add_distributor(self, name, email, phone, address):
        connection = create_connection()
        if connection is None:
            return False

        cursor = connection.cursor()
        insert_query = """
        INSERT INTO distributor (dist_name, dist_email, dist_phone, dist_address)
        VALUES (%s, %s, %s, %s)
        """
        try:
            cursor.execute(insert_query, (name, email, phone, address))
            connection.commit()
            print(f"Distributor '{name}' added successfully!")
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return False
        finally:
            cursor.close()
            connection.close()

        return True

    def update_distributor(self, dist_id, name, email, phone, address):
        dist_id = int(dist_id)
        connection = create_connection()
        if connection is None:
            return False

        cursor = connection.cursor()

        update_query = """
        UPDATE distributor 
        SET dist_name = %s, dist_email = %s, dist_phone = %s, dist_address = %s
        WHERE dist_id = %s
        """
        try:
            cursor.execute(update_query, (name, email, phone, address, dist_id))
            connection.commit()
            print(f"Distributor with ID {dist_id} updated successfully!")
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return False
        finally:
            cursor.close()
            connection.close()

        return True

    def load_products(self):
        connection = create_connection()
        query = "SELECT * FROM products"
        self.products = pd.read_sql(query, connection)
        connection.close()

    def delete_product(self, product_id):
        connection = create_connection()
        cursor = connection.cursor()
        delete_query = f"DELETE FROM products WHERE pro_id = {product_id}"
        cursor.execute(delete_query)
        connection.commit()
        cursor.close()
        connection.close()
    def get_orders(self):
        connection = create_connection()
        query = "SELECT * FROM orders" 
        self.orders = pd.read_sql(query, connection)
        connection.close()
        return self.orders
    def get_products(self):
        connection = create_connection()
        query = "SELECT * FROM products" 
        self.products = pd.read_sql(query, connection)
        connection.close()
        self.products['pro_price'] = self.products['pro_price'].apply(lambda x: f"{x:.2f} DH")
        return self.products
    def delete_product(self, product_id):
        connection = create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM products WHERE pro_id = %s", (product_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Erreur lors de la suppression du produit:", e)
            return False
        finally:
            cursor.close()
            connection.close()

    def get_retailers(self):
        connection = create_connection()
        query = "SELECT * FROM retailer" 
        self.retailers = pd.read_sql(query, connection)
        connection.close()
        return self.retailers
    def get_distributors(self):
        connection = create_connection()
        query = "SELECT * FROM distributor"
        self.distributors = pd.read_sql(query, connection)
        connection.close()
        return self.distributors
class BaseManager:
    def __init__(self, table_name, fields, title, id_field):
        self.table_name = table_name
        self.fields = fields
        self.title = title
        self.id_field = id_field

    def display(self):
        st.subheader(self.title)
        records = create_connection().fetch_data(f"SELECT * FROM {self.table_name}")

        for record in records:
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"ID: {record.get(self.id_field)}, {self.fields[0].capitalize()}: {record.get(self.fields[0], 'N/A')}, {self.fields[1].capitalize()}: {record.get(self.fields[1], 'N/A')}")
            col2.button("Edit", key=f"edit_{record.get(self.id_field)}", on_click=self.edit_record, args=(record,))
            col3.button("Delete", key=f"delete_{record.get(self.id_field)}", on_click=self.delete_record, args=(record.get(self.id_field),))

    def edit_record(self, record):
        st.session_state.edit_mode = True
        st.session_state.selected_record = record

        with st.form(key=f'edit_{self.table_name}'):
            inputs = {}
            for field in self.fields:
                label = field.capitalize()
                if isinstance(record[field], str):
                    inputs[field] = st.text_input(label, value=record[field], key=f"edit_{field}")
                elif isinstance(record[field], (int, float)):
                    inputs[field] = st.number_input(label, value=record[field], key=f"edit_{field}")

            submitted = st.form_submit_button("Update")
            if submitted:
                self.update_record(inputs, record[self.id_field])
                st.success(f"{self.title} updated successfully!")
                st.experimental_rerun()

    def update_record(self, inputs, record_id):
        update_query = f"UPDATE {self.table_name} SET " + ', '.join([f"{field} = %s" for field in inputs.keys()]) + f" WHERE {self.id_field} = %s"
        values = tuple(inputs.values()) + (record_id,)
        create_connection().insert_data(update_query, values)

    def delete_record(self, record_id):
        delete_query = f"DELETE FROM {self.table_name} WHERE {self.id_field} = %s"
        create_connection().insert_data(delete_query, (record_id,))
        st.success(f"{self.title} deleted successfully!")
        st.experimental_rerun()

class Distributor:
    def __init__(self, name, code, contact_info, address, city):
        self.name = name
        self.code = code
        self.contact_info = contact_info
        self.address = address
        self.city = city

class DistributorManager(BaseManager):
    def __init__(self):
        super().__init__("distributor", ["name", "address"], "Distributors List", "dist_id")

class RetailerManager(BaseManager):
    def __init__(self):
        super().__init__("retailer", ["name", "location"], "Retailers List", "retailer_id")

class ProductManager(BaseManager):
    def __init__(self):
        super().__init__("products", ["name", "price"], "Products List", "product_id")

class OrderManager(BaseManager):
    def __init__(self):
        super().__init__("orders", ["order_number", "total_amount"], "Orders List", "order_id")

class InvoiceManager(BaseManager):
    def __init__(self):
        super().__init__("invoice", ["invoice_number", "amount_due"], "Invoices List", "invoice_id")

def manage():
    st.title("Système de Gestion de la Chaîne d'Approvisionnement")
    st.markdown("<style>h1 { color: blue; }</style>", unsafe_allow_html=True)

    management_menu = ["Manage Distributors", "Manage Retailers", "Manage Products", "Manage Orders", "Manage Invoices"]
    manage_choice = st.selectbox("Select Table to Manage", management_menu)

    if manage_choice == "Manage Distributors":
        manager = DistributorManager()
    elif manage_choice == "Manage Retailers":
        manager = RetailerManager()
    elif manage_choice == "Manage Products":
        manager = ProductManager()
    elif manage_choice == "Manage Orders":
        manager = OrderManager()
    elif manage_choice == "Manage Invoices":
        manager = InvoiceManager()

    manager.display()
