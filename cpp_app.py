import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

tabla_cpp = pd.read_csv("CPP_DR.csv")

tabla_cpp = tabla_cpp.drop_duplicates()

st.title("CPP 2026 - Planes de estudios")

tabla_cpp['nivel_global'] = np.where(tabla_cpp['COD_CARRERA']=="UNICIT", "UNICIT",
    np.where(tabla_cpp['COD_CARRERA']=="MIDA", "MAGISTER",
    np.where(tabla_cpp['COD_CARRERA'].str[0:3]=="MAG","MAGISTER", 
    np.where(tabla_cpp['COD_CARRERA'].str[0:3]=="DOC","DOCTORADO",
    np.where(tabla_cpp['COD_CARRERA'].str[0:3]=="DIP","DIPLOMADO",
    np.where(tabla_cpp['COD_CARRERA'].str[0:3]=="POS","POSTITUTLO","PREGRADO"))))))

#tabla_cpp.columns
tabla_cpp=tabla_cpp[['ID', 
           'ANHO_SIES',
           'COD_PLAN', 
           'ANHO_PLAN',
           'nivel_global',
           'SIES',
           'PLAN_NOMBRE',
           'COD_CARRERA',
           'COD_FAC',
           'FACULTAD',
           'COD_DEPTO_2_CR', 
           'nombre_depto_cr']]




tabla_cpp['COD_PLAN'] = tabla_cpp['COD_PLAN'].astype(str)
tabla_cpp['FACULTAD'] = tabla_cpp['FACULTAD'].replace("Facultad de ", "", regex=True)
tabla_cpp['COD_PLAN_NOMBRE'] = tabla_cpp['COD_PLAN'].astype(str) +"-"+ tabla_cpp['PLAN_NOMBRE']


st.set_page_config(layout="wide")

programas = pd.DataFrame(tabla_cpp['COD_PLAN'].unique()).dropna()
programas_nombre = pd.DataFrame(tabla_cpp['COD_PLAN_NOMBRE'].unique()).dropna()
FACULTAD = pd.DataFrame(tabla_cpp['FACULTAD'].unique()).dropna()



#prog_sel = st.multiselect("Selecciona programa:", programas, default=programas)
#fac_sel = st.multiselect("Selecciona carrera:", FACULTAD, default=FACULTAD)

seleccion = st.multiselect("Selecciona facultad:", 
                                   tabla_cpp['FACULTAD'].unique(), 
                                   default=FACULTAD)

if seleccion:
    tabla_filtrada = tabla_cpp[tabla_cpp['FACULTAD'].isin(seleccion)]
else:    
    tabla_filtrada = tabla_cpp
    
    
seleccion_car = st.multiselect("Selecciona nivel:", 
                               tabla_filtrada['nivel_global'].unique(), 
                               default=tabla_filtrada['nivel_global'].unique())



if seleccion:
    tabla_filtrada_niv = tabla_filtrada[tabla_filtrada['nivel_global'].isin(seleccion_car)]
else:    
    tabla_filtrada_niv = tabla_cpp

#tabla_filtrada_2 = tabla_cpp[tabla_cpp['FACULTAD'].isin(seleccion)]

#tabla_ret_largo_filtrado_carr=tabla_ret_largo_carr[(tabla_ret_largo_carr['CODIGO_CARRERA_x']==ret_sel_carr)]

#tabla_cpp['COD_PLAN'].isin(seleccion).unique()
#dsdshghgh

sel=st.selectbox("Selecciona el programa a visualizar:", 
         list(tabla_filtrada_niv['COD_PLAN_NOMBRE'].unique()), 
         index=None, 
         placeholder="selecciona programa")

tabla_filtrada_2=tabla_cpp[(tabla_cpp['COD_PLAN_NOMBRE']==sel)]

sel_2=st.selectbox("Selecciona el código SIES a visualizar:", 
         list(tabla_filtrada_2['SIES'].unique()))

tabla_filtrada_3=tabla_cpp[(tabla_cpp['COD_PLAN_NOMBRE']==sel) & 
                           (tabla_cpp['SIES']==sel_2) & 
                           (tabla_cpp['FACULTAD'].isin(seleccion))]


    

if not sel:
    tabla_final = tabla_filtrada_niv
else:
    tabla_final = tabla_filtrada_3
    
tab1, tab2 = st.tabs(["programas planes", "estadístcias cpp"])

with tab1:
    st.dataframe(tabla_final, use_container_width=True)


#if sel != "TODOS":
 #   tabla_cpp[tabla_cpp['COD_PLAN']==sel]

#if sel_2:
 #   tabla_cpp[tabla_cpp['SIES']==sel_2]
    
#if len(seleccion) > 0:
 #   tabla_cpp[tabla_cpp['FACULTAD'].isin(seleccion)]

#st.write(tabla_filtrada_3['COD_PLAN'].value_counts())
#st.write("se cuentan " + str(len(tabla_filtrada_3['SIES'])) + " registros de este programa")

facultad_sel = tabla_filtrada_3['FACULTAD'].unique()
depto_sel = tabla_filtrada_3['nombre_depto_cr'].unique()

st.info(f"Se cuentan {len(tabla_filtrada_3)} registros de este programa")
st.info(f"programa pertenece a {', '.join(facultad_sel)} del {', '.join(depto_sel)} ")



#tabla_filtrada
#tabla_filtrada_2
