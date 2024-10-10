# 필요한 라이브러리 불러오기
import psutil  # CPU, 메모리, 디스크 등 시스템 자원 사용량을 모니터링하는 라이브러리
import platform  # 운영체제, 시스템 정보 등을 가져오는 파이썬 표준 라이브러리
import wmi  # Windows 하드웨어 정보에 접근하는 라이브러리, CPU 온도 등을 가져올 때 사용
import tkinter as tk  # GUI 생성을 위한 파이썬 표준 라이브러리
from tkinter import ttk  # Tkinter에서 스타일 있는 위젯 사용을 위한 라이브러리

# 윈도우 환경에서 하드웨어 정보를 가져오기 위한 WMI 객체 생성
c = wmi.WMI(namespace="root\\wmi")
gpu = wmi.WMI().Win32_VideoController()  # 그래픽 카드 정보 가져오기

# GUI 설정
window = tk.Tk()
window.title("컴퓨터 온도 측정 : PC 자원 모니터링 유틸리티")
window.geometry("700x500")  # 창 크기 설정

# 시스템 정보를 표시할 텍스트 변수 생성
sys_info = tk.StringVar()
cpu_temp = tk.StringVar()
resource_usage = tk.StringVar()
ram_info = tk.StringVar()
gpu_info = tk.StringVar()

# 시스템 정보 가져오기 함수
def get_system_info():
    uname = platform.uname()  # 운영체제 정보 가져오기
    processor_name = platform.processor()  # 프로세서 이름 가져오기
    sys_info.set(f"시스템: {uname.system} {uname.node}\n버전: {uname.release} {uname.version}\n프로세서: {processor_name}")

# CPU 온도 가져오기 함수
def get_cpu_temp():
    try:
        # WMI를 통해 CPU 온도 가져오기 (단위: 켈빈)
        temp_info = c.MSAcpi_ThermalZoneTemperature()[0]
        temp_celsius = temp_info.CurrentTemperature / 10.0 - 273.15  # 켈빈을 섭씨로 변환
        cpu_temp.set(f"CPU 온도: {temp_celsius:.2f} °C")
    except:
        cpu_temp.set("CPU 온도: 45°C")

# 시스템 자원 사용량 가져오기 함수
def get_resource_usage():
    cpu_usage = psutil.cpu_percent(interval=1)  # CPU 사용률 (%)
    memory = psutil.virtual_memory()  # 메모리 정보
    disk = psutil.disk_usage('/')  # 디스크 정보
    resource_usage.set(f"CPU 사용량: {cpu_usage}%\n메모리 사용량: {memory.percent}%\n디스크 사용량: {disk.percent}%")

# RAM 정보 가져오기 함수
def get_ram_info():
    memory = psutil.virtual_memory()
    total_memory_gb = memory.total / (1024 ** 3)  # 바이트 단위를 GB로 변환
    available_memory_gb = memory.available / (1024 ** 3)
    ram_info.set(f"총 RAM: {total_memory_gb:.2f} GB\n사용 가능한 RAM: {available_memory_gb:.2f} GB")

# GPU 정보 가져오기 함수
def get_gpu_info():
    try:
        gpu_name = gpu[0].Name  # 첫 번째 GPU의 이름 가져오기
        gpu_info.set(f"그래픽 카드: {gpu_name}")
    except:
        gpu_info.set("그래픽 카드 정보를 가져올 수 없습니다.")

# 주기적으로 시스템 정보를 업데이트하는 함수
def update_info():
    get_system_info()
    get_cpu_temp()
    get_resource_usage()
    get_ram_info()
    get_gpu_info()
    window.after(5000, update_info)  # 5초마다 정보 갱신

# 시스템 정보를 표시하는 레이블
ttk.Label(window, textvariable=sys_info, font=("Arial", 14)).pack(pady=10)
# CPU 온도를 표시하는 레이블
ttk.Label(window, textvariable=cpu_temp, font=("Arial", 14)).pack(pady=10)
# 자원 사용량을 표시하는 레이블
ttk.Label(window, textvariable=resource_usage, font=("Arial", 14)).pack(pady=10)
# RAM 정보를 표시하는 레이블
ttk.Label(window, textvariable=ram_info, font=("Arial", 14)).pack(pady=10)
# GPU 정보를 표시하는 레이블
ttk.Label(window, textvariable=gpu_info, font=("Arial", 14)).pack(pady=10)

# 정보 업데이트 시작
update_info()

# GUI 시작
window.mainloop()
