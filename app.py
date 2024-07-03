import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv('Cleaning_TBC.csv')

st.set_page_config(layout="wide")

# style CSS
st.markdown(
    """
    <style>
    .main .block-container {
        padding: 1.5rem 1.5rem;
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

    </style>
    """,
    unsafe_allow_html=True
)

# JUDUL
st.markdown("<h1 style='text-align: center;'>TBC di DUNIA</h1>", unsafe_allow_html=True)

# Layout kolom
col1, col2, col3, col4 = st.columns(4)

# Filter berdasarkan region
with col1:
    selected_region = st.selectbox('Filter memilih region', df['Region'].unique())

# Filter negara berdasarkan region yang dipilih
filtered_countries = df[df['Region'] == selected_region]['Country'].unique()

with col2:
    selected_country = st.selectbox('Filter memilih negara', filtered_countries)

# Kamus untuk mengonversi nama tabel menjadi nama penyakit
disease_dict = {
        'Prevalensi TBC': 'TB_prevalence',
        'Mortalitas TBC': 'TB_mortality',
        'Kematian TBC': 'TB_deaths',
        'Mortalitas TBC-HIV': 'TB_HIV_mortality',
        'Kematian TBC-HIV': 'TB_HIV_deaths',
        'Insiden TBC': 'TB_incidence',
        'Insiden TBC-HIV': 'TB_HIV_incidence'
}

with col3:
    disease_name = st.selectbox('Pilih Jenis Penyakit', list(disease_dict.keys()))
    disease_type = disease_dict[disease_name]

with col4:
    year_range = st.slider('Filter tahun', int(df['Year'].min()), int(df['Year'].max()), (int(df['Year'].min()), int(df['Year'].max())))

# Filter data berdasarkan pilihan pengguna
filtered_df = df[
    (df['Region'] == selected_region) &
    (df['Country'] == selected_country) &
    (df['Year'].between(year_range[0], year_range[1]))
]

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
            template='plotly_white'  # Using a white template for a clean look
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
                title=disease_type,
                tickvals=[filtered_df[disease_type].min(), filtered_df[disease_type].max()],
                ticktext=['Low', 'High']
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
                title=f"{disease_name} over the Years",
                xaxis_title="Year",
                yaxis_title=disease_name
            )
        st.plotly_chart(fig_bar, use_container_width=True)


# Line chart
if not filtered_df.empty:
    fig_line = go.Figure()

    fig_line.add_trace(go.Scatter(
        x=filtered_df['Year'], 
        y=filtered_df[disease_type], 
        mode='lines+markers+text', 
        name=disease_type, 
        line=dict(color='orange'),
        text=filtered_df[disease_type],  # Add this line to show values
        textposition='top center'  # Position the text labels
    ))

    fig_line.add_trace(go.Scatter(
        x=filtered_df['Year'], 
        y=filtered_df[disease_type+'_low'], 
        mode='lines+markers+text', 
        name=disease_type+'_low', 
        line=dict(color='blue'),
        text=filtered_df[disease_type+'_low'],  # Add this line to show values
        textposition='top center'  # Position the text labels
    ))

    fig_line.update_layout(
        title=f"{disease_name} over Time",
        xaxis_title='Year',
        yaxis_title=disease_name
    )

    st.plotly_chart(fig_line, use_container_width=True)