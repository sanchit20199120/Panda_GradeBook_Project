import pandas as pd
from pathlib import Path

Dir=Path(__file__).parent
print(Dir)
Data_file=Dir/"Data"
print(Data_file)

df1=pd.read_csv(Data_file/"roster.csv")
print(df1)

df2=pd.read_csv(Data_file/"hw_exam_grades.csv")
print(df2)


df3=pd.DataFrame()
for file_path in Data_file.glob('quiz_*_grades.csv'):
    print(file_path)
    grade_name = " ".join(file_path.stem.title().split("_")[:2])
    print(grade_name)
    df4 = pd.read_csv(file_path,
                      index_col=["Email"],
                    usecols=["Email","Grade"]).rename(columns={"Grade":grade_name})

    df3=pd.concat([df3,df4],axis=1,sort=True)
print(df3)

