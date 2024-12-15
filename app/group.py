import streamlit as st
import pandas as pd
# Group Information page
def group_information(manager):
    st.title("Informations sur les Groupes")

    group = st.text_input("Entrez le nom du groupe :", "")
    if st.button("Obtenir les informations"):
        if group.strip() == "":
            st.warning("Veuillez entrer un nom de groupe valide.")
        else:
            try:
                with st.spinner('Récupération des informations...'):
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
                tabs = st.tabs(["Groupe Parent", "Pays", "Date de Fondation", "Fondateur", "Marques", "Chiffre d'Affaires", "Investisseurs"])

                # Groupe Parent
                with tabs[0]:
                    st.subheader("Groupe Parent (Car)")
                    if parent_group_car:
                        df = pd.DataFrame(parent_group_car)
                        st.table(df)
                    else:
                        st.write("Aucune information sur le groupe parent.")

                    st.subheader("Groupe Parent (Constructeur)")
                    if parent_group_manufacturer:
                        df = pd.DataFrame(parent_group_manufacturer)
                        st.table(df)
                    else:
                        st.write("Aucune information sur le groupe parent.")

                # Pays
                with tabs[1]:
                    st.subheader("Pays du Groupe")
                    if country_info:
                        df = pd.DataFrame(country_info)
                        st.table(df)
                    else:
                        st.write("Aucune information sur le pays.")

                # Date de Fondation
                with tabs[2]:
                    st.subheader("Date de Fondation")
                    if founding_date:
                        df = pd.DataFrame(founding_date)
                        st.table(df)
                    else:
                        st.write("Aucune information sur la date de fondation.")

                # Fondateur
                with tabs[3]:
                    st.subheader("Fondateur")
                    if founder_info:
                        df = pd.DataFrame(founder_info)
                        st.table(df)
                    else:
                        st.write("Aucune information sur le fondateur.")

                # Marques
                with tabs[4]:
                    st.subheader("Liste des Marques")
                    if brands_info:
                        df = pd.DataFrame(brands_info)
                        st.table(df)
                    else:
                        st.write("Aucune information sur les marques.")

                # Chiffre d'Affaires
                with tabs[5]:
                    st.subheader("Chiffre d'Affaires")
                    if revenue_info:
                        df = pd.DataFrame(revenue_info)
                        # Convert revenue to float for better readability
                        df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
                        df = df.dropna(subset=['revenue'])
                        fig = px.bar(df, x="parentCompany", y="revenue",
                                     title="Chiffre d'Affaires des Groupes",
                                     labels={"revenue": "Chiffre d'Affaires (euros)", "parentCompany": "Groupe"})
                        st.plotly_chart(fig)
                    else:
                        st.write("Aucune information sur le chiffre d'affaires.")

                # Investisseurs
                with tabs[6]:
                    st.subheader("Investisseurs")
                    if investors_info:
                        df = pd.DataFrame(investors_info)
                        st.table(df)
                    else:
                        st.write("Aucune information sur les investisseurs.")

            except Exception as e:
                st.error(f"Erreur lors de la récupération des informations du groupe : {str(e)}")