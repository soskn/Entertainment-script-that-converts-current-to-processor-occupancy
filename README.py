import subprocess
import json
import time

def show_float_notification(content):
    subprocess.run(["termux-toast", content])

def get_current():
    try:
        output = subprocess.check_output(["termux-battery-status"]).decode("utf-8")
        battery_info = json.loads(output)
        if "current" in battery_info:
            return int(battery_info["current"])
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None

def map_current_to_cpu_usage(current):
    max_current = 2250  # Assume the maximum current is 2250 mA, corresponding to 100% CPU usage假设最大电流为2250毫安，对应100%的CPU使用率
    if current is not None:
        if current <= max_current:
            return round((current / max_current) * 100, 2)  # Round decimals to two places将小数舍入到两位
        else:
            return "Error: Current value exceeds expected maximum."
    else:
        return "Error: Unable to retrieve current value."

try:
    while True:
        # Get current value获取电流值
        current_value = get_current()

        # Calculate CPU usage计算CPU占用率
        cpu_usage_percentage = map_current_to_cpu_usage(current_value)

        # Build a floating notification message构建悬浮通知消息
        notification_text = f"Current: {current_value}mA\nEstimated CPU Usage: {cpu_usage_percentage}%"

        # Show floating notification显示悬浮通知
        show_float_notification(notification_text)
        
        time.sleep(1)  # Refresh every second每秒刷新一次
except KeyboardInterrupt:
    print("\nExiting...")
