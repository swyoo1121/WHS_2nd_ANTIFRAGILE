from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTreeWidget, QTreeWidgetItem
import pytsk3
import pyewf
from datetime import datetime

class file_open_screen(QWidget):
    def __init__(self):
        super().__init__()

        self.left_layout = QVBoxLayout()
        self.file_open_area = QTreeWidget()
        self.file_open_area.setHeaderLabels(["File Name", "Size", "Created", "Modified"])
        self.left_layout.addWidget(self.file_open_area)

        self.setLayout(self.left_layout)

    def load_file(self, file_path):
        try:
            if file_path.lower().endswith('.e01'):
                filenames = pyewf.glob(file_path)
                ewf_handle = pyewf.handle()
                ewf_handle.open(filenames)
                img_info = EWFImgInfo(ewf_handle)
            else:
                img_info = pytsk3.Img_Info(file_path)

            fs_info = pytsk3.FS_Info(img_info)
            
            self.file_open_area.clear()
            self.walk_filesystem(fs_info, self.file_open_area.invisibleRootItem(), '/')

        except Exception as e:
            self.file_open_area.clear()
            error_item = QTreeWidgetItem(["Error loading file", str(e)])
            self.file_open_area.addTopLevelItem(error_item)

    def walk_filesystem(self, fs_info, parent_item, path):
        try:
            directory = fs_info.open_dir(path)
        except:
            return

        for entry in directory:
            if entry.info.name.name in [b'.', b'..']:
                continue
            
            try:
                name = entry.info.name.name.decode('utf-8', errors='replace')
                
                # 숨김 파일 건너뛰기
                if name.startswith('.') or name.startswith('$'):
                    continue
                
                size = str(entry.info.meta.size if entry.info.meta else 'N/A')
                created_time = self.format_timestamp(entry.info.meta.crtime if entry.info.meta else None)
                modified_time = self.format_timestamp(entry.info.meta.mtime if entry.info.meta else None)
                
                item = QTreeWidgetItem(parent_item, [name, size, created_time, modified_time])
                
                if entry.info.meta and entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                    self.walk_filesystem(fs_info, item, f"{path}/{name}")
            except Exception as e:
                print(f"Error processing {name}: {str(e)}")

    def format_timestamp(self, timestamp):
        try:
            if timestamp is None or timestamp == 0:
                return 'N/A'
            return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return 'N/A'

class EWFImgInfo(pytsk3.Img_Info):
    def __init__(self, ewf_handle):
        self._ewf_handle = ewf_handle
        super().__init__(url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

    def close(self):
        self._ewf_handle.close()

    def read(self, offset, size):
        self._ewf_handle.seek(offset)
        return self._ewf_handle.read(size)

    def get_size(self):
        return self._ewf_handle.get_media_size()



# from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTreeWidget, QTreeWidgetItem
# import pytsk3
# import pyewf
# from datetime import datetime

# class file_open_screen(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.left_layout = QVBoxLayout()
#         self.file_open_area = QTreeWidget()
#         self.file_open_area.setHeaderLabels(["File Name", "Size", "Created", "Modified"])
#         self.left_layout.addWidget(self.file_open_area)

#         self.setLayout(self.left_layout)

#     def load_file(self, file_path):
#         try:
#             if file_path.lower().endswith('.e01'):
#                 filenames = pyewf.glob(file_path)
#                 ewf_handle = pyewf.handle()
#                 ewf_handle.open(filenames)
#                 img_info = EWFImgInfo(ewf_handle)
#             else:
#                 img_info = pytsk3.Img_Info(file_path)

#             fs_info = pytsk3.FS_Info(img_info)
            
#             self.file_open_area.clear()
#             self.walk_filesystem(fs_info, self.file_open_area.invisibleRootItem(), '/')

#         except Exception as e:
#             self.file_open_area.clear()
#             error_item = QTreeWidgetItem(["Error loading file", str(e)])
#             self.file_open_area.addTopLevelItem(error_item)

#     def walk_filesystem(self, fs_info, parent_item, path):
#         try:
#             directory = fs_info.open_dir(path)
#         except:
#             return

#         for entry in directory:
#             if entry.info.name.name in [b'.', b'..']:
#                 continue
            
#             try:
#                 name = entry.info.name.name.decode('utf-8', errors='replace')
                
#                 # 숨김 파일 건너뛰기
#                 if name.startswith('.') or name.startswith('$'):
#                     continue
                
#                 size = str(entry.info.meta.size if entry.info.meta else 'N/A')
#                 created_time = self.format_timestamp(entry.info.meta.crtime)
#                 modified_time = self.format_timestamp(entry.info.meta.mtime)
                
#                 item = QTreeWidgetItem(parent_item, [name, size, created_time, modified_time])
                
#                 if entry.info.meta and entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
#                     self.walk_filesystem(fs_info, item, f"{path}/{name}")
#             except Exception as e:
#                 print(f"Error processing {name}: {str(e)}")

#     def format_timestamp(self, timestamp):
#         try:
#             return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
#         except:
#             return 'N/A'

# class EWFImgInfo(pytsk3.Img_Info):
#     def __init__(self, ewf_handle):
#         self._ewf_handle = ewf_handle
#         super().__init__(url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

#     def close(self):
#         self._ewf_handle.close()

#     def read(self, offset, size):
#         self._ewf_handle.seek(offset)
#         return self._ewf_handle.read(size)

#     def get_size(self):
#         return self._ewf_handle.get_media_size()
