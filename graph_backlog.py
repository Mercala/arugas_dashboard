import pandas as pd
import numpy as np

import plotly.express as px
import plotly

from get_data import get_backlog_data

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def get_graph_backlog(backlog: pd.DataFrame, year: str) -> plotly.graph_objs.Figure:
	
	# Prep Colours to highlight import data
	pallete_1 = np.repeat('#5a5a5a', 12)
	pallete_1[backlog.loc[:, 'Delivered'].idxmin().month -1] = '#5a232d'
	pallete_1[backlog.loc[:, 'Delivered'].idxmax().month -1] = '#156563'
	
	pallete_2 = np.repeat('gray', 12)
	
	fig = px.bar(
		backlog,
		title='Delivery Backlog HSH',
		color_discrete_sequence=[pallete_1, pallete_2]
	)
	
	fig.update_xaxes(
		tickformat='%b\n%Y'
	)
	
	fig.update_traces(
		hovertemplate='<b> %{y} </b>'
	)
	
	fig.update_layout(
		hovermode='x',
		xaxis_title=None,
		yaxis_title='as a Percentage',
		font={
			'family': 'Arial Narrow',
			'size': 20
		},
		showlegend=False
# 		legend={
# 		    'yanchor': "bottom",
# 		    'y': -0.99,
# 		    'xanchor': "left",
# 		    'x': 0.01
# 		}
	)
	
	fig.update_xaxes(title_font_family='Arial Narrow')
	
	return fig

def main(year):
	backlog = get_backlog_data(year)
	fig = get_graph_backlog(backlog, year)
	
	return fig

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
if __name__ == '__main__':
	
	year = '2021'
	main()

