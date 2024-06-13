import pickle
import streamlit as st
import joblib
import numpy as np

# Loading the trained model
classifier = joblib.load('Classifier.pkl')

@st.cache_data()
def prediction(YearsAtCompany, TotalWorkingYears, Shift, JobLevel, JobInvolvement, Age):
    try:
        # Convert Shift to numerical
        if Shift == "Morning":
            Shift = 0
        elif Shift == "Afternoon":
            Shift = 1
        elif Shift == "Night":
            Shift = 2
        else:
            Shift = 3

        # Convert JobLevel to numerical
        if JobLevel == "Entry":
            JobLevel = 1
        elif JobLevel == "Intermediate":
            JobLevel = 2
        elif JobLevel == "Senior":
            JobLevel = 3
        elif JobLevel == "Managerial":
            JobLevel = 4
        else:
            JobLevel = 5

        # Convert JobInvolvement to numerical
        if JobInvolvement == "Low":
            JobInvolvement = 1
        elif JobInvolvement == "Medium":
            JobInvolvement = 2
        elif JobInvolvement == "High":
            JobInvolvement = 3
        else:
            JobInvolvement = 4

        # Create a NumPy array
        data = np.array([[YearsAtCompany, TotalWorkingYears, Shift, JobLevel, JobInvolvement, Age]])

        # Make prediction
        prediction = classifier.predict(data)

        return prediction[0]  # Return the predicted class

    except Exception as e:
        st.error("An error occurred during prediction: {}".format(str(e)))
        return None

# This is the main function in which we define our YearsAtCompany, TotalWorkingYears, Shift, JobLevel, JobInvolvement, Age
def main():
    # Front end elements of the web page
    html_temp = '''
    <div style="background-color: green;padding:10px">
    <h2 style="color:black;text-align:center;">Streamlit Attrition Prediction ML App</h2>
    </div>
    '''

    # Display the front end aspect
    st.markdown(html_temp, unsafe_allow_html=True)

    # Following lines create boxes in which user can enter data required to make prediction
    YearsAtCompany = st.number_input("Years at Company", min_value=0.0, step=0.1, format="%.1f")
    TotalWorkingYears = st.number_input("Total Working Years", min_value=0.0, step=0.1, format="%.1f")
    Shift = st.selectbox('Shift', ("Morning", "Afternoon", "Night", "24 Hours"))
    JobLevel = st.selectbox('Job Level', ("Entry", "Intermediate", "Senior", "Managerial", "Executive"))
    JobInvolvement = st.selectbox('Job Involvement', ("Low", "Medium", "High", "Very High"))
    Age = st.number_input("Age", min_value=18, max_value=60, step=1)  # Restrict age between 18 and 60 years
    result = ""

    # When 'Predict' is clicked, validate input and make prediction
    if st.button("Predict"):
        if Age < 18 or Age > 60:
            st.error("Please enter a valid age between 18 and 60")
        elif YearsAtCompany > TotalWorkingYears:
            st.error("Years at Company cannot be greater than Total Working Years")
        else:
            result = prediction(YearsAtCompany, TotalWorkingYears, Shift, JobLevel, JobInvolvement, Age)
            if result is not None:
                if result == 1:
                    st.warning("High chance of attrition")
                else:
                    st.success("Low chance of attrition")

if __name__ == '__main__':
    main()