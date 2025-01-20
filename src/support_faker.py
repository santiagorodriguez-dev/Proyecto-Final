# Importaciones
import pandas as pd # type: ignore
import time
import sys
sys.path.append("../")
from faker import Faker # type: ignore
from faker.providers import DynamicProvider # type: ignore

import os
import dotenv # type: ignore
import numpy as np # type: ignore
dotenv.load_dotenv()
from openai import OpenAI # type: ignore
import string
import random

def load_data_init_alumnos(num_registros: int = 10000):

    type_estudios = DynamicProvider(
     provider_name="estudios",
     elements=["Eso", "Bachillerato", "Grado Medio", "Grado Superior", "Licenciatura", "Grado", "Máster", "Doctorado"],
    )

    type_estudios_especialidad = DynamicProvider(
     provider_name="especialidad",
     elements=["Informatica", "Ingenieria", "Letras"],
    )
   
    fake = Faker('es_ES')
    Faker.seed(4321)
    fake.add_provider(type_estudios)
    fake.add_provider(type_estudios_especialidad)

    data = [
             { "nombre": fake.first_name(),
               "apellidos":  fake.last_name(),
               "email": fake.email(),
               "estudios": fake.estudios(),
               "especialidad": fake.especialidad(),
               "ciudad": fake.address().split('\n')[1].split(',')[0],
               "edad": np.random.randint(18, 45),
               "telefono": fake.phone_number(),
               "sexo": random.choices(['Hombre', 'Mujer'], weights=[0.5, 0.5], k=1)[0],
               "curso_01_fullstack": random.choices(['si', 'no'], weights=[0.5, 0.5], k=1)[0]
             }
             for i in range(num_registros)
         ]
    
    df = pd.DataFrame(data = data).drop_duplicates(subset=['email'], keep='first', inplace=False)

    return df


def load_data_init_leads(num_registros: int = 1000):

    type_estudios = DynamicProvider(
     provider_name="estudios",
     elements=["Eso", "Bachillerato", "Grado Medio", "Grado Superior", "Licenciatura", "Grado", "Máster", "Doctorado"],
    )

    type_estudios_especialidad = DynamicProvider(
     provider_name="especialidad",
     elements=["Informatica", "Ingenieria", "Letras"],
    )
   
    fake = Faker('es_ES')
    Faker.seed(8960)
    fake.add_provider(type_estudios)
    fake.add_provider(type_estudios_especialidad)

    data = [
             { "nombre": fake.first_name(),
               "apellidos":  fake.last_name(),
               "email": fake.email(),
               "estudios": fake.estudios(),
               "especialidad": fake.especialidad(),
               "telefono": fake.phone_number(),
               "sexo": random.choices(['Hombre', 'Mujer'], weights=[0.5, 0.5], k=1)[0]
             }
             for i in range(num_registros)
         ]
    
    df = pd.DataFrame(data = data).drop_duplicates(subset=['email'], keep='first', inplace=False)

    return df

def remove_duplicates(df_leads, df_alumnos):
    
    result = pd.merge(df_leads, df_alumnos, on=['email'], how='inner')

    for i in result['email']:
      df_leads = df_leads.loc[df_leads['email'] != i]
    
    for i in result['email']:
      df_alumnos = df_alumnos.loc[df_alumnos['email'] != i]

      df_leads = df_leads.replace(r'\n',  ' ', regex=True)
      df_alumnos = df_alumnos.replace(r'\n',  ' ', regex=True)

    return (df_leads, df_alumnos)




