#!/bin/bash

# 检查参数是否存在
if [ -z "$1" ]; then
    echo "用法: $0 <对象列表文件> [恢复目录]"
    echo "示例: $0 ~/git-deep-recovery/objects.list ~/git-deep-recovery"
    exit 1
fi

# 获取参数
OBJECTS_FILE="$1"
RECOVERY_DIR="${2:-~/git-deep-recovery}"

# 检查对象列表文件是否存在
if [ ! -f "$OBJECTS_FILE" ]; then
    echo "错误: 文件 '$OBJECTS_FILE' 不存在！"
    exit 1
fi

# 检查对象列表是否为空
object_count=$(wc -l < "$OBJECTS_FILE")
if [ "$object_count" -eq 0 ]; then
    echo "错误: 对象列表文件 '$OBJECTS_FILE' 为空！"
    echo "可能原因："
    echo "  1. Git仓库没有丢失的对象"
    echo "  2. 之前生成对象列表的命令执行失败"
    echo "  3. 文件路径不正确"
    exit 1
fi

# 创建恢复目录（如果不存在）
mkdir -p "$RECOVERY_DIR" || { echo "错误: 无法创建恢复目录 '$RECOVERY_DIR'"; exit 1; }

# 后续脚本内容保持不变...
# 检查参数是否存在
if [ -z "$1" ]; then
    echo "用法: $0 <对象列表文件> [恢复目录]"
    echo "示例: $0 ~/git-deep-recovery/objects.list ~/git-deep-recovery"
    exit 1
fi

# 获取参数
OBJECTS_FILE="$1"
RECOVERY_DIR="${2:-~/git-deep-recovery}"

# 检查对象列表文件是否存在
if [ ! -f "$OBJECTS_FILE" ]; then
    echo "错误: 文件 '$OBJECTS_FILE' 不存在！"
    exit 1
fi

# 创建恢复目录（如果不存在）
mkdir -p "$RECOVERY_DIR" || { echo "错误: 无法创建恢复目录 '$RECOVERY_DIR'"; exit 1; }

# 计算要处理的对象数量
total_objects=$(wc -l < "$OBJECTS_FILE")
processed=0
start_time=$(date +%s)

echo "开始导出Git对象..."
echo "对象列表: $OBJECTS_FILE"
echo "恢复目录: $RECOVERY_DIR"
echo "总对象数: $total_objects"
echo "------------------------"

# 逐行读取对象哈希值并导出
while IFS= read -r object; do
    # 显示进度
    ((processed++))
    elapsed=$(( $(date +%s) - start_time ))
    if [ $elapsed -gt 0 ]; then
        rate=$(echo "scale=2; $processed / $elapsed" | bc)
    else
        rate="0.00"
    fi
    eta=$(echo "scale=0; ($total_objects - $processed) / $rate" | bc)
    
    printf "\r处理中: %d/%d [%3.1f%%] 速率: %.2f 对象/秒 预计剩余时间: %d秒" \
           "$processed" "$total_objects" "$(echo "scale=2; $processed * 100 / $total_objects" | bc)" "$rate" "$eta"
    
    # 获取对象类型
    type=$(git cat-file -t "$object" 2>/dev/null)
    
    if [ $? -ne 0 ]; then
        echo -e "\n警告: 对象 '$object' 无法识别，跳过"
        continue
    fi
    
    # 导出对象内容
    git cat-file -p "$object" > "$RECOVERY_DIR/${object}.${type}" 2>/dev/null
    
    if [ $? -ne 0 ]; then
        echo -e "\n警告: 对象 '$object' 内容无法导出"
    fi
    
done < "$OBJECTS_FILE"

echo -e "\n------------------------"
echo "导出完成！"
echo "处理的对象总数: $processed"
echo "查看恢复的文件: ls -lh $RECOVERY_DIR"