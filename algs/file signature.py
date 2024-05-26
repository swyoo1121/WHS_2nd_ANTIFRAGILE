import os

# 파일 헤더 시그니처 데이터베이스
file_header_signatures = {
    "JPEG": b"\xFF\xD8\xFF",
    "PNG": b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A",
    "PDF": b"%PDF",
    "ZIP": b"\x50\x4B\x03\x04",
    "GIF": b"\x47\x49\x46\x38",
    # 다른 파일 형식 추가 가능
}

#파일 푸터 시그니처 데이터베이스
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
        for file_type, signature in file_header_signatures.items(): # ex)File_type = “png”, Signature=\x89\x50…
 
            if header.startswith(signature):
                detected_type = file_type
                break

        # 파일 푸터 시그니처와 비교 (헤더 시그니처가 일치하는 경우에 한함)
        footer_match = False
        if detected_type in file_footer_signatures: # 탐지된 파일유형이 푸터 딕셔너리에에 있는 지 확인
            footer_signature = file_footer_signatures[detected_type] 
            if footer.endswith(footer_signature):
                footer_match = True

        return detected_type, footer_match

def main():
    # 검사할 디렉토리 경로
    directory = "C:\\Users\\pcm32\\Desktop\\WHS project program\\test"

    # 디렉토리 내의 모든 파일 검사
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            detected_type, footer_match = detect_file_type(file_path)
            if detected_type:
                if footer_match:
                    print(f"{file_name}: 원본 파일 확장자는 {detected_type} 입니다. 파일 푸터 시그니처도 같습니다.")
                else:
                    print(f"{file_name}: 원본 파일 확장자는 {detected_type} 입니다. !!!파일 푸터 시그니처는 일치하지 않습니다!!!")
            else:
                print(f"{file_name}: 변조 가능성 or Unknown file type")

main()
