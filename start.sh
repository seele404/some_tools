#!/bin/bash

# 设置Python脚本的相对路径
SCRIPT1="./1_gesture/gesture.py"
SCRIPT2="./2_openai_api_test/api_test.py"
SCRIPT3="./3_quaternions_demo/quaternions_demo.py"
SCRIPT4="./4_proxy/proxy_test.py"

# 显示帮助信息的函数
show_help() {
  echo "使用:    ./start.sh [选项]"
  echo "选项:"
  echo "  1      手势识别	运行目标： $SCRIPT1"
  echo "  2      AI测试		运行目标： $SCRIPT2"
  echo "  3      四元数变换	运行目标： $SCRIPT3"
  echo "  4      代理归属地查询	运行目标： $SCRIPT4"
  echo "  h/-h   帮助"
}

# 检查参数并运行相应的Python脚本
case $1 in
  "1")
    echo -e "正在运行脚本 1: $SCRIPT1\n"
    python3 $SCRIPT1
    ;;
  "2")
    echo -e "正在运行脚本 2: $SCRIPT2\n"
    python3 $SCRIPT2
    ;;
  "3")
    echo -e "正在运行脚本 3: $SCRIPT3\n"
    python3 $SCRIPT3
    ;;
  "4")
    echo -e "正在运行脚本 4: $SCRIPT4\n"
    python3 $SCRIPT4
    ;;
  "h"|"-h")
    show_help
    ;;
  *)
    echo -e "无效的选项。附带参数 'h' 或 '-h' 查看使用说明。\n"
    exit 1
    ;;
esac

