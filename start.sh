#!/bin/bash

# 设置Python脚本的相对路径
SCRIPT1="./1_gesture/gesture.py"
SCRIPT2="./2_openai_api_test/api_test.py"

# 显示帮助信息的函数
show_help() {
  echo "使用:    ./start.sh [选项]"
  echo "选项:"
  echo "  1      运行($SCRIPT1)"
  echo "  2      运行($SCRIPT2)"
  echo "  h/-h   帮助"
}

# 检查参数并运行相应的Python脚本
case $1 in
  "1")
    echo "正在运行脚本 1: $SCRIPT1"
    python3 $SCRIPT1
    ;;
  "2")
    echo "正在运行脚本 2: $SCRIPT2"
    python3 $SCRIPT2
    ;;
  "h"|"-h")
    show_help
    ;;
  *)
    echo "无效的选项。输入 'h' 或 '-h' 查看使用说明。"
    exit 1
    ;;
esac

