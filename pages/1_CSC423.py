# # fthe imputs 

# import streamlit as st
# import sklearn 
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.model_selection import train_test_split
# import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.preprocessing import LabelEncoder
# import base64
# from sklearn.metrics import accuracy_score

# st.set_page_config(page_title="COM 423", page_icon=":guardsman:", layout="wide")

# def displaypdf(pdfFile):
#     with open(pdfFile,'rb') as f:
#         base64pdf=base64.b64encode(f.read()).decode('utf-8')
#     pdf_display = F'<iframe src="data:application/pdf;base64,{base64pdf}" width="1663" height="1000" type="application/pdf"></iframe>'
#     st.markdown(pdf_display,unsafe_allow_html=True)

# #  ######################################################################

# with st.container():
#     st.markdown('🚨')
#     st.info("Before attemping the test, it is strongly adviced you go through our materials to be adequately prepared. Thanks!")

# materials =st.selectbox("Materials",["SELECT","ONE","TWO"])
# if materials == "ONE":
#     st.info("YOU HAVE SELECTED THE FIRST MATERIAL ! ")
#     displaypdf('regression.pdf')

# if materials == "TWO":
#     st.info("YOU HAVE SELECTED THE SECOND MATERIAL !")
#     displaypdf('machilelearning.pdf')




# with st.container():
#     st.write("""
#     # COM 423 
#     EXPERT SYSTEM AND MACHINE LEARNING 
    
#     """)

# # Load the data
# df = pd.read_csv('expert.csv')

# # check for missing values
# df.isnull().sum()

# # drop missing values
# df.dropna(inplace=True)

# # check for duplicates
# df.duplicated().sum()

# # drop duplicates
# df.drop_duplicates(inplace=True)

# # Initialize the label encoder
# le = LabelEncoder()

# df_encoded = pd.get_dummies(df,columns=['Coursecode','Coursetitle','Subtopic'], drop_first=True)
# df_encoded.drop(['id','isObjective'], axis=1, inplace=True)
# df_encoded = df.apply(le.fit_transform)
# # df_encoded.groupby(['Coursecode','Coursetitle','Subtopic']).count()

# # Extract the questions and answers from the data
# questions = df['Question']
# answers = df['Answerkey']

# vectorizer = CountVectorizer()
# X = vectorizer.fit_transform(questions)
# y = answers

# #feature engineering 


# # Split the data into training and test sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# model = DecisionTreeClassifier()
# model.fit(X_train, y_train)



# # Fit the model
# model = DecisionTreeClassifier()
# model.fit(X_train, y_train)

# # evaluate the model on the test set
# from sklearn.metrics import accuracy_score
# y_pred = model.predict(X_test)
# accuracy = accuracy_score(y_test, y_pred)

# # Generate a question for the user to answer
# with st.container():

#     st.warning("""  #  40 QUESTIONS QUIZ GENERATED TO TEST YOUR PREPAREDNESS FOR THE EXPERT SYSTEM AND MACHINE LEARNING EXAMINATION 
# The questions would be auto refreshed in 30 minutes  from now and the student is expected to have been done and graded before the questions are being refreshed. """)
    

# # Create a progress bar
# progress_bar = st.progress(0)

# # Initialize counters for correct answers and total questions
# # calculate the number of correct answers
# num_correct = (y_pred == y_test).sum()
# num_questions =40
# user_answers=[None for _ in range(num_questions)]
# correct_answers=[]

# # Create a table to store the answers
# answers_df = pd.DataFrame(columns=["Question", "Correct Answer", "User Answer"])

# # Generate a question for the user to answer

# @st.cache(ttl=1800,suppress_st_warning=True, show_spinner=True, allow_output_mutation=True)

# def generate_questions():
    
#     return questions.sample(40,replace=False)
    
#     # code to generate questions

# unique_question=generate_questions()

# score = 0


# for i, question in enumerate(unique_question):
#     # Use the model to predict the correct answer
#     prediction = model.predict(vectorizer.transform([question]))[0]
#     correct_answers.append(prediction)
    
#     st.write(f"Question {i+1} of {num_questions} attempted")

#     # Use a consistent layout
#     st.subheader(f"Question {i+1}")
    
#     # Display the generated question to the user
#     st.markdown(question)
    
#     # Use more dynamic inputs
#     user_answer = st.text_input("please input your answer",key = f"question_{i+1}")
#     if user_answer:
#         progress_bar.progress((i+1)/num_questions)
#         st.write(f"{(i+1)/num_questions*100:.1f}% of questions answered, {num_questions-(i+1)} remaining")
#         user_answers.append(user_answer)
#         if user_answer == prediction:
#             score += 1

       
#     # Use error handling
#     if user_answer == "":
#         st.error("You must provide an answer, and please in capital letters")
#         continue

