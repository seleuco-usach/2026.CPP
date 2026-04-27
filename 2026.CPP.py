import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
from gspread_dataframe import set_with_dataframe

# Configurar el alcance y credenciales
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/xenomorfo/Descargas/bamboo-sweep-465617-i4-06b9bd6f36a5.json', scope)
client = gspread.authorize(credentials)
#jose-hoyos-usach-cl@bamboo-sweep-465617-i4.iam.gserviceaccount.com 
#https://docs.google.com/spreadsheets/d/17LhWP9zmDMxmyqkmlB-PTc8kf7_p6LcFHdCGAhEvi9E/edit?gid=1818427118#gid=1818427118
# Abrir la hoja de cálculo por ID
spreadsheet = client.open_by_key('17LhWP9zmDMxmyqkmlB-PTc8kf7_p6LcFHdCGAhEvi9E')
# Abrir la hoja de cálculo por ID


CPP_DR = (
gspread.authorize(credentials)
.open_by_key('17LhWP9zmDMxmyqkmlB-PTc8kf7_p6LcFHdCGAhEvi9E')
.get_worksheet(0)
.get_all_values()
# índice 0 es la primera hoja
)

CPP_DR = pd.DataFrame(CPP_DR[1:], columns=CPP_DR[0])

CPP_DR['ANHO_PLAN'] = CPP_DR['ANHO'] +'-'+ CPP_DR['COD_PLAN2']
CPP_DR['ANHO_SIES'] = CPP_DR['ANHO'] +'-'+ CPP_DR['SIES']


CPP_CARO = (
gspread.authorize(credentials)
.open_by_key('17LhWP9zmDMxmyqkmlB-PTc8kf7_p6LcFHdCGAhEvi9E')
.worksheet("CPP_CARO_2")
.get_all_values()
# índice 0 es la primera hoja
)
CPP_CARO = pd.DataFrame(CPP_CARO[2:], columns=CPP_CARO[0])

CPP_DR['ANHO_PLAN'].astype(str)
CPP_CARO['ANHO_PLAN'].astype(str)

CPP_DR.drop_duplicates()

CPP_DR.to_csv("CPP_DR.csv", index=False)
