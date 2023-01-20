import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from sales_volume_price import get_total_volume

def get_graph_volume(total_volume: pd.DataFrame, unit: str, freq: str, legend: bool, mode: str) -> go.Figure:
	
	pal_1 = np.repeat('grey', len(total_volume))
	pal_2 = np.repeat('darkgrey', len(total_volume))
	
	fig = px.bar(
		total_volume / 1_000,
		title='LPG Sales Volume',
		barmode=mode,
		color_discrete_sequence=[pal_1, pal_2]
	)
	
	fig.update_layout(
		title=f'Sales Volume<br><sup>in 000s {unit.title()}</sup>',
		hovermode='x',
		showlegend=legend,
		xaxis_title=None,
		yaxis_title=None,
		font={
			'family': 'Arial Narrow',
			'size': 20
		}
	)
	
	fig.update_traces(
		hovertemplate='<b> %{y:,.0f} </b>'
	)
	
	fig.update_xaxes(
		title_font_family='Arial Narrow',
		tickformat='%b\n%Y'
	)
	
	fig.update_yaxes(
		title_font_family='Arial Narrow',
		tickformat=',.0f'
	)
	
	return fig

def main(unit: str, years: list, freq: str, legend: str, mode: str) -> go.Figure:
	
	total_volume = get_total_volume(unit, years, freq)
	fig = get_graph_volume(total_volume, unit, freq, legend, mode)
	
	return fig
	
