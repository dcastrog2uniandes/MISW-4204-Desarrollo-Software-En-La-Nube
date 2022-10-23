''' Para la ejecución de este script de análisis (que no hace parte funcional de la aplicación) se requiere instalar las librerías panas y matplotlib'''

import pandas as pd
from matplotlib import pyplot as plt
f = open("logArchiv.txt", "r").read()
datos = f.split('\n')
print(len(datos))
df = pd.DataFrame([{'archivo': i.split(' hora:')[0].split(': ')[-1].split('/')[-1].split('.')[0], 
                      'hora': i.split('hora:  ')[-1].split(' archivo')[0]
                     } for i in datos])
df.hora = pd.to_datetime(df.hora)
df['tProceso'] = (df.hora - df.hora.shift()).astype('timedelta64[ms]')/1000
plt.figure(figsize=(10, 6), dpi=80)
df.tProceso.plot()
plt.title('Tiempo de procesamiento: escenario 2')
plt.xlabel('n_archivos')
plt.ylabel('tiempo de proceso (s)')

pd.DataFrame(df.tProceso.describe())