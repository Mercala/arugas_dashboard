import streamlit as st
from datetime import datetime

import graph_total_volume
import graph_backlog
import graph_margin

legend = st.sidebar.selectbox('Legend', options=[False, True])
mode = st.sidebar.selectbox('Barmode', options=['group', 'relative'])
freq = st.sidebar.selectbox('Frequency', options=['M', 'W'])
unit = st.sidebar.selectbox('Unit', options=['pounds', 'liters', 'gallons', 'kilos'])

years = st.sidebar.multiselect('Years', options=['2021', '2022', '2023'], default='2022')

route = st.sidebar.selectbox('Route', options=['all', '1', '2', '3A', '3B', '4', '5', '6'])
currency = st.sidebar.selectbox('Currency', options=['awg', 'usd'])
skew = st.sidebar.selectbox(
	'SKU', options=[
  		'HSH 100 lbs', 
		'HSH 60 lb',
		'HSH BULK',
		'COM 20 lb',
		'COM 60 lb',
		'COM 100 lb',
		'COM MIX',
		'COM BULK',
		'MOTOR FUEL'
	]
)

st.title('Arugas Financial Dashboard')

fig_volume = graph_total_volume.main(unit, years, freq, legend, mode)
st.plotly_chart(
	fig_volume,
	kwargs={
		'unit': unit,
		'freq': freq,
		'legend': legend,
		'mode': mode
	}
)

fig_backlog = graph_backlog.main(route, years, freq, legend)
st.plotly_chart(
	fig_backlog, 
	kwargs={
		'years': years,
		'route': route,
		'freq': freq,
		'legend': legend
	}
)

fig_margin = gross_margin.main(skew, unit, currency, legend)
st.plotly_chart(
	fig_margin,
	kwargs={
		'skew': skew,
		'unit': unit,
		'currency': currency,
		'legend': legend
	}
)
