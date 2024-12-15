import streamlit as st
import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from car_search.sparql_manager import SparqlManager

from about import about
from home import home
from models import models
from stats import stats

# Initialize SPARQL manager (global for reuse)
manager = SparqlManager()

st.set_page_config(
    page_title="Moteur de recherche automobile",  # Titre de la page
    page_icon="🚗",  # Icône de la page
    layout="wide",  # Active la mise en page large
    initial_sidebar_state="expanded",  # État initial de la barre latérale (ouverte)
    menu_items={
        'Get Help': 'https://www.streamlit.io',
        'About': 'https://www.streamlit.io/about',
    }
)

# Page d'accueil
def home():
    # Create two columns for layout
    col1, col2 = st.columns([2, 0.5])

    with col1:
        st.markdown("""
        <h1>Bienvenue sur AutoSearch</h1>
        <p><em>Découvrez le monde automobile avec notre moteur de recherche intelligent</em></p>
        <hr>
        """, unsafe_allow_html=True)

    st.markdown("## Nos Fonctionnalités")
    st.markdown("### Recherchez des constructeurs de voitures spécifiques")

    with col2:
        # Centered image with reduced size
        st.image("https://png.pngtree.com/png-vector/20220617/ourmid/pngtree-auto-car-logo-template-png-image_5181062.png", width=250)

    query = st.text_input(
        "Votre choix :",
        key="query",
        placeholder="Entrez un constructeur...",
        help="Tapez un constructeur pour voir des suggestions.",
        autocomplete="off",
    )

    if query:
        try:
            # Get live suggestions based on the query
            suggestions = manager.get_manufacturers_suggestions(query)
            if suggestions:
                selected_manufacturer = st.selectbox(
                    "Constructeurs :",
                    suggestions,
                    key="manufacturer_suggestions"
                )
                if selected_manufacturer:
                    st.write(f"**Modèles de {selected_manufacturer}:**")
                    if st.button("Voir les modèles"):
                        st.session_state.page = "Modèles"
                        st.session_state.search_performed = True
                        st.session_state.manufacturer = selected_manufacturer
                        st.rerun()
        except Exception as e:
            st.error(f"Erreur lors de la recherche des suggestions: {str(e)}")

    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
    st.markdown("## Nos choix du jour")
    # Random interesting section
    st.markdown("### 🎲 Constructeur")

    # Initialize random manufacturer if not already set
    if "random_manufacturer" not in st.session_state:
        try:
            random_letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            random_manufacturers = manager.get_manufacturers_suggestions(random_letter)
            st.session_state.random_manufacturer = random.choice(random_manufacturers)
        except Exception as e:
            st.warning("Impossible de générer un constructeur aléatoire.")
            st.session_state.random_manufacturer = None

    # Display the random manufacturer if available
    if st.session_state.random_manufacturer:
        st.write(f"Constructeur : **{st.session_state.random_manufacturer}**")

        # Button to view models of the random manufacturer
        if st.button("Voir les modèles du jour"):
            st.session_state.page = "Modèles"
            st.session_state.search_performed = True
            st.session_state.manufacturer = st.session_state.random_manufacturer
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### ♫ Devinette Automobile")

    # Initialize question if not already set
    if "question" not in st.session_state:
        devinettes = [
            {"question": "Quel constructeur a inventé la première voiture à essence ?",
            "reponses": ["Benz", "Mercedes", "Daimler", "Mercedes-Benz"]},
            {"question": "Quel constructeur a produit la première voiture de série ?",
            "reponses": ["Ford"]},
            {"question": "Quand a été fondé le constructeur japonais Toyota ?",
             "reponses": ["1937"]},
            {"question": "A quelle date a été crée la première voiture/engin électrique ?",
                "reponses": ["1834"]}
            # Autres devinettes...
        ]
        st.session_state.question = random.choice(devinettes)

    devinette = st.session_state.question
    st.write(devinette["question"])
    reponse = st.text_input("Votre réponse :", key="reponse", placeholder="Entrez votre réponse", autocomplete="off")
    if st.button("Vérifier"):
        if reponse.lower() in [r.lower() for r in devinette["reponses"]]:
            st.success("Bravo ! Bonne réponse 🏆")
        else:
            st.error("Pas tout à fait. Réessayez !")

    # Initialize citation if not already set
    if "citation" not in st.session_state:
        citations = [
            "L'automobile est la passion qui transforme un trajet en aventure.",
            "Chaque voiture raconte une histoire, chaque marque une légende.",
            "L'innovation automobile, c'est repousser les limites du possible."
        ]
        st.session_state.citation = random.choice(citations)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 💬 Citation")
    st.markdown(st.session_state.citation)


