import os

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

# 추가$$ 뒤에 숨겨진 파일이나 데이터 탐지
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

    # print(f"{len(footer_signature)}") 테스트

    if hidden_data == "":
        print(f"{file_path}: 숨겨진 데이터 X") # 이거 출력 안되는 것 수정필요###############
        return

    # 숨겨진 데이터가 있는 경우
    file_out = None

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
    print(f"{file_path}: 숨겨진 파일 복구 완료 -> {file_out}")


def main():
    # 검사할 디렉토리 경로
    directory = "C:\\Users\\pcm32\\Desktop\\WHS project program\\test"
    recover_directory = "C:\\Users\\pcm32\\Desktop\\WHS project program\\test\\ANTIFRAGILE 복구폴더"

    # 디렉토리 내의 모든 파일 검사
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            detected_type, footer_match = detect_file_type(file_path)
            if detected_type:
                if footer_match:
                    print(f"{file_name}: 원본 파일 확장자는 {detected_type} 입니다. 파일 푸터 시그니처도 같습니다.")
                else:
                    hidden_data_detect(file_path, detected_type, recover_directory)
            else:
                print(f"{file_name}: 변조 가능성 or Unknown file type")
            
main()