#     # Grade the user's answer and provide feedback
#     if user_answer == prediction:
#         num_correct += 1
#         st.success("Correct! Great job.")
#     else:
#         st.error("oops!, incorrect")
    
#     # # Update the answers_df DataFrame with the user's answer
#     # answers_df = answers_df.append({'Question':question,'Correct Answer':prediction,'User Answer':user_answer},ignore_index=True)
#     # Create a temporary DataFrame for the new result
# new_data = pd.DataFrame([{
#     'Question': question, 
#     'Correct Answer': prediction, 
#     'User Answer': user_answer
# }])

# # Use concat instead of append
# answers_df = pd.concat([answers_df, new_data], ignore_index=True)

# st.subheader("Score")
# st.write(f"Your score is {score:.1f} out of {num_questions}")

# # Provide feedback and suggestions
# if score >= 10.0:
#     st.write("Great job! Keep up the good work.")
# elif score <= 9.0:
#     st.write("You're doing well, but there's still room for improvement.")
# else:
#     st.write("You'll need to work a bit harder to improve your score.")


# # Show the answers table
# st.write("Answers:")
# st.table(answers_df)

# df_encoded['Question'] = question
# df_encoded['Answerkey'] = prediction
# df_encoded['User_Answer'] = user_answer
# grouped_df = df.groupby(['Question', 'Coursecode', 'Coursetitle', 'Subtopic']).size().reset_index(name='number of questions')

# st.info("TABLE CONTAINING ALL THE QUESTIONS AND THEIR CATEGORIES")
# st.write(grouped_df)

# # Use the merge function to join the grouped_df DataFrame with the answers_df DataFrame on the 'Question' column
# merged_df = pd.merge(answers_df, grouped_df, left_on='Question', right_on='Question')

# # Create a new column that shows the student's score for each question
# merged_df['Score'] = (merged_df['User Answer'] == merged_df['Correct Answer']).astype(int)

# # Group the merged_df DataFrame by the Coursecode, Coursetitle, and Subtopic columns and calculate the student's score for each group
# performance_df = merged_df.groupby(['Coursecode', 'Coursetitle', 'Subtopic']).agg({'number of questions': 'first', 'Score': 'mean'}).reset_index()

# # Calculate the total number of questions for each group
# # performance_df['total number of questions'] = performance_df['number of questions'].sum()

# # Create a new column that shows the student's percentage score for each group
# performance_df['Overall Percentage Score'] = performance_df['Score']/ performance_df['number of questions'] * 100

# # Group the performance_df DataFrame by the Coursetitle column and calculate the number of questions answered for each coursetitle
# courses_df = performance_df.groupby('Coursetitle').agg({'number of questions': 'sum', 'Score': 'sum'}).reset_index()

# # Create a new column that shows the student's percentage score for each coursetitle
# courses_df['Overall Percentage Score'] = courses_df['Score'] / courses_df['number of questions'] * 100

# # Group the performance_df DataFrame by the Subtopic column and calculate the number of questions answered for each subtopic
# subtopics_df = performance_df.groupby('Subtopic').agg({'number of questions': 'sum', 'Score': 'sum'}).reset_index()

# # Create a new column that shows the student's percentage score for each subtopic
# subtopics_df['Overall Percentage Score'] = subtopics_df['Score'] / subtopics_df['number of questions'] * 100

# # Display the results to the user

# import plotly.express as px

# # Create a new DataFrame that only contains the 'Coursetitle' and 'Percentage Score' columns
# pie_dfy = performance_df[['Subtopic', 'Overall Percentage Score']]
# pie_dfy = pie_dfy.dropna()
# print (pie_dfy.columns)
# print(pie_dfy)

# # Use the pivot_table function to create a new DataFrame with one row for each Coursetitle and one column for each Percentage Score
# pie_dfy = pie_dfy.pivot_table(index='Subtopic', values=['Overall Percentage Score'], aggfunc='sum')

# # Extract the values of the 'Percentage Score' column from the `pie_df` DataFrame
# valuesy= pie_dfy['Overall Percentage Score'].tolist()
# # Create a pie chart using Plotly
# if pie_dfy.empty:
#     st.write("no data to display")
# else:
#     figy = px.pie(pie_dfy, values=valuesy, names=pie_dfy.index, title='Percentage of Questions Answered Correctly by Subtopic')
#     figy.update_traces(textposition='inside', textinfo='percent+label')

# # Display the pie chart in Streamlit
#     st.plotly_chart(figy)
#     st.success("The percentage allocated to each category is done based on the real time data being processed. The category with the highest percentage shows where your stregnth lies and in that order the data shows you areas where you performed well and areas where you need to improve more on. The table above containing all questions is there to assist you in knowing the category the questions you got wrongly or correctly falls under. ")


