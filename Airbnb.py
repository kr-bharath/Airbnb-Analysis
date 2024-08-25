#Libraries
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import time

#Setting page configuration
st.set_page_config(page_title= "Airbnb Analysis",
                   layout= "wide",initial_sidebar_state='expanded')
st.markdown("<h1 style='text-align: center; color: #ff5a5f;'>Airbnb Analysis</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: right;'>"
    "<span style='color: #ff5a5f;'>Domain:</span> Travel, Property and Tourism"
    "</h3>", 
    unsafe_allow_html=True)

# CREATING OPTION MENU
selected = option_menu(None, ["HOME","EXPLORE","EDA","TOP INSIGHTS"], 
                       icons=["house","binoculars","search","lightbulb"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"container": {"padding": "0!important", "background-color": "#fafafa","width": "100%","text-align": "center","margin": "0 auto"},
                               "icon": {"color": "#ff5a5f", "font-size": "20px"},
                               "nav-link": {"font-size": "20px", "text-align": "center", "margin":"0px", "--hover-color": "#eee","padding": "10px 20px"},
                               "nav-link-selected": {"background-color": "#6495ED","color": "white","border-radius": "5px","padding": "10px 20px"}})
df = pd.read_csv("D:\Data Science\Airbnb_data.csv")

if selected == "HOME":

    st.markdown("<h1 style='text-align: center; color: #ff5a5f;'>Airbnb Analysis</h1>", unsafe_allow_html=True)

    st.subheader(":red[**Project Overview:**]")
    st.markdown('''The Airbnb Analysis project explores insights from a comprehensive dataset using data science techniques, tools, 
                and aims to uncover trends, patterns, and valuable insights in the hospitality and travel sector through Airbnb listings data.''')
    
    st.subheader(""" :red[**Key Objectives:**]
                 
    - Utilize MongoDB Atlas for efficient data storage and retrieval, enhancing skills in NoSQL database management.
    - Analyze pricing dynamics and availability patterns across various regions and property types.
    - Implement geospatial analysis to visualize the distribution and clustering of Airbnb listings.
    - Employ Python and Pandas for data cleaning, analysis, and visualization tasks.
    - Develop interactive web applications using Streamlit for intuitive data exploration and visualization.
    - Create dynamic dashboards using tools like Tableau or Power BI to present insights effectively.
    - Foster collaboration and project management skills through the end-to-end development of the project, focusing on task planning, coordination, and timely delivery of milestones.""")

    st.subheader(""" :red[**Learning Outcomes:**]
    
    - Gain proficiency in MongoDB Atlas for scalable data storage and retrieval.
    - Master data cleaning techniques for maintaining data quality and consistency.
    - Apply geospatial analysis techniques to understand spatial patterns in Airbnb listings.
    - Enhance Python data analysis skills for effective manipulation and visualization of datasets.
    - Develop user-friendly web applications with Streamlit for interactive data exploration.
    - Hone problem-solving skills by extracting actionable insights from complex datasets.
    - Foster data-driven decision-making through visualizations and analytical findings.
    - Strengthen collaboration and project management abilities in a real-world data science project context.""")

    st.subheader(':red[**Conclusion :**]')
    st.markdown('''
    This project not only deepens understanding of Airbnb's operational dynamics but also equips with practical skills 
    in data management, analysis, and visualization.''')

