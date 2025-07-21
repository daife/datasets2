import os

folder = r'd:\Github\datasets2\rawimg_2\rawimg'
offset = 45

for filename in os.listdir(folder):
    name, ext = os.path.splitext(filename)
    if ext.lower() in ['.jpg', '.json']:
        try:
            num = int(name)
            new_name = f"{num + offset:04d}{ext}"
            src = os.path.join(folder, filename)
            dst = os.path.join(folder, new_name)
            os.rename(src, dst)
            print(f"{filename} -> {new_name}")
        except ValueError:
            # 跳过非数字命名的文件
            continue
