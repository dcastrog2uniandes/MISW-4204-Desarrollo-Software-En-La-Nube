import pandas as pd
from matplotlib import pyplot as plt


df = pd.read_csv('logsGCS_experimento2.csv', index=False)
plt.figure(figsize=(10, 6), dpi=80)
df.tProceso.plot(ylim=(0))
plt.title('Tiempo de procesamiento: escenario 2')
plt.xlabel('n_archivos')
plt.ylabel('tiempo de proceso (s)')


print('Se tiene un tiempo medio de procesamiento de {:.1f}s, con desviación de {:.1f}s. Esto equivale a {:.1f} archivos por minuto'.format(df.tProceso.mean(), df.tProceso.std(), 60/df.tProceso.mean()))
pd.DataFrame(df.tProceso.describe())