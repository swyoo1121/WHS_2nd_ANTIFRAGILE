import os

def detect_deleted_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'rb') as f:
                    # MFT 엔트리 헤더 읽기 (처음 24바이트)
                    mft_header = f.read(24)
                    
                    # MFT 플래그와 0x0001을 &&연산
                    flag = int.from_bytes(mft_header[22:24], byteorder='little')
                    if flag & 0x0001 == 0:
                        print(f"{file} 삭제 됨")
            except Exception as e:
                print(f"경로가 올바르지 않음 {file_path}: {str(e)}")

directory_path = r"C:\Users\hj021\Desktop\test"
#directory_path = "C:\\"
detect_deleted_files(directory_path)
