import wx
import pyewf
import pytsk3
import os

class FileOpenScreen(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Antifragile", size=(800, 600))
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.file_picker = wx.FilePickerCtrl(panel, message="Select image file", wildcard="Image files (*.E01;*.dd)|*.E01;*.dd")
        self.file_picker.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_file_selected)
        vbox.Add(self.file_picker, 0, wx.EXPAND | wx.ALL, 5)

        self.tree = wx.TreeCtrl(panel)
        vbox.Add(self.tree, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(vbox)

    def on_file_selected(self, event):
        file_path = self.file_picker.GetPath()
        if file_path:
            if file_path.lower().endswith('.e01'):
                self.load_e01_file(file_path)
            elif file_path.lower().endswith('.dd'):
                self.load_dd_file(file_path)
            else:
                wx.MessageBox(f"Unsupported file format: {file_path}", "Error", wx.OK | wx.ICON_ERROR)

    def load_e01_file(self, file_path):
        try:
            filenames = pyewf.glob(file_path)
            ewf_handle = pyewf.handle()
            ewf_handle.open(filenames)

            tsk_img = EwfImgInfo(ewf_handle)
            self.load_image(tsk_img, file_path)
        except Exception as e:
            wx.MessageBox(f"Error loading file: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def load_dd_file(self, file_path):
        try:
            tsk_img = pytsk3.Img_Info(file_path)
            self.load_image(tsk_img, file_path)
        except Exception as e:
            wx.MessageBox(f"Error loading file: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def load_image(self, tsk_img, file_path):
        try:
            partition_table = pytsk3.Volume_Info(tsk_img)

            self.tree.DeleteAllItems()
            root = self.tree.AddRoot(os.path.basename(file_path))

            for part in partition_table:
                partition_item = self.tree.AppendItem(root, f"Partition {part.addr} ({part.desc.decode()})")

                try:
                    fs_info = pytsk3.FS_Info(tsk_img, offset=part.start * partition_table.info.block_size)
                    self.load_directory(fs_info.open_dir(path="/"), partition_item)
                except Exception as e:
                    self.tree.AppendItem(partition_item, f"Error loading filesystem: {e}")

            self.tree.Expand(root)
        except IOError:
            try:
                fs_info = pytsk3.FS_Info(tsk_img)
                self.tree.DeleteAllItems()
                root = self.tree.AddRoot(os.path.basename(file_path))
                self.load_directory(fs_info.open_dir(path="/"), root)
                self.tree.Expand(root)
            except Exception as e:
                wx.MessageBox(f"Error loading file system: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def load_directory(self, directory, parent_item):
        for entry in directory:
            if entry.info.name.name in [b".", b".."]:
                continue

            name = entry.info.name.name.decode("utf-8")
            item = self.tree.AppendItem(parent_item, name)

            if entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                try:
                    subdir = entry.as_directory()
                    self.load_directory(subdir, item)
                except Exception as e:
                    self.tree.AppendItem(item, f"Error loading directory: {e}")

class EwfImgInfo(pytsk3.Img_Info):
    def __init__(self, ewf_handle):
        self._ewf_handle = ewf_handle
        super(EwfImgInfo, self).__init__(url="",
                                         type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

    def close(self):
        self._ewf_handle.close()

    def read(self, offset, size):
        self._ewf_handle.seek(offset)
        return self._ewf_handle.read(size)

    def get_size(self):
        return self._ewf_handle.get_media_size()
