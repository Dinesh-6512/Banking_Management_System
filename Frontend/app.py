import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.title("🏦 Bank Management System")

menu = st.sidebar.selectbox("Menu", ["View", "Add", "Update", "Delete"])

# 1. VIEW
if menu == "View":
    st.subheader("All Accounts")
    response = requests.get(f"{API_URL}/accounts")
    if response.status_code == 200:
        data = response.json()
        if data:
            df = pd.DataFrame(data) 
            df = df.sort_values(by="id") 
            st.dataframe(df[["id", "account_holder", "account_type", "balance"]], hide_index=True)

# 2. ADD
elif menu == "Add":
    st.subheader("Add Account")
    name = st.text_input("Name")
    acc_type = st.selectbox("Type", ["savings", "salary account"])
    bal = st.number_input("Balance", min_value=0.0)
    if st.button("Submit"):
        payload = {
            "account_holder": name, 
            "account_type": acc_type, 
            "balance": bal
        }
        res = requests.post(f"{API_URL}/accounts", json=payload)
        if res.status_code == 200:
            st.success("Added Successfully!")
        else:
            st.error("Error adding account")

# 3. UPDATE
elif menu == "Update":
    st.subheader("Update Account")
    acc_id = st.number_input("ID", min_value=1, step=1)
    u_name = st.text_input("New Name")
    u_type = st.selectbox("New Type", ["savings", "salary account"])
    u_bal = st.number_input("New Balance", min_value=0.0)
    
    if st.button("Update"):
        payload = {
            "account_holder": u_name, 
            "account_type": u_type, 
            "balance": u_bal
        }
        res = requests.put(f"{API_URL}/details/{int(acc_id)}", json=payload)
        
        if res.status_code == 200:
            # This "highlights" the success and survives the rerun!
            st.success(f"Account {acc_id} Updated Successfully!", icon="✅")
        else:
            st.error("Update failed. Check if the ID exists.")

# 4. DELETE
elif menu == "Delete":
    st.subheader("Delete Account")
    del_id = st.number_input("ID to Delete", min_value=1, step=1)   
    
    if st.button("Delete"):
        res = requests.delete(f"{API_URL}/accounts/{int(del_id)}")
        
        if res.status_code == 200:
            # This popup stays visible to confirm the deletion
            st.success(f"Account {del_id} Deleted!", icon="🗑️")
        else:
            st.error("Account not found")
