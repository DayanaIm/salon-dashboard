import streamlit as st
import pandas as pd
import plotly.express as px

# Load data directly from the uploaded files
services_df = pd.read_csv('services_data.csv')
products_df = pd.read_csv('products_data.csv')

services_df['Date'] = pd.to_datetime(services_df['Date']) 
products_df['Date'] = pd.to_datetime(products_df['Date'])  

# Define consistent color mapping for each product
product_colors = {
    'Shampoo': '#F94144',
    'Conditioner': '#F3722C',
    'Hair Mask': '#F8961E',
    'Styling Gel': '#F9C74F',
    'Hair Spray': '#90BE6D',
    'Serum': '#43AA8B',
    'Hair Brush': '#577590'
}

# Define consistent color mapping for each service
service_colors = {
    'Haircut (Men)': '#F94144',
    'Haircut (Women)': '#F3722C',
    'Haircut (Kids)': '#F8961E',
    'Color': '#F9C74F',
    'Treatment': '#90BE6D',
    'Extensions': '#43AA8B',
    'Styling': '#577590'
}

# Create the tabs for the dashboard (only one set of tabs here)
tab1, tab2, tab3 = st.tabs(["Services", "Products", "Total Revenue by Month"])

# Tab 1: Services Overview with From and To Date Filters and Consistent Colors
with tab1:
    st.header("Services Overview")

    # Date range input for filtering services data
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("From", value=services_df['Date'].min().date(), key="service_start_date")
    with col2:
        end_date = st.date_input("To", value=services_df['Date'].max().date(), key="service_end_date")
    
    # Filter data based on selected date range
    filtered_services_df = services_df[(services_df['Date'] >= pd.to_datetime(start_date)) & (services_df['Date'] <= pd.to_datetime(end_date))]

    # Calculate total revenue by service and the overall total revenue
    total_revenue_by_service = filtered_services_df.groupby('Service')['Revenue'].sum().reset_index()
    overall_total_service_revenue = total_revenue_by_service['Revenue'].sum()

    # Display the overall total revenue next to the pie chart
    col1, col2 = st.columns([2, 1])
    with col1:
        # Plot the filtered Total Revenue Pie Chart with consistent colors
        fig_service_revenue_pie = px.pie(
            total_revenue_by_service, 
            names='Service', 
            values='Revenue', 
            title=f"Total Revenue by Service from {start_date} to {end_date}",
            hole=0.3,  # Optional, for a donut-style chart
            color='Service',  # Use 'Service' as color to apply custom colors
            color_discrete_map=service_colors  # Apply color mapping
        )
        # Add custom hover information to show both percentage and amount
        fig_service_revenue_pie.update_traces(
            textinfo='percent+label',  # Show both percentage and service label
            hovertemplate='<b>%{label}</b><br>Revenue: $%{value}<br>Percent: %{percent}'
        )
        st.plotly_chart(fig_service_revenue_pie)

    with col2:
        # Display the overall total revenue in a text box next to the pie chart
        st.metric(label="Total Service Revenue", value=f"${overall_total_service_revenue:,.2f}")

     # Calculate most and least popular service
    if not filtered_services_df.empty:
        service_counts = filtered_services_df['Service'].value_counts()
        most_popular_service = service_counts.idxmax()
        least_popular_service = service_counts.idxmin()
    else:
        most_popular_service = "No data"
        least_popular_service = "No data"

    # Display most and least popular service as cards
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Most Popular Service", value=most_popular_service)
    with col2:
        st.metric(label="Least Popular Service", value=least_popular_service)

    # Plot the Most Popular Services Bar Chart with consistent colors
    service_counts_df = service_counts.reset_index()
    service_counts_df.columns = ['Service', 'Count']
    fig_service_popularity = px.bar(
        service_counts_df,
        x='Service', 
        y='Count', 
        title=f"Service Sales from {start_date} to {end_date}",
        color='Service',
        color_discrete_map=service_colors  # Apply color mapping
    )
    st.plotly_chart(fig_service_popularity)


