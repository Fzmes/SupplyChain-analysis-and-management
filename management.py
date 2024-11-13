import streamlit as st
import pandas as pd
import mysql.connector
import connection as connection 
from supply_chain import SupplyChain,Product,Retailer,Order,Distributor
from time import sleep
import warnings
import streamlit as st
from streamlit_option_menu import option_menu
def manage(st):
    warnings.simplefilter(action='ignore', category=FutureWarning)

    if "button_clicked" not in st.session_state:
        st.session_state.button_clicked = False

    def callback():
        st.session_state.button_clicked = True

    supply_chain = SupplyChain()

    st.markdown(
        """
        <style>
            .main {
                text-align: center; 
            }
            div.block-containers{
                padding-top: 0.5rem;
            }
            .st-emotion-cache-z5fcl4{
                padding-top: 1rem;
                padding-bottom: 1rem;
                padding-left: 1.5rem;
                padding-right: 2.8rem;
                overflow-x: hidden;
            }
            .st-emotion-cache-16txtl3{
                padding: 2.7rem 0.6rem;
            }
            div.st-emotion-cache-1r6slb0{
                padding: 15px 5px;
                border-radius: 5px;
                border: 3px solid #5E0303;
                opacity: 0.9;
            }
            div.st-emotion-cache-1r6slb0:hover{
                transition: all 0.5s ease-in-out;
                background-color: #000;  
                border: 3px solid red;
                opacity: 1;
            }
            .plot-container.plotly{
                border: 4px solid #333;
                border-radius: 7px;
                
            }
            div.st-emotion-cache-1r6slb0 span.st-emotion-cache-10trblm{
                font: bold 24px tahoma;
            }
            div [data-testid=stImage]{
                text-align: center;
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 100%;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    sub_options_style = {
    "container": {
        "padding": "8!important", 
        "background-color": '#101010',
        "border": "2px solid darkorange"
    },
    "nav-link": {
        "color": "white", 
        "padding": "10px", 
        "font-size": "15px", 
        "text-align": "center", 
        "margin": "10px 0px"
    },
    "nav-link-selected": {
        "background-color": "#FFA500"
    },
}

    header = st.container()
    content = st.container()

    with st.sidebar:
        st.title("Supply Chain Management")
        page = option_menu(
            menu_title='Système de Gestion',
            options=['Commandes','Produits', 'Distributeurs','Détailant'],
            menu_icon='archive',
            default_index=0,
            styles={
            "container": {"padding": "10!important", "background-color": '#000'},
            "icon": {"color": "white", "font-size": "22px"},
            "nav-link": {"color": "white", "font-size": "18px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#FFA500"},
            }
        )
        st.write("***")

        if page == 'Détailant':
            with header:
                st.title('Gestion des Détailants 🏪')
                retailer_option = option_menu(menu_title=None, options=["Ajouter Détailant", "Mettre à Jour Détailant", "Vue d'Ensemble Détailants"],
                                            icons=[" "] * 3, menu_icon="people", default_index=0,
                                            orientation="horizontal", styles=sub_options_style)

            with content:
                if retailer_option == "Ajouter Détailant":
                    st.subheader("Ajouter un nouveau Détailant")
                    with st.form('add_retailer'):
                        [c1, c2] = st.columns(2)
                        with c1:
                            retailer_name = st.text_input("Nom du Détailant").strip()
                            retailer_password = st.text_input("Mot de Passe").strip()
                            phone = st.text_input("Téléphone").strip()

                        with c2:
                            address = st.text_input("Adresse").strip()
                            area_id = st.number_input("ID de la Zone", min_value=1, step=1)
                            email = st.text_input("Email").strip()

                        add_retailer = st.form_submit_button(label='Ajouter Détailant')
                        
                        if add_retailer:
                            if retailer_name and retailer_password and phone and address and area_id:
                                new_retailer = Retailer(username=retailer_name, password=retailer_password, address=address, area_id=area_id, phone=phone, email=email)
                                if supply_chain.add_retailer(new_retailer.username, new_retailer.password, new_retailer.address, new_retailer.area_id, new_retailer.phone, new_retailer.email):
                                    st.success(f"Détailant '{retailer_name}' ajouté avec succès.")
                                else:
                                    st.warning(f"Détailant '{retailer_name}' existe déjà.")
                            else:
                                st.warning("Veuillez remplir tous les champs requis.")
                elif retailer_option == "Mettre à Jour Détailant":
                    st.subheader("Mettre à jour les informations du Détailant")

                    retailers = supply_chain.get_retailers()
                    if isinstance(retailers, pd.DataFrame) and not retailers.empty:
                        retailer_dict = dict(zip(retailers['username'], retailers['retailer_id']))
                        
                        retailer_names = list(retailer_dict.keys())
                        selected_retailer_name = st.selectbox("Sélectionnez le Détailant à mettre à jour", retailer_names)
                        
                        selected_retailer_id = retailer_dict[selected_retailer_name]
                        
                        selected_retailer = retailers[retailers['retailer_id'] == selected_retailer_id]
                        if not selected_retailer.empty:
                            selected_retailer = selected_retailer.iloc[0]
                            with st.form(key='update_retailer'):
                                new_name = st.text_input("Nom du Détailant", value=selected_retailer['username'])
                                new_password = st.text_input("Mot de Passe", value=selected_retailer['password'])
                                new_address = st.text_input("Adresse", value=selected_retailer['address'])
                                new_area_id = st.number_input("ID de la Zone", min_value=1, step=1, value=selected_retailer['area_id'])
                                new_phone = st.text_input("Téléphone", value=selected_retailer['phone'])
                                new_email = st.text_input("Email", value=selected_retailer['email'])
                                
                                submit_update = st.form_submit_button(label='Mettre à Jour')
                                
                                if submit_update:
                                    update_success = supply_chain.update_retailer(
                                        selected_retailer_id, new_name, new_password, new_address, new_area_id, new_phone, new_email
                                    )
                                    
                                    if update_success:
                                        st.success(f"Détailant '{new_name}' mis à jour avec succès.")
                                    else:
                                        st.warning(f"Erreur lors de la mise à jour du Détailant '{new_name}'.")
                    else:
                        st.warning("Aucun détailant trouvé.")

                elif retailer_option == "Vue d'Ensemble Détailants":
                    st.text(f'Tous les Détailants dans votre chaine d\'approvisionnement"')
                    df_retailers = supply_chain.get_retailers()
                    st.table(df_retailers)

        if page == 'Produits':
            with header:
                st.title('Gestion des Produits 📦')
                product_option = option_menu(menu_title=None, options=["Ajouter Produit", "Mettre à Jour Produit", "Vue d'Ensemble Produits"],
                                            icons=[" "] * 3, menu_icon="archive", default_index=0,
                                            orientation="horizontal", styles=sub_options_style)

            with content:
                if product_option == "Ajouter Produit":
                    st.text('Ajouter un nouveau Produit'.title())
                    with st.form(key='add_product_form'):
                        product_name = st.text_input("Nom du produit")
                        product_description = st.text_area("Description du produit")
                        price_per_unit = st.number_input("Prix par unité", min_value=0.0, step=0.1)
                        unit = st.selectbox("Unité", ["Pieces", "Kilo Gram", "Litre"]) 
                        category = st.number_input("Catégorie", min_value=1, step=1)
                        stock_quantity = st.number_input("Quantité en stock", min_value=0, step=1)
                        submit_button = st.form_submit_button(label='Ajouter produit')

                    if submit_button:
                        if product_name and product_description:  
                            new_product = Product(product_name, product_description, price_per_unit, unit, category, stock_quantity)
                            
                            if supply_chain.add_product(new_product):
                                st.success(f"Produit '{product_name}' ajouté avec succès!")
                            else:
                                st.error("Une erreur est survenue lors de l'ajout du produit.")
                        else:
                            st.error("Veuillez remplir tous les champs obligatoires.")
                elif product_option == "Mettre à Jour Produit":
                    st.text('Mettre à jour les informations du Produit'.title())
                    products = supply_chain.get_products() 
                    if isinstance(products, pd.DataFrame) and not products.empty:
                        product_dict = dict(zip(products['pro_name'], products['pro_id']))
                        product_names = list(product_dict.keys())
                        selected_product_name = st.selectbox("Sélectionnez le Produit à mettre à jour", product_names)
                        selected_product_id = product_dict[selected_product_name]
                        selected_product = products[products['pro_id'] == selected_product_id]
                        if not selected_product.empty:
                            selected_product = selected_product.iloc[0]
                            with st.form(key='update_product'):
                                new_name = st.text_input("Nom du Produit", value=selected_product['pro_name'])
                                new_description = st.text_area("Description du Produit", value=selected_product['pro_desc'])
                                # Remove the " DH" and any spaces, then convert to float
                                pro_price_str = selected_product['pro_price'].replace(" DH", "").strip()
                                new_price = st.number_input("Prix par Unité", value=float(pro_price_str), min_value=0.0, format="%.2f")
                                new_unit = st.number_input("Unité", value=int(selected_product['unit']))
                                new_category = st.number_input("Catégorie", value=int(selected_product['pro_cat']))
                                new_stock_quantity = st.number_input("Quantité en Stock", value=float(selected_product['quantity']), min_value=0.0)

                                submit_update = st.form_submit_button(label='Mettre à Jour')

                                if submit_update:
                                    update_success = supply_chain.update_product(
                                        selected_product_id,
                                        new_name,
                                        new_description,
                                        new_price,
                                        new_unit,
                                        new_category,
                                        new_stock_quantity
                                    )
                                    
                                    if update_success:
                                        st.success(f"Produit '{new_name}' mis à jour avec succès.")
                                    else:
                                        st.warning(f"Erreur lors de la mise à jour du Produit '{new_name}'.")
                    else:
                        st.warning("Aucun produit trouvé.")

                elif product_option == "Vue d'Ensemble Produits":
                    st.text(f'Tous les Produits dans votre chaine d\'approvisionnement')
                    df_products = supply_chain.get_products()
                    st.table(df_products)

        if page == 'Commandes':
            with header:
                st.title('Gestion des Commandes 📜')
                order_option = option_menu(menu_title=None, options=["Ajouter Commande", "Mettre à Jour Commande", "Vue d'Ensemble Commandes"],
                                            icons=[" "] * 3, menu_icon="clipboard", default_index=0,
                                            orientation="horizontal", styles=sub_options_style)

            with content:
                if order_option == "Ajouter Commande":
                    st.text('Ajouter une nouvelle Commande'.title())
                    with st.form('add_order'):
                        [c1, c2] = st.columns(2)
                        with c1:
                            retailer_code = st.text_input("Code du Détailant").strip()
                            order_date = st.date_input("Date de Commande")
                            total_amount = st.number_input("Montant Total", min_value=0.0, step=0.01)

                        with c2:
                            approved = st.selectbox("Approuvé", [True, False])
                            status = st.selectbox("Statut", [1, 2, 3], format_func=lambda x: ["Pending", "Shipped", "Delivered"][x - 1])
                        add_order = st.form_submit_button(label='Ajouter Commande')
                        
                        if add_order:
                            if retailer_code:
                                try:
                                    success = supply_chain.add_order(retailer_code, order_date, approved, status, float(total_amount))
                                    
                                    if success:
                                        st.success("Commande ajoutée avec succès.")
                                    else:
                                        st.warning("La commande existe déjà.")
                                except Exception as e:
                                    st.error(f"Erreur lors de l'ajout de la commande: {e}")
                            else:
                                st.warning("Veuillez remplir tous les champs requis.")

                elif order_option == "Mettre à Jour Commande":
                    st.text('Mettre à jour les informations de la Commande'.title())
                    orders = supply_chain.get_orders()
                    order_ids = orders['order_id'].tolist()
                    selected_order_id = st.selectbox("Sélectionnez la Commande à mettre à jour", order_ids)
                    
                    if isinstance(orders, pd.DataFrame):
                        selected_order = orders[orders['order_id'] == selected_order_id]
                        if not selected_order.empty:
                            selected_order = selected_order.iloc[0]
                        else:
                            selected_order = None 
                    
                    if selected_order is not None and not selected_order.empty:
                        with st.form(key='update_order'):
                            new_retailer_code = st.text_input("Code du Détailant", value=selected_order['retailer_id'])
                            new_order_quantity = st.number_input("Prix total", value=float(selected_order['total_amount']), min_value=0.0)
                            new_order_date = st.date_input("Date de Commande", value=selected_order['date'])

                            submit_update = st.form_submit_button(label='Mettre à Jour')

                            if submit_update:
                                order_id = int(selected_order['order_id'])
                                retailer_code = str(new_retailer_code)
                                order_quantity = float(new_order_quantity)
                                order_date = new_order_date.strftime('%Y-%m-%d')
                                if supply_chain.update_order(order_id, retailer_code, order_quantity, order_date):
                                    st.success(f"Commande '{selected_order_id}' mise à jour avec succès.")
                                else:
                                    st.warning(f"Erreur lors de la mise à jour de la Commande '{selected_order_id}'.")

                elif order_option == "Vue d'Ensemble Commandes":
                    st.text(f'Toutes les Commandes dans votre chaine d\'approvisionnement')
                    df_orders = supply_chain.get_orders()
                    st.table(df_orders)

        if page == 'Distributeurs':
            with header:
                st.title('Gestion des Distributeurs 🚚')
                distributor_option = option_menu(menu_title=None, options=["Ajouter Distributeur", "Mettre à Jour Distributeur", "Vue d'Ensemble Distributeurs"],
                                                icons=[" "] * 3, menu_icon="truck", default_index=0,
                                                orientation="horizontal", styles=sub_options_style)

            with content:
                if distributor_option == "Ajouter Distributeur":
                    st.text('Ajouter un nouveau Distributeur'.title())
                    with st.form('add_distributor'):
                        [c1, c2] = st.columns(2)
                        with c1:
                            distributor_name = st.text_input("Nom du Distributeur").strip()
                            distributor_email = st.text_input("Email du Distributeur").strip()
                            distributor_phone = st.text_input("Téléphone du Distributeur").strip()

                        with c2:
                            address = st.text_input("Adresse").strip()
                        add_distributor = st.form_submit_button(label='Ajouter Distributeur')
                        
                        if add_distributor:
                            if distributor_name:
                                if supply_chain.add_distributor(distributor_name, distributor_email, distributor_phone,address):
                                    st.success(f"Distributeur '{distributor_name}' ajouté avec succès.")
                                else:
                                    st.warning(f"Distributeur '{distributor_name}' existe déjà.")
                            else:
                                st.warning("Veuillez remplir tous les champs requis.")

                elif distributor_option == "Mettre à Jour Distributeur":
                    st.text('Mettre à jour les informations du Distributeur'.title())
                    
                    distributors = supply_chain.get_distributors()
                    if isinstance(distributors, pd.DataFrame) and not distributors.empty:
                        distributor_dict = dict(zip(distributors['dist_name'], distributors['dist_id']))
                        
                        distributor_names = list(distributor_dict.keys())
                        selected_distributor_name = st.selectbox("Sélectionnez le Distributeur à mettre à jour", distributor_names)
                        
                        selected_distributor_id = distributor_dict[selected_distributor_name]
                        
                        selected_distributor = distributors[distributors['dist_id'] == selected_distributor_id]
                        if not selected_distributor.empty:
                            selected_distributor = selected_distributor.iloc[0]
                            with st.form(key='update_distributor'):
                                new_name = st.text_input("Nom du Distributeur", value=selected_distributor['dist_name'])
                                new_email = st.text_input("Email du Distributeur", value=selected_distributor['dist_email'])
                                new_phone = st.text_input("Téléphone", value=selected_distributor['dist_phone'])
                                new_address = st.text_input("Adresse", value=selected_distributor['dist_address'])

                                submit_update = st.form_submit_button(label='Mettre à Jour')
                                
                                if submit_update:
                                    update_success = supply_chain.update_distributor(
                                        selected_distributor_id, new_name, new_email, new_phone, new_address
                                    )
                                    if update_success:
                                        st.success(f"Distributeur '{new_name}' mis à jour avec succès.")
                                    else:
                                        st.warning(f"Erreur lors de la mise à jour du Distributeur '{new_name}'.")
                    else:
                        st.warning("Aucun distributeur trouvé.")

                elif distributor_option == "Vue d'Ensemble Distributeurs":
                    st.text(f'Tous les Distributeurs dans votre chaine d\'approvisionnement')
                    df_distributors = supply_chain.get_distributors()
                    st.table(df_distributors)
