import pandas as pd  # pylint: disable=import-error
import matplotlib.pyplot as plt  # pylint: disable=import-error


def create_dataframe(csv_path):
    """
    Convert csv file to pandas dataframe

    Args:
        csv_path: A string representing the name of the csv being converted
    """
    return pd.read_csv(csv_path)


def student_vs_score(summaries, assignment_name, ax):
    """
    Create a bar graph where students are on the x-axis and scores are on the y-axis
    Create graph using data from the specified assignment

    Args:
        assignment_name: String representing the name of the assignment being graphed
        summares: dataframe that contains all the Canvas data
        ax: a Pandas axes
    """

    filtered_data = summaries[summaries["Assignment"] == assignment_name]
    scores = filtered_data["Quiz Grade"]
    names = filtered_data["name"]
    ax.bar(names, scores)
    ax.set_xlabel("Student")
    ax.set_ylabel("Quiz Score (%)")
    ax.set_title(f"Scores for {assignment_name}")
    ax.set_ylim(0, 100)


def student_vs_time(summaries, assignment_name, ax):
    """
    Create a histogram of time spent on the specified assignment

    Args:
        assignment_name: String representing the name of the assignment being graphed
        summares: dataframe that contains all the Canvas data
        ax: a Pandas axes
    """
    filtered_data = summaries[summaries["Assignment"] == assignment_name]
    time = filtered_data["How much time (in hours) did you spend on this assignment?"]

    # Make it so times go in order
    time_spent_order = ["0-2", "3-5", "6-8", "9-11", "12-14", ">= 15"]
    time_existing = []
    for t in time_spent_order:
        if t in time.values:
            time_existing.append(t)

    # Plot times
    time.value_counts().loc[time_existing].plot.bar(ax=ax)
    ax.set_xlabel("Time Spent (Hours)")
    ax.set_ylabel("Number of Students")
    ax.set_title(f"Time Spent for {assignment_name}")


def assignment_vs_score(summaries, num_students, ax):
    """
    Create a line graph of num_students random students where the assignment
    number is the x-axis and the quiz score is the y-axis

    Args:
        summares: dataframe that contains all the Canvas data
        num_students: an int representing the number of students to plot
            Must be less than or equal to the number of students in the class
        ax: a Pandas axes
    """
    if num_students > len(summaries["name"].unique()):
        raise ValueError(
            "num_students must be less than or equal to the number of students in the class"
        )

    students_plotted = []

    for _ in range(num_students):
        student_name = get_random_student(summaries)
        while student_name in students_plotted:
            student_name = get_random_student(summaries)
        student_data = summaries[summaries["name"] == student_name]
        assignment_names = student_data["Assignment"].values

        # Isolate Assignment numbers
        assignment_numbers = []
        for assignment in assignment_names:
            assignment_num = int(assignment[9:])
            assignment_numbers.append(assignment_num)

        quiz_scores = student_data["Quiz Grade"]
        ax.plot(assignment_numbers, quiz_scores, "-o", label=f"{student_name}")
        students_plotted.append(student_name)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Assignment Number")
    ax.set_ylabel("Quiz Score (%)")
    ax.set_title("Scores Across Assignments")


def individual_assignment_vs_score(summaries, student_name, ax):
    """
    Create a line graph for the specified student where assignment number is the
    x-axis and the quiz score is the y-axis

    Args:
        summares: dataframe that contains all the Canvas data
        student_name: a String representing the student we're plotting
        ax: a Pandas axes
    """
    student_data = summaries[summaries["name"] == student_name]
    assignment_names = student_data["Assignment"].values

    # Isolate Assignment numbers
    assignment_numbers = []
    for assignment in assignment_names:
        assignment_num = int(assignment[9:])
        assignment_numbers.append(assignment_num)

    quiz_scores = student_data["Quiz Grade"]
    ax.plot(assignment_numbers, quiz_scores, "-o", label=f"{student_name}")
    ax.set_ylim(0, 100)
    ax.set_xlabel("Assignment Number")
    ax.set_ylabel("Quiz Score (%)")
    ax.set_title("Scores Across Assignments")


def average_assignment_vs_score(summaries, ax):
    """
    Create a line graph where assignment number is the
    x-axis and the average quiz score is the y-axis

    Args:
        summares: dataframe that contains all the Canvas data
        ax: a Pandas axes
    """
    assignment_names = [
        "Homework 1",
        "Homework 2",
        "Homework 3",
        "Homework 4",
        "Homework 5",
        "Homework 6",
        "Homework 7",
        "Homework 8",
        "Homework 9",
        "Homework 10",
    ]
    existing_assignments = []
    quiz_averages = []
    for assignment_name in assignment_names:
        if not summaries[summaries["Assignment"] == assignment_name].empty:
            filtered_data = summaries[summaries["Assignment"] == assignment_name]
            scores = filtered_data["Quiz Grade"]
            existing_assignments.append(assignment_name)
            average_score = scores.mean()
            quiz_averages.append(average_score)

    # Isolate Assignment numbers
    assignment_numbers = []
    for assignment in existing_assignments:
        assignment_num = int(assignment[9:])
        assignment_numbers.append(assignment_num)

    ax.plot(assignment_numbers, quiz_averages, "-o")
    ax.set_ylim(0, 100)
    ax.set_xlabel("Assignment Number")
    ax.set_ylabel("Quiz Average (%)")
    ax.set_title("Quiz Scores Across Assignments")


