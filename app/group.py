import streamlit as st
import pandas as pd
import plotly.express as px
import os
from logo_image import get_car_brand_logo
# Helper function to format currency
def format_currency(value, currency):
    try:
        value = float(value)
        return f"{value:,.2f} {currency}"
    except (ValueError, TypeError):
        return "N/A"

# Group Information pageimport os
import streamlit as st
import pandas as pd
from PIL import Image

def group_information(manager):
    st.title("🚗 Informations sur les Groupes")

    st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Retrieve the manufacturer from session state
    group = st.session_state.get("manufacturer", "")

    if not group:
        st.warning("⚠️ Aucun groupe sélectionné.")
        return

    # Display the group's logo
    st.markdown("### 🏁 Logo du Groupe")

    # Call the function to fetch the logo
    logo_path = get_car_brand_logo(group, save_path=f"car_logos/{group}_logo.jpg")

    if os.path.exists(logo_path):
        # Display the logo if it was successfully retrieved
        image = Image.open(logo_path)
        st.image(image, caption=f"Logo de {group}", width=300)
    else:
        st.warning(f"⚠️ Logo introuvable pour le groupe : {group}")

    # Fetch other group-related information
    search_button = st.button("Obtenir les informations")

    if search_button or st.session_state.get("search_performed", False):
        if not group.strip():
            st.warning("⚠️ Veuillez entrer un nom de groupe valide.")
        else:
            try:
                with st.spinner('🔄 Récupération des informations...'):
                    # Fetch group-related data
                    parent_group_car = manager.get_parent_group_of_car(group)
                    parent_group_manufacturer = manager.get_parent_group_of_manufacturer(group)
                    country_info = manager.get_country_of_group(group)
                    founding_date = manager.get_founding_date_of_group(group)
                    founder_info = manager.get_founder_of_group(group)
                    brands_info = manager.get_list_of_brands_of_group(group)
                    revenue_info = manager.get_revenue_of_group(group)
                    investors_info = manager.get_investors_of_group(group)

                # Use tabs to organize information
                tabs = st.tabs([
                    "📦 Groupe Parent",
                    "🌍 Pays",
                    "📅 Date de Fondation",
                    "👤 Fondateur",
                    "🏷️ Marques",
                    "💼 Investisseurs"
                ])

                # Groupe Parent Tab
                with tabs[0]:
                    st.markdown("### 📦 Groupe Parent (Constructeur)")
                    if parent_group_manufacturer:
                        df_manufacturer = pd.DataFrame(parent_group_manufacturer)
                        st.dataframe(df_manufacturer, use_container_width=True)
                    else:
                        st.info("Aucune information sur le groupe parent (Constructeur).")

                # Pays Tab
                with tabs[1]:
                    st.markdown("### 🌍 Pays du Groupe")
                    if country_info:
                        df_country = pd.DataFrame(country_info)
                        st.dataframe(df_country, use_container_width=True)
                    else:
                        st.info("Aucune information sur le pays.")

                # Date de Fondation Tab
                with tabs[2]:
                    st.markdown("### 📅 Date de Fondation")
                    if founding_date:
                        df_founding = pd.DataFrame(founding_date)
                        st.dataframe(df_founding, use_container_width=True)
                    else:
                        st.info("Aucune information sur la date de fondation.")

                # Fondateur Tab
                with tabs[3]:
                    st.markdown("### 👤 Fondateur")
                    if founder_info:
                        df_founder = pd.DataFrame(founder_info)
                        st.dataframe(df_founder, use_container_width=True)
                    else:
                        st.info("Aucune information sur le fondateur.")

                # Marques Tab
                with tabs[4]:
                    st.markdown("### 🏷️ Liste des Marques")
                    if brands_info:
                        df_brands = pd.DataFrame(brands_info)
                        st.dataframe(df_brands, use_container_width=True)
                    else:
                        st.info("Aucune information sur les marques.")

                # Investisseurs Tab
                with tabs[5]:
                    st.markdown("### 💼 Investisseurs")
                    if investors_info:
                        df_investors = pd.DataFrame(investors_info)
                        st.dataframe(df_investors, use_container_width=True)
                    else:
                        st.info("Aucune information sur les investisseurs.")

                # Reset the search_performed flag
                st.session_state.search_performed = False

            except Exception as e:
                st.error(f"❌ Erreur lors de la récupération des informations du groupe : {str(e)}")