if selected == "EXPLORE":
    st.title("Geospatial Visualization")

    # Create a select box to choose a country
    unique_countries = sorted(["ALL COUNTRIES"] + sorted(df["country"].unique()))
    country = st.selectbox("Select the Country", unique_countries, key="country6")

    # Create a select box to choose a property type
    unique_property_types = sorted(["ALL PROPERTY TYPES"] + sorted(df["property_type"].unique()))
    property_type = st.selectbox("Select the Property Type", unique_property_types, key="property_type3")

    # Filter the DataFrame based on the selected country
    if country == "ALL COUNTRIES":
        df_selected_country = df.copy() 
    else:
        df_selected_country = df[df["country"] == country]
        
    if property_type != "ALL PROPERTY TYPES":
        df_selected_country = df_selected_country[df_selected_country["property_type"] == property_type]

    df_selected_country.reset_index(drop=True, inplace=True)
    # Set initial zoom level and center coordinates as world map view
    center_lat = 0
    center_lon = 0
    zoom_level = 1  # Low zoom level for a world view

    # Adjust center coordinates and zoom level if a specific country is selected
    if country != "ALL COUNTRIES" and not df_selected_country.empty:
        center_lat = df_selected_country['latitude'].mean()
        center_lon = df_selected_country['longitude'].mean()
        zoom_level = 3  
    # Create the scatter mapbox plot

    fig = px.scatter_mapbox(df_selected_country,lat='latitude',lon='longitude',hover_name="name",hover_data={"price": True, "room_type": True},
                             size_max=15,color='room_type',
                             color_discrete_map={'Entire home/apt': 'red', 'Private room': 'blue', 'Shared room': 'Green'},
                             zoom=zoom_level,  # Set initial zoom level
                             center=dict(lat=center_lat, lon=center_lon))

    fig.update_layout(mapbox_style="open-street-map",
                       mapbox_zoom=zoom_level,  # Update zoom level
                       mapbox_center=dict(lat=center_lat, lon=center_lon)) 
    fig.update_layout(title=f'{country} view of total hotel listings' if country != "ALL COUNTRIES" else 'Global view of total hotel listings in every countries',
                       height=800, width=1150)

    st.plotly_chart(fig,use_container_width=True)

