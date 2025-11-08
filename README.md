# Dashboard de Cobertura Móvil Colombia

Este proyecto crea un dashboard interactivo en Streamlit para analizar la cobertura móvil en Colombia desde 2017 hasta 2024.

## 📊 Descripción

El dashboard analiza datos de cobertura móvil incluyendo:
- Cobertura por tecnología (2G, 3G, 4G, 5G)
- Análisis geográfico por departamentos y municipios
- Comparación entre proveedores
- Indicadores socioeconómicos
- Series de tiempo

## 🚀 Instalación

### Opción 1: Usar Python instalado
1. Instala Python desde [python.org](https://www.python.org/downloads/)
2. Abre una terminal/Command Prompt
3. Navega a la carpeta del proyecto:
   ```bash
   cd "e:\Talentos Tech\streamlit"
   ```
4. Instala las dependencias:
   ```bash
   pip install streamlit pandas numpy matplotlib seaborn
   ```

### Opción 2: Usar Anaconda
1. Instala Anaconda desde [anaconda.com](https://www.anaconda.com/products/individual)
2. Abre Anaconda Prompt
3. Navega a la carpeta del proyecto:
   ```bash
   cd "e:\Talentos Tech\streamlit"
   ```
4. Instala las dependencias:
   ```bash
   conda install streamlit pandas numpy matplotlib seaborn
   ```

## 📋 Archivos del Proyecto

- `cobertura_colombia_2017_2024_limpio_V2.csv` - Datos de cobertura móvil
- `dashboard_simple.py` - Dashboard simplificado
- `dashboard_cobertura.py` - Dashboard completo (requiere más dependencias)
- `requirements.txt` - Lista de dependencias

## 🎯 Ejecución

### Dashboard Simplificado (Recomendado)
```bash
streamlit run dashboard_simple.py
```

### Dashboard Completo
```bash
streamlit run dashboard_cobertura.py
```

## 📈 Características

### Dashboard Simplificado:
- ✅ Análisis de cobertura por tecnología
- ✅ Visualizaciones geográficas
- ✅ Comparación de proveedores
- ✅ Indicadores socioeconómicos
- ✅ Series de tiempo
- ✅ Filtros interactivos
- ✅ Resumen ejecutivo

### Dashboard Completo:
- ✅ Todas las características del simplificado
- ✅ Gráficos más avanzados con Plotly
- ✅ Interacciones adicionales
- ✅ Visualizaciones mejoradas

## 🔧 Solución de Problemas

### Error: "pip no reconocido"
- Asegúrate de que Python esté instalado
- Usa `py -m pip install` en lugar de `pip install`
- En Anaconda, usa `conda install` en lugar de `pip install`

### Error: "streamlit no reconocido"
- Asegúrate de que Streamlit esté instalado
- Prueba `python -m streamlit run dashboard_simple.py`
- O `py -m streamlit run dashboard_simple.py`

### Error: "No se encuentra el archivo CSV"
- Verifica que `cobertura_colombia_2017_2024_limpio_V2.csv` esté en la misma carpeta
- Asegúrate de tener permisos de lectura

## 📊 Estructura de Datos

El archivo CSV contiene columnas como:
- `AÑO`, `TRIMESTRE` - Información temporal
- `DEPARTAMENTO`, `MUNICIPIO` - Información geográfica
- `NOMBRE_PROVEEDOR_COMERCIAL` - Proveedor de servicios
- `COBERTURA_2G`, `COBERTURA_3G`, `COBERTURA_4G`, `COBERTURA_5G` - Cobertura por tecnología
- `INGRESO_PROMEDIO_HOGAR`, `TASA_POBREZA` - Indicadores socioeconómicos

## 🎨 Personalización

Puedes personalizar el dashboard:
- Modificar colores en los gráficos
- Agregar nuevos filtros
- Añadir más visualizaciones
- Cambiar el diseño

## 📞 Soporte

Si encuentras problemas:
1. Verifica que Python esté correctamente instalado
2. Asegúrate de tener todas las dependencias
3. Comprueba que el archivo CSV esté en la ubicación correcta
4. Prueba con el dashboard simplificado primero

## 📝 Licencia

Este proyecto es de código abierto y está disponible para uso educativo y análisis de datos.