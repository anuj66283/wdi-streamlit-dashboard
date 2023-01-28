import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title = "WDI dashboard",
    layout = 'wide'
)

@st.cache
def loader():
    df = pd.read_csv('main.csv')
    df.fillna(0, inplace=True)
    return df


df = loader()
df2 = df.set_index('Country Name')

st.markdown("<h1 style='text-align: center;'>World Development Indicator</h1>", unsafe_allow_html=True)
st.empty()

home, compare = st.tabs(["home", "compare"])

with home:
    country = st.sidebar.selectbox('Choose Country', df['Country Name'].unique())

    #Get all indicator names associated with the certain country
    #Some indicator names for some countries are missing
    indx = df[df['Country Name'] == country]['Indicator Name']

    indicator= st.sidebar.multiselect('Choose data', indx, default='Population, total')
    
    #Store all the plot details of a country
    data = []

    for ind in indicator:
        temp = df2.loc[df2['Indicator Name'] == ind]
        chart = go.Scatter(name=ind, x=temp.columns[2:], y=temp.loc[country][2:], mode='lines')
        data.append(chart)

    fig = go.Figure(data=data)
    st.plotly_chart(fig, use_container_width=True)


with compare:

    cnt_1, cnt_2 = st.columns(2)
    
    with cnt_1:
        country_filter_2 = st.selectbox("Select Country", df['Country Name'].unique(), key="cmp2")
    
    with cnt_2:
        ind_name = df[df['Country Name'] == country_filter_2]['Indicator Name']

        #As some countries have missing indicator names it helps to prevent error
        if len(ind_name)<len(indx):
            ind = ind_name

        indicator_filter_1 = st.selectbox("Select Data", indx, key="indc")

    df3 =  df.set_index('Country Name')
    df3 = df3.loc[df3['Indicator Name'] == f'{indicator_filter_1}']

    plot = go.Figure(data=[go.Bar(
        name=country,
        x = pd.to_datetime(df3.columns[2:]),
        y = df3.loc[country][2:]
    ),
        go.Scatter(name=country_filter_2,
        x = pd.to_datetime(df3.columns[2:]),
        y = df3.loc[country_filter_2][2:],
        line=dict(color="#F2921D")
    )
    ]).update_layout(title=f'{country} vs {country_filter_2}')

    st.plotly_chart(plot, use_container_width=True)
