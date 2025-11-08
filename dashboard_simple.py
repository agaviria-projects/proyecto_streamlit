import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Cobertura Móvil Colombia 2017-2024",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("📱 Dashboard de Cobertura Móvil en Colombia 2017-2024")
st.markdown("Análisis integral de la cobertura de telecomunicaciones móviles en Colombia")

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
    
    # Filtro de año
    years = sorted(df['AÑO'].unique())
    selected_years = st.sidebar.multiselect(
        "Seleccionar Años:",
        years,
        default=years
    )
    
    # Filtro de departamento
    departments = sorted(df['DEPARTAMENTO'].unique())
    selected_departments = st.sidebar.multiselect(
        "Seleccionar Departamentos:",
        departments,
        default=departments[:5] if len(departments) > 5 else departments
    )
    
    # Filtro de proveedor
    providers = sorted(df['NOMBRE_PROVEEDOR_COMERCIAL'].unique())
    selected_providers = st.sidebar.multiselect(
        "Seleccionar Proveedores:",
        providers,
        default=providers
    )
    
    # Filtrar datos
    filtered_df = df[
        (df['AÑO'].isin(selected_years)) &
        (df['DEPARTAMENTO'].isin(selected_departments)) &
        (df['NOMBRE_PROVEEDOR_COMERCIAL'].isin(selected_providers))
    ]
    
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
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Cobertura", 
        "🗺️ Geografía", 
        "🏢 Proveedores",
        "💰 Socioeconomía", 
        "📅 Series Tiempo"
    ])
    
    with tab1:
        st.header("📈 Análisis de Cobertura por Tecnología")
        
        # Calcular cobertura por tecnología
        coverage_cols = ['COBERTURA_2G', 'COBERTURA_3G', 'COBERTURA_4G', 'COBERTURA_5G']
        coverage_summary = {}
        
        for col in coverage_cols:
            coverage_summary[col.replace('COBERTURA_', '')] = (filtered_df[col] == 'SÍ').sum()
        
        # Gráfico de barras
        fig, ax = plt.subplots(figsize=(10, 6))
        technologies = list(coverage_summary.keys())
        counts = list(coverage_summary.values())
        
        bars = ax.bar(technologies, counts, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        ax.set_title('Cobertura por Tecnología (Total de Localidades)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Tecnología')
        ax.set_ylabel('Número de Localidades')
        
        # Añadir valores en las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height):,}', ha='center', va='bottom')
        
        st.pyplot(fig)
        
        # Porcentajes
        st.subheader("📊 Porcentaje de Cobertura")
        total_locations = len(filtered_df)
        
        col1, col2, col3, col4 = st.columns(4)
        for i, (tech, count) in enumerate(coverage_summary.items()):
            pct = (count/total_locations)*100
            if i == 0:
                col1.metric(f"📡 {tech}", f"{pct:.1f}%")
            elif i == 1:
                col2.metric(f"📶 {tech}", f"{pct:.1f}%")
            elif i == 2:
                col3.metric(f"🚀 {tech}", f"{pct:.1f}%")
            else:
                col4.metric(f"⚡ {tech}", f"{pct:.1f}%")
    
    with tab2:
        st.header("🗺️ Análisis Geográfico")
        
        # Top departamentos
        dept_counts = filtered_df['DEPARTAMENTO'].value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(range(len(dept_counts)), dept_counts.values, color='skyblue')
        ax.set_title('Top 10 Departamentos por Número de Registros', fontsize=14, fontweight='bold')
        ax.set_xlabel('Departamento')
        ax.set_ylabel('Número de Registros')
        ax.set_xticks(range(len(dept_counts)))
        ax.set_xticklabels(dept_counts.index, rotation=45, ha='right')
        
        # Añadir valores
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height):,}', ha='center', va='bottom')
        
        st.pyplot(fig)
        
        # Análisis por cabecera municipal
        cabecera_analysis = filtered_df['CABECERA_MUNICIPAL'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(cabecera_analysis.values, labels=cabecera_analysis.index, autopct='%1.1f%%', startangle=90)
        ax.set_title('Distribución: Cabecera vs No Cabecera', fontsize=14, fontweight='bold')
        st.pyplot(fig)
    
    with tab3:
        st.header("🏢 Análisis por Proveedor")
        
        # Distribución de registros por proveedor
        provider_counts = filtered_df['NOMBRE_PROVEEDOR_COMERCIAL'].value_counts()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(range(len(provider_counts)), provider_counts.values, color='lightgreen')
        ax.set_title('Número de Registros por Proveedor', fontsize=14, fontweight='bold')
        ax.set_xlabel('Proveedor')
        ax.set_ylabel('Número de Registros')
        ax.set_xticks(range(len(provider_counts)))
        ax.set_xticklabels(provider_counts.index, rotation=45, ha='right')
        
        # Añadir valores
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height):,}', ha='center', va='bottom')
        
        st.pyplot(fig)
    
    with tab4:
        st.header("💰 Análisis Socioeconómico")
        
        # Ingreso promedio por departamento
        ingreso_dept = filtered_df.groupby('DEPARTAMENTO')['INGRESO_PROMEDIO_HOGAR'].mean().sort_values(ascending=False).head(10)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(range(len(ingreso_dept)), ingreso_dept.values, color='gold')
        ax.set_title('Top 10 Departamentos por Ingreso Promedio', fontsize=14, fontweight='bold')
        ax.set_xlabel('Departamento')
        ax.set_ylabel('Ingreso Promedio')
        ax.set_xticks(range(len(ingreso_dept)))
        ax.set_xticklabels(ingreso_dept.index, rotation=45, ha='right')
        
        # Añadir valores
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${int(height):,}', ha='center', va='bottom')
        
        st.pyplot(fig)
        
        # Tasa de pobreza
        pobreza_dept = filtered_df.groupby('DEPARTAMENTO')['TASA_POBREZA'].mean().sort_values(ascending=False).head(10)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(range(len(pobreza_dept)), pobreza_dept.values, color='salmon')
        ax.set_title('Top 10 Departamentos con Mayor Tasa de Pobreza', fontsize=14, fontweight='bold')
        ax.set_xlabel('Tasa de Pobreza (%)')
        ax.set_ylabel('Departamento')
        ax.set_yticks(range(len(pobreza_dept)))
        ax.set_yticklabels(pobreza_dept.index)
        
        # Añadir valores
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f'{width:.1f}%', ha='left', va='center')
        
        st.pyplot(fig)
    
    with tab5:
        st.header("📅 Análisis de Series de Tiempo")
        
        # Evolución por año
        yearly_data = filtered_df.groupby('AÑO').agg({
            'INGRESO_PROMEDIO_HOGAR': 'mean',
            'TASA_POBREZA': 'mean',
            'PCT_HOGARES_INTERNET': 'mean'
        }).reset_index()
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12))
        
        # Ingreso promedio
        ax1.plot(yearly_data['AÑO'], yearly_data['INGRESO_PROMEDIO_HOGAR'], marker='o', color='blue', linewidth=2)
        ax1.set_title('Evolución del Ingreso Promedio por Año', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Ingreso Promedio')
        ax1.grid(True, alpha=0.3)
        
        # Tasa de pobreza
        ax2.plot(yearly_data['AÑO'], yearly_data['TASA_POBREZA'], marker='s', color='red', linewidth=2)
        ax2.set_title('Evolución de la Tasa de Pobreza por Año', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Tasa de Pobreza (%)')
        ax2.grid(True, alpha=0.3)
        
        # Hogares con Internet
        ax3.plot(yearly_data['AÑO'], yearly_data['PCT_HOGARES_INTERNET'], marker='^', color='green', linewidth=2)
        ax3.set_title('Evolución del % de Hogares con Internet por Año', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Año')
        ax3.set_ylabel('% Hogares con Internet')
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    # Resumen ejecutivo
    st.header("📋 Resumen Ejecutivo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_4g = (filtered_df['COBERTURA_4G'] == 'SÍ').mean() * 100
        st.metric("📡 Cobertura 4G", f"{avg_4g:.1f}%")
    
    with col2:
        avg_5g = (filtered_df['COBERTURA_5G'] == 'SÍ').mean() * 100
        st.metric("🚀 Cobertura 5G", f"{avg_5g:.1f}%")
    
    with col3:
        avg_internet = filtered_df['PCT_HOGARES_INTERNET'].mean()
        st.metric("🌐 Internet Hogares", f"{avg_internet:.1f}%")
    
    # Principales hallazgos
    st.subheader("🔍 Principales Hallazgos")
    
    findings = []
    
    if avg_4g > 70:
        findings.append(f"✅ Buena cobertura 4G: El {avg_4g:.1f}% de las localidades tiene cobertura 4G")
    else:
        findings.append(f"⚠️ Cobertura 4G limitada: Solo el {avg_4g:.1f}% de las localidades tiene cobertura 4G")
    
    if avg_5g > 5:
        findings.append(f"🚀 Despliegue de 5G: El {avg_5g:.1f}% de las localidades ya tiene cobertura 5G")
    else:
        findings.append(f"📱 5G en desarrollo: Solo el {avg_5g:.1f}% de las localidades tiene cobertura 5G")
    
    if avg_internet < 60:
        findings.append(f"⚠️ Brecha digital: Solo el {avg_internet:.1f}% de los hogares tiene acceso a Internet")
    else:
        findings.append(f"✅ Buena penetración: El {avg_internet:.1f}% de los hogares tiene acceso a Internet")
    
    # Proveedor líder
    top_provider = filtered_df['NOMBRE_PROVEEDOR_COMERCIAL'].value_counts().index[0]
    top_provider_count = filtered_df['NOMBRE_PROVEEDOR_COMERCIAL'].value_counts().iloc[0]
    findings.append(f"🏆 Proveedor líder: {top_provider} con {top_provider_count:,} registros")
    
    for finding in findings:
        st.markdown(finding)
    
    # Recomendaciones
    st.subheader("💡 Recomendaciones")
    
    recommendations = [
        "🎯 Priorizar despliegue 5G en áreas urbanas de alto ingreso",
        "🌐 Ampliar cobertura 4G en zonas rurales y remotas",
        "📚 Implementar programas de alfabetización digital",
        "🤝 Fomentar la competencia entre proveedores",
        "💰 Incentivar inversión en infraestructura"
    ]
    
    for rec in recommendations:
        st.markdown(rec)

else:
    st.error("❌ No se pudieron cargar los datos. Por favor, verifica que el archivo CSV existe.")

# Footer
st.markdown("---")
st.markdown("📊 Dashboard de Cobertura Móvil Colombia | Desarrollado con Streamlit | Datos 2017-2024")