def get_random_student(summaries):
    """
    Get a random row from the given data frame and extract the value from the name column

    Args:
        summaries: dataframe that contains all the Canvas data

    Returns:
        name: a String that represents the name of a student
    """
    random_row = summaries.sample()
    name = random_row["name"].values[0]
    return name


def assignment_vs_time(summaries, num_students, ax):
    """
    Create a line graph of num_students random students where the assignment
    number is the x-axis and the time spent is the y-axis

    Args:
        summares: dataframe that contains all the Canvas data
        num_students: an int representing the number of students to plot
            Must be less than or equal to the number of students in the class
        ax: a Pandas axes
    """
    unique_students = len(summaries["name"].unique())
    if num_students > unique_students:
        raise ValueError(
            f"num_students must be less than or equal to the number of students in the class, which is {unique_students}"
        )

    students_plotted = []
    y_order = ["0-2", "3-5", "6-8", "9-11", "12-14", ">= 15"]

    for _ in range(num_students):
        student_name = get_random_student(summaries)
        while student_name in students_plotted:
            student_name = get_random_student(summaries)
        student_data = summaries[summaries["name"] == student_name]
        assignment_names = student_data["Assignment"].values

        # Isolate Assignment numbers
        assignment_numbers = []
        for assignment in assignment_names:
            assignment_num = int(assignment[9:])
            assignment_numbers.append(assignment_num)

        # Convert time spent to a categorical type with the specified order
        student_data["Time Spent"] = pd.Categorical(
            student_data["How much time (in hours) did you spend on this assignment?"],
            categories=y_order,
            ordered=True,
        )

        time_spent_codes = student_data["Time Spent"].cat.codes

        ax.plot(assignment_numbers, time_spent_codes, "-o", label=f"{student_name}")
        students_plotted.append(student_name)
    ax.set_xlabel("Assignment Number")
    ax.set_ylabel("Time Spent (Hours)")
    ax.set_yticks(range(len(y_order)), y_order)

    ax.set_title("Time Across Assignments")


def individual_assignment_vs_time(summaries, student_name, ax):
    """
    Create a line graph for the specified student where assignment number is the
    x-axis and the time spent is the y-axis

    Args:
        summares: dataframe that contains all the Canvas data
        student_name: a String representing the student we're plotting
        ax: a Pandas axes
    """
    y_order = ["0-2", "3-5", "6-8", "9-11", "12-14", ">= 15"]
    student_data = summaries[summaries["name"] == student_name]
    assignment_names = student_data["Assignment"].values

    # Isolate Assignment numbers
    assignment_numbers = []
    for assignment in assignment_names:
        assignment_num = int(assignment[9:])
        assignment_numbers.append(assignment_num)

        # Convert time spent to a categorical type with the specified order
        student_data["Time Spent"] = pd.Categorical(
            student_data["How much time (in hours) did you spend on this assignment?"],
            categories=y_order,
            ordered=True,
        )

        time_spent_codes = student_data["Time Spent"].cat.codes

    ax.plot(assignment_numbers, time_spent_codes, "-o", label=f"{student_name}")
    ax.set_xlabel("Assignment Number")
    ax.set_ylabel("Time Spent")
    ax.set_yticks(range(len(y_order)), y_order)
    ax.set_title("Time Spent Across Assignments")


def average_assignment_vs_time(summaries, ax):
    """
    Create a line graph where assignment number is the
    x-axis and the average quiz score is the y-axis

    Args:
        summares: dataframe that contains all the Canvas data
        ax: a Pandas axes
    """
    assignment_names = [
        "Homework 1",
        "Homework 2",
        "Homework 3",
        "Homework 4",
        "Homework 5",
        "Homework 6",
        "Homework 7",
        "Homework 8",
        "Homework 9",
        "Homework 10",
    ]
    y_order = ["0-2", "3-5", "6-8", "9-11", "12-14", ">= 15"]
    existing_assignments = []
    time_averages = []
    for assignment_name in assignment_names:
        if not summaries[summaries["Assignment"] == assignment_name].empty:
            filtered_data = summaries[summaries["Assignment"] == assignment_name]
            filtered_data["Time Spent"] = pd.Categorical(
                filtered_data[
                    "How much time (in hours) did you spend on this assignment?"
                ],
                categories=y_order,
                ordered=True,
            )

            time_spent_codes = filtered_data["Time Spent"].cat.codes
            existing_assignments.append(assignment_name)
            average_time = time_spent_codes.mean()
            time_averages.append(average_time)

    # Isolate Assignment numbers
    assignment_numbers = []
    for assignment in existing_assignments:
        assignment_num = int(assignment[9:])
        assignment_numbers.append(assignment_num)

    ax.plot(assignment_numbers, time_averages, "-o")
    ax.set_xlabel("Assignment Number")
    ax.set_ylabel("Time Average (Hours)")
    ax.set_yticks(range(len(y_order)), y_order)

    ax.set_title("Time Spent Across Assignments")


def get_summary(gpt_summaries, assignment_name):
    assignment_summary = gpt_summaries[gpt_summaries["Assignment"] == assignment_name]
    return assignment_summary["Summary"].values[0]
