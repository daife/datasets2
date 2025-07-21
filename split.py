import os
import random
import shutil

def split_train_val(
    base_dir=r'd:\Github\datasets2',
    train_folder='train',
    val_folder='val',
    val_ratio=0.2,
    seed=42
):
    img_train_dir = os.path.join(base_dir, 'images', train_folder)
    lbl_train_dir = os.path.join(base_dir, 'labels', train_folder)
    img_val_dir = os.path.join(base_dir, 'images', val_folder)
    lbl_val_dir = os.path.join(base_dir, 'labels', val_folder)

    os.makedirs(img_val_dir, exist_ok=True)
    os.makedirs(lbl_val_dir, exist_ok=True)

    # 获取所有图片文件名（不含扩展名）
    img_files = [f for f in os.listdir(img_train_dir) if os.path.splitext(f)[1].lower() in ['.jpg', '.jpeg', '.png', '.bmp']]
    img_basenames = [os.path.splitext(f)[0] for f in img_files]

    # 随机抽取部分用于验证集
    random.seed(seed)
    val_count = int(len(img_basenames) * val_ratio)
    val_samples = set(random.sample(img_basenames, val_count))

    moved = 0
    for basename in img_basenames:
        if basename in val_samples:
            # 移动图片
            for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
                img_path = os.path.join(img_train_dir, basename + ext)
                if os.path.exists(img_path):
                    shutil.move(img_path, os.path.join(img_val_dir, basename + ext))
                    break
            # 移动标签
            label_path = os.path.join(lbl_train_dir, basename + '.txt')
            if os.path.exists(label_path):
                shutil.move(label_path, os.path.join(lbl_val_dir, basename + '.txt'))
            moved += 1

    print(f"已将 {moved} 个样本从 train 拆分到 val。")
    print(f"train 剩余图片数: {len(os.listdir(img_train_dir))}")
    print(f"val 图片数: {len(os.listdir(img_val_dir))}")

if __name__ == "__main__":
    split_train_val()
