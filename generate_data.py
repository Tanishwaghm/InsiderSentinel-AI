import pandas as pd
import numpy as np

np.random.seed(42)

data = []

for i in range(1500):
    login_hour = np.random.normal(10, 2)
    files_accessed = np.random.normal(8, 3)
    data_downloaded = np.random.normal(50, 20)
    failed_logins = np.random.poisson(1)

    data.append([
        abs(round(login_hour, 2)),
        abs(round(files_accessed, 2)),
        abs(round(data_downloaded, 2)),
        failed_logins
    ])

df = pd.DataFrame(data, columns=[
    "login_hour",
    "files_accessed",
    "data_downloaded_MB",
    "failed_logins"
])

df.to_csv("employee_activity.csv", index=False)
print("Dataset generated successfully!")
