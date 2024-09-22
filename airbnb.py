import pandas as pd
import streamlit as st 
from streamlit_option_menu import option_menu
pd.set_option('display.max_columns', None)
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="AIRBNB ANALYSIS",layout="wide")
st.write("")

df = pd.read_csv(r"C:\Users\Happy\Desktop\Naren Baskar\Airbnb analysis\Airbnb_analysis")
print(df)

with st.sidebar:
    select= option_menu("Main Menu", ["Home", "Data Exploration", "About"])

if select == "Home":

    image1= Image.open(r"C:\Users\Happy\Desktop\Naren Baskar\Airbnb analysis\airbnb_image.jpg")
    st.image(image1)

    st.header("About Airbnb")
    st.write("")
    st.write('''***Airbnb is an online marketplace that connects people who want to rent out
                their property with people who are looking for accommodations,
                typically for short stays. Airbnb offers hosts a relatively easy way to
                earn some income from their property.Guests often find that Airbnb rentals
                are cheaper and homier than hotels.***''')
    st.write("")
    st.write('''***Airbnb is a web-based platform that connects travelers with people who want to rent out their homes, apartments, and other properties.
                The company was founded in 2007 by Brian and Joe and started as a place for owners to rent out a spare room or their entire home. Today, Airbnb also allows professional accommodation providers like boutique hotels, serviced apartments, and B&Bs to create listings. 
                Airbnb's name comes from its original name, Airbed & Breakfast. The company's business model is based on the sharing economy, and Airbnb takes a cut from every stay. Hosts pay a fee of approximately 3% of the amount they take in, and guest fees typically max out at 14.2%. 
                Travelers can use filters to search for accommodations that's right for them, such as number of bedrooms, location, and price. Airbnb also establishes trust by asking both guests and hosts to review each other, which creates a rating system for all listings.***''')


