import pandas as pd
import numpy as np

import plotly.graph_objects as go

from backlog import get_backlog_data

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def get_graph_backlog(backlog_time: pd.Series, route: str, legend: str) -> go.Figure:
	
	fig = go.Figure()
	freq = 'W'
	def subheader(freq: str) -> str:
		dct ={
			'M': 'Months',
			'W': 'Weeks',
			'Q': 'Quarters',
			'A': 'Years'
		}
		
		return dct.get(freq)
	
	def route_name(route) -> str:
		dct = {
			'1': 'Noord',
			'2': 'Tanki Leendert',
			'3A': 'Oranjestad A',
			'3B': 'Oranjestad B',
			'4': 'St. Cruz',
			'5': 'Savaneta',
			'6': 'San Nicolas',
			'all': 'All Routes'
		}
		
		return dct.get(route)
	
	fig.update_layout(
		title=f'Estimated Delivery time {route_name(route)}<br><sup>in {subheader(freq)}</sup>',
		hovermode='x',
		showlegend=legend,
		font={
			'family': 'Arial Narrow',
			'size': 20
		}
	)
			
	fig.add_scatter(
		x=backlog_time.index,
		y=backlog_time.values,
		name='backlog',
		line={
			'shape': 'hv',
			'color': 'darkgrey'
		}
	)
	
	fig.update_traces(
		hovertemplate='<b> %{y:,.1f} </b>'
	)
	
	fig.update_xaxes(title_font_family='Arial Narrow')
	fig.update_yaxes(
		title_font_family='Arial Narrow',
		tickformat=',.0f'
			)
	
	return fig

def main(route, years, freq, legend):
	backlog_time = get_backlog_data(route, years, freq)
	fig = get_graph_backlog(backlog_time, route, freq, legend)
	
	return fig
