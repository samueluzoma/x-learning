import streamlit as st
import pandas as pd
import base64
import plotly.express as px
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="GNS 425 Law of Contract", page_icon="⚖️", layout="wide")

# --- 2. DATA LOADING & CACHING ---
@st.cache_data(ttl=1800)
def load_and_clean_law_data(file_path):
    """Loads CSV specifically for Law of Contract course."""
    try:
        df = pd.read_csv(file_path)
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        return df
    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return pd.DataFrame()

def display_pdf(pdf_file):
    """Displays legal materials."""
    try:
        with open(pdf_file, 'rb') as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Legal document {pdf_file} not found.")

# --- 3. SESSION STATE GUARD ---
if "current_course" not in st.session_state or st.session_state["current_course"] != "GNS425":
    st.session_state["current_course"] = "GNS425"
    st.session_state["quiz_submitted"] = False
    st.cache_data.clear() # Clears memory of previous course questions

# --- 4. UI: MATERIALS SECTION ---
st.title("GNS 425: Law of Contract")

with st.expander("⚖️ Legal Study Materials"):
    st.info("Study the cases and lecture notes below before attempting the diagnostic test.")
    materials = st.selectbox("Select Material", ["SELECT", "General Law", "Lecture Notes", "Case Study 1", "Case Study 2"])
    if materials == "General Law":
        display_pdf('law.pdf')
    elif materials == "Lecture Notes":
        display_pdf('lecture.pdf')
    elif materials == "Case Study 1":
        display_pdf('case1.pdf')
    elif materials == "Case Study 2":
        display_pdf('case2.pdf')

# --- 5. CORE LOGIC: ML MODEL ---
df1 = load_and_clean_law_data('lawcont.csv')

if not df1.empty:
    # Inference Engine Training
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df1['Question'])
    y = df1['Answerkey']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    # Quiz Generation
    @st.cache_data(ttl=1800)
    def generate_law_quiz(dataframe):
        return dataframe.sample(n=min(40, len(dataframe)), replace=False)

    quiz_questions = generate_law_quiz(df1)

    # --- 6. THE QUIZ FORM ---
    st.success("⚖️ **Contract Law Diagnostic:** 40 Questions. Please ensure answers are in CAPITAL LETTERS.")
    
    with st.form("law_quiz_form"):
        user_responses = []
        
        for i, row in enumerate(quiz_questions.itertuples()):
            st.markdown(f"**Question {i+1}:** {row.Question}")
            ans = st.text_input("Enter Answer:", key=f"law_{row.Index}").strip().upper()
            
            # Predictive Grading (ML Inference)
            prediction = model.predict(vectorizer.transform([row.Question]))[0]
            
            user_responses.append({
                "Question": row.Question,
                "Correct Answer": prediction,
                "User Answer": ans,
                "Subtopic": row.Subtopic,
                "Coursecode": row.Coursecode
            })
        
        submit_button = st.form_submit_button("Submit Assessment")

    # --- 7. ANALYSIS & RESULTS ---
    if submit_button:
        results_df = pd.DataFrame(user_responses)
        results_df['IsCorrect'] = (results_df['User Answer'] == results_df['Correct Answer']).astype(int)
        
        score = results_df['IsCorrect'].sum()
        st.write(f"## Your Final Score: {score} / {len(quiz_questions)}")

        # Analytics by Subtopic
        performance = results_df.groupby('Subtopic')['IsCorrect'].mean().reset_index()
        performance['ScorePercentage'] = performance['IsCorrect'] * 100

        col1, col2 = st.columns([1.5, 1])

        with col1:
            if not performance.empty:
                fig = px.pie(performance, values='ScorePercentage', names='Subtopic', 
                             title='Law of Contract Mastery Levels',
                             hole=0.4, color_discrete_sequence=px.colors.qualitative.Antique)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("#### Result Interpretation")
            if score >= 30:
                st.balloons()
                st.success("Distinction level mastery! You have a firm grasp of contract law.")
            elif score >= 20:
                st.warning("Good attempt. Review the case studies to improve your specific knowledge.")
            else:
                st.error("Further study is required. Focus on the lecture notes provided above.")

        with st.expander("Review Detailed Answer Table"):
            st.table(results_df[['Question', 'Correct Answer', 'User Answer', 'IsCorrect']])
            
        st.warning("The visual data shows your performance trends. The largest slices represent your strongest understanding of legal concepts.")

else:
    st.error("Missing Data: 'lawcont.csv' not found.")