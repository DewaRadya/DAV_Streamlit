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
        padding: 3rem 3rem;
        
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

# sidebar for navigation
# Sidebar
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>MENU</h1>", unsafe_allow_html=True)

    selected_region = st.selectbox('Filter memilih region', df['Region'].unique())

    filtered_countries = df[df['Region'] == selected_region]['Country'].unique()
    selected_country = st.selectbox('Filter memilih negara', filtered_countries)

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

    filtered_df = df[
    (df['Region'] == selected_region) &
    (df['Country'] == selected_country) &
    (df['Year'].between(year_range[0], year_range[1]))
]


# Layout kolom
col1, col2, col3 = st.columns(3)

# Total deaths for the selected country
with col1:
    total_deaths_country = int(filtered_df[disease_type].sum())
    st.metric(label=f'Total {disease_name} di {selected_country}', value=total_deaths_country)

# Total deaths for all years for the selected country
with col2:
    total_deaths_all_years = int(df[(df['Region'] == selected_region) & (df['Country'] == selected_country)][disease_type].sum())
    st.metric(label=f'Total {disease_name} di {selected_country} (Semua Tahun)', value=f"{total_deaths_all_years}")

# Additional value - average deaths per year for the selected country
with col3:
    avg_deaths_per_year = filtered_df[disease_type].mean()
    st.metric(label=f'Rata-rata {disease_name} per Tahun di {selected_country}', value=f"{avg_deaths_per_year:.1f}")



# Pemilihan Map
# Pemilihan Map
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        if not filtered_df.empty:
            # Choose a color scale that is more distinct and suitable for the disease type
            color_scale = px.colors.sequential.Oranges

            fig_map = px.choropleth(
                filtered_df,
                locations="ISO_3",  # Kolom yang berisi kode ISO negara
                color=disease_type,  # Kolom yang akan diwarnai
                hover_name="Country",  # Nama negara yang akan ditampilkan saat dihover
                color_continuous_scale=color_scale,  # Skema warna
                projection="natural earth",  # Proyeksi peta (dalam hal ini, bumi alami)
                title=f"{disease_name} di {selected_country}",  # Menggunakan selected_country dari selectbox negara
                template='plotly_white'  # Using a dark template for a clean look
            )

            # Mendefinisikan interaktivitas di peta
            fig_map.update_geos(
                resolution=110,  # Resolusi peta
                showcoastlines=True,  # Menampilkan garis pantai
                coastlinecolor="Black",  # Warna garis pantai
                showland=True,  # Menampilkan daratan
                landcolor="White",  # Warna daratan
                showocean=True,  # Menampilkan lautan
                oceancolor="LightBlue",  # Warna lautan
                showlakes=True,  # Menampilkan danau
                lakecolor="LightBlue",  # Warna danau
                showcountries=True,  # Menampilkan batas negara
                countrycolor="Black"  # Warna batas negara
            )

            # Update layout for better visualization
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


# Bar chart
with col2:
    if not filtered_df.empty:
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

