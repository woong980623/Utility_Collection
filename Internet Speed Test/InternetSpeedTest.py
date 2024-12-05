import speedtest

def test_speed():
    st = speedtest.Speedtest()
    print("서버 목록을 불러오는 중...")
    st.get_servers()
    print("가장 최적의 서버를 선택하는 중...")
    st.get_best_server()
    
    print("\n다운로드 속도 측정 중...")
    download_speed = st.download() / 1_000_000  # Mbps로 변환
    print(f"다운로드 속도: {download_speed:.2f} Mbps")
    
    print("\n업로드 속도 측정 중...")
    upload_speed = st.upload() / 1_000_000  # Mbps로 변환
    print(f"업로드 속도: {upload_speed:.2f} Mbps")
    
    print("\n핑(Ping) 테스트 중...")
    ping = st.results.ping
    print(f"핑: {ping:.2f} ms")

if __name__ == "__main__":
    print("=== 인터넷 속도 측정기 ===")
    test_speed()