# Page à propos
def about():
    st.title("À propos de AutoSearch")

    st.markdown("""
    ## Notre équipe

    ### Développeurs
    - **Audrey SOULET**
    - **Abderrahmane BOUZIANE**
    - **Noam CATHERINE**
    - **Quentin MARIAT**
    - **Théo CLOUSCARD**

    ## Notre projet
    AutoSearch est un moteur de recherche automobile innovant qui permet aux utilisateurs de découvrir et explorer différents constructeurs et modèles de véhicules en détail.

    ### Technologies/Ressources utilisées
    - Streamlit
    - SPARQL
    - DBpedia

    ### Note
    Ce projet a été réalisé dans le cadre d'un projet scolaire à l'INSA de Lyon afin de mettre en pratique nos compétences liées au web sémantique et aux technologies web.
    """)


# Page des modèles automobiles
def models():
    st.title("Modèles automobiles")

    # Récupérer la marque sélectionnée depuis la session
    manufacturer = st.session_state.get("manufacturer", None)
    if manufacturer:
        try:
            cars = manager.get_car_models(manufacturer)

            if cars:
                st.write(f"### Modèles {manufacturer}")

                # Affichage des résultats en grille
                for car in cars:
                    with st.expander(car['name']['value']):
                        # Informations de base
                        if 'year' in car:
                            st.write(f"Released year : {car['year']['value']}")
                        if 'description' in car:
                            st.write(f"Description : {car['description']['value']}")
                        if 'image' in car:
                            st.image(car['image']['value'], use_container_width=True)
                        # Lien vers la page DBpedia
                        st.write(f"[Voir sur DBpedia]({car['car']['value']})")
            else:
                st.warning("Aucun résultat trouvé")
        except Exception as e:
            st.error(f"Erreur lors de la recherche des modèles: {str(e)}")
    else:
        st.warning("Aucune marque sélectionnée. Retournez à l'accueil pour rechercher une marque.")


