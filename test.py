import streamlit as st

# Initialiser l'état de la session pour la navigation
if 'page' not in st.session_state:
    st.session_state.page = "Page 1"

# Fonction pour changer de page
def change_page(page):
    st.session_state.page = page

# Boutons de navigation
st.sidebar.button("Page 1", on_click=change_page, args=["Page 1"])
st.sidebar.button("Page 2", on_click=change_page, args=["Page 2"])
st.sidebar.button("Page 3", on_click=change_page, args=["Page 3"])

# Afficher le contenu de la page sélectionnée
if st.session_state.page == "Page 1":
    st.header("Page 1")
    st.write("Contenu de la page 1")
elif st.session_state.page == "Page 2":
    st.header("Page 2")
    st.write("Contenu de la page 2")
elif st.session_state.page == "Page 3":
    st.header("Page 3")
    st.write("Contenu de la page 3")
