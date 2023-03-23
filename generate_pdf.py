#import dependencies 
from datetime import date
from pathlib import Path
import sqlite3

import pandas as pd
import plotly.express as px
from fpdf import FPDF

#define paths and charts
plotly_template = "presentation"

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
database_path = current_dir/"sales.db"
output_dir = current_dir/"output"

output_dir.mkdir(parents=True, exist_ok=True)

#total sales by month
con = sqlite3.connect(database_path)

query = '''SELECT sale_date, SUM(total_price) as total_sales
           FROM sales
           GROUP BY sale_date
           ORDER BY sale_date ASC'''

df = pd.read_sql_query(query, con)
print(df)
df.info()

df['sale_date'] = df.to_datetime(df['sale_date'])
df.info()

df = df.set_index('sale_date')
df.head(3)

df_monthly = df.resample('M').sum()
df_monthly

df_monthly['month_name'] = df_monthly.index.strftime('%b')
df_monthly

fig = px.bar(df_monthly,
             x='month_name',
             y='total_sales',
             template=plotly_template,
             text='total_sales')

fig.update_layout(
    title='Total Sales by Month',
    xaxis_title='Month',
    yaxis_title='Total Sales in $',
    yaxis_tickprefix='$'
)

fig.write_image(output_dir / 'monthly_sales.png',
                width=1200,
                height=400,
                scale=4)

#total sales by product
query_product = '''SELECT p.product_name, SUM(s.total_price) as total_sales
                   FROM sales s
                   JOIN products p ON s.product_id = p.product_id
                   GROUP BY p.product_name'''
df_product = pd.read_sql_query(query_product, con)
df_product

fig_product = px.bar(df_product,
                     x='product_name',
                     y='total_sales',
                     template=plotly_template,
                     text='total_sales')

fig_product.update_layout(
    title='Total Sales by Product',
    xaxis_title='Product',
    yaxis_title='Total Sales in $',
    yaxis_tickprefix='$'    
) 

fig_product.write_image(output_dir/'product_sales.png',
                        width=1200,
                        height=400,
                        scale=4)