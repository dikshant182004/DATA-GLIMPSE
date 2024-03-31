import streamlit as st

# Define a class to store tag details
class TagDetails:
    def __init__(self, tag_name, id_or_class, class_name, find_method, other_info):
        self.tag_name = tag_name
        self.id_or_class = id_or_class
        self.class_name = class_name
        self.find_method = find_method
        self.other_info = other_info

# Function to display selected tags
def display_selected_tags(tag_details_list):
    if not tag_details_list:
        st.write("No tags selected.")
    else:
        for index, tag_details in enumerate(tag_details_list, start=1):
            st.write(f"Tag {index} details:",tag_details_list)
            st.write("")

# Display form for selecting tag details
st.header("Tag Details")
st.write("Specify the details for each tag you want to scrape.")

tag_details_list = []

tag_index = 0
while st.checkbox(f"Add Tag {tag_index + 1}"):
    with st.expander(f"Tag {tag_index + 1} Details"):
        tag_name = st.selectbox("Select Tag Name", ['div', 'span', 'a', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 'img', 'form', 'input', 'button', 'textarea'], key=f"tag_name_{tag_index}")
        id_or_class = st.radio("Select Id or Class", ["id", "class"], key=f"id_or_class_{tag_index}")
        class_name = st.text_input("Enter Id or Class Name", key=f"class_name_{tag_index}")
        find_method = st.radio("Select Find Method", ["find", "find_all"], key=f"find_method_{tag_index}")
        other_info = st.text_input("Enter Other Info (if any)", key=f"other_info_{tag_index}")

    tag_details = TagDetails(tag_name, id_or_class, class_name, find_method, other_info)
    tag_details_list.append(tag_details)

    tag_index += 1

if st.button('Show Tag Details'):
    display_selected_tags(tag_details_list)
