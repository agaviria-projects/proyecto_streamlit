import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Cobertura Móvil Colombia 2017-2024",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<div class="main-header">📱 Dashboard de Cobertura Móvil en Colombia 2017-2024</div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; font-size: 1.2rem; color: #7f8c8d; margin-bottom: 2rem;">
    Análisis integral de la cobertura de telecomunicaciones móviles en Colombia
</div>
""", unsafe_allow_html=True)

# Función para cargar datos
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('cobertura_colombia_2017_2024_limpio_V2.csv')
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return None

# Cargar datos
df = load_data()

if df is not None:
    # Sidebar - Filtros
    st.sidebar.header("🎛️ Filtros")
    
    # Filtro de año con selectbox mejorado
    years = sorted(df['AÑO'].unique())
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        selected_year = st.selectbox(
            "📅 Seleccionar Año:",
            ['Todos'] + years,
            index=0,
            help="Selecciona un año específico o 'Todos' para ver todos los años"
        )
    with col2:
        if st.button("🔄", help="Limpiar filtro de año"):
            selected_year = 'Todos'
    
    # Filtro de departamento con selectbox mejorado
    departments = sorted(df['DEPARTAMENTO'].unique())
    col3, col4 = st.sidebar.columns([3, 1])
    with col3:
        selected_department = st.selectbox(
            "🏛️ Seleccionar Departamento:",
            ['Todos'] + departments,
            index=0,
            help="Selecciona un departamento específico o 'Todos' para ver todos"
        )
    with col4:
        if st.button("🔄", help="Limpiar filtro de departamento", key="dept_clear"):
            selected_department = 'Todos'
    
    # Filtro de proveedor con selectbox mejorado
    providers = sorted(df['NOMBRE_PROVEEDOR_COMERCIAL'].unique())
    col5, col6 = st.sidebar.columns([3, 1])
    with col5:
        selected_provider = st.selectbox(
            "📡 Seleccionar Proveedor:",
            ['Todos'] + providers,
            index=0,
            help="Selecciona un proveedor específico o 'Todos' para ver todos"
        )
    with col6:
        if st.button("🔄", help="Limpiar filtro de proveedor", key="prov_clear"):
            selected_provider = 'Todos'
    
    # Botón para limpiar todos los filtros
    if st.sidebar.button("🧹 Limpiar Todos los Filtros", use_container_width=True):
        selected_year = 'Todos'
        selected_department = 'Todos'
        selected_provider = 'Todos'
        st.rerun()
    
    # Aplicar filtros
    filtered_df = df.copy()
    
    if selected_year != 'Todos':
        filtered_df = filtered_df[filtered_df['AÑO'] == selected_year]
    
    if selected_department != 'Todos':
        filtered_df = filtered_df[filtered_df['DEPARTAMENTO'] == selected_department]
    
    if selected_provider != 'Todos':
        filtered_df = filtered_df[filtered_df['NOMBRE_PROVEEDOR_COMERCIAL'] == selected_provider]
    
    # Mostrar estado de filtros activos
    active_filters = []
    if selected_year != 'Todos':
        active_filters.append(f"📅 Año: {selected_year}")
    if selected_department != 'Todos':
        active_filters.append(f"🏛️ Dept: {selected_department}")
    if selected_provider != 'Todos':
        active_filters.append(f"📡 Prov: {selected_provider}")
    
    if active_filters:
        st.sidebar.success("✅ Filtros activos: " + " | ".join(active_filters))
    else:
        st.sidebar.info("ℹ️ Sin filtros aplicados - Mostrando todos los datos")
    
    # Verificar si hay datos después del filtrado
    if filtered_df.empty:
        st.warning("⚠️ No hay datos disponibles con los filtros seleccionados. Por favor, ajusta tus filtros.")
    else:
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_records = len(filtered_df)
            st.metric("📊 Total de Registros", f"{total_records:,}")
        
        with col2:
            total_departments = filtered_df['DEPARTAMENTO'].nunique()
            st.metric("🏛️ Departamentos", total_departments)
        
        with col3:
            total_municipalities = filtered_df['MUNICIPIO'].nunique()
            st.metric("🏘️ Municipios", total_municipalities)
        
        with col4:
            total_providers = filtered_df['NOMBRE_PROVEEDOR_COMERCIAL'].nunique()
            st.metric("📡 Proveedores", total_providers)
        
        # Tabs para diferentes secciones
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "📈 Análisis de Cobertura", 
            "🗺️ Análisis Geográfico", 
            "🏢 Análisis por Proveedor",
            "💰 Análisis Socioeconómico", 
            "📅 Series de Tiempo", 
            "🔍 Análisis Detallado",
            "📋 Resumen Ejecutivo"
        ])
        
        with tab1:
            st.markdown('<div class="section-header">📈 Análisis de Cobertura por Tecnología</div>', unsafe_allow_html=True)
            
            # Calcular cobertura por tecnología
            coverage_cols = ['COBERTURA_2G', 'COBERTURA_3G', 'COBERTURA_HSPA_HSPA_DC', 'COBERTURA_4G', 'COBERTURA_LTE', 'COBERTURA_5G']
            
            coverage_summary = {}
            for col in coverage_cols:
                coverage_summary[col.replace('COBERTURA_', '')] = (filtered_df[col] == 'SÍ').sum()
            
            # Gráfico de barras de cobertura
            fig_coverage = px.bar(
                x=list(coverage_summary.keys()), 
                y=list(coverage_summary.values()),
                title="📊 Cobertura por Tecnología (Total de SÍ)",
                labels={'x': 'Tecnología', 'y': 'Número de Localidades'},
                color=list(coverage_summary.values()),
                color_continuous_scale='Blues'
            )
            fig_coverage.update_layout(height=400)
            st.plotly_chart(fig_coverage, use_container_width=True)
            
            # Porcentaje de cobertura
            col1, col2 = st.columns(2)
            
            with col1:
                # Calcular porcentajes
                total_locations = len(filtered_df)
                coverage_pct = {tech: (count/total_locations)*100 for tech, count in coverage_summary.items()}
                
                fig_pie = px.pie(
                    values=list(coverage_pct.values()),
                    names=list(coverage_pct.keys()),
                    title="🥧 Porcentaje de Cobertura por Tecnología",
                    color_discrete_map={'2G': '#FF9999', '3G': '#66B2FF', 'HSPA_HSPA_DC': '#99FF99', '4G': '#FFCC99', 'LTE': '#FF99CC', '5G': '#99CCFF'}
                )
                fig_pie.update_layout(height=400)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Heatmap de cobertura por departamento y tecnología
                dept_coverage = []
                for dept in departments[:10]:  # Limitar a 10 departamentos para mejor visualización
                    dept_data = filtered_df[filtered_df['DEPARTAMENTO'] == dept]
                    dept_row = {'Departamento': dept}
                    for tech in ['2G', '3G', '4G', 'LTE', '5G']:
                        col_name = f'COBERTURA_{tech}' if tech != 'LTE' else 'COBERTURA_LTE'
                        pct = (dept_data[col_name] == 'SÍ').mean() * 100 if len(dept_data) > 0 else 0
                        dept_row[tech] = pct
                    dept_coverage.append(dept_row)
                
                dept_df = pd.DataFrame(dept_coverage)
                
                fig_heatmap = px.imshow(
                    dept_df.set_index('Departamento')[['2G', '3G', '4G', 'LTE', '5G']].T,
                    title="🔥 Heatmap de Cobertura por Departamento (%)",
                    color_continuous_scale='RdYlGn',
                    aspect="auto"
                )
                fig_heatmap.update_layout(height=400)
                st.plotly_chart(fig_heatmap, use_container_width=True)
        
        with tab2:
            st.markdown('<div class="section-header">🗺️ Análisis Geográfico</div>', unsafe_allow_html=True)
            
            # Mapa interactivo de cobertura
            st.markdown("### 🗺️ Mapa de Cobertura por Departamento")
            
            # Crear datos para el mapa con coordenadas de departamentos colombianos
            dept_coords = {
                'AMAZONAS': {'lat': -3.4422, 'lon': -69.7097},
                'ANTIOQUIA': {'lat': 6.2170, 'lon': -75.5812},
                'ARAUCA': {'lat': 7.0819, 'lon': -70.7591},
                'ATLÁNTICO': {'lat': 10.9685, 'lon': -74.7813},
                'BOLÍVAR': {'lat': 10.3910, 'lon': -75.4794},
                'BOYACÁ': {'lat': 5.4545, 'lon': -73.3620},
                'CALDAS': {'lat': 5.0684, 'lon': -75.5178},
                'CAQUETÁ': {'lat': 1.5736, 'lon': -75.6491},
                'CASANARE': {'lat': 5.7589, 'lon': -71.5724},
                'CAUCA': {'lat': 2.4448, 'lon': -76.6147},
                'CESAR': {'lat': 9.3373, 'lon': -73.6536},
                'CHOCÓ': {'lat': 5.6960, 'lon': -76.6477},
                'CÓRDOBA': {'lat': 8.7479, 'lon': -75.8814},
                'CUNDINAMARCA': {'lat': 4.7110, 'lon': -74.0721},
                'GUAINÍA': {'lat': 2.5854, 'lon': -68.5247},
                'GUAVIARE': {'lat': 2.0436, 'lon': -71.8897},
                'HUILA': {'lat': 2.5359, 'lon': -75.5227},
                'LA GUAJIRA': {'lat': 11.5449, 'lon': -72.9048},
                'MAGDALENA': {'lat': 11.2408, 'lon': -74.2110},
                'META': {'lat': 3.2723, 'lon': -73.0877},
                'NARIÑO': {'lat': 1.2073, 'lon': -77.2771},
                'NORTE DE SANTANDER': {'lat': 7.8787, 'lon': -72.5004},
                'PUTUMAYO': {'lat': 0.6721, 'lon': -76.8457},
                'QUINDÍO': {'lat': 4.5339, 'lon': -75.6811},
                'RISARALDA': {'lat': 4.8133, 'lon': -75.6966},
                'SANTANDER': {'lat': 6.6437, 'lon': -73.6536},
                'SUCRE': {'lat': 8.8140, 'lon': -74.7258},
                'TOLIMA': {'lat': 4.4333, 'lon': -75.2167},
                'VALLE DEL CAUCA': {'lat': 3.8009, 'lon': -76.6413},
                'VAUPÉS': {'lat': 0.8554, 'lon': -70.8120},
                'VICHADA': {'lat': 4.4234, 'lon': -69.2878}
            }
            
            # Crear datos para el mapa
            map_data = filtered_df.groupby('DEPARTAMENTO').agg({
                'COBERTURA_4G': lambda x: (x == 'SÍ').mean() * 100,
                'COBERTURA_5G': lambda x: (x == 'SÍ').mean() * 100,
                'INGRESO_PROMEDIO_HOGAR': 'mean',
                'TASA_POBREZA': 'mean',
                'MUNICIPIO': 'nunique',
                'NOMBRE_PROVEEDOR_COMERCIAL': 'nunique'
            }).round(2)
            
            map_data.columns = ['Cobertura_4G_%', 'Cobertura_5G_%', 'Ingreso_Promedio', 'Tasa_Pobreza_%', 'Num_Municipios', 'Num_Proveedores']
            map_data = map_data.reset_index()
            
            # Agregar coordenadas
            map_data['lat'] = map_data['DEPARTAMENTO'].map(lambda x: dept_coords.get(x, {}).get('lat', 4.5709))
            map_data['lon'] = map_data['DEPARTAMENTO'].map(lambda x: dept_coords.get(x, {}).get('lon', -74.2973))
            
            # Selector de variable para el mapa
            map_variable = st.selectbox(
                "Seleccionar variable para mostrar en el mapa:",
                ['Cobertura_4G_%', 'Cobertura_5G_%', 'Ingreso_Promedio', 'Tasa_Pobreza_%', 'Num_Municipios', 'Num_Proveedores'],
                format_func=lambda x: {
                    'Cobertura_4G_%': '📡 Cobertura 4G (%)',
                    'Cobertura_5G_%': '🚀 Cobertura 5G (%)',
                    'Ingreso_Promedio': '💰 Ingreso Promedio',
                    'Tasa_Pobreza_%': '📊 Tasa de Pobreza (%)',
                    'Num_Municipios': '🏘️ Número de Municipios',
                    'Num_Proveedores': '📡 Número de Proveedores'
                }[x]
            )
            
            # Crear el mapa interactivo
            fig_map = px.scatter_mapbox(
                map_data,
                lat='lat',
                lon='lon',
                size=map_variable if map_variable in ['Num_Municipios', 'Num_Proveedores'] else None,
                color=map_variable,
                hover_name='DEPARTAMENTO',
                hover_data={
                    'Cobertura_4G_%': ':.1f',
                    'Cobertura_5G_%': ':.1f',
                    'Ingreso_Promedio': ':,.0f',
                    'Tasa_Pobreza_%': ':.1f',
                    'Num_Municipios': ':.0f',
                    'Num_Proveedores': ':.0f',
                    'lat': False,
                    'lon': False
                },
                title=f"🗺️ {dict({
                    'Cobertura_4G_%': '📡 Cobertura 4G (%)',
                    'Cobertura_5G_%': '🚀 Cobertura 5G (%)',
                    'Ingreso_Promedio': '💰 Ingreso Promedio',
                    'Tasa_Pobreza_%': '📊 Tasa de Pobreza (%)',
                    'Num_Municipios': '🏘️ Número de Municipios',
                    'Num_Proveedores': '📡 Número de Proveedores'
                })[map_variable]} por Departamento",
                color_continuous_scale='RdYlGn' if 'Cobertura' in map_variable else 'Blues',
                size_max=50,
                zoom=4,
                center={"lat": 4.5709, "lon": -74.2973}
            )
            
            fig_map.update_layout(
                mapbox_style="open-street-map",
                height=600,
                margin={"r":0,"t":50,"l":0,"b":0}
            )
            
            st.plotly_chart(fig_map, use_container_width=True)
            
            # Tabla de datos del mapa
            if st.checkbox("Mostrar tabla de datos del mapa"):
                st.dataframe(map_data[['DEPARTAMENTO', 'Cobertura_4G_%', 'Cobertura_5G_%', 'Ingreso_Promedio', 'Tasa_Pobreza_%', 'Num_Municipios', 'Num_Proveedores']].sort_values(map_variable, ascending=False))
            
            # Top 10 departamentos por número de registros
            dept_counts = filtered_df['DEPARTAMENTO'].value_counts().head(10)
            
            fig_dept = px.bar(
                x=dept_counts.index, 
                y=dept_counts.values,
                title="📍 Top 10 Departamentos por Número de Registros",
                labels={'x': 'Departamento', 'y': 'Número de Registros'},
                color=dept_counts.values,
                color_continuous_scale='Viridis'
            )
            fig_dept.update_layout(xaxis_tickangle=-45, height=400)
            st.plotly_chart(fig_dept, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Análisis por cabecera municipal
                cabecera_analysis = filtered_df['CABECERA_MUNICIPAL'].value_counts()
                fig_cabecera = px.pie(
                    values=cabecera_analysis.values,
                    names=cabecera_analysis.index,
                    title="🏘️ Distribución: Cabecera vs No Cabecera",
                    color_discrete_map={'SÍ': '#2E8B57', 'NO': '#CD5C5C'}
                )
                fig_cabecera.update_layout(height=350)
                st.plotly_chart(fig_cabecera, use_container_width=True)
            
            with col2:
                # Altitud promedio por departamento
                altitud_dept = filtered_df.groupby('DEPARTAMENTO')['ALTITUD_MSNM'].mean().sort_values(ascending=False).head(10)
                
                fig_altitud = px.bar(
                    x=altitud_dept.values,
                    y=altitud_dept.index,
                    orientation='h',
                    title="⛰️ Top 10 Departamentos por Altitud Promedio (msnm)",
                    labels={'x': 'Altitud Promedio (msnm)', 'y': 'Departamento'},
                    color=altitud_dept.values,
                    color_continuous_scale='earth'
                )
                fig_altitud.update_layout(height=350)
                st.plotly_chart(fig_altitud, use_container_width=True)
        
        with tab3:
            st.markdown('<div class="section-header">🏢 Análisis por Proveedor</div>', unsafe_allow_html=True)
            
            # Distribución de registros por proveedor
            provider_counts = filtered_df['NOMBRE_PROVEEDOR_COMERCIAL'].value_counts()
            
            fig_providers = px.bar(
                x=provider_counts.index, 
                y=provider_counts.values,
                title="📡 Número de Registros por Proveedor",
                labels={'x': 'Proveedor', 'y': 'Número de Registros'},
                color=provider_counts.values,
                color_continuous_scale='Plasma'
            )
            fig_providers.update_layout(xaxis_tickangle=-45, height=400)
            st.plotly_chart(fig_providers, use_container_width=True)
            
            # Cobertura promedio por proveedor
            provider_coverage = []
            for provider in providers:
                provider_data = filtered_df[filtered_df['NOMBRE_PROVEEDOR_COMERCIAL'] == provider]
                if len(provider_data) > 0:
                    coverage_scores = {}
                    for tech in ['2G', '3G', '4G', 'LTE', '5G']:
                        col_name = f'COBERTURA_{tech}' if tech != 'LTE' else 'COBERTURA_LTE'
                        score = (provider_data[col_name] == 'SÍ').mean() * 100
                        coverage_scores[tech] = score
                    
                    provider_coverage.append({
                        'Proveedor': provider,
                        '2G': coverage_scores['2G'],
                        '3G': coverage_scores['3G'],
                        '4G': coverage_scores['4G'],
                        'LTE': coverage_scores['LTE'],
                        '5G': coverage_scores['5G']
                    })
            
            if provider_coverage:
                coverage_df = pd.DataFrame(provider_coverage)
                
                fig_provider_heatmap = px.imshow(
                    coverage_df.set_index('Proveedor')[['2G', '3G', '4G', 'LTE', '5G']].T,
                    title="🔥 Cobertura Promedio por Proveedor (%)",
                    color_continuous_scale='RdYlGn',
                    aspect="auto"
                )
                fig_provider_heatmap.update_layout(height=400)
                st.plotly_chart(fig_provider_heatmap, use_container_width=True)
        
        with tab4:
            st.markdown('<div class="section-header">💰 Análisis Socioeconómico</div>', unsafe_allow_html=True)
            
            # Ingreso promedio por departamento
            ingreso_dept = filtered_df.groupby('DEPARTAMENTO')['INGRESO_PROMEDIO_HOGAR'].mean().sort_values(ascending=False).head(10)
            
            fig_ingreso = px.bar(
                x=ingreso_dept.index, 
                y=ingreso_dept.values,
                title="💰 Ingreso Promedio por Hogar por Departamento",
                labels={'x': 'Departamento', 'y': 'Ingreso Promedio'},
                color=ingreso_dept.values,
                color_continuous_scale='Blues'
            )
            fig_ingreso.update_layout(xaxis_tickangle=-45, height=400)
            st.plotly_chart(fig_ingreso, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Tasa de pobreza por departamento
                pobreza_dept = filtered_df.groupby('DEPARTAMENTO')['TASA_POBREZA'].mean().sort_values(ascending=False).head(10)
                
                fig_pobreza = px.bar(
                    x=pobreza_dept.values,
                    y=pobreza_dept.index,
                    orientation='h',
                    title="📊 Top 10 Departamentos con Mayor Tasa de Pobreza (%)",
                    labels={'x': 'Tasa de Pobreza (%)', 'y': 'Departamento'},
                    color=pobreza_dept.values,
                    color_continuous_scale='Reds'
                )
                fig_pobreza.update_layout(height=350)
                st.plotly_chart(fig_pobreza, use_container_width=True)
            
            with col2:
                # Tasa de desempleo por departamento
                desempleo_dept = filtered_df.groupby('DEPARTAMENTO')['TASA_DESEMPLEO'].mean().sort_values(ascending=False).head(10)
                
                fig_desempleo = px.bar(
                    x=desempleo_dept.values,
                    y=desempleo_dept.index,
                    orientation='h',
                    title="👥 Top 10 Departamentos con Mayor Tasa de Desempleo (%)",
                    labels={'x': 'Tasa de Desempleo (%)', 'y': 'Departamento'},
                    color=desempleo_dept.values,
                    color_continuous_scale='Oranges'
                )
                fig_desempleo.update_layout(height=350)
                st.plotly_chart(fig_desempleo, use_container_width=True)
            
            # Correlación entre variables socioeconómicas
            socio_vars = ['INGRESO_PROMEDIO_HOGAR', 'TASA_POBREZA', 'TASA_DESEMPLEO', 'ESTRATO_PROMEDIO', 'PCT_HOGARES_INTERNET']
            socio_corr = filtered_df[socio_vars].corr()
            
            fig_corr = px.imshow(
                socio_corr,
                title="🔗 Correlación entre Variables Socioeconómicas",
                color_continuous_scale='RdBu',
                aspect="auto",
                zmin=-1, zmax=1
            )
            fig_corr.update_layout(height=400)
            st.plotly_chart(fig_corr, use_container_width=True)
        
        with tab5:
            st.markdown('<div class="section-header">📅 Análisis de Series de Tiempo</div>', unsafe_allow_html=True)
            
            # Evolución de cobertura por año
            yearly_coverage = []
            for year in years:
                year_data = filtered_df[filtered_df['AÑO'] == year]
                if len(year_data) > 0:
                    year_stats = {'Año': year}
                    for tech in ['2G', '3G', '4G', 'LTE', '5G']:
                        col_name = f'COBERTURA_{tech}' if tech != 'LTE' else 'COBERTURA_LTE'
                        pct = (year_data[col_name] == 'SÍ').mean() * 100
                        year_stats[tech] = pct
                    yearly_coverage.append(year_stats)
            
            if yearly_coverage:
                yearly_df = pd.DataFrame(yearly_coverage)
                
                fig_time_series = px.line(
                    yearly_df, 
                    x='Año', 
                    y=['2G', '3G', '4G', 'LTE', '5G'],
                    title="📈 Evolución de la Cobertura por Tecnología (2017-2024)",
                    labels={'value': 'Porcentaje de Cobertura (%)', 'variable': 'Tecnología'},
                    markers=True
                )
                fig_time_series.update_layout(height=400)
                st.plotly_chart(fig_time_series, use_container_width=True)
            
            # Evolución de indicadores socioeconómicos
            yearly_socio = []
            for year in years:
                year_data = filtered_df[filtered_df['AÑO'] == year]
                if len(year_data) > 0:
                    yearly_socio.append({
                        'Año': year,
                        'Ingreso_Promedio': year_data['INGRESO_PROMEDIO_HOGAR'].mean(),
                        'Tasa_Pobreza': year_data['TASA_POBREZA'].mean(),
                        'Tasa_Desempleo': year_data['TASA_DESEMPLEO'].mean(),
                        'Internet_Hogares': year_data['PCT_HOGARES_INTERNET'].mean()
                    })
            
            if yearly_socio:
                yearly_socio_df = pd.DataFrame(yearly_socio)
                
                fig_socio_time = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('💰 Ingreso Promedio', '📊 Tasa de Pobreza', '👥 Tasa de Desempleo', '🌐 % Hogares con Internet'),
                    specs=[[{"secondary_y": False}, {"secondary_y": False}],
                           [{"secondary_y": False}, {"secondary_y": False}]]
                )
                
                fig_socio_time.add_trace(go.Scatter(x=yearly_socio_df['Año'], y=yearly_socio_df['Ingreso_Promedio'], name='Ingreso Promedio'), row=1, col=1)
                fig_socio_time.add_trace(go.Scatter(x=yearly_socio_df['Año'], y=yearly_socio_df['Tasa_Pobreza'], name='Tasa Pobreza'), row=1, col=2)
                fig_socio_time.add_trace(go.Scatter(x=yearly_socio_df['Año'], y=yearly_socio_df['Tasa_Desempleo'], name='Tasa Desempleo'), row=2, col=1)
                fig_socio_time.add_trace(go.Scatter(x=yearly_socio_df['Año'], y=yearly_socio_df['Internet_Hogares'], name='Internet Hogares'), row=2, col=2)
                
                fig_socio_time.update_layout(height=600, showlegend=False, title_text="📊 Evolución de Indicadores Socioeconómicos")
                st.plotly_chart(fig_socio_time, use_container_width=True)
        
        with tab6:
            st.markdown('<div class="section-header">🔍 Análisis Detallado</div>', unsafe_allow_html=True)
            
            # Análisis de cobertura 5G
            st.markdown("### 📡 Análisis de Cobertura 5G")
            
            cobertura_5g = filtered_df[filtered_df['COBERTURA_5G'] == 'SÍ']
            if len(cobertura_5g) > 0:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Departamentos con 5G
                    dept_5g = cobertura_5g['DEPARTAMENTO'].value_counts().head(10)
                    fig_5g_dept = px.bar(
                        x=dept_5g.index, 
                        y=dept_5g.values,
                        title="🏛️ Departamentos con Cobertura 5G",
                        labels={'x': 'Departamento', 'y': 'Número de Localidades'},
                        color=dept_5g.values,
                        color_continuous_scale='Purples'
                    )
                    fig_5g_dept.update_layout(xaxis_tickangle=-45, height=350)
                    st.plotly_chart(fig_5g_dept, use_container_width=True)
                
                with col2:
                    # Proveedores con 5G
                    prov_5g = cobertura_5g['NOMBRE_PROVEEDOR_COMERCIAL'].value_counts()
                    fig_5g_prov = px.pie(
                        values=prov_5g.values,
                        names=prov_5g.index,
                        title="📡 Proveedores con Cobertura 5G",
                        color_discrete_sequence=px.colors.sequential.Purples
                    )
                    fig_5g_prov.update_layout(height=350)
                    st.plotly_chart(fig_5g_prov, use_container_width=True)
            
            # Análisis de estratos
            st.markdown("### 🏠 Análisis por Estratos")
            
            estrato_analysis = filtered_df.groupby('ESTRATO_PROMEDIO').agg({
                'INGRESO_PROMEDIO_HOGAR': 'mean',
                'TASA_POBREZA': 'mean',
                'PCT_HOGARES_INTERNET': 'mean'
            }).round(2)
            
            fig_estratos = make_subplots(
                rows=1, cols=3,
                subplot_titles=('💰 Ingreso Promedio', '📊 Tasa de Pobreza', '🌐 % Hogares con Internet'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}]]
            )
            
            fig_estratos.add_trace(go.Bar(x=estrato_analysis.index, y=estrato_analysis['INGRESO_PROMEDIO_HOGAR'], name='Ingreso'), row=1, col=1)
            fig_estratos.add_trace(go.Bar(x=estrato_analysis.index, y=estrato_analysis['TASA_POBREZA'], name='Pobreza'), row=1, col=2)
            fig_estratos.add_trace(go.Bar(x=estrato_analysis.index, y=estrato_analysis['PCT_HOGARES_INTERNET'], name='Internet'), row=1, col=3)
            
            fig_estratos.update_layout(height=400, showlegend=False, title_text="📈 Análisis por Estratos")
            st.plotly_chart(fig_estratos, use_container_width=True)
            
            # Tabla de datos filtrados
            st.markdown("### 📊 Tabla de Datos Detallados")
            
            # Mostrar estadísticas descriptivas
            numeric_cols = ['ESTRATO_PROMEDIO', 'INGRESO_PROMEDIO_HOGAR', 'TASA_POBREZA', 'TASA_DESEMPLEO', 'PCT_HOGARES_INTERNET', 'ALTITUD_MSNM', 'PRECIPITACION_MEDIA', 'INV_PUBLICA_PER_CAPITA']
            
            if st.checkbox("Mostrar estadísticas descriptivas"):
                st.dataframe(filtered_df[numeric_cols].describe())
            
            if st.checkbox("Mostrar datos filtrados"):
                st.dataframe(filtered_df)
        
        with tab7:
            st.markdown('<div class="section-header">📋 Resumen Ejecutivo</div>', unsafe_allow_html=True)
            
            # KPIs principales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                # Cobertura 4G promedio
                avg_4g = (filtered_df['COBERTURA_4G'] == 'SÍ').mean() * 100
                st.metric("📡 Cobertura 4G Promedio", f"{avg_4g:.1f}%")
            
            with col2:
                # Cobertura 5G
                avg_5g = (filtered_df['COBERTURA_5G'] == 'SÍ').mean() * 100
                st.metric("🚀 Cobertura 5G Promedio", f"{avg_5g:.1f}%")
            
            with col3:
                # Hogares con Internet
                avg_internet = filtered_df['PCT_HOGARES_INTERNET'].mean()
                st.metric("🌐 Internet en Hogares", f"{avg_internet:.1f}%")
            
            with col4:
                # Inversión pública promedio
                avg_inversion = filtered_df['INV_PUBLICA_PER_CAPITA'].mean()
                st.metric("💰 Inversión Pública/Persona", f"${avg_inversion:,.0f}")
            
            # Principales hallazgos
            st.markdown("### 🔍 Principales Hallazgos")
            
            findings = []
            
            # Hallazgo 1: Cobertura 4G
            if avg_4g > 70:
                findings.append(f"✅ **Buena cobertura 4G**: El {avg_4g:.1f}% de las localidades tiene cobertura 4G")
            else:
                findings.append(f"⚠️ **Cobertura 4G limitada**: Solo el {avg_4g:.1f}% de las localidades tiene cobertura 4G")
            
            # Hallazgo 2: Cobertura 5G
            if avg_5g > 5:
                findings.append(f"🚀 **Despliegue de 5G**: El {avg_5g:.1f}% de las localidades ya tiene cobertura 5G")
            else:
                findings.append(f"📱 **5G en desarrollo**: Solo el {avg_5g:.1f}% de las localidades tiene cobertura 5G")
            
            # Hallazgo 3: Brecha digital
            if avg_internet < 60:
                findings.append(f"⚠️ **Brecha digital**: Solo el {avg_internet:.1f}% de los hogares tiene acceso a Internet")
            else:
                findings.append(f"✅ **Buena penetración**: El {avg_internet:.1f}% de los hogares tiene acceso a Internet")
            
            # Hallazgo 4: Proveedores líderes
            top_provider = filtered_df['NOMBRE_PROVEEDOR_COMERCIAL'].value_counts().index[0]
            top_provider_count = filtered_df['NOMBRE_PROVEEDOR_COMERCIAL'].value_counts().iloc[0]
            findings.append(f"🏆 **Proveedor líder**: {top_provider} con {top_provider_count:,} registros")
            
            # Hallazgo 5: Departamentos con mejor cobertura
            dept_4g_coverage = filtered_df.groupby('DEPARTAMENTO').apply(lambda x: (x['COBERTURA_4G'] == 'SÍ').mean() * 100).sort_values(ascending=False)
            if len(dept_4g_coverage) > 0:
                best_dept = dept_4g_coverage.index[0]
                best_coverage = dept_4g_coverage.iloc[0]
                findings.append(f"🌟 **Mejor departamento**: {best_dept} con {best_coverage:.1f}% de cobertura 4G")
            
            for finding in findings:
                st.markdown(finding)
            
            # Recomendaciones
            st.markdown("### 💡 Recomendaciones")
            
            recommendations = [
                "🎯 **Priorizar despliegue 5G** en áreas urbanas de alto ingreso",
                "🌐 **Ampliar cobertura 4G** en zonas rurales y remotas",
                "📚 **Implementar programas de alfabetización digital** para reducir la brecha",
                "🤝 **Fomentar la competencia** entre proveedores para mejorar servicios",
                "💰 **Incentivar inversión** en infraestructura en departamentos con baja cobertura",
                "🏘️ **Enfocarse en cabeceras municipales** para máximo impacto"
            ]
            
            for rec in recommendations:
                st.markdown(rec)
            
            # Información adicional
            st.markdown("### 📈 Datos Adicionales")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Período de análisis:**")
                st.markdown(f"- Desde: {min(years)}")
                st.markdown(f"- Hasta: {max(years)}")
                st.markdown(f"- Total de años: {len(years)}")
                
                st.markdown("**Cobertura por tecnología:**")
                for tech, count in coverage_summary.items():
                    pct = (count/total_records)*100
                    st.markdown(f"- {tech}: {count:,} localidades ({pct:.1f}%)")
            
            with col2:
                st.markdown("**Indicadores socioeconómicos promedio:**")
                st.markdown(f"- Ingreso promedio: ${filtered_df['INGRESO_PROMEDIO_HOGAR'].mean():,.0f}")
                st.markdown(f"- Tasa de pobreza: {filtered_df['TASA_POBREZA'].mean():.1f}%")
                st.markdown(f"- Tasa de desempleo: {filtered_df['TASA_DESEMPLEO'].mean():.1f}%")
                st.markdown(f"- Hogares con Internet: {filtered_df['PCT_HOGARES_INTERNET'].mean():.1f}%")
                st.markdown(f"- Altitud promedio: {filtered_df['ALTITUD_MSNM'].mean():.0f} msnm")
                st.markdown(f"- Inversión pública: ${filtered_df['INV_PUBLICA_PER_CAPITA'].mean():,.0f} per cápita")

else:
    st.error("❌ No se pudieron cargar los datos. Por favor, verifica que el archivo CSV existe en la ubicación correcta.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 0.9rem;">
    📊 Dashboard de Cobertura Móvil Colombia | Desarrollado con Streamlit | Datos 2017-2024
</div>
""", unsafe_allow_html=True)