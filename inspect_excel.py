import pandas as pd

file_path = "/Users/nileshtiwari/Downloads/DKD_Member_Name_UAN_Wages_DOJ.xlsx"
df = pd.read_excel(file_path)
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print("First 15 rows of the DataFrame:")
for idx, row in df.head(15).iterrows():
    print(f"Row {idx}: {row.tolist()}")
