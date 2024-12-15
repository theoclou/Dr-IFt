import streamlit as st

# Page à propos
def about(manager):
    st.title("À propos de AutoSearch")

    st.markdown("""
    ## Notre équipe

    ### Développeurs
    - **Audrey SOULET**
    - **Abderrahlane BOUZIANE**
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