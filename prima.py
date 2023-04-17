import streamlit as st


import pandas as pd
import numpy as np
#import yfinance as yf

import datetime


import matplotlib.pyplot as plt

#from full_fred.fred import Fred

#from fredapi import Fred
from PIL import Image

#st.pyplot(fig)
tab1,tab2,tab3,tab4 = st.tabs(["Intro","Modello Settoriale", "Metodologia AMC", "Backtest"])

with tab1:

    #altri_asset = st.file_uploader("altri_assets.xlsx")
    #dati = st.file_uploader("settori.xlsx")


    altri_asset = pd.read_excel("AMC/altri_assets.xlsx", index_col = 0)
    dati = pd.read_excel("AMC/settori.xlsx", index_col = 0)

    dati_per_dopo = dati


    st.title("Mercati azionari agitati oppure calmi?")
    st.subheader('Un AMC per affrontare ogni situazione.')

    st.divider()
    st.subheader('La strategia')

    st.caption("Un approccio sistematico che utilizza indicatori trend-following, overcomprato/venduto e forza relativa per market timing e sector positioning. Il modello identifica sector leadership nel mercato equity americano mentre gestisce i momenti difficili tramite asset allocation in altre asset class che includono money market, Treasury e oro.")
    st.divider()

    st.subheader('Punti di Forza')
    col1, col2 = st.columns(2)

    with col1:
        #st.divider()
        st.caption("Indicatori tecnici per identificare leadership settoriale")
        st.divider()

    #st.image("https://static.streamlit.io/examples/cat.jpg")

    with col2:
        #st.divider()
        st.caption("Market risk review per Risk-On & Risk-Off allocation")
        st.divider()

    #st.image("https://static.streamlit.io/examples/dog.jpg")




