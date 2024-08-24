from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox, QWidget, QTreeWidget, QTreeWidgetItem, QPushButton, QLabel, QFileDialog
import pytsk3
import pyewf
from datetime import datetime
from simple_delete_detection import read_usn_journal_file, parse_usn_journal
from show_result_screen import show_result_screen
import subprocess
import sys

class file_open_screen(QWidget):
    def __init__(self):
        super().__init__()

        self.left_layout = QVBoxLayout()
        self.file_open_area = QTreeWidget()
        self.file_open_area.setHeaderLabels(["File Name", "Size", "Created", "Modified"])
        self.left_layout.addWidget(self.file_open_area)

        # Store results in memory
        self.journal_results = None
        self.journal_filtered_results = None
        self.falsify_results = None

        # $J 관련 버튼들 그룹 박스
        self.j_group_box = QGroupBox("$J Operations")
        self.j_group_box.setStyleSheet("QGroupBox { font-weight: bold; border: 1.4px solid gray; }")
        j_layout = QVBoxLayout()

        self.load_file_button = QPushButton("$J : Load File")
        self.load_file_button.clicked.connect(self.open_file_dialog)
        j_layout.addWidget(self.load_file_button)

        self.file_path_label = QLabel("No file selected")
        j_layout.addWidget(self.file_path_label)

        self.execute_button = QPushButton("$J : Execute")
        self.execute_button.clicked.connect(self.execute_analysis)
        j_layout.addWidget(self.execute_button)

        self.j_group_box.setLayout(j_layout)
        self.left_layout.addWidget(self.j_group_box)

        # Falsify 및 Recover 관련 버튼들 그룹 박스
        self.fr_group_box = QGroupBox("Falsify and Recover Operations")
        self.fr_group_box.setStyleSheet("QGroupBox { font-weight: bold; border: 1.4px solid gray; }")
        fr_layout = QVBoxLayout()

        self.load_file_button2 = QPushButton("Falsify : Load Folder")
        self.load_file_button2.clicked.connect(self.open_folder_dialog2)
        fr_layout.addWidget(self.load_file_button2)
        
        self.file_path_label2 = QLabel("No folder selected")
        fr_layout.addWidget(self.file_path_label2)

        self.load_file_button3 = QPushButton("Recover : Load Folder")
        self.load_file_button3.clicked.connect(self.open_folder_dialog3)
        fr_layout.addWidget(self.load_file_button3)

        self.file_path_label3 = QLabel("No folder selected")
        fr_layout.addWidget(self.file_path_label3)

        self.execute_button3 = QPushButton("Execute")
        self.execute_button3.clicked.connect(self.execute_analysis3)
        fr_layout.addWidget(self.execute_button3)

        self.fr_group_box.setLayout(fr_layout)
        self.left_layout.addWidget(self.fr_group_box)

        self.setLayout(self.left_layout)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open USN Journal File", "", "All Files (*)")
        if file_path:
            self.file_path_label.setText(file_path)

    def open_folder_dialog2(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open Falsify Folder", "")
        if folder_path:
            self.file_path_label2.setText(folder_path)

    def open_folder_dialog3(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open Recovery Folder", "")
        if folder_path:
            self.file_path_label3.setText(folder_path)

    def execute_analysis(self):
        file_path = self.file_path_label.text()
        if file_path and file_path != "No file selected":
            journal_data = read_usn_journal_file(file_path)
            if journal_data:
                self.journal_results, self.journal_filtered_results = parse_usn_journal(journal_data)
                self.show_results(self.journal_results, self.journal_filtered_results)

    def execute_analysis3(self):
        falsify_folder = self.file_path_label2.text()
        recover_folder = self.file_path_label3.text()
        if falsify_folder and falsify_folder != "No folder selected" and recover_folder and recover_folder != "No folder selected":
            try:
                result = subprocess.run([sys.executable, "detect_data_falsify.py", falsify_folder, recover_folder],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp949')
                if result.stdout:
                    self.falsify_results = result.stdout.splitlines()
                    self.show_falsify_results(self.falsify_results)
                else:
                    print("No output received from the command.")
                    self.falsify_results = []
            except subprocess.CalledProcessError as e:
                print(f"Error executing command: {e}")
                print(f"stderr: {e.stderr}")

    def show_results(self, results, filtered_results):
        self.result_screen_widget.clear_tables()
        for result in results:
            try:
                file_name, delete_type, timestamp = map(str.strip, result.split(","))
                self.result_screen_widget.add_single_delete_record(file_name, delete_type, timestamp)
            except ValueError:
                #print(f"Skipping invalid record: {result}")
                print("")

        for result in filtered_results:
            pass

    def show_falsify_results(self, results):
        self.result_screen_widget.clear_tables()
        for result in results:
            try:
                fields = result.split(",")
                file_name = fields[0].strip()
                falsify_type = ",".join(fields[1:-2]).strip()
                recovery_path = fields[-2].strip()
                formatted_timestamp = fields[-1].strip()
                self.result_screen_widget.add_signature_mod_record(file_name, falsify_type, recovery_path, formatted_timestamp)
            except ValueError:
                print(f"Skipping invalid record: {result}")

    def display_journal_results(self):
        if self.journal_results is not None:
            self.show_results(self.journal_results, self.journal_filtered_results)

    def display_falsify_results(self):
        if self.falsify_results is not None:
            self.show_falsify_results(self.falsify_results)

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
