import pandas as pd
from pathlib import Path

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
final_data["sum_homework_score"] = final_data.filter(regex=r"^Homework \d\d?$", axis=1).sum(axis=1)
final_data["sum_Homework_Max_Points"] = final_data.filter(regex=r"^Homework \d\d? -", axis=1).sum(axis=1)
final_data["Total Homework"]= (final_data["sum_homework_score"]/final_data["sum_Homework_Max_Points"])

print(final_data.columns)
print(final_data[["sum_homework_score","sum_Homework_Max_Points","Total Homework"]])

