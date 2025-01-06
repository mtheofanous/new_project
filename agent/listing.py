import streamlit as st
from navigation_buttons import home_button, back_button, log_out_button
from app.components.utils import scrape_data_to_dict

def listing():
    
    back_button()
    
    st.title("Property Profile Generator")
    st.write("Enter a property URL to generate its profile.")

    url = st.text_input("Property URL:", placeholder="Enter the property URL here")
    if st.button("Generate Profile"):
        if url:
            with st.spinner("Scraping data..."):
                try:
                    property_data = scrape_data_to_dict(url)
                    st.success("Data scraped successfully!")

                    # Display Property Information
                    st.header("Property Information")
                    st.write(f"**Type:** {property_data.get('property_type', 'N/A')}")
                    st.write(f"**Size:** {property_data.get('property_size', 'N/A')} sq.m.")
                    st.write(f"**Location:** {property_data.get('property_location', 'N/A')}")
                    st.write(f"**Price:** {property_data.get('property_price', 'N/A')} €")
                    st.write(f"**Price per sq.m.:** {property_data.get('price_per_sqm', 'N/A')} €")

                    # Display Characteristics
                    st.subheader("Characteristics")
                    characteristics = property_data.get('characteristics', {})
                    for key, value in characteristics.items():
                        st.write(f"- **{key}:** {value}")

                    # Display Statistics
                    st.subheader("Statistics")
                    statistics = property_data.get('statistics', {})
                    for key, value in statistics.items():
                        st.write(f"- **{key}:** {value}")

                    # Display Images
                    st.subheader("Images")
                    images = property_data.get('images', [])
                    for img in images:
                        st.image(img['src'], caption=img.get('alt', ''), use_column_width=True)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a valid URL.")
            
if __name__ == "__main__":
    listing()