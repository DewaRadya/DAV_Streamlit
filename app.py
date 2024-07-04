import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv('Cleaning_TBC.csv')

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# style CSS
st.markdown(
    """
    <style>
    .main .block-container {
        padding: 1rem 1rem;
    }
    .css-1lcbmhc.e1fqkh3o1 {
        padding: 0rem 0rem;
    }
    .css-1kyxreq.e1fqkh3o3 {
        padding: 0rem 0rem;
    }
    .stApp {
        height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }
    .stMetricText {
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center;'>Persebaran TBC di Seluruh Dunia</h1>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>MENU</h1>", unsafe_allow_html=True)

    # Radio button to choose between one or two countries
    num_countries = st.radio('Pilih Jumlah Negara', ['1 Negara', '2 Negara'])

    selected_region = st.selectbox('Filter memilih region', df['Region'].unique())

    filtered_countries = df[df['Region'] == selected_region]['Country'].unique()
    
    # If one country is selected
    if num_countries == '1 Negara':
        selected_country = st.selectbox('Filter memilih negara', filtered_countries)
    # If two countries are selected
    else:
        selected_country1 = st.selectbox('Filter memilih negara pertama', filtered_countries, key='country1')
        selected_country2 = st.selectbox('Filter memilih negara kedua', filtered_countries, key='country2')

    disease_dict = {
        'Prevalensi TBC': 'TB_prevalence',
        'Mortalitas TBC': 'TB_mortality',
        'Kematian TBC': 'TB_deaths',
        'Mortalitas TBC-HIV': 'TB_HIV_mortality',
        'Kematian TBC-HIV': 'TB_HIV_deaths',
        'Insiden TBC': 'TB_incidence',
        'Insiden TBC-HIV': 'TB_HIV_incidence'
    }

    disease_name = st.selectbox('Pilih Jenis Penyakit', list(disease_dict.keys()))
    disease_type = disease_dict[disease_name]

    year_range = st.slider('Filter tahun', int(df['Year'].min()), int(df['Year'].max()), (int(df['Year'].min()), int(df['Year'].max())))

    if num_countries == '1 Negara':
        filtered_df = df[
            (df['Region'] == selected_region) &
            (df['Country'] == selected_country) &
            (df['Year'].between(year_range[0], year_range[1]))
        ]
    else:
        filtered_df1 = df[
            (df['Region'] == selected_region) &
            (df['Country'] == selected_country1) &
            (df['Year'].between(year_range[0], year_range[1]))
        ]
        filtered_df2 = df[
            (df['Region'] == selected_region) &
            (df['Country'] == selected_country2) &
            (df['Year'].between(year_range[0], year_range[1]))
        ]

# Layout kolom
if num_countries == '1 Negara':
    col1, col2, col3 = st.columns(3)
else:
    col1, col2 = st.columns(2)

# Metrics for one country
if num_countries == '1 Negara':
    with col1:
        total_deaths_country = int(filtered_df[disease_type].sum())
        st.metric(label=f'Total {disease_name} di {selected_country}', value=total_deaths_country)

    with col2:
        total_deaths_all_years = int(df[(df['Region'] == selected_region) & (df['Country'] == selected_country)][disease_type].sum())
        st.metric(label=f'Total {disease_name} di {selected_country} (Semua Tahun)', value=f"{total_deaths_all_years}")

    with col3:
        avg_deaths_per_year = filtered_df[disease_type].mean()
        st.metric(label=f'Rata-rata {disease_name} per Tahun di {selected_country}', value=f"{avg_deaths_per_year:.1f}")

# Metrics for two countries
else:
    with col1:
        st.metric(label=f'Total {disease_name} di {selected_country1}', value=int(filtered_df1[disease_type].sum()))
        st.metric(label=f'Total {disease_name} di {selected_country1} (Semua Tahun)', value=int(df[(df['Region'] == selected_region) & (df['Country'] == selected_country1)][disease_type].sum()))
        st.metric(label=f'Rata-rata {disease_name} per Tahun di {selected_country1}', value=f"{filtered_df1[disease_type].mean():.1f}")

    with col2:
        st.metric(label=f'Total {disease_name} di {selected_country2}', value=int(filtered_df2[disease_type].sum()))
        st.metric(label=f'Total {disease_name} di {selected_country2} (Semua Tahun)', value=int(df[(df['Region'] == selected_region) & (df['Country'] == selected_country2)][disease_type].sum()))
        st.metric(label=f'Rata-rata {disease_name} per Tahun di {selected_country2}', value=f"{filtered_df2[disease_type].mean():.1f}")

# Pemilihan Map
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        if num_countries == '1 Negara' and not filtered_df.empty:
            color_scale = px.colors.sequential.Oranges

            fig_map = px.choropleth(
                filtered_df,
                locations="ISO_3",
                color=disease_type,
                hover_name="Country",
                color_continuous_scale=color_scale,
                projection="natural earth",
                title=f"{disease_name} di {selected_country}",
                template='plotly_dark'
            )

            fig_map.update_geos(
                resolution=110,
                showcoastlines=True,
                coastlinecolor="Black",
                showland=True,
                landcolor="White",
                showocean=True,
                oceancolor="LightBlue",
                showlakes=True,
                lakecolor="LightBlue",
                showcountries=True,
                countrycolor="Black"
            )

            fig_map.update_layout(
                coloraxis_colorbar=dict(
                    title=disease_name,
                    tickvals=[filtered_df[disease_type].min(), filtered_df[disease_type].max()],
                    ticktext=['Low', 'High'],
                ),
                margin={"r":0,"t":50,"l":0,"b":0},
                height=400
            )

            st.plotly_chart(fig_map, use_container_width=True)
    #bar chart
    with col2:
        if num_countries == '1 Negara' and not filtered_df.empty:
            fig_bar = px.bar(
                filtered_df, 
                x='Year', 
                y=disease_type, 
                color_discrete_sequence=['orange'], 
                barmode='group',
                text=disease_type  # Add this line to show values on bars
            )

            fig_bar.update_traces(texttemplate='%{text}', textposition='outside')

            fig_bar.update_layout(
                    clickmode='event+select',
                    title=f"{disease_name} dari Tahun ke Tahun",
                    xaxis_title="Year",
                    yaxis_title=disease_name
                )
            st.plotly_chart(fig_bar, use_container_width=True)

if num_countries == '2 Negara' and not filtered_df1.empty and not filtered_df2.empty:
    col1, col2 = st.columns(2)
    with col1:
        color_scale1 = px.colors.sequential.Oranges

        fig_map1 = px.choropleth(
            filtered_df1,
            locations="ISO_3",
            color=disease_type,
            hover_name="Country",
            color_continuous_scale=color_scale1,
            projection="natural earth",
            title=f"{disease_name} di {selected_country1}",
            template='plotly_dark'
        )

        fig_map1.update_geos(
            resolution=110,
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="White",
            showocean=True,
            oceancolor="LightBlue",
            showlakes=True,
            lakecolor="LightBlue",
            showcountries=True,
            countrycolor="Black"
        )

        fig_map1.update_layout(
            coloraxis_colorbar=dict(
                title=disease_name,
                tickvals=[filtered_df1[disease_type].min(), filtered_df1[disease_type].max()],
                ticktext=['Low', 'High'],
            ),
            margin={"r":0,"t":50,"l":0,"b":0},
            height=400
        )

        st.plotly_chart(fig_map1, use_container_width=True)

    with col2:
        color_scale2 = px.colors.sequential.Oranges

        fig_map2 = px.choropleth(
            filtered_df2,
            locations="ISO_3",
            color=disease_type,
            hover_name="Country",
            color_continuous_scale=color_scale2,
            projection="natural earth",
            title=f"{disease_name} di {selected_country2}",
            template='plotly_dark'
        )

        fig_map2.update_geos(
            resolution=110,
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="White",
            showocean=True,
            oceancolor="LightBlue",
            showlakes=True,
            lakecolor="LightBlue",
            showcountries=True,
            countrycolor="Black"
        )

        fig_map2.update_layout(
            coloraxis_colorbar=dict(
                title=disease_name,
                tickvals=[filtered_df2[disease_type].min(), filtered_df2[disease_type].max()],
                ticktext=['Low', 'High'],
            ),
            margin={"r":0,"t":50,"l":0,"b":0},
            height=400
        )

        st.plotly_chart(fig_map2, use_container_width=True)

    #Bar chart
    combined_df = pd.concat([filtered_df1, filtered_df2])
    fig_bar = px.bar(
        combined_df,
        x='Year',
        y=disease_type,
        color='Country',
        color_discrete_map={selected_country1: 'yellow', selected_country2: 'darkorange'}, 
        barmode='group',
        text=disease_type
    )

    fig_bar.update_traces(texttemplate='%{text}', textposition='outside')

    fig_bar.update_layout(
        clickmode='event+select',
        title=f"{disease_name} dari Tahun ke Tahun",
        xaxis_title="Year",
        yaxis_title=disease_name
    )
    st.plotly_chart(fig_bar, use_container_width=True)
