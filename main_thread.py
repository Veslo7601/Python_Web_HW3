import os
import logging
import shutil
from pathlib import Path
from threading import Thread, active_count
from time import time, sleep


class ScanFolder():
    def __init__(self, default_folder):
        self.default_folder = default_folder
        self.cash = {
            "images_cash" : [],
            "video_cash" : [],
            "documents_cash" : [],
            "audio_cash" : [],
            "archives_cash" : [],
            "others_cash" : [],
        }

    def start_scan(self, target_folder):
        """function scan folder"""
        for elem in target_folder.iterdir():
            if elem.is_dir() and elem.name not in ["archives", "video", "audio", "documents", "images", "others"]:
                self.start_scan(elem)
            else:
                if elem.is_file():
                    suffix = self.suffix_file(elem)
                    self.sort_file(elem, suffix)
             
    def suffix_file(self, elem):
        """Function find Suffix"""
        elem_suffix = elem.suffix[1:].upper()
        return elem_suffix
    
    def sort_file(self, file, sufiix):
        """Function sotr file"""
        if sufiix in ('JPEG', 'PNG', 'JPG', 'SVG'): 
            self.cash["images_cash"].append(file)
        elif sufiix in ('AVI', 'MP4', 'MOV', 'MKV'):
            self.cash["video_cash"].append(file)
        elif sufiix in ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'):
            self.cash["documents_cash"].append(file)
        elif sufiix in ('MP3', 'OGG', 'WAV', 'AMR'):
            self.cash["audio_cash"].append(file)
        elif sufiix in ('ZIP', 'GZ', 'TAR'):
            self.cash["archives_cash"].append(file)
        else:
            self.cash["others_cash"].append(file)

    def work_to_cash(self, cash, folder):
        """Function move file"""
        for file in cash:
            self.move_file(file, folder)

    def move_file(self, file, folder):
        """Function move file"""
        path_to_new_folder = self.create_default_folder(self.default_folder,folder)
        path_to_old_elem = Path(file)
        shutil.move(path_to_old_elem, path_to_new_folder)

    def create_default_folder(self, path_to_folder, name_folder):
        """Function create new folder"""
        new_dir = path_to_folder/name_folder
        new_dir.mkdir(exist_ok=True)
        return new_dir

    def delete_folder(self,target_folder):
        """Function delete folder"""
        for elem in target_folder.iterdir():
            if elem.is_dir() and elem.name not in ["archives", "video", "audio", "documents", "images", "others"]:
                self.delete_folder(elem)
                try:
                    elem.rmdir()
                except:
                    "Error delet folder"


def main():
    timer = time()
    target_folders = Path("Temp")
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    scan = ScanFolder(target_folders)

    tr = Thread(target=scan.start_scan, args=(target_folders, ))
    tr.start()

    for key, value in scan.cash.items():
        tred = Thread(target=scan.work_to_cash, args=(value, key))
        tred.start()

    scan.delete_folder(target_folders)
    print(f"Thred: {active_count()}")

    logging.debug(f'Done {time() - timer}')

if __name__== "__main__":
    main()