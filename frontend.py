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
    execute = st.button(label="Execute")
    if(command != "" and execute):  
        try:
            st.dataframe(dbcommands.execute_any_command(cursor, command))
        except Exception as e:
            st.write("Not a valid command:")
            st.error(f"{e}")

elif(choice == "Gamer"):
    operation = st.radio("Select operation", (
    "Insert Gamer Info",
    "Update Gamer Info",
    "Delete Gamer Info",
    "View/Buy",
    "Complaint",
    "Participate in Contest"
    ))
    if(operation == "Insert Gamer Info"):
        with st.form(key='Users'):
            first_name = st.text_input(label='First name')
            last_name = st.text_input(label='Last name')
            email = st.text_input(label='E-mail')
            phone = st.text_input(label='Phone')
            addr = st.text_input(label='Address')
            submit_button = st.form_submit_button(label='Submit')
        if(submit_button):
            values = f"('{first_name}','{last_name}','{email}','{phone}')"
            column_names = '(first_name, last_name, e_mail, phone)'
            user_id = dbcommands.insert_into_table(cursor, "users",column_names, values,'user_id')
            st.success(f"Your user id is : {user_id}")
            values = f"('{user_id}','{addr}')"
            column_names = '(user_id, address)'
            dbcommands.insert_into_table(cursor, "address",column_names, values,'user_id')
            
    elif(operation == "Update Gamer Info"):
        with st.form(key='Users'):
            first_name = st.text_input(label='First name')
            last_name = st.text_input(label='Last name')
            email = st.text_input(label='E-mail')
            phone = st.text_input(label='Phone')
            addr = st.text_input(label='Address')
            submit_button = st.form_submit_button(label='Submit')
    elif(operation == "Delete Gamer Info"):
        with st.form(key='delete user'):
            user_id = st.text_input(label='Enter user id')
            submit_button = st.form_submit_button(label='Delete user')
        if(submit_button):
            st.info(dbcommands.delete_entry_from_table(cursor, "users", "user_id", user_id))
    elif(operation == "Complaint"):
        # complaint_id and user_id ?
        with st.form(key='complaint'):
            comp_desc = st.text_input(label='Complaint Description')
            comp_date = st.text_input(label='Complaint Date')
            submit_button = st.form_submit_button(label='Submit')
    elif(operation == "View/Buy"):
        # complaint_id and user_id ?
        with st.form(key='Cart item/Cart/Payment'):
            # product_id
            pay_mode = st.text_input(label='Payment Mode')
            pay_date = st.text_input(label='Payment Date')
            amnt_paid = st.text_input(label='Amount Paid')
            date_add = st.text_input(label='Date Added')
            quant_wish = st.text_input(label='Quantity wished')
            submit_button = st.form_submit_button(label='Submit')
    elif(operation == "Participate in Contest"):
        # complaint_id and user_id ?
        with st.form(key='Participates/Team/Belongs_to'):
            # points gained, prize won, total points
            contest_id = st.text_input(label='Contest name/Id')
            team_id = st.text_input(label='Team Id')
            submit_button = st.form_submit_button(label='Submit')

elif(choice == "Manager"):

    operation = st.radio("Select operation", (
    "Insert Product Details",
    "Update Product Details",
    "Delete a product",
    ))

    if(operation == "Insert Product Details"):
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

    elif(operation == "Update Product Details"):
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
    
    elif(operation == "Delete a product"):
        with st.form(key='delete product'):
            product_id = st.text_input(label='product id')
            product_type = st.selectbox("Product type", (
            "None",
            "Game",
            "Accessory",
            "Contest details"
            ))
            submit_button = st.form_submit_button(label='Submit')
        if(submit_button):
            st.info(dbcommands.delete_entry_from_table(cursor, "product", "product_id", product_id))
conn.commit()
conn.close()