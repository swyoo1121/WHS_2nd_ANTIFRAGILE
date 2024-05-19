#틀 잡은 코드
import os

#MFT entry Header 가져옴
def detect_delete_type(file_path):
    with open(file_path, "rb") as file:
        file.seek(22)
        flag = file.read(2)

        # Flag 값과 0x0001을 AND 연산하여 결과가 0이면 파일이 삭제된 상태
        if int.from_bytes(flag, byteorder='little') & 0x0001 == 0:
            return "완전 삭제"
        else:
            return "일반 삭제"

def main():
    #directory = "C:\\Users\\hj021\\Desktop\\test"
    directory = "C:\\"

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            delete_type = detect_delete_type(file_path)
            print(f"{filename}: {delete_type}")

main()
