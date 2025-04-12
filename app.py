import streamlit as st
from fake_useragent import UserAgent

from engines.utilities import scrape_fragrance

import boto3
from botocore.exceptions import ClientError

def connect_to_dynamodb(dynamodb_table_name):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(dynamodb_table_name)
        return table
    except ClientError as e:
        print(f"Error accessing DynamoDB: {e.response['Error']['Message']}")

ua = UserAgent()

# Streamlit App
st.title("Fragrantica Scraper")
st.write("Enter a Fragrantica URL to scrape fragrance data and save it to AWS DynamoDB.")

# url = st.text_input("Fragrance URL", "https://www.fragrantica.com/perfume/Creed/Aventus-9828.html")

dynamodb_table_name = "fragrance-data"

table = connect_to_dynamodb(
    dynamodb_table_name="fragrance-data"
)

# Input field

url = st.text_input(
    "Fragrance URL", 
    "https://www.fragrantica.com/perfume/Creed/Aventus-9828.html"
)
# Button to trigger scraping and saving
if st.button("Scrape and Save"):
    if url:
        # First, check if it's in DynamoDB
        with st.spinner("Checking DynamoDB..."):
            response = table.get_item(
                Key={'url': url}
            )
        if 'Item' in response:
            st.success("Data found in DynamoDB.")
            fragrance_data = response['Item']
        else:
            st.warning("Data not found in DynamoDB. Scraping the website...")
            # If not found, scrape the data
            with st.spinner("Scraping data..."):
                fragrance_data = scrape_fragrance(url)
                st.success("Scraping data from Fragrantica...")
                # Save the scraped data to DynamoDB
                table.put_item(
                    Item={
                        'url': url,
                        'data': fragrance_data
                    }
                )
            st.success("Data saved to DynamoDB.")
            
        if "error" in fragrance_data:
            st.error(fragrance_data["error"])
        else:
            # st.success(f"Scraped: {fragrance_data['data']['name']}")
            st.json(fragrance_data)  # Display the data
    else:
        st.warning("Please enter a URL.")
