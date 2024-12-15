import streamlit as st
import random
from app.logo_image import get_car_brand_logo
import os
import base64

def get_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    return f"data:image/jpeg;base64,{encoded_string}"
    
# Page d'accueil
def home(manager):
    # Create two columns for layout
    st.markdown("""
    <div style="display: flex; align-items: center;">
        <div>
            <h1>Bienvenue sur AutoSearch</h1>
            <p><em>Découvrez le monde automobile avec notre moteur de recherche intelligent</em></p>
        </div>
        <div style="margin-left: 10px;">
            <img src="https://png.pngtree.com/png-vector/20220617/ourmid/pngtree-auto-car-logo-template-png-image_5181062.png" width="250">
        </div>
    </div>
    <hr style="margin: 20px 0;">
    """, unsafe_allow_html=True)

    st.markdown("## Nos Fonctionnalités")
    st.markdown("### Recherchez des constructeurs de voitures spécifiques")

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

            while len(random_manufacturers) == 0:
                random_letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                random_manufacturers = manager.get_manufacturers_suggestions(random_letter)
            
            st.session_state.random_manufacturer = random.choice(random_manufacturers)
            
        except Exception as e:
            st.warning("Impossible de générer un constructeur aléatoire.")
            st.session_state.random_manufacturer = None

    # Display the random manufacturer if available
    if st.session_state.random_manufacturer:
        logo_path = get_car_brand_logo(st.session_state.random_manufacturer)

        if logo_path and os.path.exists(logo_path):
            base64_logo = get_image_as_base64(logo_path)
            st.markdown(f"""
            <div style="display: flex; align-items: center;">
                <div>
                    <h3><strong>{st.session_state.random_manufacturer}</strong></h3>
                </div>
                <div style="margin-left: 5px;">
                    <img src="{base64_logo}" width="100">
                </div>
            </div>
            <br>
            """, unsafe_allow_html=True)
        else:
            st.write(f"Constructeur : **{st.session_state.random_manufacturer}**")
            st.write("Logo non trouvé.")

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