if selected == "EDA":
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["CATEGORICAL ANALYSIS", "PRICE ANALYSIS", "AVAILABILITY ANALYSIS",
                                                  "HOST ANALYSIS", "CORRELATION ANALYSIS"])

    with tab1:
        st.title("Categorical Analysis")

        col1, col2, col3 = st.columns([5, 1, 5])
        with col1:
            # Create a select box to choose a country
            country_list = sorted(["ALL COUNTRIES"] + sorted(df["country"].unique()))
            country_1 = st.selectbox("Select the Country", country_list, key="country1")
            # Filter the DataFrame based on the selected country
            if country_1 == "ALL COUNTRIES":
                df_country_1 = df.copy()  # Select all countries
            else:
                df_country_1 = df[df["country"] == country_1]  # Filter based on selected country
            # Reset the index of the filtered DataFrame
            df_country_1.reset_index(drop=True, inplace=True)

            # Group by Room Type
            df_country_1_room = pd.DataFrame(df_country_1.groupby("room_type")[["host_listings_count"]].sum())
            df_country_1_room.reset_index(inplace= True)
            df_country_1_room.index +=1
            st.dataframe(df_country_1_room)

        with col3:
            # Bar chart - Room Type & Host Listing Count        
            fig_bar_1 = px.bar(df_country_1_room, x='host_listings_count', y= "room_type", title= "Room Type & Host Listing Count",
                    hover_data=["host_listings_count"],color='room_type', width=400, height=500)
            fig_bar_1.update_layout(xaxis_title="Total Host Listing Count",yaxis_title="Room Type")
            st.plotly_chart(fig_bar_1, use_container_width=True)

        col1,col2,col3 = st.columns([3,1,6])
        with col1:
            # Create a select box to choose a Property Type
            property_types = ["All Property Types"] + sorted(df_country_1["property_type"].unique())
            property_type_1 = st.selectbox("Select the Property Type", property_types, key="property1")
            # Filter the DataFrame based on the selected property type
            if property_type_1 == "All Property Types":
                df_country_1_property = df_country_1.copy()  # Select all property types
            else:
                df_country_1_property = df_country_1[df_country_1["property_type"] == property_type_1]
            # Group by Market
            df_country_1_property_market = pd.DataFrame(df_country_1_property.groupby("market")[["host_listings_count"]].sum())
            df_country_1_property_market.reset_index(inplace= True)
            # Sort the Group by Market
            df_country_1_property_market_sorted = df_country_1_property_market.sort_values(by="host_listings_count", ascending=False)
            df_country_1_property_market_sorted.reset_index(drop=True, inplace=True)
            df_country_1_property_market_sorted.index += 1
            st.dataframe(df_country_1_property_market_sorted)
            
        with col3:
            # Bar chart - Market & Host Listing Count
            fig_bar_3 = px.bar(df_country_1_property_market_sorted, x='host_listings_count', y="market", title="Market & Host Listing Count",
                                hover_data=["host_listings_count"],color= "market")
            fig_bar_3.update_layout(xaxis_title="Total Host Listing Count",yaxis_title="Market")
            st.plotly_chart(fig_bar_3, use_container_width=True)

        # Pie chart - Cancellation Policy
        cancellation_counts_df = pd.DataFrame(df['cancellation_policy'].value_counts().reset_index(), columns=['cancellation_policy', 'count'])
        fig = px.pie(cancellation_counts_df, values='count', names='cancellation_policy',
                    title='Distribution of Cancellation Policies', color_discrete_sequence=px.colors.sequential.Viridis_r)
        fig.update_traces(textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        with tab2:
            st.title("Price Analysis")
        # Scatter Plot - Price and Country
        fig_country_price = px.scatter(df, x='price', y='country', title='Comparison of Price and Country', color='country')
        st.plotly_chart(fig_country_price, use_container_width=True)

        col1, col2,col3 = st.columns([5,1,5])
        with col1:
            # Create a select box to choose a country
            country_list = sorted(["ALL COUNTRIES"] + sorted(df["country"].unique()))
            country_2 = st.selectbox("Select the Country", country_list, key="country2")
            # Filter the DataFrame based on the selected country
            if country_2 == "ALL COUNTRIES":
                df_country_2 = df.copy()  
            else:
                df_country_2 = df[df["country"] == country_2] 
            # Group by Room Type
            df_country_2_room = pd.DataFrame(df_country_2.groupby("room_type")["price"].mean())
            df_country_2_room.reset_index(inplace= True)
            # Bar Chart - Room Type & Average Price($)
            fig_bar_3 = px.bar(df_country_2_room, x='room_type', y= "price", title= "Room Type & Average Price($)",hover_data=["price"], color= "room_type")
            st.plotly_chart(fig_bar_3, use_container_width=True) 

        with col3:
            # Create a select box to choose a Room Type
            room_types_2 = ["All Room Types"] + sorted(df_country_2["room_type"].unique())
            room_type_2 = st.selectbox("Select the Room Type",room_types_2, key="room2")
            # Filter the DataFrame based on the selected Room Type
            if room_type_2 == "All Room Types":
                df_country_2_room = df_country_2.copy()
            else:
                df_country_2_room= df_country_2[df_country_2["room_type"] == room_type_2]
            df_country_2_room.reset_index(drop= True, inplace= True)
            # Group by Property Type
            df_bar = pd.DataFrame(df_country_2_room.groupby("property_type")["price"].mean())
            df_bar.reset_index(inplace= True)
            # Bar Chart - Property Type & Average Price($)
            fig_bar_4 = px.bar(df_bar, y='property_type', x = "price", title= "Property Type & Average Price($)",hover_data=["price"], color ="price")
            st.plotly_chart(fig_bar_4, use_container_width=True) 

        col1, col2,col3 = st.columns([5,1,5])
        with col1:
            # Group by Country   
            country_prices = df_country_2.groupby('country')[['price', 'security_deposit', 'cleaning_fee']].mean()      
            country_prices.reset_index(inplace= True)
            # Bar Chart - Comparison of Price, Security Deposit, and Cleaning Fee by Country
            fig_country_price = px.bar(country_prices, y='country', x=['price', 'security_deposit', 'cleaning_fee'], 
                                    title='Comparison of Price, Security Deposit, and Cleaning Fee by Country', 
                                    barmode='group',color_discrete_sequence=px.colors.sequential.Electric_r)
            st.plotly_chart(fig_country_price, use_container_width=True)

        with col3: 
            # Group by Market      
            country_prices_1 = df_country_2.groupby('market')[['price', 'security_deposit', 'cleaning_fee']].mean()      
            country_prices_1.reset_index(inplace= True)
            # Bar Chart - Comparison of Price, Security Deposit, and Cleaning Fee by Market
            fig_con_price_1 = px.bar(country_prices_1, y='market', x=['price', 'security_deposit', 'cleaning_fee'], 
                                    title='Comparison of Price, Security Deposit, and Cleaning Fee by Market', 
                                    barmode='group',color_discrete_sequence=px.colors.sequential.Rainbow_r)
            st.plotly_chart(fig_con_price_1, use_container_width=True)

    with tab3:
        st.title("Availability Analysis")

        country_list = sorted(["ALL COUNTRIES"] + sorted(df["country"].unique()))
        country_5 = st.selectbox("Select the Country", country_list, key="country5")
        if country_5 == "ALL COUNTRIES":
            df1_a = df.copy()  # Select all countries
        else:
            df1_a = df[df["country"] == country_5]
        df1_a.reset_index(drop=True, inplace=True)

        property_types = ["All Property Types"] + sorted(df_country_1["property_type"].unique())
        property_type_2 = st.selectbox("Select the Property Type", property_types, key="property2")

        if property_type_2 == "All Property Types":
            df2_a = df1_a.copy()  # Select all property
        else:
            df2_a = df1_a[df1_a["property_type"] == property_type_2]
        df2_a.reset_index(drop=True, inplace=True)

        col1,col2= st.columns(2)

        with col1:

            df_a_sunb_30= px.sunburst(df2_a, path=["room_type","bed_type","host_response_time"], values="availability_30",width=600,height=500,title="Availability_30",color_discrete_sequence=px.colors.sequential.Peach_r)
            st.plotly_chart(df_a_sunb_30)
        
        with col2:
            df_a_sunb_60 = px.sunburst(df2_a, path=["room_type", "bed_type", "host_response_time"], values="availability_60", width=600, height=500, title="Availability_60", color_discrete_sequence=px.colors.sequential.Blues_r)
            st.plotly_chart(df_a_sunb_60)

        col1,col2= st.columns(2)

        with col1:
            
            df_a_sunb_90= px.sunburst(df2_a, path=["room_type","bed_type","host_response_time"], values="availability_90",width=600,height=500,title="Availability_90",color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
            st.plotly_chart(df_a_sunb_90)

        with col2:

            df_a_sunb_365= px.sunburst(df2_a, path=["room_type","bed_type","host_response_time"], values="availability_365",width=600,height=500,title="Availability_365",color_discrete_sequence=px.colors.sequential.Greens_r)
            st.plotly_chart(df_a_sunb_365)

        # Create a select box to choose a country
        country_list = sorted(["ALL COUNTRIES"] + sorted(df["country"].unique()))
        country_3 = st.selectbox("Select the Country", country_list, key="country3")
        # Filter the DataFrame based on the selected country
        if country_3 == "ALL COUNTRIES":
            df_country_3 = df.copy()  
        else:
            df_country_3 = df[df["country"] == country_3]  
        # Create a select box to choose a Room Type
        roomtype_list = sorted(["ALL ROOM TYPES"] + sorted(df["room_type"].unique()))
        roomtype_3 = st.selectbox("Select the Room Type",roomtype_list,key = "room3")
        # Filter the DataFrame based on the selected room type
        if roomtype_3 == "ALL ROOM TYPES":
            df_roomtype_3 = df_country_3.copy()  
        else:
            df_roomtype_3 = df_country_3[df_country_3["room_type"] == roomtype_3]
        # Group by Host Response Time
        df_roomtype_3_avail = pd.DataFrame(df_roomtype_3.groupby("host_response_time")[["availability_30","availability_60","availability_90","availability_365","price"]].sum())
        df_roomtype_3_avail.reset_index(inplace= True)
        # Bar Chart - Availability Based on Host Response Time
        fig_roomtype_3_avail = px.bar(df_roomtype_3_avail, x='host_response_time', 
                                      y=['availability_30', 'availability_60', 'availability_90', "availability_365"], 
        title='Availability Based on Host Response Time', barmode='group',color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_roomtype_3_avail, use_container_width=True)

    with tab4:
        st.title("Host Analysis")
        # Create a select box to choose a country
        country_4= st.selectbox("Select the Country",sorted(df["country"].unique()))

        df1_l= df[df["country"] == country_4]
        df1_l.reset_index(drop= True, inplace= True)
        # Top 10 most reviewed hosts based on selected country
        host_most_reviewed=df.groupby(['host_name','country'])['total_reviews'].max().reset_index()
        reviewed = host_most_reviewed.sort_values(by='total_reviews', ascending=False)
        reviewed.reset_index(drop= True, inplace= True)
        # Bar Chart - Top 10 most reviewed hosts
        fig_top_10_host_rated = px.bar(reviewed[reviewed['country'] == f'{country_4}'].head(10), y='total_reviews', x='host_name', title=f'Top 10 most reviewed hosts in {country_4} ',hover_data=["total_reviews"],color = 'host_name')
        fig_top_10_host_rated.update_layout(xaxis_title='Host Name',yaxis_title='Total Reviews',yaxis_categoryorder='total ascending')
        st.plotly_chart(fig_top_10_host_rated, use_container_width=True)

        # Top 10 host listing counts based on location
        host=df.groupby(['host_name','country'])['host_listings_count'].max().reset_index()
        top_10_host=host.sort_values(by='host_listings_count',ascending=False).head(10)
        top_10_host.reset_index(drop= True, inplace= True)
        # Bar Chart - Top 10 Host Listings
        fig_top_10_host = px.bar(top_10_host, y='host_name', x='host_listings_count', title='Top 10 host who has most listing counts',hover_data=["host_listings_count"],color = 'host_name')
        fig_top_10_host.update_layout(xaxis_title='Host Listings Count',yaxis_title='Host Name',yaxis_categoryorder='total ascending')
        st.plotly_chart(fig_top_10_host, use_container_width=True)

        col1, col2,col3 = st.columns([5,1,5])
        with col1:
            # Count occurrences of 'Yes' and 'No' in the 'host_is_superhost' column
            superhost_counts = df['host_is_superhost'].value_counts().reset_index()
            superhost_counts.columns = ['host_is_superhost', 'Count']

            # Pie Chart - Superhosts
            fig_superhost_pie = px.pie(superhost_counts, values='Count',  names='host_is_superhost',  
                                    title='Distribution of Superhosts (Yes/No)')  
            st.plotly_chart(fig_superhost_pie, use_container_width=True)

        with col3:
            # Create a select box to choose a country
            country_list = sorted(["ALL COUNTRIES"] + sorted(df["country"].unique()))
            country_4 = st.selectbox("Select the Country", country_list, key="country4")

            # Filter the DataFrame based on the selected country
            if country_4 == "ALL COUNTRIES":
                df_country_4 = df.copy()  
            else:
                df_country_4 = df[df["country"] == country_4] 

            df_country_4.reset_index(drop=True, inplace=True)

            # Count number of 'yes' superhosts in each market
            df_yes = df_country_4[df_country_4['host_is_superhost'] == 'Yes']
            df_yes_count = df_yes.groupby('country').size().reset_index(name='Yes')

            # Count number of 'no' superhosts in each market
            df_no = df_country_4[df_country_4['host_is_superhost'] == 'No']
            df_no_count = df_no.groupby('country').size().reset_index(name='No')

            # Merge DataFrames
            df_merged = df_yes_count.merge(df_no_count, on='country', how='outer').fillna(0)

            # Bar Chart - Number of Superhosts (Yes/No) in Each Country 
            fig_superhost = px.bar(df_merged, x='country', y=['Yes', 'No'], 
                                    title='Number of Superhosts (Yes/No) in Each Country', 
                                    barmode='group', color_discrete_sequence=px.colors.sequential.Rainbow_r)
            st.plotly_chart(fig_superhost, use_container_width=True)

    with tab5:
        st.title("Correlation Analysis")

        selected_columns=['_id','minimum_nights','maximum_nights','accommodates','bedrooms','bathrooms','price','security_deposit','cleaning_fee','extra_people','guests_included','host_response_rate','total_reviews','rating']
        corr = df[selected_columns].corr()
        plt.figure(figsize=(12, 6))
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm')
        plt.title('Correlation Matrix of Airbnb Numerical Listing Features', fontsize=16)
        st.pyplot(plt)

if selected == "TOP INSIGHTS":

    opt = ["Top 10 Expensive Hotel rooms",
           "Top 10 Affordable Hotel Rooms",
           "Total Count of Hotels Listed in Every Countries",
           "10 Leading Host Names with Highest Host Listings",
           "Hotel Counts with Top most Ratings",
           "Toprated 10 host who has Most Reviews",
           "Average Availability of Hotel Rooms in Every Countries per month"]

    st.markdown('<div style="color: #ff5a5f; font-weight: bold;">Select the insight you want to see</div>', unsafe_allow_html=True)
    query = st.selectbox('', options=opt, index=0)

    def stream_text(text):
        for char in text:
            yield char
            time.sleep(0.02)

    if query == opt[0]:
        col1, col2 = st.columns(2)

        with col1:
            top_10_expensive = df[['name', 'price', 'country']].sort_values(by="price", ascending=False).head(10)
            top_10_expensive.reset_index(drop=True, inplace=True)

            fig1 = px.bar(top_10_expensive, x='name', y='price',
                         labels={'name': 'Hotel Name', 'price': 'Price'},
                         title='Top 10 Expensive Hotel Rooms',
                         color='country', color_continuous_scale='rainbow')
            fig1.update_layout(xaxis_title='Hotel Name', yaxis_title='Price')
            st.plotly_chart(fig1, use_container_width=True)

            st.write('<div style="color: #ff5a5f; font-weight: bold;">Top 3 expensive hotel rooms in the world are:</div>', unsafe_allow_html=True)
            
            detailed_descriptions = [
                "1. Turkey: 'Center of Istanbul Sisli' stands out as the most expensive accommodation with a price of 48,842 Turkish Lira, reflecting its prime location in the heart of Istanbul's vibrant Sisli district.",
                "2. Hong Kong: The city boasts several high-priced accommodations, including 'HS1-2人大床房+丰泽､苏宁､百脑汇+女人街+美食中心' and '良德街3号温馨住宅' priced at 11,681 Hong Kong Dollars each, suggesting a strong demand.",
                "3. Brazil: Not to be outdone, Brazil features luxurious accommodations like 'Apartamento de luxo em Copacabana - 4 quartos' and 'Deslumbrante apartamento na AV.Atlantica' with prices exceeding 6,000 Brazilian Reais."]
            
            for description in detailed_descriptions:
                st.write_stream(stream_text(description))
        
        with col2:

            st.write('')
            st.dataframe(top_10_expensive, hide_index=True)
                
    elif query == opt[1]:
        col1, col2 = st.columns(2)

        with col1:
            top_10_affordable = df[['name', 'price', 'country']].sort_values(by="price").head(10)
            top_10_affordable.reset_index(drop=True, inplace=True)

            fig3 = px.bar(top_10_affordable, x='name', y='price',
                         labels={'name': 'Hotel Name', 'price': 'Price'},
                         title='Top 10 Affordable Hotel Rooms',
                         color='country', color_continuous_scale='viridis')
            fig3.update_layout(xaxis_title='Hotel Name', yaxis_title='Price')
            st.plotly_chart(fig3, use_container_width=True)
            
            st.write('<div style="color: #ff5a5f; font-weight: bold;">Top 3 affordable hotel rooms in the world are:</div>', unsafe_allow_html=True)

            detailed_descriptions = [
                "1. Among the top 10 Affordable Hotel Rooms, the most budget-friendly options are found in Portugal and Spain.",
                "2. Portugal offers the most affordable accommodations, with prices ranging from 9 to 13 dollars.",
                "3. Spain also provides reasonably priced options, with room rates ranging from 10 to 12 dollars."]
            
            for description in detailed_descriptions:
                st.write_stream(stream_text(description))

        with col2:

            st.write('')
            st.dataframe(top_10_affordable, hide_index=True)

    elif query == opt[2]:

            hotel_count = df['country'].value_counts().reset_index()
            hotel_count.columns = ['country', 'count']

            fig5 = px.bar(hotel_count, x='country', y='count',
                            color='country',color_continuous_scale='viridis',
                            labels={'country': 'Country', 'count': 'Number of Hotels'},
                            title='Number of Hotels per Country')
            fig5.update_layout(xaxis_title='Country', yaxis_title='Count')
            st.plotly_chart(fig5,use_container_width=True)

            st.write('<div style="color: #ff5a5f; font-weight: bold;">Top 3 countries with Maximum number of Hotels:</div>', unsafe_allow_html=True)
            
            detailed_descriptions = [
            "1. United States Tops the list with 1222 Hotel Rooms",
            "2. Turkey follows Us with 661 Rooms",
            "3. Canada follows Turkey in the list with 649 Rooms"]

            for description in detailed_descriptions:
                st.write_stream(stream_text(description))

    elif query == opt[3]:

        host=df.groupby(['host_name','country'])['host_listings_count'].max().reset_index()
        top_10_host=host.sort_values(by='host_listings_count',ascending=False).head(10)
        top_10_host.reset_index(drop= True, inplace= True)

        fig_top_10_host = px.bar(top_10_host, y='host_name', x='host_listings_count', title='Top 10 host who has most listing counts',hover_data=["host_listings_count"],color = 'host_name')
        fig_top_10_host.update_layout(xaxis_title='Host Listings Count',yaxis_title='Host Name',yaxis_categoryorder='total ascending')
        st.plotly_chart(fig_top_10_host, use_container_width=True)

        st.write('<div style="color: #ff5a5f; font-weight: bold;">Top 3 Host Names with Maximum Listing Counts:</div>', unsafe_allow_html=True)
        
        detailed_descriptions = [
        "1. Sonder Tops the list with 1198 Listing Counts",
        "2. Kara with 799 Listing Counts",
        "3. Claudia in the list with 508 Listing Counts"]

        for description in detailed_descriptions:
                st.write_stream(stream_text(description))

    elif query == opt[4]:

            rating_counts = df['rating'].value_counts().reset_index()
            rating_counts.columns = ['Rating', 'Count']

            sorted_df=rating_counts.sort_values(by="Rating", ascending=False)

            top_10_ratings = sorted_df.head(10).reset_index(drop=True)

            # Plotting hotel count by rating using Plotly bar chart
            fig = px.bar(top_10_ratings, x='Rating', y='Count',
                            labels={'Rating': 'Rating', 'Count': 'Hotel Count'},
                            title='Hotel Counts with Top most Ratings',
                            color='Rating',color_continuous_scale='thermal')

            fig.update_layout(xaxis_title='Rating', yaxis_title='Hotel Count')
            st.plotly_chart(fig,use_container_width=True)

            st.write('<div style="color: #ff5a5f; font-weight: bold;">Top 3 Ratings with Maximum Hotel Counts:</div>', unsafe_allow_html=True)

            detailed_descriptions=[
            "1. There are 982 Hotels listed with 100 rating rate",
            "2. There are 188 Hotels listed with 98 rating rate",
            "3. There are 291 Hotels listed with 97 rating rate"]

            for description in detailed_descriptions:
                st.write_stream(stream_text(description))
            

    elif query == opt[5]:

        col1,col2=st.columns(2)
        with col1:           

            host_most_reviewed=df.groupby(['host_name','host_location','property_type'])['total_reviews'].max().reset_index()
            top_10_review=host_most_reviewed.sort_values(by='total_reviews',ascending=False).head(10)

            # Create the bar chart
            fig = px.bar(top_10_review, x='host_name', y='total_reviews',
                        labels={'host_name': 'Host Name', 'total_reviews': 'Total Reviews'},
                        title='Top 10 Hosts with Most Reviews',
                        color='host_name',
                        color_continuous_scale='Viridis')

            fig.update_layout(xaxis_title='Host Name', yaxis_title='Total Reviews')

            st.plotly_chart(fig,use_container_width=True)

            st.write('<div style="color: #ff5a5f; font-weight: bold;">Top 3 Host Names with Maximum Reviews:</div>', unsafe_allow_html=True)

            detailed_descriptions =[
            "1. Dana's condominium in the beautiful location of Honolulu, Hawaii, United States, stands out as the most reviewed property, with 533 reviews.",
            "2. Shuang's guest suite in New South Wales, Australia, has garnered a substantial 469 reviews.",
            "3. Julián's apartment in Barcelona, Cataluña, Spain, has accumulated 463 reviews, reflecting its popularity among travelers."]

            for description in detailed_descriptions:
                st.write_stream(stream_text(description))

        with col2:

            st.write('')
            st.dataframe(top_10_review,hide_index=True)

    elif query == opt[6]:

        col1,col2=st.columns(2)

        with col1:

            columns=df[['country','availability_30']]

            df=pd.DataFrame(columns)

            avg_availability_by_country = df.groupby('country')['availability_30'].mean().reset_index()
            avg_availability_by_country['availability_30'] = avg_availability_by_country['availability_30'].round(2)
            df1= avg_availability_by_country.sort_values(by='availability_30', ascending=False).head(10)

            fig = px.pie(df1, names='country', values='availability_30',
                            color='availability_30',color_discrete_sequence=px.colors.sequential.Rainbow_r,  
                            labels={'availability_30': 'Average Availability'},
                            title=("Average Avilability of Hotel Rooms in Every Countries per month"))
            st.plotly_chart(fig,use_container_width=True)

            st.write('<div style="color: #ff5a5f; font-weight: bold;">Top 3 Host Names with Maximum Reviews:</div>', unsafe_allow_html=True)
            
            detailed_descriptions=[
                "1. Hotels in Turkey. Tops the Position with maximum availability of 22 days per month",
                "2. Hotels in China, Second tops the List with maximum availability of 19 days in a month.",
                "3. Portugal holds the 3rd Position with availability of 16 days."]

            for description in detailed_descriptions:
                    st.write_stream(stream_text(description))
            
        with col2:
                
            st.write("")
            st.dataframe(df1,hide_index=True)
