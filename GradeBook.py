import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
import mysql.connector
cnx = mysql.connector.connect(user='root', password='20Sep199120@',
                              host='localhost',
                              database='grades',
                              )
cnx.close()


Dir = Path(__file__).parent
Data_file = Dir/"Data"

# loading data from 3 different sources anf transforming data

roster = pd.read_csv(Data_file/"roster.csv",
                     converters={"NetID": str.lower, "Email Address": str.lower},
                     usecols=["Section", "NetID", "Email Address"],
                     index_col="NetID")

hw_exam_grades=pd.read_csv(Data_file/"hw_exam_grades.csv",
                           converters={"SID":str.lower},
                           usecols=lambda x:"Submission" not in x,
                           index_col="SID")
quiz_grades=pd.DataFrame()
for file_path in Data_file.glob('quiz_*_grades.csv'):

    quiz_name = " ".join(file_path.stem.title().split("_")[:2])

    quiz = pd.read_csv(file_path,
                       converters={"Email": str.lower},
                       index_col=["Email"],
                       usecols=["Email", "Grade"]).rename(columns={"Grade": quiz_name})

    quiz_grades = pd.concat([quiz_grades, quiz], axis=1, sort=True)

# merging

merge_data = pd.merge(roster,
                      hw_exam_grades,
                      left_index=True,
                      right_index=True
                      )
final_data = pd.merge(merge_data,
                      quiz_grades,
                      left_on="Email Address",
                      right_index=True
                      )
final_data = final_data.fillna(0)

# calculating exam score
# loop over exam score and range is 1,4 beacuse there are only 3 exam in total


for n in range(1, 4):
    final_data[f"Exam {n} Score"] = (
        final_data[f"Exam {n}"] / final_data[f"Exam {n} - Max Points"]
    )


# calculating homework Score

homework_scores = final_data.filter(regex=r"^Homework \d\d?$", axis=1)
homework_max_points = final_data.filter(regex=r"^Homework \d\d? -", axis=1)

sum_of_hw_scores = homework_scores.sum(axis=1)

sum_of_hw_max = homework_max_points.sum(axis=1)

final_data["Total Homework"] = sum_of_hw_scores / sum_of_hw_max

hw_max_renamed = homework_max_points.set_axis(homework_scores.columns, axis=1,inplace=False)

average_hw_scores = (homework_scores / hw_max_renamed).sum(axis=1)

final_data["Average Homework"] = average_hw_scores / homework_scores.shape[1]


final_data["Homework Score"] = final_data[
    ["Total Homework", "Average Homework"]
].max(axis=1)


# calculating quiz score


quiz_scores = final_data.filter(regex=r"^Quiz \d$", axis=1)

quiz_max_points = pd.Series(
    {"Quiz 1": 11, "Quiz 2": 15, "Quiz 3": 17, "Quiz 4": 14, "Quiz 5": 12}
)
print(quiz_scores)
print(quiz_max_points)
sum_of_quiz_scores = quiz_scores.sum(axis=1)
sum_of_quiz_max = quiz_max_points.sum()
final_data["Total Quizzes"] = sum_of_quiz_scores / sum_of_quiz_max

average_quiz_scores = (quiz_scores / quiz_max_points).sum(axis=1)
final_data["Average Quizzes"] = average_quiz_scores / quiz_scores.shape[1]

final_data["Quiz Score"] = final_data[
    ["Total Quizzes", "Average Quizzes"]
].max(axis=1)






