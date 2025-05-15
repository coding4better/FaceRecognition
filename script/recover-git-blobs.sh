#!/bin/bash

# 指定你的项目路径
PROJECT_PATH="E:/study/project/face/FaceRecognition"

# 创建恢复目录
RECOVERY_DIR="$HOME/git-recovery"
mkdir -p "$RECOVERY_DIR"

# 切换到项目目录
cd "$PROJECT_PATH" || { echo "错误: 无法进入项目目录"; exit 1; }

# 获取所有dangling blob的哈希值
blobs=$(git fsck --lost-found 2>/dev/null | grep "dangling blob" | awk '{print $3}')

# 检查是否找到任何blob
if [ -z "$blobs" ]; then
    echo "未找到dangling blob，可能所有文件都已正确引用。"
    exit 0
fi

# 恢复每个blob
echo "找到 $(echo "$blobs" | wc -l) 个dangling blob，开始恢复..."
for blob in $blobs; do
    echo "正在恢复: $blob"
    git cat-file -p "$blob" > "$RECOVERY_DIR/$blob" 2>/dev/null
done

echo "恢复完成！文件已保存到 $RECOVERY_DIR"

# 在恢复完成后添加验证
echo "验证恢复结果..."
file_count=$(ls -1 "$RECOVERY_DIR" 2>/dev/null | wc -l)

if [ "$file_count" -eq 0 ]; then
    echo "错误: 未恢复任何文件！可能是git命令执行失败。"
else
    echo "成功恢复 $file_count 个文件。"
    echo "查看恢复的文件: ls -lh $RECOVERY_DIR"
fi

read -p "按Enter键退出..."