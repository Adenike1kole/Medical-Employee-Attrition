import pickle
import streamlit as st
import joblib
import numpy as np

# Loading the trained model
classifier = joblib.load('Classifier.pkl')

@st.cache()
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

        prediction = classifier.predict(data)

        if prediction[0] > 0:
            result = "Positive"
        else:
            result = "Negative"

        return result

    except Exception as e:
        st.error("An error occurred during prediction: {}".format(str(e)))


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
    YearsAtCompany = st.number_input("Years at Company")
    TotalWorkingYears = st.number_input("Total Working Years")
    Shift = st.selectbox('Shift', ("Morning", "Afternoon", "Night", "24 Hours"))
    JobLevel = st.selectbox('Job Level', ("Entry", "Intermediate", "Senior", "Managerial", "Executive"))
    JobInvolvement = st.selectbox('Job Involvement', ("Low", "Medium", "High", "Very High"))
    Age = st.number_input("Age")
    result = ""

    # When 'Predict' is clicked, make prediction and store it
    if st.button("Predict"):
        result = prediction(YearsAtCompany, TotalWorkingYears, Shift, JobLevel, JobInvolvement, Age)
    st.success("Employee Prediction: {}".format(result))


if __name__ == '__main__':
    main()