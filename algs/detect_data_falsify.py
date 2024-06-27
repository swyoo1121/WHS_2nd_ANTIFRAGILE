import os
from datetime import datetime
    
# 파일 헤더 시그니처 데이터베이스
file_header_signatures = {
    "JPEG": b"\xFF\xD8\xFF",
    "PNG": b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A",
    "PDF": b"%PDF",
    "ZIP": b"\x50\x4B\x03\x04",
    "GIF": b"\x47\x49\x46\x38",
    "BMP": b"\x42\x4D"
    # 다른 파일 형식 추가 가능
}

# 파일 푸터 시그니처 데이터베이스
file_footer_signatures = {
    "JPEG": b"\xFF\xD9",
    "PNG": b"\x49\x45\x4E\x44\xAE\x42\x60\x82",
    "GIF": b"\x00\x3B",
    "ZIP": b"\x50\x4B"
}

file_extensions = {
    "JPEG": [".jpg", ".jpeg"],
    "PNG": [".png"],
    "PDF": [".pdf"],
    "ZIP": [".zip"],
    "GIF": [".gif"],
    "BMP": [".bmp"]
}

# JPEG 파일 sos 마커 뒷부분 데이터
sos_marker = b"\xFF\xDA"
sos_marker_behind = b"\x00\x0C\x03\x01\x00\x02\x11\x03\x11\x00\x3F\x00"


def detect_file_type(file_path):
    with open(file_path, "rb") as file:
        # 파일의 헤더 부분 바이트 읽어오기
        header = file.read(16)

        # 파일의 푸터 부분 바이트 읽어오기
        file.seek(-16, 2)  # 파일 끝에서 16바이트 앞부분으로 이동, whence 2 = 끝에서 부터 커서 이동
        footer = file.read(16)

        # 파일 헤더 시그니처와 비교하여 파일 형식 결정
        detected_type = None
        for file_type, signature in file_header_signatures.items():
            if header.startswith(signature):
                detected_type = file_type
                break

        # 파일 푸터 시그니처와 비교 (헤더 시그니처가 일치하는 경우에 한함)
        footer_match = False
        if detected_type in file_footer_signatures:
            footer_signature = file_footer_signatures[detected_type]
            if footer.endswith(footer_signature):
                footer_match = True

        return detected_type, footer_match

#코드 변경 후 파일 확장자 비교부분 따로 추가
def check_file_extension(file_path, detected_type):
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()
    
    if detected_type in file_extensions:
        return file_extension in file_extensions[detected_type]
    return False

# 뒤에 숨겨진 파일이나 데이터 탐지
def hidden_data_detect(file_path, detected_type, recover_directory):
    # ANTIFRAGILE 복구폴더가 없다면 생성
    if not os.path.exists(recover_directory):
        os.makedirs(recover_directory)

    with open(file_path, "rb") as file:
        # 파일 다 읽어오기
        full_data = file.read()

    footer_signature = file_footer_signatures[detected_type]
    hidden_data_start = full_data.find(footer_signature) + len(footer_signature)
    hidden_data = full_data[hidden_data_start:]

    if len(hidden_data) == 0:
        return None

    # 파일이름이 같으면 덮어쓰기가 됨. -> 인덱스로 해결
    index = len(os.listdir(recover_directory)) + 1
    # index = 1로 하면 프로그램 다시 돌리면 오류 가능. 그래서 디렉토리 내 파일 개수를 기준으로 함.


    # JPEG 일때
    if hidden_data.startswith(b'\xFF\xD8'):
        file_out = os.path.join(recover_directory, f"복구파일_{index}.jpg")
    # PDF 일때
    elif hidden_data.startswith(b'%PDF'):
        file_out = os.path.join(recover_directory, f"복구파일_{index}.pdf")
    # PNG 일때
    elif hidden_data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        file_out = os.path.join(recover_directory, f"복구파일_{index}.png")
    # 그 외
    else:
        file_out = os.path.join(recover_directory, f"복구파일_{index}.txt")
        # file_out = f"{recovered_file}_복구파일.txt"

    # 숨겨진 데이터 파일로 저장
    with open(file_out, 'wb') as hidden_file:
        hidden_file.write(hidden_data)
        
    return file_out

def check_sos_marker(file_path):
    with open(file_path, "rb") as file:
        data = file.read()

    # SOS 마커 위치 찾기
    sos_marker_position = data.find(sos_marker)
    if sos_marker_position == -1:
        print(f"{file_path}: SOS 마커를 찾을 수 없습니다.")
        return False

    # SOS 마커 뒤의 데이터 추출 및 비교
    sos_data = data[sos_marker_position + len(sos_marker):sos_marker_position + len(sos_marker) + len(sos_marker_behind)]
    #ex) sos 마커 위치가 0이면 data[2:13]

    if sos_data != sos_marker_behind:
        # SOS 마커 뒤의 데이터가 변조된 경우, 원래 데이터로 교체
        repair_data = (data[:sos_marker_position + len(sos_marker)] +
                         sos_marker_behind +
                         data[sos_marker_position + len(sos_marker) + len(sos_marker_behind):])
        return False, repair_data

    return True, None


def process_file(file_path, recover_directory):
    filename = os.path.basename(file_path)
    falsify_types = []
    recovery_path = "없음"

    detected_type, footer_match = detect_file_type(file_path)

    if detected_type:
        extension_match = check_file_extension(file_path, detected_type)
        if not extension_match:
            falsify_types.append("파일 확장자 불일치")
        
        if not footer_match:
            falsify_types.append("푸터 시그니처 변조")
        
        hidden_data_path = hidden_data_detect(file_path, detected_type, recover_directory)
        if hidden_data_path:
            falsify_types.append("숨겨진 데이터 탐지")
            recovery_path = hidden_data_path
        
        if detected_type == "JPEG":
            sos_correct, repair_data = check_sos_marker(file_path)
            if not sos_correct:
                falsify_types.append("SOS 마커 변조")
                index = len(os.listdir(recover_directory)) + 1
                repaired_file_path = os.path.join(recover_directory, f"복구파일_{index}.jpg")
                with open(repaired_file_path, "wb") as file:
                    file.write(repair_data)
                recovery_path = repaired_file_path
    else:
        falsify_types.append("변조 가능성 또는 알 수 없는 파일 형식")

    falsify_type = ", ".join(falsify_types) if falsify_types else "정상"

    formatted_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{filename}, {falsify_type}, {recovery_path}, {formatted_timestamp}")

def main():
    # 검사할 디렉토리 경로
    directory = "C:\\Users\\pcm32\\Desktop\\WHS project program\\test"
    recover_directory = "C:\\Users\\pcm32\\Desktop\\WHS project program\\test\\ANTIFRAGILE 복구폴더"

    # 디렉토리 내의 모든 파일에 대해 처리
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            process_file(file_path, recover_directory)

if __name__ == "__main__":
    main()
