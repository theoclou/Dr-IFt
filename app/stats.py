import streamlit as st
import pandas as pd
import plotly.express as px

# Page des statistiques

def stats(manager):
    st.title("Statistiques")

    # Afficher les statistiques
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Nombre total de constructeurs")
        total_manufacturers = manager.get_total_manufacturers()
        st.write(f"Total des constructeurs : {total_manufacturers}")

    with col2:    
        st.subheader("Nombre total de voitures")
        total_cars = manager.get_total_cars()
        st.write(f"Total des voitures : {total_cars}")

    with col1:
        st.subheader("Top 10 constructeurs (par nombre de voitures produites)")
        top_manufacturers = manager.get_top_manufacturers()
        df_top_manufacturers = pd.DataFrame([
            {"manufacturer": manufacturer['manufacturerName']['value'], "count": manufacturer['count']['value']}
            for manufacturer in top_manufacturers
        ])
        fig = px.bar(df_top_manufacturers, x="manufacturer", y="count", labels={"count": "Nombre de voitures"}, color="manufacturer")
        fig.update_layout(xaxis=dict(showticklabels=False))
        st.plotly_chart(fig)

    with col2:
        st.subheader("Top 5 types de moteurs")
        top_engine_types = manager.get_top_engine_types()
        df_top_engine_types = pd.DataFrame([
            {"engineType": engine_type['engineType']['value'], "count": engine_type['count']['value']}
            for engine_type in top_engine_types
        ])
        fig = px.bar(df_top_engine_types, x="engineType", y="count", labels={"count": "Nombre de voitures"}, color="engineType")
        fig.update_layout(xaxis=dict(showticklabels=False))
        st.plotly_chart(fig)

    with col1:
        st.subheader("Voitures par année de production (1950-2022)")
        car_by_decade = manager.get_car_by_production_year_from1950_to2020()
        df_car_by_decade = pd.DataFrame([
            {"year": decade['yearnum']['value'], "count": decade['count']['value']}
            for decade in car_by_decade
        ])
        fig = px.line(df_car_by_decade, x="year", y="count", labels={"count": "Nombre de voitures"})
        fig.update_layout(xaxis=dict(showticklabels=False))
        st.plotly_chart(fig)

    with col2:
        st.subheader("Répartition des constructeurs par pays")
        manufacturers_by_country = manager.get_manufacturers_by_country()
        df_manufacturers_by_country = pd.DataFrame([
            {"country": country['country']['value'], "count": int(country['count']['value'])}
            for country in manufacturers_by_country
        ])

        fig = px.pie(df_manufacturers_by_country, values='count', names='country', title='Répartition des constructeurs par pays')
        st.plotly_chart(fig)

    with col1:
        st.subheader("Carrosseries de voitures les plus utilisées (Top 5)") 
        best_carrosserie = manager.get_best_carrosserie()
        df_best_carrosserie = pd.DataFrame([
            {"name": carrosserie['name']['value'], "count": carrosserie['count']['value']}
            for carrosserie in best_carrosserie
        ])
        fig = px.bar(df_best_carrosserie, x="name", y="count", labels={"count": "Nombre de voitures"}, color="name")
        fig.update_layout(xaxis=dict(showticklabels=False))
        st.plotly_chart(fig)

    with col2:
        st.subheader("Classes de voitures les plus populaires (Top 5)") 
        class_car = manager.get_class_car()
        df_class_car = pd.DataFrame([
            {"carClass": car_class['carClass']['value'], "count": car_class['count']['value']}
            for car_class in class_car
        ])
        fig = px.bar(df_class_car, x="carClass", y="count", labels={"count": "Nombre de voitures"}, color="carClass")
        fig.update_layout(xaxis=dict(showticklabels=False))
        st.plotly_chart(fig)

    with col1:
        st.subheader("TOP 5 Chiffre d'affaires des entreprises sur un an (en euros)")
        company_turnover = manager.get_company_turnover()
        df_company_turnover = pd.DataFrame([
            {"manufacturer": company['manufacturer']['value'], "salary": float(company['salary']['value'])}
            for company in company_turnover
        ])
        fig = px.bar(df_company_turnover, x="manufacturer", y="salary", labels={"salary": "Chiffre d'affaires (euros)"}, color="manufacturer")
        fig.update_layout(xaxis=dict(showticklabels=False))
        st.plotly_chart(fig)