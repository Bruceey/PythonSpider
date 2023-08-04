import os
import shutil


dir = r'D:\Users\Pictures\xrmn\杨晨晨'
os.makedirs(os.path.join(dir, 'total'), exist_ok=True)

for subdir in os.listdir(dir):
    if subdir != "total":
        print(f"进入 {subdir}")
        for file in os.listdir(os.path.join(dir, subdir)):
            filename = f"{subdir}_{file}"
            shutil.copy(os.path.join(dir, subdir, file), os.path.join(dir, "total", filename))