with tab2:
    st.title("Sector Leadership")
    

    st.subheader("Un modello con particolare enfasi su indicatori per l'individuazione di trend e trend reversal.")

    st.caption("Il modello si propone di individuare i settori leader sul mercato americano. I leader sono definiti come quei settori che hanno un forte trend rialzista che non sia però infulenzato da movimenti esagerati di breve termine.")

    st.caption("Per farlo, il modello valuta la media mobile dei prezzi a 50 e 200 periodi, la forza relativa e indicaotri di overcomprato/venduto.")


    st.divider()

    st.subheader("Prova il modello selezionando un settore")

    subset = st.selectbox(
        'Seleziona un settore',
        ('SPX Index', 'S5FINL Index',"S5INFT Index","S5ENRS Index","S5HLTH Index","S5UTIL Index","S5INDU Index","S5COND Index","S5TELS Index","S5RLST Index","S5CONS Index","S5MATR Index"))

    #st.write('You selected:', subset)

    inizio = st.date_input(
        "Data Inizio",
        datetime.date(2000, 1, 2),
        min_value = datetime.date(1995, 1, 2),
        max_value = datetime.date(2023, 1, 1))
    #st.write('Hai selezionato:', inizio)

    fine = st.date_input(
        "Data Fine",
        datetime.date(2023, 4, 10),
        min_value = datetime.date(1996, 1, 2),
        max_value = datetime.date(2023, 4, 10)
        )
    #st.write('Hai selezionato:', fine)
    st.divider()

    #st.write('Visualizzazione:', subset)
    st.subheader("Hai Selezionato {}".format(subset))


    #fred = Fred(api_key='9fdbe15d6f2a42bf93b5b1cf112cdf47')


    #prezzi_spx = pd.DataFrame(dati["SPX Index"])
    #prezzi_settori = dati.iloc[:,1:]

    ma50 = dati.rolling(50).mean().iloc[199:]
    ma200 = dati.rolling(200).mean().iloc[199:]

    dati = dati[199:]

    plot_statico = pd.DataFrame(dati["{}".format(subset)])

    #test = pd.DataFrame(prezzi_settori.iloc[:,1])
    plot_statico["Media Mobile 50"] = plot_statico.iloc[:,0].rolling(50).mean()
    plot_statico["Media Mobile 200"] = plot_statico.iloc[:,0].rolling(200).mean()
    plot_statico["segnali"] = np.where(plot_statico["Media Mobile 50"] > plot_statico["Media Mobile 200"],1,0)
    plot_statico["posizioni"] = plot_statico.segnali.diff()




    plt.style.use("dark_background")

    fig2, ax = plt.subplots(figsize=(20,8))
    ax.plot(plot_statico.iloc[:,0]["{}".format(inizio):  "{}".format(fine) ], color = "white", alpha = 1, linewidth=1, label = "{}".format(subset))
    plt.title("{}".format(subset))
    y_bottom, y_top = ax.get_ylim()

    #ax.fill_between(prezzi_vecchi.index,prezzi_vecchi.iloc[:,0], y_bottom, color = "royalblue", alpha = 0.7 )
    #ax.fill_between(plot_statico["{}".format(inizio):  "{}".format(fine) ].index,plot_statico.iloc[:,0]["{}".format(inizio):  "{}".format(fine) ], y_bottom, color = "royalblue", alpha = 0.7 )
    ax.plot(plot_statico["Media Mobile 50"]["{}".format(inizio):  "{}".format(fine) ], label = "Media Mobile 50")
    ax.plot(plot_statico["Media Mobile 200"]["{}".format(inizio):  "{}".format(fine) ], label = "Media Mobile 200")
    ax.scatter(plot_statico[plot_statico.posizioni == 1]["{}".format(inizio):  "{}".format(fine) ].index, plot_statico[plot_statico.posizioni == 1].iloc[:,0]["{}".format(inizio):  "{}".format(fine) ], color = "green", s = 200, marker = "^")
    ax.scatter(plot_statico[plot_statico.posizioni == -1]["{}".format(inizio):  "{}".format(fine) ].index, plot_statico[plot_statico.posizioni == -1].iloc[:,0]["{}".format(inizio):  "{}".format(fine) ], color = "red", s = 200, marker = "v")

    #ax.scatter(prezzi_vecchi.index[-1], prezzi_vecchi.iloc[:,0][-1], color = "white", s=100)
    ax.grid(color = "white", alpha = 0.2)

    plt.legend()

    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)

    st.pyplot(fig2)


    dati_da_plottare = plot_statico["{}".format(inizio):  "{}".format(fine) ].iloc[:,:-2]



    #dati_da_plottare["Media Mobile 50"] = dati_da_plottare.rolling(50).mean()
    #dati_da_plottare["Media Mobile 200"] = dati_da_plottare.iloc[:,0].rolling(200).mean()

    #dati_da_plottare = dati_da_plottare[200:]

    #dati_da_plottare = dati_da_plottare["{}".format(inizio):  "{}".format(fine) ]

    st.line_chart(dati_da_plottare)

    apertura = plot_statico[plot_statico.posizioni==1]
    chiusura = plot_statico[plot_statico.posizioni==-1]

    ritorni = []
        #daily = []

    lunghezza_trades = []
    for i in range(len(chiusura)):
        dati = plot_statico[apertura.index[i]:chiusura.index[i]]
        lunghezza_trades.append(len(dati))

        iniziale = dati.iloc[0,0]
        finale = dati.iloc[-1,0]

        rit_trade = (finale-iniziale)/iniziale

        ritorni.append(rit_trade)

    ritorno_medio = np.mean(ritorni)*100
    lunghezza_media = np.mean(lunghezza_trades)

    ritorni_trades_df = pd.DataFrame(ritorni)
    totale_trades = len(ritorni_trades_df)
    totale_positivi = len(ritorni_trades_df[ritorni_trades_df.iloc[:,0] > 0])

    percent_positivi = totale_positivi/totale_trades


    #st.metric("Ritorno Medio Trades", "{}%".format(round(ritorno_medio,2)), "%")
    st.divider()
    st.header('Info sui Trades')

    col1, col2, col3 = st.columns(3)
    col1.metric("Ritorno Medio Trades", "{}%".format(round(ritorno_medio,2)))
    col2.metric("Lunghezza Media Trades", "{} gg".format(round(lunghezza_media)))
    col3.metric("Win Rate", "{}%".format(round(percent_positivi*100,2)) , "{} trades positivi su {}".format(totale_positivi, totale_trades))


    st.subheader('Ritorni dei Trades')

    fig3, ax = plt.subplots(figsize=(20,9))

    plt.title("Ritorni dei trades")

    plt.tick_params(left = False,labelleft = False)


    pps = ax.bar(x = np.arange(len(ritorni)), height = ritorni,color = 'red', alpha = 0.3,edgecolor = 'white',width = 0.8)

    colori = []
    for p in pps:
        height = p.get_height()

        if height > 0:
            colori.append("green")
        else:
            colori.append("red")

    ppg = ax.bar(x = np.arange(len(ritorni)), height = ritorni,color = colori, alpha = 0.4, edgecolor = 'white',width = 0.8)


    for p in ppg:
        height = p.get_height()

        ax.text(x=p.get_x() + p.get_width() / 2, y=height+.10,
            s="{}%".format(round(height*100,2)),
            ha='center', color = "white", fontsize = 15)
    
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax.axhline(0, color = "black", linewidth= 0.5, linestyle = "--")



    st.pyplot(fig3)


    st.divider()







