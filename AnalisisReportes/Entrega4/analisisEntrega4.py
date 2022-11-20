import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_excel('informe.xlsx').rename(columns = {'Clase de almacenamiento':'hora'}).sort_values('hora').reset_index()
df['tProceso'] = (df.hora - df.hora.shift()).astype('timedelta64[ms]')/1000
plt.figure(figsize=(10, 6), dpi=80)
df.tProceso.plot(ylim=(0))
plt.title('Tiempo de procesamiento: escenario 2')
plt.xlabel('n_archivos')
plt.ylabel('tiempo de proceso (s)')


print('Se tiene un tiempo medio de procesamiento de {:.1f}s, con desviación de {:.1f}s. Esto equivale a {:.1f} archivos por minuto'.format(df.tProceso.mean(), df.tProceso.std(), 60/df.tProceso.mean()))
pd.DataFrame(df.tProceso.describe())