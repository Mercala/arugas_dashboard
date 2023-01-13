import streamlit as st
import graph_sales
import graph_backlog
import gross_margin
import sales

PATH = ''

# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
st.sidebar.subheader('LPG Sales Volume')
toggle = st.sidebar.radio('Purchase', ('ON', 'OFF'))
sales_fig = graph_sales.main(toggle)

st.title('Arugas Financial Dashboard')

st.plotly_chart(
	sales_fig,
  	theme='streamlit',
  	use_container_width=True,
  	kwargs={'toggle': toggle}
  	)
# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
st.sidebar.subheader('Backlog')
year = st.sidebar.selectbox('Year', options=['2021', '2022'])
backlog_fig = graph_backlog.main(year)

st.plotly_chart(
	backlog_fig,
	theme='streamlit',
	use_container_width=True,
	kwargs={'year': year}
	)
# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# st.sidebar.subheader('Gross Margin')
# skew = st.sidebar.selectbox('SKU', options=['HSH 100 lb', 'HSH 60 lb', 'COM 20 lb', 'COM 60 lb', 'COM 100 lb', 'COM MIX', 'COM BULK', 'MOTOR BULK'])
# currency = st.sidebar.radio('Currency', ('awg', 'usd'))
# unit = st.sidebar.selectbox('Quantity unit', options=['kilos', 'pounds', 'gallons', 'liters'])

# gross_margin_fig = gross_margin.graph(skew, currency, unit)

# st.plotly_chart(
# 	gross_margin_fig,
# 	theme='streamlit',
# 	use_container_width=True,
# 	kwargs={
# 		'skew': skew,
# 		'currency': currency,
# 		'unit': unit
# 		}
# 	)
