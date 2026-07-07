import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

@st.cache_data
def cargar_cpp():
    tabla_cpp = pd.read_csv("CPP_DR.csv")
    tabla_cpp = tabla_cpp.drop_duplicates()
    return tabla_cpp

tabla_cpp = cargar_cpp()

from io import BytesIO
import requests
import pandas as pd

@st.cache_data
def cargar_oferta():
    oa_usach = pd.read_excel("OA_2026.xlsx")
    return oa_usach
# def cargar_oferta():
#     oa_2026 = "https://mifuturo.cl/wp-content/uploads/2026/01/Oferta_Academica_2010_al_2026_SIES_12_01_2026_WEB_E.zip"
#     result = requests.get(oa_2026)
#     oa_histo = pd.read_csv(BytesIO(result.content),compression='zip', 
#                      header=0, sep=';', 
#                      quotechar='"', 
#                      encoding='latin-1')
#     return oa_histo



oa_usach = cargar_oferta()
#oa_2026 = "https://mifuturo.cl/wp-content/uploads/2026/01/Oferta_Academica_2010_al_2026_SIES_12_01_2026_WEB_E.zip"

# result = requests.get(oa_2026)
# oa_histo = pd.read_csv(BytesIO(result.content),compression='zip', 
#                  header=0, sep=';', 
#                  quotechar='"', 
#                  encoding='latin-1')



#oa_usach = oa_histo[oa_histo['Código IES']==71]
oa_usach['Año'] = oa_usach['Año'].str.replace("OFE_", "", regex=False)

oa_usach_col = oa_usach[['Año','Código Único','Código Carrera','Vigencia']]

oa_usach_col['id'] = oa_usach_col['Año'] +'-'+ oa_usach_col['Código Único']

oa_usach_col.drop(columns=['Año','Código Único'], inplace=True)

st.title("CPP 2026 - Planes de estudios")

tabla_cpp = tabla_cpp.merge(oa_usach_col[['id','Vigencia']], left_on='ANHO_SIES', right_on='id', how='left')

tabla_cpp['nivel_global'] = np.where(tabla_cpp['COD_CARRERA']=="UNICIT", "UNICIT",
    np.where(tabla_cpp['COD_CARRERA']=="MIDA", "MAGISTER",
    np.where(tabla_cpp['COD_CARRERA'].str[0:3]=="MAG","MAGISTER", 
    np.where(tabla_cpp['COD_CARRERA'].str[0:3]=="DOC","DOCTORADO",
    np.where(tabla_cpp['COD_CARRERA'].str[0:3]=="DIP","DIPLOMADO",
    np.where(tabla_cpp['COD_CARRERA'].str[0:3]=="POS","POSTITULO","PREGRADO"))))))

#tabla_cpp.columnsD
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
           'nombre_depto_cr', 'Vigencia']]




tabla_cpp['COD_PLAN'] = tabla_cpp['COD_PLAN'].astype(str)
tabla_cpp['FACULTAD'] = tabla_cpp['FACULTAD'].replace("Facultad de ", "", regex=True)
tabla_cpp['COD_PLAN_NOMBRE'] = tabla_cpp['COD_PLAN'].astype(str) +"-"+ tabla_cpp['PLAN_NOMBRE']

tabla_cpp['COD_PLAN_NOMBRE'] = tabla_cpp['COD_PLAN_NOMBRE'].str.strip()

reemplazos = {"Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U"}

tabla_cpp['COD_PLAN_NOMBRE'] = tabla_cpp['COD_PLAN_NOMBRE'].replace(reemplazos, regex=True)
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
    
tab1, tab2, tab3 = st.tabs(["programas planes", "estadístcias cpp", "Oferta académica"])

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

st.info(f"Se cuentan {len(tabla_filtrada_niv)} registros")
st.info(f"Se cuentan {len(tabla_filtrada_niv['COD_PLAN'].drop_duplicates())} planes únicos")
st.info(f"Se cuentan {len(tabla_filtrada_3)} registros de este programa")
st.info(f"programa pertenece a {', '.join(facultad_sel)} del {', '.join(depto_sel)} ")


#tabla_filtrada
#tabla_filtrada_2

with tab3:
    st.dataframe(oa_usach_col, use_container_width=True)