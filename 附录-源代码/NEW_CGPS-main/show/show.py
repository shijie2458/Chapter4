import os
import json
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 读取JSON文件
with open('E:/person_search/CGPS-main/CGPS-main/show/results.json', 'r') as file:
    data = json.load(file)

# 查询图像的文件名
query_gt_filename = "s13011.jpg"

# 存储路径
save_path = "C:/Users/shijie/Desktop/2/data/"

# 查找包含当前查询图像的条目
query_info = None
for entry in data["results"]:
    if entry.get("query_img") == query_gt_filename:
        query_info = entry
        break

if query_info is None:
    print(f"Query image {query_gt_filename} not found in the data.")
    exit()

# 提取query_gt图像和gallery图像信息
query_gt_info = query_info["query_roi"]
gallery_info = query_info["gallery"]

# 创建包含query_img_filename的文件夹
query_save_path = os.path.join(save_path, query_gt_filename)
os.makedirs(query_save_path, exist_ok=True)

# 显示query_gt图像
query_img_path = "E:/person_search/COAT-main/COAT-main/datasets/cuhk_sysu/cuhk_sysu/Image/SSM/" + query_gt_filename
query_img = Image.open(query_img_path)

# 显示query_roi
query_roi = query_gt_info
query_bbox = patches.Rectangle((query_roi[0], query_roi[1]), query_roi[2] - query_roi[0], query_roi[3] - query_roi[1],
                               linewidth=2, edgecolor='y', facecolor='none')
plt.imshow(query_img)
plt.gca().add_patch(query_bbox)
plt.title('Query Image')

# 保存query_gt图像
query_gt_save_filename = f'query_gt_result_{query_gt_filename}'
query_gt_save_path = os.path.join(query_save_path, query_gt_save_filename)
plt.savefig(query_gt_save_path)
plt.show()

# 显示并保存gallery图像
for i, gallery_item in enumerate(gallery_info):
    # 判断是否为查询图像
    gallery_img_path = "E:/person_search/COAT-main/COAT-main/datasets/cuhk_sysu/cuhk_sysu/Image/SSM/" + gallery_item["img"]
    gallery_img = Image.open(gallery_img_path)

    # 根据correct字段决定框的颜色
    if gallery_item["correct"] == 0:
        bbox_color = 'r'  # 红色框
    else:
        bbox_color = 'g'  # 绿色框

    # 显示gallery_roi
    gallery_roi = gallery_item["roi"]
    gallery_bbox = patches.Rectangle((gallery_roi[0], gallery_roi[1]), gallery_roi[2] - gallery_roi[0],
                                     gallery_roi[3] - gallery_roi[1], linewidth=2, edgecolor=bbox_color, facecolor='none')

    plt.imshow(gallery_img)
    plt.gca().add_patch(gallery_bbox)
    plt.title(f'Gallery Image {gallery_item["img"]} - Score: {gallery_item["score"]}')

    # 保存每个gallery图像
    gallery_save_filename = f'gallery_result_{gallery_item["img"]}'
    gallery_save_path = os.path.join(query_save_path, gallery_save_filename)
    plt.savefig(gallery_save_path)
    plt.show()
