import re

# 운영체제가 생성하는 파일 확장자 제외 리스트
excluded_extensions = [".exe", ".dll", ".sys", ".drv", ".bat", ".cmd", ".ini", ".cfg", ".inf", 
                       ".log", ".msi", ".ocx", ".scr"]

def print_file_info(filename, reason):
    if reason == 0x00002000:
        print(f"파일 명 : {filename}, 삭제 유형 : 일반삭제")
    elif reason == 0x80000200:
        print(f"파일 명 : {filename}, 삭제 유형 : 완전삭제")

with open(r'D:\usn_test.txt', 'r', encoding='utf-8') as file:
    while True:
        line = file.readline()
        if not line:
            break

        match = re.search(r"File name\s+:\s+(.+)", line)
        if match:
            filename = match.group(1).strip()
            if not any(filename.endswith(ext) for ext in excluded_extensions):
                while True:
                    reason_line = file.readline()
                    if not reason_line:
                        break
                    reason_match = re.search(r"Reason\s+:\s+0x([0-9A-Fa-f]+)", reason_line)
                    if reason_match:
                        reason = int(reason_match.group(1), 16)
                        if reason in (0x00002000, 0x80000200):
                            print_file_info(filename, reason)
                        break
