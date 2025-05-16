# Face Recognition Project  
## 人脸识别项目  

### 项目概述  
本项目是基于Python和OpenCV的人脸识别系统，包含人脸检测、年龄性别识别、关键点检测等功能，适用于AI课程设计或计算机视觉相关开发。  

### 文件夹结构  
    FaceRecognition/
    ├── scripts/ # 脚本文件
    │ ├── export_git_objects.sh # Git 对象导出脚本
    │ ├── txt_to_json_converter.sh # 格式转换脚本
    │ └── recover_git_blobs.sh # Git 对象恢复脚本
    ├── src/ # 源代码
    │ ├── data_processing/ # 数据获取和预处理
    │ │ ├── face_capture_dataset.py # 数据集获取
    │ │ ├── image_dataset_preprocessing.py # 获取人脸预处理
    │ │ └── load_face_dataset.py # 加载数据
    │ ├── models/ 
    │ │ ├── face_dataset_and_model.py # 数据加载和模型构建
    │ │ └── face_verification.py # 人脸验证
    │ ├── detection/ # 检测功能模块
    │ │ └── landmarks_detector.py 
    │ └── ui/ # UI界面
    │   ├── config.py # 配置文件
    │   └── data_utils.py # 数据处理工具
    ├── models/ # 模型管理
    │ └── manage.xml
    ├── data/ 
    │ ├── dataset/ 
    │ │ ├── train/ # 训练数据
    │ │ └── test/ # 测试数据
    │ └── dataset_metadata.json # 数据集元数据
    ├── LICENSE # 开源协议
    └── README.md # 项目说明


## 结构说明
1. **scripts/**  
   存放与版本控制（Git）和数据格式转换相关的脚本，用于辅助项目管理和数据处理。

2. **src/**  
   核心功能代码按模块划分：  
   - **data/**：负责数据加载、清洗和预处理。  
   - **models/**：包含模型构建、训练和评估的代码。  
   - **detectors/**：实现具体的计算机视觉检测功能。  
   - **ui/**：处理用户界面逻辑，通常基于PyQt或Tkinter。  
   - **utils/**：存放通用工具函数，提高代码复用性。

3. **models/**  
   存储预训练模型文件和配置，便于快速调用和部署。

4. **ui_design/**  
   保存UI设计的源文件（如Qt的.ui文件），可通过工具转换为Python代码。

5. **data/**  
   包含示例数据和训练数据，建议按类型或用途进一步细分目录。

6. **tests/**  
   维护单元测试代码，确保各功能模块的稳定性。

---
# Face Recognition Project

## Folder Structure
    FaceRecognition/
    ├── scripts/ # 脚本文件
    │ ├── export_git_objects.sh # Git 对象导出脚本
    │ ├── txt_to_json_converter.sh # 格式转换脚本
    │ └── recover_git_blobs.sh # Git 对象恢复脚本
    ├── src/ # 源代码
    │ ├── data_processing/ # 数据获取和预处理
    │ │ ├── face_capture_dataset.py # 数据集获取
    │ │ ├── image_dataset_preprocessing.py # 获取人脸预处理
    │ │ └── load_face_dataset.py # 加载数据
    │ ├── models/ 
    │ │ ├── face_dataset_and_model.py # 数据加载和模型构建
    │ │ └── face_verification.py # 人脸验证
    │ ├── detection/ # 检测功能模块
    │ │ └── landmarks_detector.py 
    │ └── ui/ # UI界面
    │   ├── config.py # 配置文件
    │   └── data_utils.py # 数据处理工具
    ├── models/ # 模型管理
    │ └── manage.xml
    ├── data/ 
    │ ├── dataset/ 
    │ │ ├── train/ # 训练数据
    │ │ └── test/ # 测试数据
    │ └── dataset_metadata.json # 数据集元数据
    ├── LICENSE # 开源协议
    └── README.md # 项目说明


## Structure Explanation
1. **scripts/**  
   Stores scripts for version control (Git) and data format conversion, aiding project management and data processing.

2. **src/**  
   Core functionality organized by module:  
   - **data/**: Handles data loading, cleaning, and preprocessing.  
   - **models/**: Contains model building, training, and evaluation code.  
   - **detectors/**: Implements computer vision detection features.  
   - **ui/**: Manages user interface logic, typically based on PyQt or Tkinter.  
   - **utils/**: Houses reusable utility functions to enhance code efficiency.

3. **models/**  
   Stores pretrained models and configurations for quick integration and deployment.

4. **ui_design/**  
   Saves UI design source files (e.g., Qt .ui files), which can be converted to Python code.

5. **data/**  
   Contains sample and training data, organized by type or purpose.

6. **tests/**  
   Maintains unit tests to ensure the stability of functional modules.