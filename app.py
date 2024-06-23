import base64
import os
import streamlit as st
import folium
import json
from streamlit.components.v1 import html

# Set page configuration for a better appearance
st.set_page_config(
    page_title="Peta Kepadatan Penduduk",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Skema warna dari merah, kuning, hingga hijau (9 warna)
colors = [
    "#00441b",  # Hijau gelap
    "#006d2c",
    "#238b45",
    "#41ab5d",
    "#78c679",
    "#addd8e",
    "#d9f0a3",
    "#f7fcb9",
    "#c7e9c0",
    "#a1d99b",  # Hijau terang
]



# Menampilkan judul untuk peta
st.title("Peta Kepadatan Penduduk Banggae Timur")
st.write("Peta dengan skala warna berdasarkan kepadatan penduduk, dari merah tua, kuning, hingga hijau muda.")
st.write("Setiap warna mewakili tingkat kepadatan yang berbeda, dengan warna merah tua menunjukkan kepadatan tertinggi.")
# Membaca data GeoJSON
with open('map.geojson') as f:
    geojson_data = json.load(f)

# Mengambil kepadatan penduduk
densities = [feature['properties']['KEPADATAN'] for feature in geojson_data['features']]
min_density = min(densities)
max_density = max(densities)

# Fungsi untuk membuat popup untuk setiap fitur
def popup_function(feature):
    density = feature['properties']['KEPADATAN']
    return folium.Popup(f"Nama Desa: {feature['properties']['DESA']} KEPADATAN: {density}", parse_html=True)

# Urutkan fitur berdasarkan kepadatan dari tinggi ke rendah
sorted_features = sorted(geojson_data['features'], key=lambda x: x['properties']['KEPADATAN'], reverse=True)

# Buat daftar warna sesuai urutan fitur yang diurutkan
feature_colors = {feature['properties']['DESA']: colors[i] for i, feature in enumerate(sorted_features)}

# Membuat peta Folium
m = folium.Map()

# Menambahkan data GeoJSON ke peta dengan warna abu-abu dan popup
for feature in sorted_features:
    desa_name = feature['properties']['DESA']
    color = feature_colors[desa_name]
    
    style_function = lambda x, color=color: {
        'fillColor': color,
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7,
    }
    
    geojson_layer = folium.GeoJson(
        feature,
        style_function=style_function,
        popup=popup_function(feature)
    )
    geojson_layer.add_to(m)

# Menyesuaikan peta ke batas data GeoJSON
m.fit_bounds(m.get_bounds())

# Menyimpan peta ke file HTML sementara
m.save('index.html')

# Membaca konten HTML dari file
with open('index.html', 'r', encoding='utf-8') as f:
    map_html = f.read()

# Menampilkan peta di Streamlit menggunakan komponen HTML
html(map_html, height=600)

