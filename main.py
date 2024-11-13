import streamlit as st
import connection as conn
from dashboard import show_main_page
from  management import manage
import supply_chain as supply_chain
import plotly.io as pio
from streamlit.components.v1 import html

html("""
<script>
    document.addEventListener('fullscreenchange', (event) => {
        if (document.fullscreenElement) {
            document.fullscreenElement.style.backgroundColor = "black";
        } else {
            document.body.style.backgroundColor = "";
        }
    });
</script>
""", height=0)
headerSection = st.container()
loginSection = st.container()
logOutSection = st.container()
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
         
         div.st-emotion-cache-1r6slb0:hover{
            transition: all 0.5s ease-in-out;
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


def manage_table(table_name, fields, title, id_field):
    st.subheader(title)
    records = conn.fetch_data(f"SELECT * FROM {table_name}")

    for record in records:
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.write(
            f"ID: {record.get(id_field)}, {fields[0].capitalize()}: {record.get(fields[0], 'N/A')}, "
            f"{fields[1].capitalize()}: {record.get(fields[1], 'N/A')}"
        )
        col2.button("Edit", key=f"edit_{record.get(id_field)}", on_click=edit_record, args=(table_name, record, id_field))
        col3.button("Delete", key=f"delete_{record.get(id_field)}", on_click=delete_record, args=(table_name, record.get(id_field), id_field))

def edit_record(table_name, record, id_field):
    st.session_state.edit_mode = True
    st.session_state.selected_record = record

    with st.form(key=f'edit_{table_name}'):
        inputs = {}
        for field, value in record.items():
            label = field.capitalize()
            if isinstance(value, str):
                inputs[field] = st.text_input(label, value=value, key=f"edit_{field}")
            elif isinstance(value, (int, float)):
                inputs[field] = st.number_input(label, value=value, key=f"edit_{field}")
                
        submitted = st.form_submit_button("Update")
        
        if submitted:
            update_query = f"UPDATE {table_name} SET " + ', '.join([f"{field} = %s" for field in inputs.keys()]) + f" WHERE {id_field} = %s"
            values = tuple(inputs.values()) + (record[id_field],)
            conn.insert_data(update_query, values)
            st.success(f"{table_name.capitalize()} updated successfully!")
            st.experimental_rerun()

def delete_record(table_name, record_id, id_field):
    delete_query = f"DELETE FROM {table_name} WHERE {id_field} = %s"
    conn.insert_data(delete_query, (record_id,))
    st.success(f"{table_name.capitalize()} deleted successfully!")
    st.experimental_rerun()

def edit_distributor(dist):
    st.session_state.edit_mode = True
    st.session_state.selected_distributor = dist

    with st.form(key='edit_distributor'):
        name = st.text_input("Name", value=dist['name'], key="edit_name")
        address = st.text_input("Address", value=dist['address'], key="edit_address")
        submitted = st.form_submit_button("Update Distributor")
        
        if submitted:
            update_query = "UPDATE distributor SET name = %s, address = %s WHERE id = %s"
            values = (name, address, dist['id'])
            conn.insert_data(update_query, values)
            st.success("Distributor updated successfully!")
            st.experimental_rerun()

def delete_distributor(dist_id):
    delete_query = "DELETE FROM distributor WHERE id = %s"
    conn.insert_data(delete_query, (dist_id,))
    st.success("Distributor deleted successfully!")
    st.experimental_rerun()

def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
    st.session_state['username'] = ''
    st.experimental_set_query_params(dummy='refresh')

def LoggedIn_Clicked(username, password):
    if conn.login(username, password):
        st.session_state['loggedIn'] = True
        st.session_state['username'] = username
        st.experimental_set_query_params(dummy='refresh')
    else:
        st.session_state['loggedIn'] = False
        st.error("Invalid username or password")

def show_logout_page():
    logOutSection.empty()
    with logOutSection:
        st.button("Log Out", key="logout", on_click=LoggedOut_Clicked)

def show_login_page():
    with loginSection:
        st.subheader("Authentification")
        username = st.text_input("Nom d'utilisateur", placeholder="Entrez votre nom d'utilisateur")
        password = st.text_input("Mot de passe", placeholder="Entrez votre mot de passe", type="password")
        st.button("Connexion", on_click=LoggedIn_Clicked, args=(username, password))

with headerSection:
    st.title("Segmentation de la Chaîne d'Approvisionnement")
    menu = ["Acceuil", "Système de Gestion", "Paramètres"]
    
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False

    choice = st.sidebar.selectbox("Sélectionner une Action", menu)

    if not st.session_state['loggedIn']:
        show_login_page()
    else:
        if choice == 'Acceuil':
            st.subheader("Bienvenue dans l'application d'analyse et de  gestion de la chaîne d'approvisionnement")
            show_main_page(st)
        elif choice == "Système de Gestion":
            manage(st)
        elif choice == "Paramètres":
            st.subheader("Paramètres")
            
            st.write("Ajustez les paramètres ci-dessous pour personnaliser votre expérience.")

            feature_enabled = st.checkbox("Activer la fonction avancée", value=False)
            if feature_enabled:
                st.success("La fonction avancée est activée!")
            else:
                st.warning("La fonction avancée est désactivée.")

            threshold = st.slider("Définir le seuil de notification", min_value=0, max_value=100, value=50)
            st.write(f"Le seuil de notification est réglé à: {threshold}")

            user_preference = st.text_input("Entrez votre préférence de nom d'utilisateur", "Nom d'utilisateur")
            st.write(f"Votre nom d'utilisateur préféré est: {user_preference}")

            st.write("Enregistrez vos paramètres pour les appliquer.")

        show_logout_page()
            
            