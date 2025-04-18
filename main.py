import streamlit as st

st.set_page_config(
    page_title="CGPA Calculator",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        "Get Help": "https://github.com/Siddhesh-Agarwal/CGPA-Calculator/discussions",
        "Report a bug": "https://github.com/Siddhesh-Agarwal/CGPA-Calculator/issues/new",
        "About": None,
    },
)


grade_to_point = {
    "O": 10,
    "A+": 9,
    "A": 8,
    "B+": 7,
    "B": 6,
    "C": 5,
}
grades = list(grade_to_point.keys())


def calculate_cgpa(
    grade_points: list[int],
    credits: list[float],
    previous_cgpa: float = 0,
    previous_credit: float = 0,
):
    total_credit = sum(credits) + previous_credit
    total_grade = sum(grade_point * credit for grade_point, credit in zip(grade_points, credits)) + (previous_cgpa * previous_credit)
    return total_grade / total_credit


def calculate_sgpa_from_marks(
    marks: list[float],
    credits: list[float],
):
    total_credit = sum(credits)
    total_weighted_marks = sum(mark * credit for mark, credit in zip(marks, credits))
    return total_weighted_marks / total_credit


st.title("CGPA Calculator")

# Create tabs for different calculation methods
tab1, tab2 = st.tabs(["Grade-Based CGPA", "Marks-Based SGPA"])

with tab1:
    st.markdown(
        "This is a simple CGPA calculator that calculates your CGPA based on your grades and credits"
    )

    st.latex(r"CGPA = \frac{\sum_{i=1}^{n} (grade_i * credit_i)}{\sum_{i=1}^{n} credit_i}")

    cols = st.columns(2)
    previous_cgpa = cols[0].number_input(
        label="Previous CGPA",
        help="Enter Your CGPA upto previous semester",
        min_value=0.00,
        value=0.00,
        step=0.01,
    )
    previous_credit = cols[1].number_input(
        label="Previous Credit",
        help="Enter the total number of credits you have taken upto previous semester",
        min_value=0.0,
        value=0.0,
        step=0.5,
    ).__int__()
    number_of_subjects = st.number_input(
        label="Number of Subjects",
        help="Enter the number of subjects you are taking this semester",
        min_value=1,
        max_value=10,
        value=5,
    ).__int__()

    grade = [grades[0]] * number_of_subjects
    credit = [0.0] * number_of_subjects
    for i in range(number_of_subjects):
        st.subheader(f"Subject #{i+1}")
        cols = st.columns(2)
        grade[i] = cols[0].selectbox(
                label=f"Grade",
                options=grades,
                key=f"grade_{i}",
                index=0,
            ).__str__()

        credit[i] = cols[1].number_input(
            label=f"Credit",
            min_value=1.0,
            max_value=10.0,
            value=4.0,
            step=0.5,
            key=f"credit_{i}",
        )

    if st.button("Calculate CGPA"):
        grade_points = [grade_to_point[x] for x in grade]
        st.info(f"Your semester GPA is {calculate_cgpa(grade_points, credit):.2f}")
        st.success(
            f"Your Cumulative GPA is {calculate_cgpa(grade_points, credit, previous_cgpa, previous_credit):.2f}"
        )

with tab2:
    st.markdown(
        "This calculator computes SGPA directly from marks and credits without converting to grade points"
    )
    
    st.latex(r"SGPA = \frac{\sum_{i=1}^{n} (marks_i \times credit_i)}{\sum_{i=1}^{n} credit_i}")
    
    number_of_subjects_marks = st.number_input(
        label="Number of Subjects",
        help="Enter the number of subjects you are taking this semester",
        min_value=1,
        max_value=10,
        value=5,
        key="num_subjects_marks",
    ).__int__()

    marks = [0.0] * number_of_subjects_marks
    credit_marks = [0.0] * number_of_subjects_marks
    
    for i in range(number_of_subjects_marks):
        st.subheader(f"Subject #{i+1}")
        cols = st.columns(2)
        marks[i] = cols[0].number_input(
            label=f"Marks",
            min_value=0.0,
            max_value=100.0,
            value=75.0,
            step=0.5,
            key=f"marks_{i}",
        )

        credit_marks[i] = cols[1].number_input(
            label=f"Credit",
            min_value=1.0,
            max_value=10.0,
            value=4.0,
            step=0.5,
            key=f"credit_marks_{i}",
        )

    if st.button("Calculate SGPA"):
        weighted_marks_table = []
        total_credits = sum(credit_marks)
        total_weighted_marks = 0
        
        # Create a table showing calculation details
        for i, (mark, credit) in enumerate(zip(marks, credit_marks)):
            weighted_mark = mark * credit
            total_weighted_marks += weighted_mark
            weighted_marks_table.append({
                "Subject": f"Subject #{i+1}",
                "Marks": f"{mark:.1f}",
                "Credit": f"{credit:.1f}",
                "Marks × Credit": f"{weighted_mark:.1f}"
            })
        
        # Display calculation table
        st.markdown("### Calculation Details")
        st.table(weighted_marks_table)
        
        # Calculate and display SGPA
        sgpa = calculate_sgpa_from_marks(marks, credit_marks)
        st.info(f"Total Weighted Marks: {total_weighted_marks:.1f}")
        st.info(f"Total Credits: {total_credits:.1f}")
        st.success(f"Your SGPA is {sgpa:.2f}")


st.markdown("Made with ❤️ by [Siddhesh Agarwal](https://github.com/Siddhesh-Agarwal)")
st.markdown("Contributed by [Mit](https://github.com/vaguemit)")