import streamlit as st
from math import sqrt
from scipy.stats import norm, t, chi2

def calcular_intervalo_media(media, desviacion, muestra, nivel_confianza):
    z = norm.ppf(1 - (1 - nivel_confianza) / 2)
    error_estandar = desviacion / sqrt(muestra)
    margen_error = z * error_estandar
    return media - margen_error, media + margen_error

def calcular_intervalo_proporcion(exitos, muestra, nivel_confianza):
    proporcion = exitos / muestra
    z = norm.ppf(1 - (1 - nivel_confianza) / 2)
    error_estandar = sqrt((proporcion * (1 - proporcion)) / muestra)
    margen_error = z * error_estandar
    return proporcion, proporcion - margen_error, proporcion + margen_error

def calcular_intervalo_varianza(muestra, varianza_muestral, nivel_confianza):
    chi2_inf = chi2.ppf((1 - nivel_confianza) / 2, muestra - 1)
    chi2_sup = chi2.ppf(1 - (1 - nivel_confianza) / 2, muestra - 1)
    var_inf = (muestra - 1) * varianza_muestral / chi2_sup
    var_sup = (muestra - 1) * varianza_muestral / chi2_inf
    return var_inf, var_sup

st.title("Cálculo de Estimaciones Puntuales y por Intervalo")

# Menú principal
menu_principal = st.selectbox("Selecciona el tipo de estimación:", ["Estimación puntual", "Estimación por intervalo"])

if menu_principal == "Estimación puntual":
    st.subheader("Cálculo de estimaciones puntuales")
    tipo_estimacion = st.selectbox("¿Qué parámetro deseas estimar?", ["Media", "Proporción", "Varianza/Desviación estándar"])

    if tipo_estimacion == "Media":
        st.write("### Ejemplo: \nUn administrador quiere estimar el tiempo promedio de respuesta de un servidor. \nDe una muestra de 50 respuestas, la suma de los tiempos fue de 1000 ms. Calcula la estimación puntual de la media.")
        st.write("Introduce los datos para calcular la media:")
        suma_valores = st.number_input("Suma de los valores observados:", value=1000.0)
        cantidad_valores = st.number_input("Número de observaciones:", value=50, step=1)

        if st.button("Calcular media"):
            media = suma_valores / cantidad_valores
            st.success(f"La estimación puntual de la media es: {media:.2f}")

    elif tipo_estimacion == "Proporción":
        st.write("### Ejemplo: \nUn equipo de desarrollo realiza una encuesta para evaluar la satisfacción del cliente. \nDe 100 respuestas, 80 indicaron satisfacción. Calcula la proporción puntual.")
        st.write("Introduce los datos para calcular la proporción:")
        exitos = st.number_input("Número de éxitos:", value=80, step=1)
        muestra = st.number_input("Tamaño de la muestra:", value=100, step=1)

        if st.button("Calcular proporción"):
            proporcion = exitos / muestra
            st.success(f"La estimación puntual de la proporción es: {proporcion:.4f}")

    elif tipo_estimacion == "Varianza/Desviación estándar":
        st.write("### Ejemplo: \nUn analista financiero quiere estimar la variabilidad de los retornos de una acción. \nCon una muestra de 30 días, la suma de los cuadrados de las diferencias respecto a la media fue de 450. Calcula la varianza y desviación estándar puntuales.")
        st.write("Introduce los datos para calcular la varianza:")
        suma_cuadrados = st.number_input("Suma de los cuadrados de las diferencias respecto a la media:", value=450.0)
        muestra = st.number_input("Tamaño de la muestra:", value=30, step=1)

        if st.button("Calcular varianza y desviación estándar"):
            varianza = suma_cuadrados / (muestra - 1)
            desviacion_estandar = sqrt(varianza)
            st.success(f"La estimación puntual de la varianza es: {varianza:.2f}")
            st.success(f"La estimación puntual de la desviación estándar es: {desviacion_estandar:.2f}")

elif menu_principal == "Estimación por intervalo":
    st.subheader("Cálculo de estimaciones por intervalo")
    tipo_intervalo = st.selectbox("¿Qué intervalo deseas calcular?", ["Media", "Proporción", "Varianza"])

    if tipo_intervalo == "Media":
        st.write("### Ejemplo: \nUn administrador quiere estimar el tiempo promedio de respuesta de un servidor. \nDe una muestra de 50 respuestas, la media fue de 200 ms con una desviación estándar de 30 ms. Calcula el intervalo de confianza al 95%.")
        st.write("Introduce los datos para calcular el intervalo de confianza para la media:")
        media = st.number_input("Media muestral:", value=200.0)
        desviacion = st.number_input("Desviación estándar muestral:", value=30.0)
        muestra = st.number_input("Tamaño de la muestra:", value=50, step=1)
        nivel_confianza = st.slider("Nivel de confianza (%):", min_value=90, max_value=99, value=95) / 100

        if st.button("Calcular intervalo para la media"):
            limite_inferior, limite_superior = calcular_intervalo_media(media, desviacion, muestra, nivel_confianza)
            st.write(f"### Estimación puntual: {media:.2f}")
            st.success(f"Intervalo de confianza al {nivel_confianza * 100}%: [{limite_inferior:.2f}, {limite_superior:.2f}]")

    elif tipo_intervalo == "Proporción":
        st.write("### Ejemplo: \nUn equipo de desarrollo realiza una encuesta para evaluar la satisfacción del cliente. \nDe 100 respuestas, 80 indicaron satisfacción. Calcula la proporción puntual y su intervalo de confianza al 95%.")
        st.write("Introduce los datos para calcular el intervalo de confianza para la proporción:")
        exitos = st.number_input("Número de éxitos:", value=80, step=1)
        muestra = st.number_input("Tamaño de la muestra:", value=100, step=1)
        nivel_confianza = st.slider("Nivel de confianza (%):", min_value=90, max_value=99, value=95) / 100

        if st.button("Calcular intervalo para la proporción"):
            proporcion, limite_inferior, limite_superior = calcular_intervalo_proporcion(exitos, muestra, nivel_confianza)
            st.write(f"### Estimación puntual: {proporcion:.4f}")
            st.success(f"Intervalo de confianza al {nivel_confianza * 100}%: [{limite_inferior:.4f}, {limite_superior:.4f}]")

    elif tipo_intervalo == "Varianza":
        st.write("### Ejemplo: \nUn analista financiero quiere estimar la variabilidad de los retornos de una acción. \nCon una muestra de 30 días, la varianza muestral es de 25. Calcula el intervalo de confianza al 95%.")
        st.write("Introduce los datos para calcular el intervalo de confianza para la varianza:")
        varianza_muestral = st.number_input("Varianza muestral:", value=25.0)
        muestra = st.number_input("Tamaño de la muestra:", value=30, step=1)
        nivel_confianza = st.slider("Nivel de confianza (%):", min_value=90, max_value=99, value=95) / 100

        if st.button("Calcular intervalo para la varianza"):
            limite_inferior, limite_superior = calcular_intervalo_varianza(muestra, varianza_muestral, nivel_confianza)
            st.write(f"### Estimación puntual: {varianza_muestral:.2f}")
            st.success(f"Intervalo de confianza al {nivel_confianza * 100}%: [{limite_inferior:.2f}, {limite_superior:.2f}]")