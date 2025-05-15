#!/bin/bash

RECOVERY_DIR="${1:-$HOME/git-recovery}"
echo "处理目录: $RECOVERY_DIR"

# 验证目录是否存在且非空
if [ ! -d "$RECOVERY_DIR" ]; then
    echo "错误: 目录 $RECOVERY_DIR 不存在！"
    exit 1
fi

if [ -z "$(ls -A "$RECOVERY_DIR")" ]; then
    echo "错误: 目录 $RECOVERY_DIR 为空！"
    exit 1
fi

cd "$RECOVERY_DIR" || { echo "错误: 无法进入目录 $RECOVERY_DIR"; exit 1; }

echo "开始将 .txt 文件转换为 .json 后缀..."
txt_count=0
converted_count=0

for file in *.txt; do
    if [ -f "$file" ]; then
        ((txt_count++))
        new_filename="${file%.txt}.json"
        mv "$file" "$new_filename"
        echo "已转换: $file -> $new_filename"
        ((converted_count++))
    fi
done

echo -e "\n处理完成！"
echo "共找到 $txt_count 个 .txt 文件"
echo "成功转换 $converted_count 个文件为 .json 后缀"