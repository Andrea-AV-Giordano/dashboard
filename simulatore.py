import pandas as pd
import numpy as np


def variazione(x,y):
    variazione = np.random.uniform(x,y, 12)
    return variazione

x = np.random.randn(500)
y = np.random.randn(500)+1

PREZZO_GRANO = np.random.uniform(220,250,1).round(0)
PREZZO_RISO = np.random.uniform(350,380,1).round(0)
PREZZO_MAIS = np.random.uniform(200,280,1).round(0)



DATA = pd.date_range(start='1/1/2025', periods=12, freq='ME')


risorse_amb = pd.DataFrame({
        'energia': np.random.uniform(9500,15000, 12).round(1),
        'emissioni': np.random.uniform(5000,7000, 12).round(1),
},
    index=DATA
                           )

spese = pd.DataFrame({
    'manodopera': np.random.uniform(17000,20000, 12).round(1),
    'pesticidi': np.random.uniform(2000,2200, 12).round(1),
    'fertilizzanti': np.random.uniform(3000,3200, 12).round(1)

}, index=DATA)

temperatura =  (np.array([10, 14, 17, 19, 24, 28, 32, 33, 27, 23, 17, 10]) + variazione(-3,3)).round(1)
precipitazioni =  (np.array([55, 60, 70, 45, 35, 25, 15, 20, 40, 55, 60, 65]) + variazione(-3,3)).round(1)
soglia = 35  # percentuale sotto la quale consideri "stagione secca"

clima = pd.DataFrame({
 'temperatura':  temperatura,
 'precipitazioni': precipitazioni,
 'umidita' : np.add((precipitazioni)*0.6,(temperatura)*0.4),
 },
    index=DATA
                     )

   
colture = pd.DataFrame({
    'mais': np.random.uniform(80,100, 12).round(1),
    'riso': np.random.uniform(30,50, 12).round(1),
    'grano': np.random.uniform(40,60, 12).round(1),
 },
    index=DATA
)


sommaSpese = pd.DataFrame({
    'Spesa': ['Pesticidi', 'fertilizzanti', 'Manodopera', ],
        'Valore': [
            spese['pesticidi'].sum(),
            spese['fertilizzanti'].sum(),
            spese['manodopera'].sum()],
    
})
sommaColture = pd.DataFrame({
    'Coltura': ['Riso', 'Grano', 'Mais', ],
        'Valore': [
            colture['riso'].sum(),
            colture['grano'].sum(),
            colture['mais'].sum()],
})


df = spese.join(colture)




clima['umidita_normale'] = clima['umidita'].where(clima["umidita"] >= soglia )
clima['umidita_secca'] = clima['umidita'].where(clima["umidita"] < soglia)




df['valoreGrano'] = np.multiply(colture['grano'], PREZZO_GRANO).round(2)
df['valoreRiso']= np.multiply(colture['riso'], PREZZO_RISO).round(2)
df['valoreMais']= np.multiply(colture['mais'], PREZZO_MAIS).round(2)
df['totale'] =  ((df['valoreGrano'] + df['valoreMais'] + df['valoreRiso']) - (df['fertilizzanti'] + df['pesticidi'] + df['manodopera'])).round(2) 

temp = pd.DataFrame(df.filter(items=['valoreRiso', 'valoreGrano', 'valoreMais']))
filtro = (pd.DataFrame(temp.join(colture))).reset_index()
filtro['index']= filtro['index'].dt.strftime('%d-%m-%Y')

df = df.reset_index()
df['index'] = df['index'].dt.strftime('%d-%m-%Y')
df_dict = df.to_dict('records')

