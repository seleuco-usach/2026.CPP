import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

tabla_cpp = pd.read_csv("CPP_DR.csv")

tabla_cpp = tabla_cpp.drop_duplicates()

st.title("CPP 2026 - Planes de estudio")

#tabla_cpp.columns
tabla_cpp=tabla_cpp[['ID', 
           'ANHO_SIES',
           'COD_PLAN', 
           'ANHO_PLAN', 
           'SIES',
           'PLAN_NOMBRE',
           'COD_CARRERA',
           'COD_FAC',
           'FACULTAD',
           'COD_DEPTO_2_CR', 
           'nombre_depto_cr']]



tabla_cpp['COD_PLAN'] = tabla_cpp['COD_PLAN'].astype(str)

st.set_page_config(layout="wide")

programas = pd.DataFrame(tabla_cpp['COD_PLAN'].unique()).dropna()
FACULTAD = pd.DataFrame(tabla_cpp['FACULTAD'].unique()).dropna()

#prog_sel = st.multiselect("Selecciona programa:", programas, default=programas)
#fac_sel = st.multiselect("Selecciona carrera:", FACULTAD, default=FACULTAD)

#seleccion = st.multiselect("Selecciona facultad:", tabla_cpp['FACULTAD'].unique(), default=FACULTAD)

#tabla_filtrada_2 = tabla_cpp[tabla_cpp['FACULTAD'].isin(seleccion)]

#tabla_ret_largo_filtrado_carr=tabla_ret_largo_carr[(tabla_ret_largo_carr['CODIGO_CARRERA_x']==ret_sel_carr)]

sel=st.selectbox("Selecciona el programa a visualizar:", 
         list(tabla_cpp['COD_PLAN'].unique()))



tabla_filtrada_2=tabla_cpp[(tabla_cpp['COD_PLAN']==sel)]

sel_2=st.selectbox("Selecciona el código SIES a visualizar:", 
         list(tabla_filtrada_2['SIES'].unique()))

tabla_filtrada_3=tabla_cpp[(tabla_cpp['COD_PLAN']==sel) & (tabla_cpp['SIES']==sel_2)]

if sel == "TODOS":
    tabla_cpp
else:
    tabla_filtrada_3

#tabla_filtrada
#tabla_filtrada_2
