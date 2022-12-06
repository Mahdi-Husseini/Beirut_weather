import pandas as pd
import streamlit as st
from prophet.plot import plot_plotly, plot_components_plotly
from PIL import Image
import statsmodels
from prophet import Prophet
import base64
import plotly.express as px
image = Image.open('beirut.jpg')
st.image(image, use_column_width= True)
st.title("Beirut Weather")
st.write("""
    this app represents the statistics of the weather in Beirut recorded from Rafiq Al-Hariri Int. Airport
    \nthe data used in this is app downloaded and cleaned from [opendatalebanon](https://www.opendatalebanon.org/job/weather/)
    \n* **Python libraries:** streamlit, pandas, PIL, statsmodels, prophet, base64, plotly
    \n***
""")
file = "BeirutTemp.csv"
#In case file encoding error
# with open(file, 'rb') as rawdata:
#     result = chardet.detect(rawdata.read(100000))
data = pd.read_csv(file)
st.subheader("weather dataset used")
st.dataframe(data)
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="BeirutWeather.csv">Download CSV</a>'
    return href

st.markdown(filedownload(data), unsafe_allow_html=True)
st.write("***")
temp = px.line(data, x="Year", y="MeanTemp",text="MeanTemp", title="Mean temperature in Beirut over 1996-2010", labels={"MeanTemp": "Mean Temperature (C)"})
temp.update_traces(textposition='top left')
st.write(temp)
humidity = px.line(data, x="Year", y="humidity",text="humidity", title="humidity in Beirut over 1996-2010", labels={"humidity": "humidity (%)"})
humidity.update_traces(textposition='top left')
st.write(humidity)
rain = px.line(data, x="Year", y="rain", text="rain", title="rain in Beirut over 1996-2010", labels={"rain": "rain (mm)"})
rain.update_traces(textposition='top left')
st.write(rain)

scatter = px.scatter(data_frame = data, x="humidity",
                    y="MeanTemp", size="MeanTemp", 
                    trendline="ols", 
                    title = "Relationship Between Temperature and Humidity")

st.write(scatter)
st.write("we see there is a negative correlation beween humidity and temperature, hence higher temperature results in low humidity and lower temperature results in high humidity\n")

forecast_data = data.rename(columns = {"Year": "ds", 
                                       "MeanTemp": "y"})
#Forecasting Weather
model = Prophet()
model.fit(forecast_data)
forecasts = model.make_future_dataframe(periods=20000)
predictions = model.predict(forecasts)
if st.checkbox("show temperature forecasting demo"):
    st.write(plot_plotly(model, predictions))