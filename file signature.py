# 일단 파일명 변조만 되어있을 경우 탐지하는 부분 작성해봄.
# 추후 악의적으로 파일 시그니처가 에디터로 변경되었을 경우 탐지하는 부분 개발 예정(현재 서칭중,,)

import os

# 파일 시그니처 데이터베이스
file_signatures = {
    "JPEG": b"\xFF\xD8\xFF",
    "PNG": b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A",
    "PDF": b"%PDF",
    # b -> 아스키 문자열을 바이트로 표현
    # 다른 파일 형식의 시그니처들 일단 노가다로 추가예정
}

def detect_file_type(file_path):
    with open(file_path, "rb") as file:
        # 파일의 헤더부분 바이트 읽어오기
        header = file.read(16)

        # 파일 시그니처 데이터베이스와 비교
        detected_type = None
        for file_type, signature in file_signatures.items():
            if header.startswith(signature):
                detected_type = file_type
                break

        return detected_type

def main():
    # 검사할 디렉토리
    directory = "C:\\Users\\pcm32\\Desktop\\WHS project program"

    # 디렉토리 내의 모든 파일 검사
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            detected_type = detect_file_type(file_path)
            if detected_type:
                print(f"{filename}: 원본 파일 확장자는 {detected_type} 입니다.")
            else:
                print(f"{filename}: 변조 가능성 or Unknown file type")

    main()
