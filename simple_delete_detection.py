import struct
import os
import datetime

# Constants for File Attributes
SYSTEM_FILE_ATTRIBUTES = [
    0x00000001,
    0x00000002,  # 숨김
    0x00000004,  # 시스템
    0x00000006,  # 숨김 + 시스템
    0x00000010,  # 디렉토리
    0x00000014,  # 디렉토리 + 시스템
    0x00000016,  # 숨김 + 시스템 + 디렉토리
    0x00000024,  # 시스템 + 아카이브
    0x00000030,  # Hidden | Archive
    0x00000026,  # 숨김 + 시스템 + 아카이브 
    0x00000100,
    0x00002000
]

# Constants for Reason Flags
REASON_FLAG_DELETE = 0x00002000
REASON_FLAG_DELETE_FULL = 0x80000200
REASON_FLAG_STANDARD_DELETE = 0x00001000  # 추가된 일반삭제 플래그

def convert_windows_timestamp(timestamp):
    """Convert Windows FILETIME timestamp to human-readable format."""
    return datetime.datetime.utcfromtimestamp((timestamp - 116444736000000000) / 10000000)

def read_usn_record(data, offset):
    try:
        size_of_record = struct.unpack_from('<I', data, offset)[0]
        if size_of_record <= 0 or size_of_record + offset > len(data):
            # Invalid record size
            return None
        major_version = struct.unpack_from('<H', data, offset + 4)[0]
        minor_version = struct.unpack_from('<H', data, offset + 6)[0]
        file_reference_number = struct.unpack_from('<Q', data, offset + 8)[0]
        parent_file_reference_number = struct.unpack_from('<Q', data, offset + 16)[0]
        usn = struct.unpack_from('<Q', data, offset + 24)[0]
        timestamp = struct.unpack_from('<Q', data, offset + 32)[0]
        reason_flag = struct.unpack_from('<I', data, offset + 40)[0]
        source_info = struct.unpack_from('<I', data, offset + 44)[0]
        security_id = struct.unpack_from('<I', data, offset + 48)[0]
        file_attributes = struct.unpack_from('<I', data, offset + 52)[0]
        size_of_filename = struct.unpack_from('<H', data, offset + 56)[0]
        offset_to_filename = struct.unpack_from('<H', data, offset + 58)[0]
        filename = data[offset + 60:offset + 60 + size_of_filename].decode('utf-16')
    except Exception as e:
        print(f"Error reading USN record at offset {offset}: {e}")
        return None

    return {
        'size_of_record': size_of_record,
        'major_version': major_version,
        'minor_version': minor_version,
        'file_reference_number': file_reference_number,
        'parent_file_reference_number': parent_file_reference_number,
        'usn': usn,
        'timestamp': timestamp,
        'reason_flag': reason_flag,
        'source_info': source_info,
        'security_id': security_id,
        'file_attributes': file_attributes,
        'filename': filename
    }

def parse_usn_journal(data):
    results = []
    filtered_results = []
    file_deletion_info = {}
    seen_filenames = set()
    offset = 0
    record_count = 0

    while offset < len(data):
        record = read_usn_record(data, offset)
        if record is None:
            offset += 4  # 유효하지 않은 레코드 크기 표시를 건너뛰고 계속
            continue
        offset += record['size_of_record']
        record_count += 1

        # 시스템 파일인지 확인하는 조건
        is_system_file = any(record['file_attributes'] & attr == attr for attr in SYSTEM_FILE_ATTRIBUTES)
        is_system_file |= record['filename'].startswith('C:\\Windows') or record['filename'].startswith('C:\\Program Files')
        
        if is_system_file:
            filtered_results.append(f"Filtered out system file or directory: {record['filename']}, attributes: {record['file_attributes']}")
            continue

        # 다양한 이유 플래그를 확인하여 삭제된 파일로 간주
        deletion_type = None
        if record['reason_flag'] & (REASON_FLAG_DELETE | REASON_FLAG_STANDARD_DELETE):
            deletion_type = "일반삭제"
        elif record['reason_flag'] & REASON_FLAG_DELETE_FULL:
            deletion_type = "완전삭제"

        if deletion_type:
            timestamp = convert_windows_timestamp(record['timestamp'])
            if record['filename'] not in seen_filenames:
                seen_filenames.add(record['filename'])
                results.append(f"{record['filename']}, {deletion_type}, {timestamp}")

    return results, filtered_results

def read_usn_journal_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No such file: '{file_path}'")
    
    with open(file_path, 'rb') as file:
        data = file.read()
    
    return data

if __name__ == "__main__":
    file_path = r"C:\Users\hj021\Desktop\$J.copy5"

    journal_data = read_usn_journal_file(file_path)
    if journal_data:
        results, filtered_results = parse_usn_journal(journal_data)
        print("\n")
        for result in results:
            print(result)
