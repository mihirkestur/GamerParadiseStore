import streamlit as st
st.set_page_config(page_title='GamerParadiseStore', layout = 'wide', initial_sidebar_state = 'auto')
import dbcommands
import psycopg2

conn = psycopg2.connect(**st.secrets["postgres"])
cursor = conn.cursor()

choice = st.radio("Who are you?", (
    "Developer",
    "Gamer",
    "Manager"
))

if(choice == "Developer"):
    command = st.text_area(label="Enter command")
    if(command != "" and st.button(label="Execute")):  
        try:
            st.dataframe(dbcommands.execute_any_command(cursor, command))
        except Exception as e:
            st.write("Not a valid command\n{e}")

elif(choice == "Gamer"):
    operation = st.radio("Select operation", (
    "Insert",
    "Update",
    "Delete"
    ))
    if(operation == "Insert"):
        with st.form(key='User'):
            first_name = st.text_input(label='First name')
            last_name = st.text_input(label='Last name')
            email = st.text_input(label='E-mail')
            phone = st.text_input(label='Phone')
            addr = st.text_input(label='Address')
            comp_desc = st.text_input(label='Complaint Description')
            comp_date = st.text_input(label='Complaint Date')
            pay_mode = st.text_input(label='Payment Mode')
            pay_date = st.text_input(label='Payment Date')
            amnt_paid = st.text_input(label='Amount Paid')
            date_add = st.text_input(label='Date Added')
            quant_wish = st.text_input(label='Quantity wished')
            submit_button = st.form_submit_button(label='Submit')

elif(choice == "Manager"):

    operation = st.radio("Select operation", (
    "Insert",
    "Update",
    "Delete"
    ))
    if(operation == "Insert"):
        sup_name = st.text_input(label='Supplier Name')
        sup_phone = st.text_input(label='Supplier Phone')
        coo = st.text_input(label='Country of origin')
        price = st.text_input(label='Price')
        rating = st.text_input(label='Rating')
        desc = st.text_input(label='Description')
        off_desc = st.text_input(label='Offer description')
        off_et = st.text_input(label='Offer end-time')
        product_type = st.selectbox("Product type", (
        "None",
        "Game",
        "Accessory",
        "Contest details"
        ))
        if(product_type == "Game"):
            with st.form(key='Game'):
                game_name = st.text_input(label='Game name')
                genre = st.text_input(label='Genre')
                specs = st.text_input(label='Specifications')
                platform = st.text_input(label='Platform')
                rel_date = st.text_input(label='Release Date')
                submit_button = st.form_submit_button(label='Submit')
        elif(product_type == "Accessory"):
            with st.form(key='Accessory'):
                accessory_name = st.text_input(label='Accessory name')
                length = st.text_input(label='Length')
                breadth = st.text_input(label='Breadth')
                width = st.text_input(label='Width')
                quant = st.text_input(label='Quantity')
                sub_cat = st.text_input(label='Sub-Category')
                submit_button = st.form_submit_button(label='Submit')
        elif(product_type == "Contest details"):
            with st.form(key='Contest'):
                game_name = st.text_input(label='Game name')
                contest_desc = st.text_input(label='Contest Description')
                start_date = st.text_input(label='Start Date')
                end_date = st.text_input(label='End Date')
                quant = st.text_input(label='Quantity')
                sub_cat = st.text_input(label='Sub-Category')
                submit_button = st.form_submit_button(label='Submit')

# conn.commit()
conn.close()