# Data Exploration tab
if select == "Data Exploration":
    # Define tabs for data exploration
    tabs = st.tabs(["PRICE ANALYSIS", "AVAILABILITY ANALYSIS", "LOCATION BASED", "GEOSPATIAL VISUALIZATION", "TOP CHARTS"])

    # Price Analysis tab
    with tabs[0]:
        st.title("PRICE DIFFERENCE")
        col1, col2 = st.columns(2)

        with col1:
            # Country selection and filtering
            country = st.selectbox("Select the Country", df["country"].unique(), key='country_selectbox')
            df_country = df[df["country"] == country]

            # Room type selection and filtering
            room_type = st.selectbox("Select the Room Type", df_country["room_type"].unique(), key='room_type_selectbox')
            df_room = df_country[df_country["room_type"] == room_type]

            # Bar chart for price by property type
            df_bar = df_room.groupby("property_type")[["price", "review_scores", "number_of_reviews"]].sum().reset_index()
            fig_bar = px.bar(df_bar, x='property_type', y='price', title="PRICE FOR PROPERTY TYPES",
                            hover_data=["number_of_reviews", "review_scores"],
                            color_discrete_sequence=px.colors.sequential.Redor_r, width=600, height=500)
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            # Property type selection and filtering
            property_type = st.selectbox("Select the Property Type", df_room["property_type"].unique(), key='property_type_selectbox_price')
            df_property = df_room[df_room["property_type"] == property_type]

            # Pie chart for price difference based on host response time
            df_pie = df_property.groupby("host_response_time")[["price", "bedrooms"]].sum().reset_index()
            fig_pie = px.pie(df_pie, values="price", names="host_response_time", hover_data=["bedrooms"],
                            color_discrete_sequence=px.colors.sequential.BuPu_r,
                            title="PRICE DIFFERENCE BASED ON HOST RESPONSE TIME", width=600, height=500)
            st.plotly_chart(fig_pie, use_container_width=True)

            # Filter by host response time and create additional charts
            host_response_time = st.selectbox("Select the Host Response Time", df_property["host_response_time"].unique(), key='host_response_time_selectbox')
            df_host = df_property[df_property["host_response_time"] == host_response_time]

            # Bar chart for minimum and maximum nights
            df_nights = df_host.groupby("bed_type")[["minimum_nights", "maximum_nights", "price"]].sum().reset_index()
            fig_nights = px.bar(df_nights, x='bed_type', y=['minimum_nights', 'maximum_nights'],
                            title='MINIMUM NIGHTS AND MAXIMUM NIGHTS', hover_data="price",
                            barmode='group', color_discrete_sequence=px.colors.sequential.Rainbow, width=600, height=500)
            st.plotly_chart(fig_nights, use_container_width=True)

            # Bar chart for bedrooms, beds, and accommodates
            df_beds = df_host.groupby("bed_type")[["bedrooms", "beds", "accommodates", "price"]].sum().reset_index()
            fig_beds = px.bar(df_beds, x='bed_type', y=['bedrooms', 'beds', 'accommodates'],
                            title='BEDROOMS AND BEDS ACCOMMODATES', hover_data="price",
                            barmode='group', color_discrete_sequence=px.colors.sequential.Rainbow_r, width=600, height=500)
            st.plotly_chart(fig_beds, use_container_width=True)

    # Availability Analysis tab
    with tabs[1]:
        st.title("AVAILABILITY ANALYSIS")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            # Country selection and filtering
            country_avail = st.selectbox("Select the Country", df["country"].unique(), key='country_selectbox_avail')
            df_country_avail = df[df["country"] == country_avail]

            # Property type selection and filtering
            property_type = st.selectbox("Select the Property Type", df_country_avail['property_type'].unique(), key='property_type_selectbox_avail')
            df_property_type = df_country_avail[df_country_avail['property_type'] == property_type]

            # Sunburst chart for availability in 30 days
            fig_sunburst_30 = px.sunburst(df_property_type, path=["room_type", "bed_type", "is_location_exact"],
                                        values="availability_30", width=600, height=500,
                                        title="Availability in 30 Days", color_discrete_sequence=px.colors.sequential.Peach_r)
            st.plotly_chart(fig_sunburst_30, use_container_width=True)

        with col2:
            # Sunburst chart for availability in 60 days
            fig_sunburst_60 = px.sunburst(df_property_type, path=["room_type", "bed_type", "is_location_exact"],
                                        values="availability_60", width=600, height=500,
                                        title="Availability in 60 Days", color_discrete_sequence=px.colors.sequential.Peach_r)
            st.plotly_chart(fig_sunburst_60, use_container_width=True)

        with col3:
            # Sunburst chart for availability in 90 days
            fig_sunburst_90 = px.sunburst(df_property_type, path=["room_type", "bed_type", "is_location_exact"],
                                        values="availability_90", width=600, height=500,
                                        title="Availability in 90 Days", color_discrete_sequence=px.colors.sequential.Peach_r)
            st.plotly_chart(fig_sunburst_90, use_container_width=True)

        with col4:
            # Sunburst chart for availability in 365 days
            fig_sunburst_365 = px.sunburst(df_property_type, path=["room_type", "bed_type", "is_location_exact"],
                                        values="availability_365", width=600, height=500,
                                        title="Availability in 365 Days", color_discrete_sequence=px.colors.sequential.Peach_r)
            st.plotly_chart(fig_sunburst_365, use_container_width=True)

            # Room type selection for further analysis
            room_type_selection = st.selectbox("Select the Room Type", df_property_type["room_type"].unique(), key='room_type_selectbox_avail')
            df_room_a = df_property_type[df_property_type["room_type"] == room_type_selection]

            # Bar chart for availability based on host response time
            df_availability = df_room_a.groupby("host_response_time")[["availability_30", "availability_60", "availability_90", "availability_365", "price"]].sum().reset_index()
            fig_availability = px.bar(df_availability, x='host_response_time', y=['availability_30', 'availability_60', 'availability_90', 'availability_365'],
                                    title='Availability Based on Host Response Time', hover_data="price",
                                    barmode='group', color_discrete_sequence=px.colors.sequential.Rainbow_r, height=500, width=600)
            st.plotly_chart(fig_availability, use_container_width=True)
    # location tab        
    with tabs[2]:
        st.title("LOCATION ANALYSIS")
        
        # Selecting country and property type
        country_l = st.selectbox("Select the country",df["country"].unique())
        country_loc = df[df['country']==country_l]
        
        property_p = st.selectbox("select the property type",country_loc['property_type'].unique())
        property_type_loc = country_loc[country_loc['property_type']==property_p]
        
        # Create a scatter plot on a map
        fig = px.scatter_mapbox(
            property_type_loc,
            lat='latitude',
            lon='longitude',
            color='price',
            size='price',
            hover_name='property_type',
            mapbox_style='open-street-map', 
            title=f"Scatter Map for Property Type: {property_p}",
            color_continuous_scale=px.colors.cyclical.IceFire,
            size_max=15
        )

        # Show the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    
    # GEOSPATIAL VISUALIZATION   
    with tabs[3]:
        st.title("GEOSPATIAL VISUALIZATION")
        fig_geo = px.scatter_mapbox(
            df,
            lat='latitude',
            lon='longitude',
            color='price',
            size='price',
            hover_name='property_type',
            mapbox_style='open-street-map',  
            title=f"GEOSPATIAL VISUALIZATION",
            color_continuous_scale=px.colors.cyclical.IceFire,
            size_max=15
        )

        # Show the plot in Streamlit
        st.plotly_chart(fig_geo, use_container_width=True)
        
    with tabs[4]:
        st.title("TOP CHARTS")
        
        # Top 10 properties by price
        top_properties = df.nlargest(10, 'price')
        fig_top_properties = px.bar(top_properties, x='property_type', y='price', title='Top 10 Properties by Price',
                                    color_discrete_sequence=px.colors.sequential.Plasma, width=800, height=500)
        st.plotly_chart(fig_top_properties)

        # Top 10 properties by number of reviews
        top_reviews = df.nlargest(10, 'number_of_reviews')
        fig_top_reviews = px.bar(top_reviews, x='property_type', y='number_of_reviews', title='Top 10 Properties by Number of Reviews',
                                    color_discrete_sequence=px.colors.sequential.Viridis, width=800, height=500)
        st.plotly_chart(fig_top_reviews)

        # Top 10 properties by review scores
        top_reviews_scores = df.nlargest(10, 'review_scores')
        fig_top_reviews_scores = px.bar(top_reviews_scores, x='property_type', y='review_scores', title='Top 10 Properties by Review Scores',
                                        color_discrete_sequence=px.colors.sequential.Inferno, width=800, height=500)
        st.plotly_chart(fig_top_reviews_scores)
        
# About tab
if select == "About":
    st.header("About This Application")
    st.write("""
                ***An Airbnb analysis project typically involves exploring and visualizing data
                from Airbnb listings to uncover insights about pricing, availability, property types, and user reviews.
                The goal is often to make data-driven decisions, improve user experience, or offer recommendations based on the analysis***.
  
    """)

    
    
    
 