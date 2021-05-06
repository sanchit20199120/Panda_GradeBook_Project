import pandas as pd
from pathlib import Path

Dir=Path(__file__).parent
print(Dir)
Data_file=Dir/"Data"
print(Data_file)

df1=pd.read_csv(Data_file/"roster.csv")

df2=pd.read_csv(Data_file/"hw_exam_grades.csv")


df3=pd.DataFrame()
for file_path in Data_file.glob('quiz_*_grades.csv'):
    grade_name=" ".join(file_path.stem.title().split("_"))
    print(file_path)
    print(grade_name)
    df4=pd.read_csv(file_path,
                    usecols=["Email","Grade"])


    print(df4)
    pd.concat([df3,df4],axis=0)
print(df3)

