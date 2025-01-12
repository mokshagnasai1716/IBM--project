import streamlit as st
st.set_page_config(page_title="ADMIN PAGE")
def admin_login():
    """
    Function to display the admin login interface.
    It collects username and password and verifies them.
    Returns True if the login is successful, otherwise returns False.
    """
    st.title("Welcome to the Health Prediction ")
    
    
    st.subheader("Admin Login")
    
    
    # Create input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # Check for the login button click
    if st.button("Login"):
        # Verify credentials and update session state
        if verify_credentials(username, password):
            st.session_state["logged_in"] = True
            st.success("Login successful! Redirecting to the prediction page...")
            # Use the session state to trigger a page refresh
            st.experimental_rerun()  # Redirect to the main page immediately
        else:
            st.error("Invalid username or password.")

def verify_credentials(username, password):
    """
    Function to verify the provided username and password.
    In a real application, you would check against a database or secure storage.
    Here we use hardcoded credentials for demonstration purposes.

    Args:
        username (str): The username entered by the admin.
        password (str): The password entered by the admin.

    Returns:
        bool: True if credentials are valid, False otherwise.
    """
    # Define hardcoded credentials for demonstration purposes
    valid_username = "bvrit"
    valid_password = "manisai1432"  # Use hashed passwords in production

    # Check if the entered credentials match the valid ones
    return username == valid_username and password == valid_password
