import json
import os
import shutil
 
 
def labelme2yolo_seg(class_name, json_dir, output_dir):
    """
        此函数用来将labelme软件标注好的json格式转换为yolov_seg中使用的txt格式
        :param json_dir: labelme标注好的*.json文件所在文件夹
        :param output_dir: 输出根目录
        :param class_name: 数据集中的类别标签
        :return:
    """
    list_labels = []  # 存放json文件的列表
 
    # 0.创建保存转换结果的文件夹结构
    train_labels_dir = os.path.join(output_dir, "labels", "train")
    train_images_dir = os.path.join(output_dir, "images", "train")
    
    os.makedirs(train_labels_dir, exist_ok=True)
    os.makedirs(train_images_dir, exist_ok=True)
 
    # 1.获取目录下所有的labelme标注好的Json文件，存入列表中
    for files in os.listdir(json_dir):  # 遍历json文件夹下的所有json文件
        if files.endswith('.json'):  # 只处理json文件
            file = os.path.join(json_dir, files)  # 获取一个json文件
            list_labels.append(file)  # 将json文件名加入到列表中
 
    processed_count = 0
    for labels in list_labels:  # 遍历所有json文件
        try:
            with open(labels, "r", encoding='utf-8') as f:  # 添加编码格式
                file_in = json.load(f)
                shapes = file_in["shapes"]
                image_path = file_in.get("imagePath", "")
                print(f"Processing: {labels}")
 
            # 检查是否有标注
            has_annotations = False
            for shape in shapes:
                if shape['shape_type'] == 'polygon' and shape['label'] in class_name:
                    has_annotations = True
                    break
            
            if has_annotations:
                # 生成txt文件
                txt_filename = os.path.basename(labels).replace(".json", ".txt")
                txt_path = os.path.join(train_labels_dir, txt_filename)
 
                with open(txt_path, "w+", encoding='utf-8') as file_handle:
                    for shape in shapes:
                        # 只处理多边形类型的标注
                        if shape['shape_type'] == 'polygon':
                            line_content = []  # 初始化一个空列表来存储每个形状的坐标信息
                            
                            # 检查标签是否在类别列表中
                            if shape['label'] in class_name:
                                line_content.append(str(class_name.index(shape['label'])))  # 添加类别索引
                                
                                # 添加坐标信息
                                for point in shape["points"]:
                                    x = point[0] / file_in["imageWidth"]
                                    y = point[1] / file_in["imageHeight"]
                                    line_content.append(str(x))
                                    line_content.append(str(y))
                                
                                # 使用空格连接列表中的所有元素，并写入文件
                                file_handle.write(" ".join(line_content) + "\n")
                            else:
                                print(f"Warning: Unknown label '{shape['label']}' in {labels}")
                
                # 复制对应的图片文件到images/train目录
                if image_path:
                    # 如果imagePath是相对路径，则在json_dir中查找
                    if not os.path.isabs(image_path):
                        source_image_path = os.path.join(json_dir, image_path)
                    else:
                        source_image_path = image_path
                    
                    if os.path.exists(source_image_path):
                        dest_image_path = os.path.join(train_images_dir, os.path.basename(image_path))
                        shutil.copy2(source_image_path, dest_image_path)
                        print(f"Copied image: {os.path.basename(image_path)}")
                    else:
                        # 尝试根据json文件名推断图片文件名
                        base_name = os.path.splitext(os.path.basename(labels))[0]
                        for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
                            potential_image = os.path.join(json_dir, base_name + ext)
                            if os.path.exists(potential_image):
                                dest_image_path = os.path.join(train_images_dir, base_name + ext)
                                shutil.copy2(potential_image, dest_image_path)
                                print(f"Copied image: {base_name + ext}")
                                break
                        else:
                            print(f"Warning: Could not find image file for {labels}")
                
                processed_count += 1
            else:
                print(f"Skipping {labels}: No valid annotations found")
                            
        except Exception as e:
            print(f"Error processing {labels}: {e}")
    
    print(f"Processed {processed_count} files with annotations")


def main():
    """
    主函数，运行labelme到yolo格式转换
    """
    # 配置参数
    json_dir = r"d:\Github\datasets2\rawimg_2\rawimg2"  # labelme标注的json文件夹路径
    output_dir = r"d:\Github\datasets2"  # YOLO数据集输出根目录
    class_name = ["0"]  # 根据您的json文件，类别标签为"0"
    
    # 检查输入目录是否存在
    if not os.path.exists(json_dir):
        print(f"Error: JSON directory '{json_dir}' does not exist!")
        return
    
    # 执行转换
    print("Starting labelme to YOLO segmentation format conversion...")
    labelme2yolo_seg(class_name, json_dir, output_dir)
    
    print("Conversion completed!")
    print(f"Dataset structure created at: {output_dir}")
    print("Directory structure:")
    print(f"  {output_dir}/")
    print("    ├── images/")
    print("    │   └── train/")
    print("    └── labels/")
    print("        └── train/")

if __name__ == "__main__":
    main()
