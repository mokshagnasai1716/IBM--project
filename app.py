import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
#from dotenv import load_dotenv
import google.generativeai as genai
from admin import admin_login  
import pandas as pd
# Import the admin login function

# Load environment variables from .env file
#load_dotenv()

# Get the GEMINI_API_KEY from environment variables
#api_key = os.getenv("GEMINI_API_KEY")
api_key = st.secrets["GEMINI_API_KEY"]

if api_key is None:
    raise ValueError("API key not found. Please set GEMINI_API_KEY in the .env file.")

# Configure the Generative AI model
genai.configure(api_key=api_key)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Admin login handling
if not st.session_state["logged_in"]:
    if admin_login():  # Call the admin login function
        st.session_state["logged_in"] = True  # Update login state if successful
else:
    # Set page configuration for the prediction app
    st.set_page_config(page_title="Health Assistant", layout="wide", page_icon="🧑‍⚕️")

    # Load saved models
    working_dir = os.path.dirname(os.path.abspath(__file__))
    diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))
    heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))

    # Sidebar navigation
    with st.sidebar:
        selected = option_menu('Multiple Disease Prediction System', 
                               ['Diabetes Prediction', 'Heart Disease Prediction'],
                               menu_icon='hospital-fill',
                               icons=['activity', 'heart'],
                               default_index=0)

    # Diabetes Prediction Page
    if selected == 'Diabetes Prediction':
        st.title('Diabetes Prediction using ML')

        # Getting user input
        col1, col2, col3 = st.columns(3)

        with col1:
            Pregnancies = st.text_input('Number of Pregnancies')

        with col2:
            Glucose = st.text_input('Glucose Level')

        with col3:
            BloodPressure = st.text_input('Blood Pressure value')

        with col1:
            SkinThickness = st.text_input('Skin Thickness value')

        with col2:
            Insulin = st.text_input('Insulin Level')

        with col3:
            BMI = st.text_input('BMI value')

        with col1:
            DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')

        with col2:
            Age = st.text_input('Age of the Person')

        # Code for Prediction
        diab_diagnosis = ''

        # Creating a button for Prediction
        if st.button('Diabetes Test Result'):
            # Check if all inputs are provided
            if any(not x for x in [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]):
                st.error("Please fill in all fields before proceeding.")
            else:
                # Gather user input into a list
                user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
                user_input = [float(x) for x in user_input]

                # Diabetes prediction
                diab_prediction = diabetes_model.predict([user_input])

                if diab_prediction[0] == 1:
                    diab_diagnosis = 'The person is diabetic'
                else:
                    diab_diagnosis = 'The person is not diabetic'

                # Display the input values as a table
                input_labels = [
                    "Pregnancies", "Glucose", "BloodPressure", 
                    "SkinThickness", "Insulin", "BMI", 
                    "DiabetesPedigreeFunction", "Age"
                ]
                user_data = pd.DataFrame({
                    "Label": input_labels,
                    "Value": user_input
                })
                st.table(user_data)  # Display the table with labels and values

                # Construct a tailored prompt for the AI model
                prompt = (
                    f"The person’s health data is shown below:\n\n"
                    f"| Label                     | Current Value |\n"
                    f"|---------------------------|---------------|\n"
                    f"| Pregnancies               | {user_input[0]}       |\n"
                    f"| Glucose                   | {user_input[1]}       |\n"
                    f"| BloodPressure             | {user_input[2]}       |\n"
                    f"| SkinThickness             | {user_input[3]}       |\n"
                    f"| Insulin                   | {user_input[4]}       |\n"
                    f"| BMI                       | {user_input[5]}       |\n"
                    f"| DiabetesPedigreeFunction  | {user_input[6]}       |\n"
                    f"| Age                       | {user_input[7]}       |\n\n"
                    f"The diabetes prediction result is: {diab_diagnosis}.\n\n"
                    "Based on this result and the health values provided, please:\n"
                    "- Assess each value in terms of its current level versus a healthy level.\n"
                    "- Provide a personalized lifestyle improvement plan, including specific diet, exercise, and lifestyle recommendations.\n"
                    "- Suggest target values for Glucose, Blood Pressure, BMI, and Insulin that would support healthier outcomes.\n"
                    "- Recommend food choices that support balanced glucose levels, healthy blood pressure, and metabolic wellness, taking into account a young adult's needs.\n"
                )

                # Generate AI response
                with st.spinner('Generating personalized lifestyle improvement plan...'):
                    response = model.generate_content(prompt)

                # Display combined message
                combined_message = f"{diab_diagnosis}\n\nLifestyle Improvement Plan:\n{response.text if response.text else 'No response received.'}"
                st.success(combined_message)

    # Heart Disease Prediction Page
    if selected == 'Heart Disease Prediction':
        st.title('Heart Disease Prediction using ML')

        # Collecting user input
        col1, col2, col3 = st.columns(3)

        with col1:
            age = st.text_input('Age')

        with col2:
            sex = st.selectbox('Sex', ['Choose an option', '0 (Male)', '1 (Female)'])

        with col3:
            cp = st.text_input('Chest Pain types')

        with col1:
            trestbps = st.text_input('Resting Blood Pressure')

        with col2:
            chol = st.text_input('Serum Cholestoral in mg/dl')

        with col3:
            fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')

        with col1:
            restecg = st.text_input('Resting Electrocardiographic results')

        with col2:
            thalach = st.text_input('Maximum Heart Rate achieved')

        with col3:
            exang = st.text_input('Exercise Induced Angina')

        with col1:
            oldpeak = st.text_input('ST depression induced by exercise')

        with col2:
            slope = st.text_input('Slope of the peak exercise ST segment')

        with col3:
            ca = st.text_input('Major vessels colored by fluoroscopy')

        with col1:
            thal = st.text_input('Thal: 0 = normal; 1 = fixed defect; 2 = reversible defect')

        # Diagnosis message
        heart_diagnosis = ''

        # Creating a button for Prediction
        if st.button('Heart Disease Test Result'):
            # Check if all inputs are provided
            if any(not x for x in [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]) or sex == 'Choose an option':
                st.error("Please fill in all fields before proceeding.")
            else:
                # Gather user input into a list and convert to appropriate types
                user_input = [
                    int(age), 
                    0 if sex == '0 (Male)' else 1,  # Convert selectbox to integer
                    int(cp), 
                    int(trestbps), 
                    int(chol), 
                    int(fbs), 
                    int(restecg), 
                    int(thalach), 
                    int(exang), 
                    float(oldpeak), 
                    int(slope), 
                    int(ca), 
                    int(thal)
                ]

                # Heart disease prediction
                heart_prediction = heart_disease_model.predict([user_input])

                if heart_prediction[0] == 1:
                    heart_diagnosis = 'The person is having heart disease'
                else:
                    heart_diagnosis = 'The person does not have any heart disease'

                # Display the input values in a table
                input_labels = [
                    "Age", "Sex", "Chest Pain types", "Resting Blood Pressure", 
                    "Serum Cholesterol", "Fasting Blood Sugar > 120 mg/dl",
                    "Resting Electrocardiographic results", "Max Heart Rate", 
                    "Exercise Induced Angina", "ST depression induced by exercise",
                    "Slope of Peak Exercise ST Segment", "Major Vessels",
                    "Thal"
                ]
                user_data = pd.DataFrame({
                    "Label": input_labels,
                    "Value": user_input
                })
                st.table(user_data)  # Display the table with labels and values

                # Construct a tailored prompt for the AI model
                prompt = (
                    f"The person’s health data is shown below:\n\n"
                    f"| Label                     | Current Value |\n"
                    f"|---------------------------|---------------|\n"
                    f"| Age                       | {user_input[0]}       |\n"
                    f"| Sex                       | {'Male' if user_input[1] == 0 else 'Female'} |\n"
                    f"| Chest Pain types          | {user_input[2]}       |\n"
                    f"| Resting Blood Pressure    | {user_input[3]}       |\n"
                    f"| Serum Cholesterol         | {user_input[4]}       |\n"
                    f"| Fasting Blood Sugar       | {user_input[5]}       |\n"
                    f"| Resting Electrocardiogram | {user_input[6]}       |\n"
                    f"| Max Heart Rate           | {user_input[7]}       |\n"
                    f"| Exercise Induced Angina   | {user_input[8]}       |\n"
                    f"| ST depression             | {user_input[9]}       |\n"
                    f"| Slope                     | {user_input[10]}       |\n"
                    f"| Major Vessels             | {user_input[11]}       |\n"
                    f"| Thal                      | {user_input[12]}       |\n\n"
                    f"The heart disease prediction result is: {heart_diagnosis}.\n\n"
                    "Based on this result and the health values provided, please:\n"
                    "- Assess each value in terms of its current level versus a healthy level.\n"
                    "- Provide a personalized lifestyle improvement plan, including specific diet, exercise, and lifestyle recommendations.\n"
                    "- Suggest target values for cholesterol, blood pressure, and heart rate that would support healthier outcomes.\n"
                    "- Recommend food choices that support heart health, taking into account age and sex.\n"
                )

                # Generate AI response
                with st.spinner('Generating personalized lifestyle improvement plan...'):
                    response = model.generate_content(prompt)

                # Display combined message
                combined_message = f"{heart_diagnosis}\n\nLifestyle Improvement Plan:\n{response.text if response.text else 'No response received.'}"
                st.success(combined_message)