with tab3:
    st.title("Metodologia")
    

    st.subheader('Una strategia per affrontare ogni situazione di mercato.')

    st.divider()
    
    
    st.subheader("Selezione tra 14 ETF per 11 slots")
    st.caption("L'obiettivo è quello di sfruttare la sector leadership mentre si gestiscono i momenti difficili di mercato attraverso asset allocation. I segnali sono ottenuti attraverso una combinazione di indicatori tecnici pensati per individuare trend nei prezzi.")
    st.caption("Il certificato ricerca il capital appreciation mentre limita i drawdown. Per fare questo, si può investire in 11 slots equal weighted. " )
    

    st.divider()


    image = Image.open('risk_on.JPEG')
    risk_off = Image.open('risk_off.JPEG')


    st.header("Risk On vs Risk Off")
    st.image(image)#, caption='Risk On')

    #st.header("Risk Off")
    st.image(risk_off)#, caption='Risk Off')

    st.divider()

    st.header('Allocation Process')

    st.caption("11 Basket equal weighted da riempire selezionando tra 14 ETFs.")
    st.caption("I settori che passano il filtro trend-following sono inclusi nel portafoglio.")
    st.caption("I settori che non passano il filtro trend-following sono esclusi ed i relativi basket sono riempiti con risk off assets (money market, Treasury e gold.)")

    allocation = Image.open('allocation.JPEG')

    st.image(allocation, caption='Esempio di Allocation')


    st.divider()