# Tab 2: Products Overview with From and To Date Filters and Consistent Colors
with tab2:
    st.header("Products Overview")
    
    # Date range input
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("From", value=products_df['Date'].min().date(), key="product_start_date")
    with col2:
        end_date = st.date_input("To", value=products_df['Date'].max().date(), key="product_end_date")
    
    # Filter data based on selected date range
    filtered_products_df = products_df[(products_df['Date'] >= pd.to_datetime(start_date)) & (products_df['Date'] <= pd.to_datetime(end_date))]

    # Calculate total revenue by product and the overall total revenue
    total_revenue_by_product = filtered_products_df.groupby('Product')['Revenue'].sum().reset_index()
    overall_total_revenue = total_revenue_by_product['Revenue'].sum()

    # Display the overall total revenue next to the pie chart
    col1, col2 = st.columns([2, 1])
    with col1:
        # Plot the filtered Total Revenue Pie Chart with consistent colors
        fig_product_revenue = px.pie(
            total_revenue_by_product, 
            names='Product', 
            values='Revenue', 
            title=f"Total Revenue by Product from {start_date} to {end_date}",
            hole=0.3,  # Optional, for a donut-style chart
            color='Product',  # Use 'Product' as color to apply custom colors
            color_discrete_map=product_colors  # Apply color mapping
        )
        # Add custom hover information to show both percentage and amount
        fig_product_revenue.update_traces(
            textinfo='percent+label',  # Show both percentage and product label
            hovertemplate='<b>%{label}</b><br>Revenue: $%{value}<br>Percent: %{percent}'
        )
        st.plotly_chart(fig_product_revenue)

    with col2:
        # Display the overall total revenue in a text box next to the pie chart
        st.metric(label="Total Revenue", value=f"${overall_total_revenue:,.2f}")

    # Calculate most and least popular product
    if not filtered_products_df.empty:
        product_counts = filtered_products_df['Product'].value_counts()
        most_popular_product = product_counts.idxmax()
        least_popular_product = product_counts.idxmin()
    else:
        most_popular_product = "No data"
        least_popular_product = "No data"

    # Display most and least popular product as cards
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Most Popular Product", value=most_popular_product)
    with col2:
        st.metric(label="Least Popular Product", value=least_popular_product)

    # Aggregate the filtered data for the Product Sales Bar Chart
    product_sales = filtered_products_df.groupby('Product')['Quantity_Sold'].sum().reset_index()

    # Plot the filtered Product Sales Bar Chart with consistent colors
    fig_product_sales = px.bar(
        product_sales, 
        x='Product', 
        y='Quantity_Sold', 
        title=f"Product Sales from {start_date} to {end_date}",
        color='Product',  # Use 'Product' as color to apply custom colors
        color_discrete_map=product_colors  # Apply color mapping
    )
    st.plotly_chart(fig_product_sales)

import datetime

# Tab 3: Total Revenue by Month from both Services and Products
with tab3:
    st.header("Total Revenue by Month")

    # Generate a list of unique month-year options from services and products data
    all_dates = pd.concat([services_df['Date'], products_df['Date']])
    month_year_options = all_dates.dt.to_period("M").unique()
    month_year_str_options = [str(month) for month in month_year_options]

    # Month-Year dropdown for selecting a specific month
    selected_month = st.selectbox("Select Month", month_year_str_options)
    selected_period = pd.Period(selected_month, freq='M')

    # Filter data based on the selected month
    filtered_services_df = services_df[services_df['Date'].dt.to_period("M") == selected_period]
    filtered_products_df = products_df[products_df['Date'].dt.to_period("M") == selected_period]

    # Calculate total revenue for services and products in the selected month
    total_service_revenue = filtered_services_df['Revenue'].sum()
    total_product_revenue = filtered_products_df['Revenue'].sum()
    total_revenue = total_service_revenue + total_product_revenue

    # Display total revenue card with breakdown
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Service Revenue", value=f"${total_service_revenue:,.2f}")
    with col2:
        st.metric(label="Total Product Revenue", value=f"${total_product_revenue:,.2f}")
    with col3:
        st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")

    # Calculate total revenue for the year-to-date
    current_year = datetime.datetime.now().year
    year_start_date = pd.Timestamp(f"{current_year}-01-01")
    ytd_services_df = services_df[services_df['Date'] >= year_start_date]
    ytd_products_df = products_df[products_df['Date'] >= year_start_date]

    ytd_service_revenue = ytd_services_df['Revenue'].sum()
    ytd_product_revenue = ytd_products_df['Revenue'].sum()
    ytd_total_revenue = ytd_service_revenue + ytd_product_revenue

    # Display year-to-date total revenue card
    st.metric(label="Total Revenue So Far This Year", value=f"${ytd_total_revenue:,.2f}")

    # Add a "Source" column to distinguish between services and products in the combined data
    services_df['Source'] = 'Service'
    products_df['Source'] = 'Product'

    # Select only necessary columns and rename for consistency
    service_revenue = services_df[['Date', 'Revenue', 'Source']]
    product_revenue = products_df[['Date', 'Revenue', 'Source']]

    # Combine both datasets
    combined_revenue_df = pd.concat([service_revenue, product_revenue])

    # Aggregate total revenue by month
    combined_revenue_df['Month'] = combined_revenue_df['Date'].dt.to_period("M")
    monthly_revenue = combined_revenue_df.groupby(['Month', 'Source'])['Revenue'].sum().reset_index()
    monthly_revenue['Month'] = monthly_revenue['Month'].dt.to_timestamp()  # Convert Period to timestamp for plotting

    # Calculate combined total revenue per month
    combined_monthly_revenue = monthly_revenue.groupby('Month')['Revenue'].sum().reset_index()

    # Define custom color mapping for Product and Service
    color_map = {
        'Product': '#577590',
        'Service': '#F3722C'
    }

    # Plot the Total Revenue by Month, split by Source (Service vs Product) with custom colors
    fig_monthly_revenue = px.bar(
        monthly_revenue, 
        x='Month', 
        y='Revenue', 
        color='Source', 
        title="Total Revenue by Month from Services and Products",
        barmode='group',
        color_discrete_map=color_map  # Apply custom colors
    )

    # Add combined total revenue as text on top of each month
    fig_monthly_revenue.add_trace(
        px.line(combined_monthly_revenue, x='Month', y='Revenue').data[0]  # Add an invisible line to place text
    )
    fig_monthly_revenue.update_traces(text=combined_monthly_revenue['Revenue'], textposition='outside', selector=dict(type='line'))

    # Display the chart
    st.plotly_chart(fig_monthly_revenue)
