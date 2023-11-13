import pandas as pd
import json
import plotly.express as px
from PIL import Image
import streamlit as st
from datetime import datetime, timezone, timedelta
import os
from variables import *
    
#SetDataframetoStreamlib
def GenerateReport(df):
    st.title("Performance Testing Dashboard", anchor=None)

    st.markdown(
        """
        <style>
            button[title^=Exit]+div [data-testid=stImage]{
                text-align: center;
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 100%;
                text-align: center
            }
        </style>
        """, unsafe_allow_html=True
    )

    df_responsecodeSummary = df.groupby(["responseCode"]).size().reset_index(name='total')
    df_responsecode = df.groupby(["label", "responseCode"]).size().reset_index(name='total')
    df_responseTime = df.groupby(["label", "Latency"]).size().reset_index(name='total')
    df_responseTime["Latency"] = df_responseTime["Latency"]
    df_responseTime.rename(columns={"Latency": "ResponseTime"}, inplace = True)

    #Store to Lists
    label = df_responsecode["label"].unique().tolist()
    responseCode = df_responsecode["responseCode"].unique().tolist()
    df_responsecode['responseCode'] = df_responsecode['responseCode'].astype(str)
    df_responsecodeSorted = df_responsecode.sort_values('responseCode')


    responseCodeSummary = df_responsecode["responseCode"].unique().tolist()
    df_responsecodeSummary['responseCode'] = df_responsecodeSummary['responseCode'].astype(str)
    df_responsecodeSummarySorted = df_responsecodeSummary.sort_values('total', ascending=False)
    df_responsecodeSummarySorted = df_responsecodeSummarySorted[df_responsecodeSummarySorted['responseCode'].isin(nonErrorResponseCode)==False]


    #Sum Berhasil, Error, dan NonHTTP
    ResponseBerhasilSum = (df['responseCode'].astype(str).isin(nonErrorResponseCode)).sum()
    ResponseErrorSum = (df['responseCode'].astype(str).isin(ErrorResponseCode)).sum()
    ResponseNonHTTPsum = (~df['responseCode'].astype(str).isin(httpResponseCode)).sum()
    totalRequest = len(df_responsecode)

    #Hits per Second
    timeStart = (df['timeStamp'].min())
    timeEnd = (df['timeStamp'].max()) + df['Latency'].iloc[-1]
    duration = (timeEnd-timeStart)/1000
    duration = round(duration,2)
    totalHPS = len(df)/duration
    totalHPS = round(totalHPS,2)
    df['timeEnd'] = (df['timeStamp']+df['Latency'])
    df['timeStamp'] = df['timeStamp']+25200000
    df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='ms').apply(lambda x: x.replace(microsecond=0))
    tanggalPengujian = df['timeStamp'].min()
    df['timeEnd'] = pd.to_datetime(df['timeEnd'], unit='ms').apply(lambda x: x.replace(microsecond=0))
    df_hps = df.groupby(['success',"timeStamp", "Latency"]).size().reset_index(name='total')
    df_hps['HPS'] = df_hps["total"]/df_hps["Latency"]*1000
    
    averageResponseTime = df['Latency'].sum()/len(df)
    averageResponseTime = round(averageResponseTime,2)
    TPS = len(df)/duration
    TPS = round(TPS,2)
    
    sumSuccessError = [ResponseBerhasilSum, ResponseErrorSum, ResponseNonHTTPsum]
    label_ratio = ["Success", "Error", "Non-HTTP Error Code"]
    
    data = {
    'banyakRequest' : [len(df)],
    'tanggalPengujian' : [tanggalPengujian],
    'duration': [duration], 
    'TPSAverage': [totalHPS],
    'HTTP Response Code' : [df['responseCode'].unique()],
    'Response Time (Highest)' : [df['Latency'].max()],
    'Response Time (Lowesst)' : [df['Latency'].min()],
    'Response Time (Average)' : [df['Latency'].sum()/len(df)],
    }
    df_table = pd.DataFrame.from_dict(data)
    col1, col2, col3, col4= st.columns([5,5,5,5])
    col5, col6, col7,inter_cols_pace= st.columns(4)
    
    with st.container():
        with col1:
            col1.metric("Banyak Request", len(df))
        with col2:
            col2.metric("Waktu Pengujian", str(tanggalPengujian))
        with col3:
            col3.metric("Durasi Pengujian", str(duration) + " Detik")
        with col4:
            col4.metric("Transaction/Second", str(TPS))
    
    with st.container():
        with col5:
            col5.metric("Response Time (Min)", str(df['Latency'].min()) + " ms")
        with col6:
            col6.metric("Response Time (Average)", str(averageResponseTime) + " ms")
        with col7:
            col7.metric("Response Time (Highest)", str(df['Latency'].max()) + " ms")
    
    with st.container():
        col1_1, col1_2, col1_3 = st.columns([5,15,6])
        col1_4, col1_5 = st.columns([10,10])
        with col1_1:
            successErrorRatio = px.pie(
                title="Success/Error Ratio",
                values=sumSuccessError, 
                names=label_ratio,
                color=label_ratio,
                color_discrete_map={
                    'Success':'#0f9758',
                    'Error':'#97220f',
                    'Non-HTTP Error Code':'#000000'
                    }
                )
            st.plotly_chart(successErrorRatio, use_container_width=True)               
        with col1_2:
            responseCodeSummary = px.bar(df_responsecodeSorted,
                title="Success/Error Code Distribution",
                x='total',
                y='label',
                color='responseCode',
                barmode='overlay',
                template='plotly_white',
                color_discrete_map = color_response_code
                )
            st.plotly_chart(responseCodeSummary, use_container_width=True)
        with col1_3:
            responseCodeSummarySorted = px.bar(df_responsecodeSummarySorted,
                title="Top Error Code",
                x='responseCode',
                y='total',
                barmode='group',
                color='responseCode',
                template='plotly_white',
                color_discrete_map = color_response_code,
                width=10
                ).update_traces(width=0.3).update(layout_yaxis_range = [0,df_responsecodeSummarySorted['total'].max()])
            st.plotly_chart(responseCodeSummarySorted, use_container_width=True)
        
    with col1_4:
        if df["Latency"].max()<1000:
            responseTimeChart = px.histogram(df_responseTime,
                title="Response Time Distribution",
                x="ResponseTime",
                y="total",
                color="label",
                template='plotly_white',
                color_discrete_map = color_response_code,
                barmode="overlay",
                width = 10
                ).update(layout_xaxis_range = [0,1000])
        elif df["Latency"].max()>1000:
                responseTimeChart = px.histogram(df_responseTime,
                title="Response Time Distribution",
                x="ResponseTime",
                y="total",
                color="label",
                template='plotly_white',
                color_discrete_map = color_response_code,
                barmode="overlay",
                width = 10
                )
        st.plotly_chart(responseTimeChart, use_container_width=True)
        
    with col1_5:   
        TPSChart = px.line(df_hps.join(df_hps.groupby(["timeStamp"], as_index=False).cumsum(), rsuffix="_cumsum"), y="total_cumsum", x="timeStamp", color="success").update(layout_yaxis_range = [0,df['timeEnd'].max()])
        st.plotly_chart(TPSChart, use_container_width=True)