with tab4:

    st.header("Backtest strategia")

    st.divider()

    st.subheader('Seleziona la data di inizio')


    inizio = st.date_input(
        "Data Inizio",
        datetime.date(2008, 1, 2),
        min_value = datetime.date(2008, 1, 2),
        max_value = datetime.date(2022, 1, 1))
    #st.write('Hai selezionato:', inizio)

    fine = st.date_input(
        "Data Fine",
        datetime.date(2022, 6, 1),
        min_value = datetime.date(2008, 1, 2),
        max_value = datetime.date(2022, 6, 1)
        )
    #st.write('Hai selezionato:', fine)
    st.divider()



    prezzi_spx = dati_per_dopo.iloc[:,0]

    prezzi_settori = dati_per_dopo.iloc[:,1:]


    segnali =  ma50 > ma200
    segnali = segnali.iloc[:,1:]

    segnali_mensili = segnali.loc[segnali.groupby(segnali.index.to_period('M')).apply(lambda x: x.index.max())]["{}".format(inizio):  "{}".format(fine) ]

    prezzi_spx = prezzi_spx.loc[prezzi_spx.groupby(prezzi_spx.index.to_period('M')).apply(lambda x: x.index.max())]["{}".format(inizio):  "{}".format(fine) ]

    prezzi_altri_asset = altri_asset.loc[altri_asset.groupby(altri_asset.index.to_period('M')).apply(lambda x: x.index.max())]["{}".format(inizio):  "{}".format(fine) ]



    ritorni = []
    peso_risk_on = []

    for i in range(len(segnali_mensili)-1):

        finale = prezzi_settori.loc[segnali_mensili.index[i+1],segnali_mensili.iloc[i,:].values]
        iniziale = prezzi_settori.loc[segnali_mensili.index[i],segnali_mensili.iloc[i,:].values]

        finale_altri = prezzi_altri_asset.loc[segnali_mensili.index[i+1],:]
        iniziale_altri = prezzi_altri_asset.loc[segnali_mensili.index[i],:]

        peso_altri_asset = 1-(len(finale)/11)

        ritorni.append((((finale-iniziale)/iniziale)*1/11).sum() + ((((finale_altri-iniziale_altri)/iniziale_altri) * peso_altri_asset).sum()))

        peso_risk_on.append(len(finale)/11)


    to_plot = pd.DataFrame(ritorni)
    to_plot.index = segnali_mensili.index[:-1]

    interattivo = np.cumprod(1+to_plot)
    interattivo.columns = ["Strategia"]
    interattivo["SPX Index"] = np.cumprod(1+pd.DataFrame(prezzi_spx.pct_change()))


    st.subheader('Ritorno strategia vs SPX Index')
    st.line_chart(interattivo)

#####################

    previous_peak_strat = interattivo.Strategia.cummax()
    drawdown_strat = (interattivo.Strategia - previous_peak_strat) / previous_peak_strat

    previous_peak_spx = interattivo["SPX Index"].cummax()
    drawdown_spx = (interattivo["SPX Index"] - previous_peak_spx) / previous_peak_spx


    dd_df = pd.DataFrame(drawdown_strat)
    dd_df["Drawdown SPX"] = drawdown_spx

    dd_df.columns = ["Drawdown Strategia","Drawdown SPX"]

    st.subheader('Drawdown strategia vs SPX Index')

    st.line_chart(dd_df*100)

    #fig5 = plt.figure(figsize=(16,8))
    #plt.title("Draw Down Strategie Momentum")

#####################
#####


    peso_risk_on = pd.DataFrame(peso_risk_on)*100
    peso_risk_on.columns = ["% Risk On in Portafoglio"]
    peso_risk_on["Risk On Medio"] = peso_risk_on.iloc[:,0].mean()
    peso_risk_on.index = interattivo.index
    
    st.subheader('% di portafoglio investita nei Risk On assets')
    st.line_chart(peso_risk_on)

    st.divider()

    st.subheader('Dati sul portafoglio')
    

    col1, col2, col3 = st.columns(3)
    col1.metric("Ritorno Totale Strategia", "{}%".format(round(((interattivo.iloc[-1,:]-1)*100)[0],2)), "Vs SPX Index {}%".format(round(((interattivo.iloc[-1,:]-1)*100)[1],2)))
    col2.metric("Volatilità Strategia", "{}%".format(round(pd.DataFrame(ritorni).std()[0]*np.sqrt(12)*100,2)), "Vs SPX Index {}%".format(round(pd.DataFrame(prezzi_spx.pct_change()).std()[0]*np.sqrt(12)*100,2)) )
    #col3.metric("Sharpe Ratio", "{}".format(round(((interattivo.iloc[-1,:]-1))[0] / pd.DataFrame(ritorni).std()[0]*np.sqrt(12),2)) , "{} trades positivi su {}".format(totale_positivi, totale_trades))




