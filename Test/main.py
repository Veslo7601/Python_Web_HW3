import os
import logging
import shutil
from pathlib import Path
from threading import Thread, Condition
from time import time, sleep


class ScanFolder():
    def __init__(self, default_folder):
        self.default_folder = default_folder

    def start_scan(self, target_folder):
        for elem in target_folder.iterdir():
            if elem.is_dir() and elem.name not in ["archives", "video", "audio", "documents", "images", "others"]:
                logging.debug(f'find {elem}')
                self.start_scan(elem)
            else:
                if elem.is_file():
                    suffix = self.suffix_file(elem)
                    self.sort_file(elem, suffix)

    def suffix_file(self, elem):
        elem_suffix = elem.suffix[1:].upper()
        logging.debug(f'find faile {elem_suffix}')
        return elem_suffix

    def sort_file(self, file, sufiix):
        if sufiix in ('JPEG', 'PNG', 'JPG', 'SVG'):
            self.move_file(file, "images")

        elif sufiix in ('AVI', 'MP4', 'MOV', 'MKV'):
            self.move_file(file, "video")

        elif sufiix in ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'):
            self.move_file(file, "documents")

        elif sufiix in ('MP3', 'OGG', 'WAV', 'AMR'):
            self.move_file(file, "audio")

        elif sufiix in ('ZIP', 'GZ', 'TAR'):
            self.move_file(file, "archives")
        else:
            self.move_file(file, "others")

    def move_file(self, file, folder):
        path_to_new_folder = self.create_default_folder(self.default_folder,folder)
        path_to_old_elem = Path(file)
        if not os.path.exists(path_to_new_folder):
            shutil.move(path_to_old_elem, path_to_new_folder)
        else:
            os.remove(path_to_old_elem)

    def create_default_folder(self, path_to_folder, name_folder):
        new_dir = path_to_folder/name_folder
        new_dir.mkdir(exist_ok=True)
        return new_dir

    def delete_folder(self,target_folder):
        for elem in target_folder.iterdir():
            if elem.is_dir() and elem.name not in ["archives", "video", "audio", "documents", "images", "others"]:
                self.delete_folder(elem)
                try:
                    elem.rmdir()
                except:
                    "Error delet folder"
        logging.debug("Folder delete")

if __name__== "__main__":
    timer = time()
    target_folders = Path("Temp copy 4")
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')

    scan = ScanFolder(target_folders)

    tr = Thread(target=scan.start_scan(target_folders))
    tr.start()

    scan.delete_folder(target_folders)
    logging.debug(f'Done {time() - timer}')
    print("End sort")