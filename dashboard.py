import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import duckdb
import time
from streamlit.components.v1 import html

st.set_page_config(page_title="Tableau de Bord Principal", page_icon=":bar_chart:", layout="wide")
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
def show_main_page(st):
    mainSection = st.container()
    with mainSection:
        st.markdown('''
            <style>
                body {
                    font-family: 'Montserrat', sans-serif;
                    color: black;
                }
                h1, h2, h3, h4, h5 {
                    color: #BE5504;
                }
                .css-18e3th9 {
                    background-color: #BE5504;
                }
                .stButton > button {
                    background-color: #BE5504;
                    color: black;
                    font-size: 16px;
                    border-radius: 5px;
                }
            </style>
        ''', unsafe_allow_html=True)

        # Caching the function to load the dataset
        @st.cache_data
        def load_data(file_path):
            return pd.read_csv(file_path)

        df = load_data('supply_chain_data.csv')


        # Filter data based on selected category

        with st.spinner('Loading app...'):
            time.sleep(1)

        # Key Insights Section (could be updated dynamically based on the category)
        st.markdown('''
            <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
        ''', unsafe_allow_html=True)
        # Make sure this path is correct

        # Use markdown to create a container with flex styling
        st.markdown("""
            <style>
                .container {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-bottom: 20px;
                }
                .logo-text {
                    font-weight: 700; 
                    font-size: 4em; 
                    font-family: "Montserrat", sans-serif; 
                    color: #ED7117; 
                    margin-left: 20px;  /* Space between logo and text */
                }
            </style>
            <div class="container">""", unsafe_allow_html=True) 
     
        st.markdown(""" 
                <div class="logo-text">Tableau de bord</div>
            </div>
        """, unsafe_allow_html=True)

        #st.image('./IMG/Logo.webp', width=10, use_column_width='auto')

        st.markdown(f'''
            ### Principaux Enseignements 🔍 
            - **Augmentation des Revenus :** L'optimisation de notre chaîne d'approvisionnement a conduit à une augmentation significative des revenus totaux.
            - **Réduction des Délais :** Des itinéraires simplifiés et une gestion efficace ont permis de réduire les délais de 20 %.
            - **Économies de Coût :** La mise en œuvre de stratégies rentables a entraîné une réduction des coûts globaux de 10 %.
        ''', unsafe_allow_html=True)

        with st.expander("📋 Afficher le Jeu de Données"):
            st.write(df)

        st.markdown(
            """
            #### Impact sur l'Entreprise :
            - **Satisfaction Client Accrue :** Des délais réduits et des processus efficaces garantissent des livraisons à temps, augmentant la satisfaction client. 😊
            - **Meilleure Répartition des Ressources :** Comprendre la distribution des coûts aide à une meilleure budgétisation et allocation des ressources. 🧩
            - **Croissance des Revenus :** Les insights issus des données permettent des décisions stratégiques ayant un impact direct sur la croissance des revenus. 💸
            """,
            unsafe_allow_html=True
        )

        # Create three columns
        col1, col2, col3 = st.columns(3)

        with col1:
            #plo1
            query = """
            SELECT SUM("Revenue generated")::DECIMAL(8, 2) AS total_revenue
            FROM df
            """
            result = duckdb.query(query).df()

            total_revenue = result['total_revenue'][0]

            fig = go.Figure()

            fig.add_trace(go.Indicator(
                mode = "number",
                value = total_revenue,
                title = {"text": "Revenu Total Généré"},
                number = {'prefix': "$", 'valueformat': ".2f"},
                domain = {'x': [0, 1], 'y': [0, 1]}
            ))
            
            fig.update_layout(
                font=dict(size=18),
                font_color = 'black',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                margin=dict(l=20, r=20, t=20, b=20),

            )

            st.plotly_chart(fig, use_container_width=True)

            #plot2
            query = """
            SELECT 
                SUM("stock levels") AS "Stock Levels",
                SUM("Lead Times") AS "Lead Times"
            FROM 
                df;
            """
            result = duckdb.query(query).df()
            total_stock_levels = result['Stock Levels'][0]
            total_lead_times = result['Lead Times'][0]

            fig_stock_levels = go.Figure(go.Indicator(
            mode="number+gauge",
            value=total_stock_levels,
            # title={'text': "Total Stock Levels"},
            gauge={
                'axis': {'range': [0, max(total_stock_levels, total_lead_times) + 100]},
                'bar': {'color': "rgba(31, 119, 180, 0.8)"},
                'steps': [
                    {'range': [0, max(total_stock_levels, total_lead_times) / 2], 'color': "lightgray"},
                    {'range': [max(total_stock_levels, total_lead_times) / 2, max(total_stock_levels, total_lead_times)], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': total_stock_levels
                    }
                }
            ))

            fig_stock_levels.update_layout(
                title={'text': "Niveaux Totaux de Stock", 'font': {'size': 20}},
                font=dict(size=18, color='black'),title_font=dict(color="black"), 
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                
            )

            st.plotly_chart(fig_stock_levels,use_container_width=True)

            #plot3
            query = """
            SELECT "Product Type",
            SUM("Revenue generated")::DECIMAL(8, 2) AS total_revenue
            FROM df
            GROUP BY "Product Type"
            ORDER BY total_revenue DESC
            """
            result = duckdb.query(query).df()

            fig = px.bar(result, 
                    x='Product type', 
                    y='total_revenue', 
                    title='Revenu Généré par Type de Produit',
                    labels={'total_revenue': 'Revenu Total ($)', 'Product Type': 'Type de Produit'}
            )
            fig.update_layout(
                xaxis_title="Type de Produit",
                yaxis_title="Revenu Total ($)",title_font=dict(color="black"), 
                xaxis=dict(
        title=dict(font=dict(color="black")), # X-axis title text color
        tickfont=dict(color="black")          # X-axis tick labels color
    ),
    yaxis=dict(
        title=dict(font=dict(color="black")), # Y-axis title text color
        tickfont=dict(color="black")          # Y-axis tick labels color
    ),
                yaxis_tickprefix="$",
                yaxis_tickformat=".2f",
                margin=dict(l=40, r=40, t=40, b=40),
                font=dict(size=14,color='black'),
                font_color='black',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)', 
                bargap=0,
                bargroupgap=0.1
            )


            fig.update_traces(marker=dict(color=['#813cf6', '#15abbd', '#df9def']))

            st.plotly_chart(fig, use_container_width=True)
            
            #plot4
            fig = px.scatter(df, 
                        x='Manufacturing costs', 
                        y='Revenue generated', 
                        size='Price', 
                        color='Product type',
                        hover_name='SKU',
                        title='Relation entre les Coûts de Fabrication et le Revenu Généré',
                        labels={'Manufacturing costs': 'Coûts de Fabrication ($)', 'Revenue generated': 'Revenu Généré ($)', 'Product type': 'Type de Produit'},
                        template='plotly_dark',
                        color_discrete_sequence=px.colors.qualitative.Dark24
                        )

            fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')),
                        selector=dict(mode='markers'))

            fig.update_layout(
                font=dict(size=14, color='black'),title_font=dict(color="black"), 
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
            )

            st.plotly_chart(fig, use_container_width=True)

            #plot5
            cost_summary = df.groupby('Inspection results').agg({'Manufacturing costs': 'sum'}).reset_index()

            total_costs = cost_summary['Manufacturing costs'].sum()

            cost_summary['Percentage Contribution'] = (cost_summary['Manufacturing costs'] / total_costs * 100).round(2)

            cost_summary['Manufacturing costs'] = cost_summary['Manufacturing costs'].astype(float).round(2)
            cost_summary['Percentage Contribution'] = cost_summary['Percentage Contribution'].astype(float).round(2)

            cost_summary = cost_summary.sort_values(by='Manufacturing costs', ascending=False)

            fig = px.pie(
            cost_summary,
            names='Inspection results',
            values='Manufacturing costs',
            title='Coûts de Fabrication par Résultats d\'Inspection',
            color_discrete_sequence=px.colors.qualitative.Pastel1
            )

            fig.update_traces(
                hoverinfo='label+value+percent',
                textinfo='value+percent'
            )

            fig.update_layout(
                font=dict(size=14,color='black'),title_font=dict(color="black"), 
                showlegend=True,
                legend_title_text='Résultats d\'Inspection',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
            )

            st.plotly_chart(fig, use_container_width=True)
            #plot6
            result = df.groupby('Location')['Order quantities'].sum().reset_index()

            result = result.sort_values(by='Order quantities', ascending=False)

            fig = px.bar(result, x='Location', y='Order quantities',
                    title='Quantités Commandées par Lieu',
                    labels={'Location': 'Lieu', 'Order quantities': 'Quantités Totales de Commandes'},
                    color='Location',
                    color_discrete_sequence=px.colors.qualitative.Dark24,
                    )

            fig.update_layout(
            xaxis_title="Lieu",
            yaxis_title="Quantités Totales Commandées",
            font=dict(size=14,color='black'),title_font=dict(color="black"), 
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            bargap=0.1, xaxis=dict(
        title=dict(font=dict(color="black")), # X-axis title text color
        tickfont=dict(color="black")          # X-axis tick labels color
    ),
    yaxis=dict(
        title=dict(font=dict(color="black")), # Y-axis title text color
        tickfont=dict(color="black")          # Y-axis tick labels color
    ),
            )

            st.plotly_chart(fig, use_container_width=True)

            #plot7
            df['Total shipping costs'] = df['Number of products sold'] * df['Shipping costs']

            fig = px.scatter(df, 
                        x='Number of products sold', 
                        y='Total shipping costs', 
                        size='Price', 
                        color='Customer demographics',
                        hover_name='SKU',
                        title='Relation entre le Nombre de Produits Vendus et les Coûts Totaux d\'Expédition',
                        labels={'Number of products sold': 'Nombre de Produits Vendus', 'Total shipping costs': 'Coûts Totaux d\'Expédition ($)', 'Customer demographics': 'Segment de Clientèle'},
                        template='plotly_dark'
                        )

            fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')),
                        selector=dict(mode='markers'))

            fig.update_layout(
                font=dict(size=14, color='black'),title_font=dict(color="black"), 
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
            )

            st.plotly_chart(fig, use_container_width=True)

            #plot8
            profitability_by_product = df.groupby('Product type').agg(
                Revenue=('Revenue generated', 'sum'),
                Cost=('Costs', 'sum')
                ).reset_index()

            profitability_by_product['Profit'] = (profitability_by_product['Revenue'] - profitability_by_product['Cost']).round(2)

            profitability_by_product = profitability_by_product.sort_values(by='Product type')

            fig = px.bar(profitability_by_product, 
                    x='Product type', 
                    y='Profit',
                    title='Rentabilité Globale par Type de Produit',
                    labels={'Profit': 'Profit ($)', 'Product type': 'Type de Produit'},
                    color='Profit',
                    color_continuous_scale=px.colors.diverging.RdYlGn,
                    )

            fig.update_layout(
                xaxis_title="Type de Produit",
                yaxis_title="Profit ($)",
                font=dict(size=14,color='black'),title_font=dict(color="black"), 
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                bargap=0.1,xaxis=dict(
        title=dict(font=dict(color="black")), # X-axis title text color
        tickfont=dict(color="black")          # X-axis tick labels color
    ),
    yaxis=dict(
        title=dict(font=dict(color="black")), # Y-axis title text color
        tickfont=dict(color="black")          # Y-axis tick labels color
    ),
            )

            st.plotly_chart(fig, use_container_width=True)

            #plot9
            numeric_columns = ['Shipping times', 'Lead times']

            transport_summary = df.groupby('Transportation modes')[numeric_columns].mean().reset_index()

            fig = px.line(transport_summary, 
                    x='Shipping times', 
                    y='Lead times', 
                    color='Transportation modes',
                    title='Temps de Réapprovisionnement Moyen vs. Temps d\'Expédition par Mode de Transport',
                    labels={'Shipping times': 'Temps d\'Expédition (jours)', 'Lead times': 'Temps de Réapprovisionnement (jours)', 'Transportation modes': 'Mode de Transport'},
                    template='plotly_dark',
                    line_shape='spline'
                    )

            fig.update_traces(mode='lines+markers')

            fig.update_layout(
                font=dict(size=14, color='black'),title_font=dict(color="black"), 
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
            )

            st.plotly_chart(fig, use_container_width=True)

            #plot10
            mode_counts = df['Transportation modes'].value_counts()

            fig = go.Figure()

            fig.add_trace(go.Pie(
                labels=mode_counts.index,
                values=mode_counts.values,
                textinfo='percent+label',
                marker_colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
                textposition='inside',
                hole=0.3
            ))

            fig.update_layout(
                title='Fréquence des Modes de Transport',title_font=dict(color="black"), 
                font=dict(size=14, color='black'),
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',

            )

            st.plotly_chart(fig, use_container_width=True)

            #plot11
            location_summary = df.groupby('Location').agg({'Production volumes': 'sum', 'Manufacturing costs': 'sum'}).reset_index()

            fig = px.scatter(location_summary, 
                        x='Production volumes', 
                        y='Manufacturing costs', 
                        color='Location',
                        size='Production volumes',
                        hover_name='Location',
                        title='Relation entre les Volumes de Production et les Coûts de Fabrication par Lieu',
                        labels={'Production volumes': 'Volumes de Production', 'Manufacturing costs': 'Coûts de Fabrication', 'Location': 'Lieu'},
                        size_max=30)

            fig.update_layout(
                font=dict(size=14, color='black'),title_font=dict(color="black"), 
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                showlegend=True,
                xaxis_title='Volumes de Production',
                yaxis_title='Coûts de Fabrication',xaxis=dict(
        title=dict(font=dict(color="black")), # X-axis title text color
        tickfont=dict(color="black")          # X-axis tick labels color
    ),
    yaxis=dict(
        title=dict(font=dict(color="black")), # Y-axis title text color
        tickfont=dict(color="black")          # Y-axis tick labels color
    ),
            )

            st.plotly_chart(fig, use_container_width=True)
        with col2:
            query = """
            SELECT 
                SUM("Order quantities") AS "Total Orders Quantity"
            FROM 
                df;
            """

            result = duckdb.query(query).fetchall()

            total_orders_quantity = result[0][0]

            fig = go.Figure()

            fig.add_trace(go.Indicator(
                mode="number",
                value=total_orders_quantity,
                title={"text": "Quantité Totale de Commandes"},
                number={"valueformat": ",.0f"}
            ))

            fig.update_layout(
                font=dict(size=18, color='black'),
                margin=dict(l=20, r=20, t=80, b=20),
                paper_bgcolor='rgba(0, 0, 0, 0)',title_font=dict(color="white"), 

            )

            st.plotly_chart(fig, use_container_width=True)

            #plot2
            fig_lead_times = go.Figure(go.Indicator(
            mode="number+gauge",
            value=total_lead_times,
            # title={'text': "Total Lead Times"},
            gauge={
                'axis': {'range': [0, max(total_stock_levels, total_lead_times) + 100]},
                'bar': {'color': "rgba(214, 39, 40, 0.8)"},
                'steps': [
                    {'range': [0, max(total_stock_levels, total_lead_times) / 2], 'color': "lightgray"},
                    {'range': [max(total_stock_levels, total_lead_times) / 2, max(total_stock_levels, total_lead_times)], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': total_lead_times
                    }
                }
            ))

            fig_lead_times.update_layout(
                                title_font=dict(color="black"), 

                title={'text': "Délais de Réapprovisionnement Totaux", 'font': {'size': 20}},
                font=dict(size=18, color='black'),
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
            )

            st.plotly_chart(fig_lead_times,use_container_width=True)

            #plot3
            query = """
            SELECT "location",
                SUM("Revenue generated")::DECIMAL(8, 2) AS total_revenue
            FROM df
            GROUP BY "location"
            ORDER BY total_revenue DESC
            """
            result = duckdb.query(query).df()

            fig = px.pie(result, 
                    values='total_revenue', 
                    names='Location', 
                    title='Distribution des Revenus par Lieu',
                    labels={'total_revenue': 'Revenu Total ($)', 'Location': 'Lieu'},
                    hover_name='Location',
                    hover_data={'total_revenue': ':,.2f'}
                    )

            fig.update_layout(
                margin=dict(l=40, r=40, t=40, b=40),
                font=dict(size=14, color='black'),
                                title_font=dict(color="black"), 

                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
            )

            fig.update_traces(marker=dict(colors=['#d62728', '#e377c2', '#ff7f0e', '#ffbb78', '#ff9896']))

            fig.update_layout(
                showlegend=True,
                title_font=dict(color="black"), 
                legend=dict(
                    title='Lieu',
                    orientation='v',
                    yanchor='top',
                    y=1,
                    xanchor='left',
                    x=0
                )
            )

            st.plotly_chart(fig, use_container_width=True)

            supplier_summary = df.groupby('Supplier name')['Manufacturing costs'].sum().reset_index()

            fig = px.bar(
                supplier_summary,
                x='Supplier name',
                y='Manufacturing costs',
                title='Distribution des Coûts de Fabrication par Fournisseur',
                labels={'Supplier name': 'Nom du Fournisseur', 'Manufacturing costs': 'Coûts de Fabrication ($)'},
                color='Supplier name',
                color_discrete_sequence=px.colors.qualitative.Set3_r
            )

            fig.update_layout(
                title_font=dict(color="black"),
                font=dict(size=14, color='black'),
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                xaxis={'categoryorder':'total descending'},
            )

            st.plotly_chart(fig, use_container_width=True)

            #plot5
            # Calculate sum of price and manufacturing costs for each product type
            price_costs_by_product = df.groupby('Product type').agg(
                Price=('Price', 'sum'),
                Manufacturing_costs=('Manufacturing costs', 'sum')
            ).reset_index()

            # Format sums of price and manufacturing costs
            price_costs_by_product['Price'] = price_costs_by_product['Price'].round(2)
            price_costs_by_product['Manufacturing_costs'] = price_costs_by_product['Manufacturing_costs'].round(2)

            # Calculate difference between price and manufacturing costs
            price_costs_by_product['Profit_margin'] = (price_costs_by_product['Price'] - price_costs_by_product['Manufacturing_costs']).round(2)

            # Sort by Product type in ascending order
            price_costs_by_product = price_costs_by_product.sort_values(by='Product type')
            fig = px.bar(price_costs_by_product, 
                    x='Product type', 
                    y=['Price', 'Manufacturing_costs'],
                    title='Comparaison des Prix et des Coûts de Fabrication par Type de Produit',
                    labels={'value': 'Coût ($)', 'Product type': 'Type de Produit', 'variable': 'Type de Coût'},
                    color_discrete_sequence=['#d62728', '#e377c2'],
                    barmode='group'
                    )

            for i, row in price_costs_by_product.iterrows():
                fig.add_annotation(
                    x=row['Product type'],
                    y=row['Price'] + 5,
                    text=f"Profit Margin: ${row['Profit_margin']}",
                    showarrow=False,
                    font=dict(size=10, color='black'),
                )

            fig.update_layout(
                title_font=dict(color="black"), 
                xaxis=dict(
        title=dict(font=dict(color="black")), # X-axis title text color
        tickfont=dict(color="black")          # X-axis tick labels color
    ),
    yaxis=dict(
        title=dict(font=dict(color="black")), # Y-axis title text color
        tickfont=dict(color="black")          # Y-axis tick labels color
    ),
                xaxis_title="Type de Produit",
                yaxis_title="Cout ($)",
                font=dict(size=14, color='black'),
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                bargap=0.2,
            )

            st.plotly_chart(fig, use_container_width=True)

            #plot6
            total_production_volumes = df['Production volumes'].sum()
            total_stock_levels = df['Stock levels'].sum()
            total_order_quantities = df['Order quantities'].sum()

            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=[total_production_volumes, total_stock_levels, total_order_quantities],
                theta=['Production Volumes', 'Stock Levels', 'Order Quantities'],
                fill='toself',
                name='Metrics',
                line_color='green'
                ))

            fig.update_layout(
                title='Relation entre le Volume de Production, les Niveaux de Stock et les Quantités Commandées',
                font=dict(size=14,color='black'),title_font=dict(color="black"), 
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, max(total_production_volumes, total_stock_levels, total_order_quantities)],
                        color = 'green'
                    )
                ),
                showlegend=True,
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                )

            st.plotly_chart(fig, use_container_width=True)

            #plot7
            shipping_summary = df.groupby('Shipping carriers')['Shipping costs'].sum().reset_index()

            fig = px.bar(
                shipping_summary,
                x='Shipping carriers',
                y='Shipping costs',
                title='Distribution des Coûts d\'Expédition par Transporteurs',
                labels={'Shipping carriers': 'Transporteurs', 'Shipping costs': 'Coûts d\'Expédition ($)'},
                color='Shipping carriers',
                color_discrete_sequence=px.colors.qualitative.Set2
            )

            fig.update_layout(
                font=dict(size=14, color='black'),title_font=dict(color="black"), 
                xaxis_title=None,
                xaxis=dict(
        title=dict(font=dict(color="black")), # X-axis title text color
        tickfont=dict(color="black")          # X-axis tick labels color
    ),
    yaxis=dict(
        title=dict(font=dict(color="black")), # Y-axis title text color
        tickfont=dict(color="black")          # Y-axis tick labels color
    ),               yaxis_title='Coûts d\'Expédition ($)',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
            )

            st.plotly_chart(fig, use_container_width=True)


            #plot8
            # Calculate average lead time for each product type
            average_lead_time_by_product = df.groupby('Product type')['Lead times'].mean().reset_index()

            # Format the average lead time to 4 decimal places
            average_lead_time_by_product['Average Lead Time'] = average_lead_time_by_product['Lead times'].round(2)

            # Sort by Product type in ascending order
            average_lead_time_by_product = average_lead_time_by_product.sort_values(by='Product type')

            fig = px.bar(average_lead_time_by_product, 
                    x='Product type', 
                    y='Average Lead Time',
                    title='Temps de Réapprovisionnement Moyen par Type de Produit',
                    labels={'Average Lead Time': 'Temps de Réapprovisionnement Moyen (jours)', 'Product type': 'Type de Produit'},
                    color='Average Lead Time',
                    color_continuous_scale='viridis',
                    )

            fig.update_layout(
                xaxis_title="Type de Produit",
                yaxis_title="Temps de Réapprovisionnement Moyen (jours)",
                title_font=dict(color="black"), 
                xaxis=dict(
        title=dict(font=dict(color="black")), # X-axis title text color
        tickfont=dict(color="black")          # X-axis tick labels color
    ),
    yaxis=dict(
        title=dict(font=dict(color="black")), # Y-axis title text color
        tickfont=dict(color="black")          # Y-axis tick labels color
    ), 
                font=dict(size=14,color='black'),
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                bargap=0.1,
            )

            st.plotly_chart(fig, use_container_width=True)

            #plot9
            route_counts = df['Routes'].value_counts()

            route_counts_df = route_counts.reset_index()
            route_counts_df.columns = ['Routes', 'Count']

            fig = px.scatter(route_counts_df, x='Routes', y='Count', size='Count', hover_name='Routes',
                    title='Graphique à Bulles des Itinéraires de Transport avec Compte',
                    labels={'Routes': 'Itinéraires de Transport', 'Count': 'Fréquence'},
                    size_max=60)

            fig.update_layout(
                showlegend=False,
                xaxis_title="Itinéraires de Transport",title_font=dict(color="black"), 
                yaxis_title="Fréquence",xaxis=dict(
        title=dict(font=dict(color="black")), # X-axis title text color
        tickfont=dict(color="black")          # X-axis tick labels color
    ),
    yaxis=dict(
        title=dict(font=dict(color="black")), # Y-axis title text color
        tickfont=dict(color="black")          # Y-axis tick labels color
    ),
                font=dict(size=14, color='black'),
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
            )

            st.plotly_chart(fig, use_container_width=True)
            #plot10
            location_summary = df.groupby('Location').agg({'Production volumes': 'sum'}).reset_index()

            total_production_volumes = location_summary['Production volumes'].sum()

            location_summary['Percentage'] = (location_summary['Production volumes'] / total_production_volumes) * 100

            location_summary = location_summary.sort_values(by='Production volumes', ascending=False)

            fig = px.pie(
                location_summary,
                names='Location',
                values='Percentage',
                title='Pourcentage des Volumes de Production Alignés sur les Demandes du Marché par Lieu',
                color_discrete_sequence=px.colors.qualitative.Set3
            )

            fig.update_layout(
                font=dict(size=14, color='black'),title_font=dict(color="black"), 
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
            )

            st.plotly_chart(fig, use_container_width=True)

            #plot12
            sum_defect_rates = df.groupby('Inspection results')['Defect rates'].sum().reset_index()

        # Calculate the total defect rate
            total_defect_rate = df['Defect rates'].sum()

        # Calculate the percentage contribution of each inspection result's defect rate
            sum_defect_rates['Percentage of Total Defect Rate'] = \
                (sum_defect_rates['Defect rates'] / total_defect_rate) * 100

        # Calculate the average defect rate for each inspection result
            avg_defect_rate = df.groupby('Inspection results')['Defect rates'].mean().reset_index()

        # Merge the results and order by 'Defect Rates'
            result = pd.merge(sum_defect_rates, avg_defect_rate, on='Inspection results', suffixes=('_sum', '_avg'))
            result = result.sort_values(by='Defect rates_sum', ascending=False)

            fig = px.sunburst(result, path=['Inspection results'], values='Defect rates_sum',
                        hover_data=['Percentage of Total Defect Rate', 'Defect rates_avg'],
                        title='Taux de Défauts par Résultats d\'Inspection (Graphique Sunburst)',
                        color='Defect rates_sum',
                        color_continuous_scale='RdBu')

            fig.update_layout(
                font=dict(size=14, color='black'),title_font=dict(color="black"), 
                plot_bgcolor='rgba(0, 0, 0, 0)', 
                paper_bgcolor='rgba(0, 0, 0, 0)', 
            )

            st.plotly_chart(fig, use_container_width=True)
        with col3:
            total_availability = df['Availability'].sum()

            fig = go.Figure()

            fig.add_trace(go.Indicator(
                mode="number",
                value=total_availability,
                title={"text": "Disponibilité Totale"},
                domain={'x': [0, 1], 'y': [0, 1]}
            ))

            fig.update_layout(
                font=dict(size=18, color='black'),title_font=dict(color="white"), 
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',

            )

            st.plotly_chart(fig, use_container_width=True)

            order_summary = df.groupby('Transportation modes')['Order quantities'].sum().reset_index()

            fig = px.sunburst(
                order_summary,
                path=['Transportation modes'],
                values='Order quantities',
                title='Quantités Totales de Commandes par Mode de Transport',
                color='Order quantities',
                color_continuous_scale=px.colors.sequential.Blues,
                labels={'Transportation modes': 'Mode de Transport', 'Order quantities': 'Quantités Totales de Commandes'},
            )

            fig.update_layout(
                font=dict(size=14, color='black'),title_font=dict(color="black"), 
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
            )

            st.plotly_chart(fig, use_container_width=True)
            #plot3
            price_revenue_summary = df.groupby('Price').agg({'Revenue generated': 'sum'}).reset_index()

            fig = px.line(price_revenue_summary, 
                    x='Price', 
                    y='Revenue generated', 
                    title='Revenu Généré par Tranche de Prix',
                    labels={'Revenue generated': 'Revenu Total ($)', 'Price Range': 'Tranche de Prix'},
                    markers=True)

            fig.update_layout(
                font=dict(size=14, color='black'),title_font=dict(color="black"), 
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
            )

            st.plotly_chart(fig, use_container_width=True)

            #plot4
            production_summary = df.groupby('Production volumes')['Manufacturing costs'].sum().reset_index()

            fig = px.scatter(production_summary, 
                        x='Production volumes', 
                        y='Manufacturing costs', 
                        trendline='ols',
                        title='Coûts de Fabrication vs. Volumes de Production',
                        labels={'Manufacturing costs': 'Coûts de Fabrication ($)', 'Production volumes': 'Volumes de Production'},
                        hover_name='Production volumes',
                        trendline_color_override='red'
                        )

            fig.update_layout(
            font=dict(size=14, color='black'),title_font=dict(color="black"), 
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            xaxis_title='Volumes de Production',
            yaxis_title='Coûts de Fabrication ($)',xaxis=dict(
        title=dict(font=dict(color="black")), # X-axis title text color
        tickfont=dict(color="black")          # X-axis tick labels color
    ),
    yaxis=dict(
        title=dict(font=dict(color="black")), # Y-axis title text color
        tickfont=dict(color="black")          # Y-axis tick labels color
    ),
            showlegend=True
            )

            st.plotly_chart(fig, use_container_width=True)

            #plot5
            costs_by_product = df.groupby('Product type')['Manufacturing costs'].sum().reset_index()

            costs_by_product['Manufacturing costs'] = costs_by_product['Manufacturing costs'].round(2)

            costs_by_product = costs_by_product.sort_values(by='Manufacturing costs', ascending=False)

            fig = px.bar(costs_by_product, 
                    x='Product type', 
                    y='Manufacturing costs', 
                    title='Coûts de Fabrication par Type de Produit',
                    labels={'Manufacturing costs': 'Coûts de Fabrication ($)', 'Product type': 'Type de Produit'},
                    color='Product type',
                    color_discrete_sequence=px.colors.qualitative.Dark24_r
                    )

            fig.update_layout(
                xaxis_title="Type de Produit",title_font=dict(color="black"), 
                yaxis_title="Coûts de Fabrication ($)",xaxis=dict(
        title=dict(font=dict(color="black")), # X-axis title text color
        tickfont=dict(color="black")          # X-axis tick labels color
    ),
    yaxis=dict(
        title=dict(font=dict(color="black")), # Y-axis title text color
        tickfont=dict(color="black")          # Y-axis tick labels color
    ),
                font=dict(size=14, color='black'),
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                bargap=0.1,
            )

            st.plotly_chart(fig, use_container_width=True)

            #plot6
            shipping_order_summary = df.groupby('Shipping costs').agg({'Order quantities': 'mean'}).reset_index()

            fig = px.bar(shipping_order_summary, 
                    x='Shipping costs', 
                    y='Order quantities', 
                    title='Quantités Moyennes de Commandes par Tranche de Coût d\'Expédition',
                    labels={'Order quantities': 'Quantités Moyennes de Commandes', 'Shipping Cost Range': 'Tranche de Coût d\'Expédition'},
                    color='Shipping costs',
                    color_discrete_sequence=px.colors.qualitative.Bold)

            fig.update_layout(
                font=dict(size=14, color='black'),title_font=dict(color="black"), 
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                xaxis={'categoryorder': 'total descending'}
                )

            st.plotly_chart(fig, use_container_width=True)

            #plot7
            transportation_summary = df.groupby('Transportation modes')['Shipping costs'].sum().reset_index()

            fig = px.bar(transportation_summary, 
                    x='Transportation modes', 
                    y='Shipping costs', 
                    color='Transportation modes',
                    hover_name='Transportation modes',
                    title='Coûts d\'Expédition par Mode de Transport',
                    labels={'Shipping costs': 'Coûts d\'Expédition ($)', 'Transportation modes': 'Mode de Transport'},
                    color_discrete_sequence=px.colors.qualitative.Safe)

            fig.update_layout(
                font=dict(size=14, color='black'),title_font=dict(color="black"), 
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                xaxis_title='Modes de Transport',
                yaxis_title='Coûts d\'Expédition ($)',xaxis=dict(
        title=dict(font=dict(color="black")), # X-axis title text color
        tickfont=dict(color="black")          # X-axis tick labels color
    ),
    yaxis=dict(
        title=dict(font=dict(color="black")), # Y-axis title text color
        tickfont=dict(color="black")          # Y-axis tick labels color
    ),
                showlegend=True
            )

            st.plotly_chart(fig, use_container_width=True)
            #plot8
            average_defect_rate = df.groupby('Product type').agg({'Defect rates': 'mean'}).reset_index()

            average_defect_rate['Defect rates'] = average_defect_rate['Defect rates'].round(2)

            average_defect_rate.columns = ['Product Type', 'Average Defect Rate']

            fig = px.pie(
            average_defect_rate,
            names='Product Type',
            values='Average Defect Rate',
            title='Taux de Défaut Moyen par Type de Produit',
            color_discrete_sequence=px.colors.qualitative.Pastel
            )

            fig.update_layout(
            font=dict(size=14,color='black'),title_font=dict(color="black"), 
            showlegend=True,
            legend_title_text='Type de Produit',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            )

            st.plotly_chart(fig, use_container_width=True)

            #plot9
            mode_summary = df.groupby('Transportation modes').agg({
            'Lead times': 'sum',
            'Costs': 'sum'
            }).reset_index()

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=mode_summary['Lead times'],
                y=mode_summary['Costs'],
                mode='markers',
                marker=dict(color='blue', size=12),
                text=mode_summary['Transportation modes'],
                hovertemplate='<b>Transport Mode</b>: %{text}<br><b>Lead Time</b>: %{x}<br><b>Cost</b>: %{y}',
            ))

            fig.update_layout(
                title='Relation entre les Modes de Transport, le Temps de Réapprovisionnement et les Coûts',
                xaxis_title='Temps de Réapprovisionnement',title_font=dict(color="black"), 
                yaxis_title='Coûts',xaxis=dict(
        title=dict(font=dict(color="black")), # X-axis title text color
        tickfont=dict(color="black")          # X-axis tick labels color
    ),
    yaxis=dict(
        title=dict(font=dict(color="black")), # Y-axis title text color
        tickfont=dict(color="black")          # Y-axis tick labels color
    ), 
                font=dict(size=14, color='black'),
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
            )

            st.plotly_chart(fig, use_container_width=True)
            #plot11
            location_summary = df.groupby('Location').agg({'Production volumes': 'sum'}).reset_index()

            location_summary = location_summary.sort_values(by='Production volumes', ascending=False)

            fig = px.treemap(
                location_summary,
                path=['Location'],
                values='Production volumes',
                color='Production volumes',
                color_continuous_scale='Viridis',
                title='Volumes de Production par Lieu',
            )

            fig.update_layout(
                font=dict(size=14, color='black'),title_font=dict(color="black"), 
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
            )

            st.plotly_chart(fig, use_container_width=True)

            
            #plot12
            route_summary = df.groupby('Routes').agg({'Lead times': 'sum', 'Costs': 'sum'}).reset_index()

            route_summary = route_summary.sort_values(by='Lead times', ascending=False)

            route_summary['Costs'] = route_summary['Costs'].round(2)

            fig = px.parallel_categories(
                route_summary,
                dimensions=['Routes', 'Lead times', 'Costs'],
                color='Lead times',
                title='Impact des Itinéraires sur les Temps de Réapprovisionnement et les Coûts',
                color_continuous_scale=px.colors.diverging.Tealrose
            )

            fig.update_layout(
                font=dict(size=14, color='black'),title_font=dict(color="black"), 
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                template="plotly_dark"
            )

            st.plotly_chart(fig, use_container_width=True)
            import streamlit as st
