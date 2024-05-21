import os

# 파일 헤더 시그니처 데이터베이스
file_header_signatures = {
    "JPEG": b"\xFF\xD8\xFF",
    "PNG": b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A",
    "PDF": b"%PDF",
    "ZIP": b"\x50\x4B\x03\x04",
    "GIF": b"\x47\x49\x46\x38",
    # b -> 아스키 문자열을 바이트로 표현
    # 다른 파일 형식의 시그니처들 일단 노가다로 추가예정
    # 출처 : https://en.wikipedia.org/wiki/List_of_file_signatures
}

#파일 푸터 시그니처 데이터베이스
file_footer_signatures = {
    "JPEG": b"\xFF\xD9",
    "PNG": b"\x49\x45\x4E\x44\xAE\x42\x60\x82",
    "GIF": b"\x00\x3B",
    "ZIP": b"\x50\x4B"
    # 헤더, 푸터 모두 있는 경우
}

def detect_file_type(file_path, file_name):
    with open(file_path, "rb") as file:
        # 파일의 헤더 부분 바이트 읽어오기
        header = file.read(16)

        # 파일의 푸터 부분 바이트 읽어오기
        file.seek(-16, 2)  # 파일 끝에서 16바이트 앞부분으로 이동
        footer = file.read(16)

        # 파일 헤더 시그니처와 비교하여 파일 형식 결정
        detected_type = None
        for file_type, signature in file_header_signatures.items():
            if header.startswith(signature):
                detected_type = file_type
                break

        # 파일 푸터 시그니처와 비교 (헤더 시그니처가 일치하는 경우에 한함)
        if detected_type == file_type:
            if detected_type in file_footer_signatures:
                footer_signature = file_footer_signatures[detected_type] # 
                if footer.endswith(footer_signature):
                    print(f"{file_name}: 파일 푸터 시그니처 일치함.")
                else:
                    print(f"{file_name}: 파일 푸터 시그니처 일치하지 않음")
                    detected_type = None

        return detected_type

def main():
    # 검사할 디렉토리 경로
    directory = "C:\\Users\\pcm32\\Desktop\\WHS project program\\test"

    # 디렉토리 내의 모든 파일 검사
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            detected_type = detect_file_type(file_path, file_name)
            if detected_type:
                print(f"{file_name}: 원본 파일 확장자는 {detected_type} 입니다.")
            else:
                print(f"{file_name}: 변조 가능성 or Unknown file type")

main()
