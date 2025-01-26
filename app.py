import streamlit as st
from math import sqrt
from scipy.stats import norm

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

st.title("Cálculo de Estimaciones Puntuales e Intervalos de Confianza")

opcion = st.selectbox("Selecciona el tipo de estimación:", ["Media", "Proporción"])

if opcion == "Media":
    st.write("### Ejemplo: Tiempo promedio de respuesta de un servidor")
    st.write("Un administrador quiere estimar el tiempo promedio de respuesta de un servidor. De una muestra de 50 respuestas, la media fue de 200 ms con una desviación estándar de 30 ms. Calcule el intervalo de confianza al 95%.")

    media = st.number_input("Introduce la media (\u03BC):", value=200.0)
    desviacion = st.number_input("Introduce la desviación estándar (\u03C3):", value=30.0)
    muestra = st.number_input("Introduce el tamaño de la muestra (n):", value=50, step=1)
    nivel_confianza = st.slider("Nivel de confianza (%):", min_value=90, max_value=99, value=95) / 100

    if st.button("Calcular intervalo para la media"):
        limite_inferior, limite_superior = calcular_intervalo_media(media, desviacion, muestra, nivel_confianza)
        st.write(f"### Estimación puntual: {media:.2f} ms")
        st.success(f"Intervalo de confianza al {nivel_confianza * 100}%: [{limite_inferior:.2f}, {limite_superior:.2f}] ms")

elif opcion == "Proporción":
    st.write("### Ejemplo: Proporción de solicitudes exitosas")
    st.write("Supongamos que un administrador desea estimar la proporción de solicitudes exitosas a un servidor. De 100 solicitudes, 80 fueron exitosas. Estime el intervalo de confianza al 95% para esta proporción.")

    exitos = st.number_input("Introduce el número de éxitos (x):", value=80, step=1)
    muestra = st.number_input("Introduce el tamaño de la muestra (n):", value=100, step=1)
    nivel_confianza = st.slider("Nivel de confianza (%):", min_value=90, max_value=99, value=95) / 100

    if st.button("Calcular intervalo para la proporción"):
        proporcion, limite_inferior, limite_superior = calcular_intervalo_proporcion(exitos, muestra, nivel_confianza)
        st.write(f"### Estimación puntual: {proporcion:.4f}")
        st.success(f"Intervalo de confianza al {nivel_confianza * 100}%: [{limite_inferior:.4f}, {limite_superior:.4f}]")