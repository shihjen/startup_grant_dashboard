# Helper Function 1
# function to convert the dataset when load for usage
def process_loaded_data(data):
    import pandas as pd
    data['Posting_Date'] = pd.to_datetime(data['Posting_Date'], dayfirst=True)
    data['Invoice_Date'] = pd.to_datetime(data['Invoice_Date'], dayfirst=True)
    data['Invoice_Year'] = data['Invoice_Date'].dt.year
    data['Invoice_Month'] = data['Invoice_Date'].dt.month
    data['Invoice_Day'] = data['Invoice_Date'].dt.day
    return data

# Helper Function 2
# function to preprocess the data for plotting heatmap
def preprocess_heatmap(data):
    import pandas as pd
    import numpy as np
    daily_total = data.groupby(['Invoice_Year','Invoice_Month','Invoice_Day'])['Value'].sum().reset_index()
    
    years = daily_total['Invoice_Year'].unique()
    months = daily_total['Invoice_Month'].unique()
    days = np.arange(1,32)

    index = pd.MultiIndex.from_product([years, months, days], names = ['Invoice_Year','Invoice_Month', 'Invoice_Day'])

    daily_total = daily_total.set_index(['Invoice_Year','Invoice_Month', 'Invoice_Day']).reindex(index, fill_value=0).reset_index()
    return daily_total

# Helper Function 3
# function to plot heatmap
def plot_heatmap(data, year):
    import pandas as pd
    import plotly.graph_objects as go
    
    selected_data = data[data['Invoice_Year'] == year]
    pivot = selected_data.pivot(index='Invoice_Month', columns='Invoice_Day', values='Value').fillna(0)

    # create the heatmap using Plotly Graph Objects
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='sunset_r',
        colorbar=dict(title='Value'),
        hovertemplate='Month: %{y}<br>Day: %{x}<br>Total Expense: S$ %{customdata:.2f}<extra></extra>',
        customdata=pivot.values
    ))

    # add border lines by drawing rectangles around each cell
    shapes = []
    for i, row in enumerate(pivot.index):
        for j, col in enumerate(pivot.columns):
            shapes.append(
                go.layout.Shape(
                    type="rect",
                    x0=col - 0.5, x1=col + 0.5,
                    y0=row - 0.5, y1=row + 0.5,
                    line=dict(color='grey', width=1)
                )
            )

    fig.update_layout(
        #title=f'Total Invoice Amount per Month per Year ({year})',
        xaxis_title='Day',
        #yaxis_title='Month',
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 32)),
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=pivot.index.tolist(),
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ),
        shapes=shapes,
        height=500,
        width=1000,
        template='plotly_dark'
    )

    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

    return fig

# Helper Function 4
# function to plot treemap
def plot_treemap(data, year):
    import pandas as pd
    import plotly.express as px
    
    if year == 'All Years':
        df = data
        con = 'All Years'
    else:
        df = data[data['Invoice_Year'] == year]
        con = f'Year: {year}'
    
    fig = px.treemap(df, path=[px.Constant(con), 'Category'], values='Value', width=800, height=500)
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    #fig.update_traces(root_color='lightgrey')
    fig.update_layout(template='plotly_dark')
    return fig

# Helper Function 5
# function to plot bubble chart
def plot_bubble(data, year):
    import plotly.express as px
    import pandas as pd
    
    # remove the negative value in the data
    df = data[data['Value'] > 0]

    # aggregate the data by summing the 'Value' for each 'Vendor' and 'Category' combination
    aggregated_data = df.query(f'Invoice_Year == {year}').groupby(['Vendor', 'Category']).agg({'Value': 'sum'}).reset_index()

    # create the bubble chart using the aggregated data
    fig = px.scatter(
        aggregated_data, 
        x='Category', 
        y='Vendor', 
        size='Value',  # column to determine the size of the bubbles
        color='Category', 
        size_max=60, 
        height=1100,
        width=500,
    )

    fig.update_layout(template='plotly_dark')
    return fig

# Helper Function 6
# function to construct a dataframe for the expenses by vendors
def vendor_by_expenses(data, year):
    import pandas as pd
    import numpy as np
    expenses = np.round(data[data['Invoice_Year']==year].groupby('Vendor')['Value'].sum(),2).sort_values(ascending=False)
    vendor_breakdown = pd.DataFrame(expenses).reset_index()
    return vendor_breakdown

# Helper Function 7
# function to get key metrics
def get_key_metrics(data, year):
    import pandas as pd
    import numpy as np
    selected_data = data[data['Invoice_Year']==year]
    exp = selected_data['Value'].sum().round(2)
    total_order = selected_data.shape[0]

    exp_vendor = selected_data[selected_data['Value']==selected_data['Value'].max()]
    exp_vendor_name = exp_vendor['Vendor'].values[0]
    exp_value = exp_vendor['Value'].values[0]

    inv_processing_time = selected_data['Posting_Date'] - selected_data['Invoice_Date']
    avg_inv_processing_time = round(inv_processing_time.dt.days.mean(),2)
    longest_inv_processing_time = round(inv_processing_time.dt.days.max(),2)
    return [exp, total_order, exp_vendor_name, exp_value, avg_inv_processing_time, longest_inv_processing_time]