# # Calculate the percentage of correct answers for each course
# performance_df['Overall Percentage Score'] = performance_df['Overall Percentage Score'] / performance_df['number of questions']*100

# # Group the performance_df DataFrame by the Coursecode column and sum the Percentage Score column
# course_scores = performance_df.groupby('Coursecode')['Overall Percentage Score'].sum().reset_index()


import streamlit as st
import pandas as pd
import base64
import plotly.express as px
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

# --- 1. PAGE CONFIG & STYLING ---
st.set_page_config(page_title="CSC 423 Expert System", page_icon="🤖", layout="wide")

# --- 2. DATA LOADING & CACHING ---
@st.cache_data(ttl=1800)
def load_and_clean_data(file_path):
    """Loads CSV, handles missing values and duplicates uniquely per file."""
    try:
        df = pd.read_csv(file_path)
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        return df
    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return pd.DataFrame()

def display_pdf(pdf_file):
    """Encodes and displays PDF in an iframe."""
    with open(pdf_file, 'rb') as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# --- 3. SESSION STATE MANAGEMENT ---
# This prevents data from "leaking" between different course pages
if "current_course" not in st.session_state or st.session_state["current_course"] != "CSC423":
    st.session_state["current_course"] = "CSC423"
    st.session_state["quiz_submitted"] = False
    st.session_state["answers_df"] = pd.DataFrame()

# --- 4. UI: MATERIALS SECTION ---
st.title("CSC 423: Expert System and Machine Learning")

with st.expander("📖 Preparatory Materials"):
    st.info("Review these materials before attempting the diagnostic test.")
    materials = st.selectbox("Select Material", ["SELECT", "Regression Analysis", "Machine Learning Fundamentals"])
    if materials == "Regression Analysis":
        display_pdf('regression.pdf')
    elif materials == "Machine Learning Fundamentals":
        display_pdf('machilelearning.pdf')

# --- 5. CORE LOGIC: ML MODEL & QUESTIONS ---
df = load_and_clean_data('expert.csv')

if not df.empty:
    # Train the Decision Tree Model (The Expert System's 'Brain')
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df['Question'])
    y = df['Answerkey']
    
    # Split and Fit
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    # Question Generation
    @st.cache_data(ttl=1800)
    def generate_random_quiz(dataframe):
        return dataframe.sample(n=min(40, len(dataframe)), replace=False)

    quiz_questions = generate_random_quiz(df)

    # --- 6. THE QUIZ FORM ---
    st.warning("⚡ **Diagnostic Quiz:** 40 Questions. Please use ALL CAPS for answers.")
    
    # We use st.form so the app doesn't refresh until the 'Submit' button is clicked
    with st.form("quiz_logic_form"):
        user_responses = []
        
        for i, row in enumerate(quiz_questions.itertuples()):
            st.markdown(f"**Question {i+1}:** {row.Question}")
            ans = st.text_input("Enter Answer:", key=f"input_{row.Index}").strip().upper()
            
            # Predict the 'Expert' answer using the ML model
            prediction = model.predict(vectorizer.transform([row.Question]))[0]
            
            user_responses.append({
                "Question": row.Question,
                "Correct Answer": prediction,
                "User Answer": ans,
                "Subtopic": row.Subtopic,
                "Coursecode": row.Coursecode
            })
        
        submit_button = st.form_submit_button("Submit and Generate Analysis")

    # --- 7. ANALYSIS & RESULTS ---
    if submit_button:
        st.session_state["quiz_submitted"] = True
        results_df = pd.DataFrame(user_responses)
        results_df['IsCorrect'] = (results_df['User Answer'] == results_df['Correct Answer']).astype(int)
        
        # Calculate Score
        total_score = results_df['IsCorrect'].sum()
        st.success(f"### Assessment Complete! Your Score: {total_score} / {len(quiz_questions)}")

        # Analytics for Expert System Diagnosis
        performance = results_df.groupby('Subtopic')['IsCorrect'].mean().reset_index()
        performance['Score%'] = performance['IsCorrect'] * 100

        col1, col2 = st.columns([2, 1])

        with col1:
            if not performance.empty:
                fig = px.pie(performance, values='Score%', names='Subtopic', 
                             title='Knowledge Strengths by Subtopic',
                             hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("#### Performance Summary")
            st.dataframe(performance[['Subtopic', 'Score%']].style.format({"Score%": "{:.1f}%"}))

        st.info("💡 **Expert Diagnosis:** The pie chart identifies your strongest domains. Areas with smaller slices require focused revision.")
        
        # Show detailed log
        with st.expander("View Detailed Answer Log"):
            st.table(results_df[['Question', 'Correct Answer', 'User Answer', 'IsCorrect']])

else:
    st.error("Missing Data: Please ensure 'expert.csv' is in the project folder.")