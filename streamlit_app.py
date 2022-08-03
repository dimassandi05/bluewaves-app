# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 09:48:45 2022

@author: Dimas Sandi
"""
import pandas as pd
from plotly import express as px
import streamlit as st

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

@st.cache
def get_data_from_excel():
    df = pd.read_excel(io="supermarkt_sales.xlsx",
            engine="openpyxl",
            sheet_name="Sales",
            skiprows=3,
            usecols="B:R",
            nrows=1000,)
    # add 'hour' colum to data frame

    df['hour'] = pd.to_datetime(df['Time'],format='%H:%M:%S').dt.hour
    
    return df

df = get_data_from_excel()




#st.dataframe(df)
# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)
customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

branch = st.sidebar.multiselect(
    "Select Branch:",
    options=df['Branch'].unique(),
    default=df['Branch'].unique()
    )

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender & Branch == @branch "
)

df_selection = df.query (
    'City == @city & Customer_type == @customer_type & Gender == @gender & Branch == @branch')

st.dataframe(df_selection)


# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


# SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)





left_column,right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)



st.markdown("""---""")

# % sales in gender
sales_gender = df_selection.groupby('Gender').agg({'Total':'sum'})
fig_sales_gender = px.pie(
    sales_gender,values='Total',names=sales_gender.index,
    title='<b>Total Sales by Gender<b>'
    )

fig_sales_gender.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

st.plotly_chart(fig_sales_gender)


st.markdown("""---""")

# % quantity in gender
quantity_gender = df_selection.groupby('Gender').agg({'Quantity':'sum'})
fig_quantity_gender = px.pie(
    quantity_gender,values='Quantity',names=quantity_gender.index,
    title='<b>Total Quantity by Gender<b>'
    )

fig_quantity_gender.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

# Total Quantity in product line
total_quantity_product_inline = df_selection.groupby(
    'Product line').agg({'Quantity':'sum'})
fig_total_quantity_product_inline = px.pie(
    total_quantity_product_inline,values='Quantity',names=total_quantity_product_inline.index,
    title='<b>Total Quantity Product Line<b>'
    )

fig_total_quantity_product_inline.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left_column,right_column = st.columns(2)
left_column.plotly_chart(fig_quantity_gender,use_container_width=True)
right_column.plotly_chart(fig_total_quantity_product_inline,use_container_width=True)
# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)