import streamlit as st
import pulp
import pandas as pd

# Configuración de página de Streamlit para presentación académica y limpia
st.set_page_config(page_title="Optimización del Plan de Medios", layout="centered")

st.title("📝 Optimización del Plan de Medios")
st.markdown("""
Esta aplicación utiliza programación lineal entera binaria para resolver el problema de selección de canales publicitarios. 
Permite determinar la combinación óptima de medios para maximizar el impacto publicitario total sin exceder el presupuesto disponible.
""")

# --- Barra lateral para parámetros del modelo ---
st.sidebar.header("⚙️ Parámetros de Optimización")

# Presupuesto general
presupuesto = st.sidebar.number_input("Presupuesto Disponible", min_value=1.0, value=9.0, step=1.0)

# Configuración de cada canal publicitario
st.sidebar.subheader("📺 Televisión (TV)")
costo_tv = st.sidebar.number_input("Costo - TV", min_value=0.0, value=8.0, step=0.5)
impacto_tv = st.sidebar.number_input("Impacto - TV", min_value=0.0, value=14.0, step=0.5)

st.sidebar.subheader("📻 Radio (R)")
costo_r = st.sidebar.number_input("Costo - Radio", min_value=0.0, value=3.0, step=0.5)
impacto_r = st.sidebar.number_input("Impacto - Radio", min_value=0.0, value=5.0, step=0.5)

st.sidebar.subheader("📱 Redes Sociales (RS)")
costo_rs = st.sidebar.number_input("Costo - Redes Sociales", min_value=0.0, value=4.0, step=0.5)
impacto_rs = st.sidebar.number_input("Impacto - Redes Sociales", min_value=0.0, value=7.0, step=0.5)

st.sidebar.subheader("📰 Prensa (P)")
costo_p = st.sidebar.number_input("Costo - Prensa", min_value=0.0, value=2.0, step=0.5)
impacto_p = st.sidebar.number_input("Impacto - Prensa", min_value=0.0, value=3.0, step=0.5)

# --- Resumen de Datos de Entrada en pantalla principal ---
st.subheader("📋 Parámetros de Entrada Cargados")
data_inicial = {
    "Canal": ["TV", "Radio", "Redes Sociales", "Prensa"],
    "Costo": [costo_tv, costo_r, costo_rs, costo_p],
    "Impacto": [impacto_tv, impacto_r, impacto_rs, impacto_p]
}
df_inicial = pd.DataFrame(data_inicial)
st.table(df_inicial.set_index("Canal"))

st.write(f"**Presupuesto total configurado:** {presupuesto}")

# --- Botón de Optimización ---
if st.button("🚀 Optimizar plan de medios", type="primary"):
    
    # 1. Definición del problema en PuLP
    prob = pulp.LpProblem("Plan_Medios_Optimo", pulp.LpMaximize)
    
    # 2. Definición de variables binarias
    x_tv = pulp.LpVariable('X_TV', cat='Binary')
    x_r = pulp.LpVariable('X_R', cat='Binary')
    x_rs = pulp.LpVariable('X_RS', cat='Binary')
    x_p = pulp.LpVariable('X_P', cat='Binary')
    
    # 3. Función Objetivo
    prob += (
        impacto_tv * x_tv + 
        impacto_r * x_r + 
        impacto_rs * x_rs + 
        impacto_p * x_p
    ), "Impacto_Total"
    
    # 4. Restricción de Presupuesto
    prob += (
        costo_tv * x_tv + 
        costo_r * x_r + 
        costo_rs * x_rs + 
        costo_p * x_p <= presupuesto
    ), "Restriccion_Presupuesto"
    
    # 5. Resolver el problema
    status = prob.solve()
    
    # Obtener valores de la resolución
    val_tv = int(x_tv.varValue) if x_tv.varValue is not None else 0
    val_r = int(x_r.varValue) if x_r.varValue is not None else 0
    val_rs = int(x_rs.varValue) if x_rs.varValue is not None else 0
    val_p = int(x_p.varValue) if x_p.varValue is not None else 0
    
    costo_total = (costo_tv * val_tv) + (costo_r * val_r) + (costo_rs * val_rs) + (costo_p * val_p)
    impacto_total = (impacto_tv * val_tv) + (impacto_r * val_r) + (impacto_rs * val_rs) + (impacto_p * val_p)
    presupuesto_restante = presupuesto - costo_total
    estado_sol = pulp.LpStatus[status]
    
    # --- Mostrar Resultados ---
    st.markdown("--- ")
    st.subheader("🏆 Resultados de la Optimización")
    
    if estado_sol == "Optimal":
        st.success(f"✅ Estado de la solución: **{estado_sol} (Óptima)**")
    else:
        st.warning(f"⚠️ Estado de la solución: **{estado_sol}**")
        
    # Métricas destacadas en columnas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Impacto Máximo Obtenido", f"{impacto_total:,.1f}")
    with col2:
        st.metric("Costo Total Plan", f"{costo_total:,.1f}")
    with col3:
        st.metric("Presupuesto Restante", f"{presupuesto_restante:,.1f}")
        
    # Clasificación de canales seleccionados vs no seleccionados
    canales_sel = []
    canales_no_sel = []
    
    if val_tv == 1: canales_sel.append("TV 📺") 
    else: canales_no_sel.append("TV 📺")
    
    if val_r == 1: canales_sel.append("Radio 📻") 
    else: canales_no_sel.append("Radio 📻")
    
    if val_rs == 1: canales_sel.append("Redes Sociales 📱") 
    else: canales_no_sel.append("Redes Sociales 📱")
    
    if val_p == 1: canales_sel.append("Prensa 📰") 
    else: canales_no_sel.append("Prensa 📰")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Canales Seleccionados:**")
        if canales_sel:
            for c in canales_sel:
                st.markdown(f"*   {c} (Variable = 1)")
        else:
            st.write("Ningún canal fue seleccionado.")
    with col_b:
        st.write("**Canales NO Seleccionados:**")
        if canales_no_sel:
            for c in canales_no_sel:
                st.markdown(f"*   {c} (Variable = 0)")
        else:
            st.write("Todos los canales fueron seleccionados.")
            
    # Tabla resumen final del estado óptimo
    st.markdown("#### Detalle Técnico del Plan Óptimo")
    df_resultado = pd.DataFrame({
        "Canal": ["TV", "Radio", "Redes Sociales", "Prensa"],
        "Costo": [costo_tv, costo_r, costo_rs, costo_p],
        "Impacto": [impacto_tv, impacto_r, impacto_rs, impacto_p],
        "Valor de Variable Binaria": [val_tv, val_r, val_rs, val_p],
        "Seleccionado": ["Sí" if val_tv == 1 else "No", 
                         "Sí" if val_r == 1 else "No", 
                         "Sí" if val_rs == 1 else "No", 
                         "Sí" if val_p == 1 else "No"]
    })
    st.dataframe(df_resultado.set_index("Canal"), use_container_width=True)