# Page des statistiques
def stats():
    st.title("Statistiques")

    # Afficher les statistiques
    st.subheader("Nombre total de constructeurs")
    total_manufacturers = manager.get_total_manufacturers()
    st.write(f"Total des constructeurs : {total_manufacturers}")

    st.subheader("Nombre total de voitures")
    total_cars = manager.get_total_cars()
    st.write(f"Total des voitures : {total_cars}")

    st.subheader("Top constructeurs")
    top_manufacturers = manager.get_top_manufacturers()
    df_top_manufacturers = pd.DataFrame([
        {"manufacturer": manufacturer['manufacturerName']['value'], "count": manufacturer['count']['value']}
        for manufacturer in top_manufacturers
    ])
    fig = px.bar(df_top_manufacturers, x="manufacturer", y="count", title="Top constructeurs", labels={"count": "Nombre de voitures"})
    st.plotly_chart(fig)

    st.subheader("Top types de moteurs")
    top_engine_types = manager.get_top_engine_types()
    df_top_engine_types = pd.DataFrame([
        {"engineType": engine_type['engineType']['value'], "count": engine_type['count']['value']}
        for engine_type in top_engine_types
    ])
    fig = px.bar(df_top_engine_types, x="engineType", y="count", title="Top types de moteurs", labels={"count": "Nombre de voitures"})
    st.plotly_chart(fig)

    st.subheader("Voitures par décennie de production (1950-2020)")
    car_by_decade = manager.get_car_by_production_decade_from1950_to2020()
    df_car_by_decade = pd.DataFrame([
        {"decade": decade['decade']['value'], "count": decade['count']['value']}
        for decade in car_by_decade
    ])
    fig = px.line(df_car_by_decade, x="decade", y="count", title="Voitures par décennie de production (1950-2020)", labels={"count": "Nombre de voitures"})
    st.plotly_chart(fig)

    st.subheader("Constructeurs par pays")
    manufacturers_by_country = manager.get_manufacturers_by_country()
    df_manufacturers_by_country = pd.DataFrame([
        {"country": country['country']['value'], "count": country['count']['value']}
        for country in manufacturers_by_country
    ])
    fig = px.bar(df_manufacturers_by_country, x="country", y="count", title="Constructeurs par pays", labels={"count": "Nombre de constructeurs"})
    st.plotly_chart(fig)

    st.subheader("Meilleures carrosseries")
    best_carrosserie = manager.get_best_carrosserie()
    df_best_carrosserie = pd.DataFrame([
        {"name": carrosserie['name']['value'], "count": carrosserie['count']['value']}
        for carrosserie in best_carrosserie
    ])
    fig = px.bar(df_best_carrosserie, x="name", y="count", title="Meilleures carrosseries", labels={"count": "Nombre de voitures"})
    st.plotly_chart(fig)

    st.subheader("Classes de voitures")
    class_car = manager.get_class_car()
    df_class_car = pd.DataFrame([
        {"carClass": car_class['carClass']['value'], "count": car_class['count']['value']}
        for car_class in class_car
    ])
    fig = px.bar(df_class_car, x="carClass", y="count", title="Classes de voitures", labels={"count": "Nombre de voitures"})
    st.plotly_chart(fig)

    st.subheader("TOP Chiffre d'affaires des entreprises sur un an")
    company_turnover = manager.get_company_turnover()
    df_company_turnover = pd.DataFrame([
        {"manufacturer": company['manufacturer']['value'], "salary": company['salary']['value']}
        for company in company_turnover
    ])
    fig = px.bar(df_company_turnover, x="manufacturer", y="salary", title="TOP Chiffre d'affaires des entreprises sur un an", labels={"salary": "Chiffre d'affaires (euros)"})
    st.plotly_chart(fig)



# Group Information page
def group_information():
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


# Manage navigation between pages
# Manage navigation between pages -> see functions in about.py, home.py, models.py, stats.py
PAGES = {
    "Accueil": home,
    "Modèles": models,
    "About": about,
    "Statistiques": stats,
    "Groupe": group_information
}

# Main function
def main():
    # Initialisation de l'état de navigation
    if "page" not in st.session_state:
        st.session_state.page = "Accueil"
    if "manufacturer" not in st.session_state:
        st.session_state.manufacturer = None
    if "search_performed" not in st.session_state:
        st.session_state.search_performed = False

    # Navigation basée sur l'état actuel
    PAGES[st.session_state.page](manager)

    # Barre latérale pour changer de page
    st.sidebar.title("Navigation")
    if st.sidebar.button("Accueil"):
        st.session_state.page = "Accueil"
        st.rerun()
    if st.sidebar.button("Modèles", disabled=not st.session_state.get('search_performed', False)):
        st.session_state.page = "Modèles"
        st.rerun()
    if st.sidebar.button("Statistiques"):
        st.session_state.page = "Statistiques"
        st.rerun()
    if st.sidebar.button("À propos"):
        st.session_state.page = "About"
        st.rerun()
    if st.sidebar.button("Groupe"):
        st.session_state.page = "Groupe"
        st.rerun()

# Entrypoint
if __name__ == "__main__":
    main()
