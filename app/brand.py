import streamlit as st
from app.logo_image import get_car_brand_logo, get_image_as_base64
import os


def brands(manager):
    st.title("Marques automobiles")

    manufacturer = st.session_state.get("manufacturer", None)
    if manufacturer:
        st.write(f"### Marque sélectionnée : {manufacturer}")
        st.write("Retournez à la page d'accueil pour changer de marque.")
        brand = manager.get_brand_details(manufacturer)
        if brand:
            # Affichage des données brutes 
            st.markdown(f'## {brand[0]["cleanName"]["value"]}') 
            logo_path = get_car_brand_logo(st.session_state.manufacturer, save_path='car_logos/logo_brand.jpg')
            print(logo_path)

            if logo_path and os.path.exists(logo_path):
              base64_logo = get_image_as_base64(logo_path)
              st.markdown(f"""
              <div style="display: flex; align-items: center;">
                  <div style="margin-left: 5px;">
                      <img src="{base64_logo}" width="100">
                  </div>
              </div>
              <br>
              """, unsafe_allow_html=True)

            try:
                if (brand[0]['description']['value'] != ""):
                    st.write(f"**Description :** {brand[0]['description']['value']}")
                else :
                    st.write(f"**Description :** Non disponible")
            except:
                st.write(f"**Description :** Non disponible")

            try :
                if (brand[0]['cleanFoundingDate']['value'] != ""):
                    st.write(f"**Date de fondation :** {brand[0]['cleanFoundingDate']['value']}")
                else :
                    st.write(f"**Date de fondation :** Non disponible")
            except:
                st.write(f"**Date de fondation :** Non disponibl")
            
            try:
                list_founders = brand[0]['cleanFounder']['value']
                print(list_founders)
                if (list_founders != ""):
                    premier = True
                    for element in list_founders.split(", ") :
                        founder_name = manager.get_object_name(element)
                        if premier :
                            chaine = founder_name[0]['cleanName']['value']
                            premier = False
                        else :
                            chaine += ", " + founder_name[0]['cleanName']['value']
                    st.write(f"**Fondateur :** {chaine}")
                else :
                    st.write(f"**Fondateur :** Non disponible")
            except:
                st.write(f"**Fondateur :** Non disponible")
            
            try:
                if (brand[0]['website']['value'] != ""):
                    st.write(f"**Site web :** {brand[0]['website']['value']}")
                else :
                    st.write(f"**Site web :** Non disponible")
            except:
                st.write(f"**Site web :** Non disponible")

            try:
                if (brand[0]['cleanLocation']['value'] != ""):
                    st.write(f"**Localisation :** {brand[0]['cleanLocation']['value']}")
                else :
                    st.write(f"**Localisation :** Non disponible")
            except:
                st.write(f"**Localisation :** Non disponible")
            
            
            try:
                if (brand[0]['longDescription']['value'] != ""):
                    st.write(f"**Description longue :** {brand[0]['longDescription']['value']}")
                else :
                    st.write(f"**Description longue :** Non disponible")
            except:
                st.write(f"**Description longue :** Non disponible")
            
            try:
                products = brand[0]['cleanProduct']['value']
                if (products != ""):
                    list_products = products.split(", ")
                    premier = 1
                    for element in list_products :
                        element_name = manager.get_object_name(element)
                        if premier == 1 :
                            chaine = element_name
                            premier = 0
                        else :
                            chaine += ", " + element_name
                    st.write(f"**Type de Produit :** {chaine}")
                else :
                    st.write(f"**Type de Produit :** Non disponible")
            except:
                st.write(f"**Type de Produit :** Non disponible")
            
            try:
                if (brand[0]['parentCompany']['value'] != ""):
                    parent_uri = brand[0]['parentCompany']['value']
                    parent_uri = parent_uri.split('/')[-1]
                    parent_name = manager.get_object_name(parent_uri)
                    if parent_name:
                        st.write(f"**Compagnie Parente :**")
                        if st.button(f"{parent_name[0]['cleanName']['value']}"):
                            st.session_state.page = "Marques"
                            st.session_state.manufacturer = parent_uri
                            st.rerun()
                    else:    
                        st.write(f"**Compagnie Parente :** Non disponible")
                else :
                    st.write(f"**Compagnie Parente :** Non disponible")
            except:
                st.write(f"**Compagnie Parente :** Non disponible")

            try:
                child_companies = brand[0]['childCompanies']['value']
                if (child_companies != ""):
                    list_child_companies = child_companies.split(", ")
                    st.write(f"**Compagnies Filiales :**")
                    
                    # Create 3 columns
                    cols = st.columns(3)
                    
                    # Iterate through child companies with column cycling
                    for i, element in enumerate(list_child_companies):
                        # Determine which column to use based on the index
                        col = cols[i % 3]
                        
                        brand_names = manager.get_object_name(element)
                        good_name = False
                        for name in brand_names:
                            if name['cleanName']['value'] != '':
                                brand_name = name
                                good_name = True
                                break
                        
                        if not good_name:
                            brand_name = {'cleanName': {'value': element}}
                        
                        with col:
                            if st.button(f"{brand_name['cleanName']['value']}"):
                                # Mettez à jour l'état et redirigez via session_state
                                st.session_state.page = "Marques"
                                st.session_state.manufacturer = element
                                st.rerun()
                else:
                    st.write(f"**Compagnies Filiales :** Non disponible1")
            except:
                st.write(f"**Compagnies Filiales :** Non disponible2")

            st.write(f"**Models :**")
            # Lien vers la page des modèles
            if st.button("Voir les modèles"):
                # Mettez à jour l'état et redirigez via session_state
                st.session_state.page = "Modèles"
                st.session_state.manufacturer = manufacturer
                st.rerun()

            st.write("### Données brutes retournées :")
            st.json(brand)
        else:
            st.warning("Aucun résultat trouvé")
    else:
        st.warning("Aucune marque sélectionnée. Retournez à l'accueil pour rechercher une marque.")