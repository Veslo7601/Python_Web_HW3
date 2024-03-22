import sys
import shutil
import normalize
from pathlib import Path

# Створення початкових папок
def create_default_folder(path,name):
    new_dir = path/name
    new_dir.mkdir(exist_ok=True)


# Створення листів розширення    
    
Known_extensions = []
Unknown_extensions = []

# Перенесення та нормалізація знайдених файлів у archives, video, audio, documents, images, others

def scan_and_move_and_rename(target_folder,default_folder):
    dir_path = Path(target_folder)
    path = Path(default_folder)
    for elem in dir_path.iterdir():
        if elem.is_dir() and elem.name not in ["archives", "video", "audio", "documents", "images", "others"]:
            scan_and_move_and_rename(elem,default_folder)
        else:
            if elem.is_file():
                elem_suffix = elem.suffix[1:].upper() 
                if elem_suffix in ('JPEG', 'PNG', 'JPG', 'SVG'): 
                    print(elem)
                    new_name = normalize.normalize(elem.name)
                    name_folder = "images"
                    create_default_folder(path,name_folder)
                    new_path = path/name_folder
                    old_path = Path(elem)
                    shutil.move(old_path, new_path/new_name)
                    Known_extensions.append(elem_suffix)

                elif elem_suffix in ('AVI', 'MP4', 'MOV', 'MKV'):
                    print(elem)
                    new_name = normalize.normalize(elem.name)
                    name_folder = "video"
                    create_default_folder(path,name_folder)
                    new_path = path/name_folder
                    old_path = Path(elem)
                    shutil.move(old_path, new_path/new_name)
                    Known_extensions.append(elem_suffix)

                elif elem_suffix in ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'):
                    print(elem)
                    new_name = normalize.normalize(elem.name)
                    name_folder = "documents"
                    create_default_folder(path,name_folder)
                    new_path = path/name_folder
                    old_path = Path(elem)
                    shutil.move(old_path, new_path/new_name)
                    Known_extensions.append(elem_suffix)

                elif elem_suffix in ('MP3', 'OGG', 'WAV', 'AMR'):
                    print(elem)
                    new_name = normalize.normalize(elem.name)
                    name_folder = "audio"
                    create_default_folder(path,name_folder)
                    new_path = path/name_folder
                    old_path = Path(elem)
                    shutil.move(old_path, new_path/new_name)
                    Known_extensions.append(elem_suffix)

                elif elem_suffix in ('ZIP', 'GZ', 'TAR'):
                    try:
                        print(elem)
                        new_name = normalize.normalize(elem.name.replace(".zip","").replace(".gz","").replace(".tar",""))
                        name_folder = "archives"
                        create_default_folder(path,name_folder)
                        new_path = path/name_folder
                        old_path = Path(elem)
                        shutil.unpack_archive(old_path, new_path/new_name)
                        old_path.unlink()
                        Known_extensions.append(elem_suffix)
                    except:
                        print("Achive Error. DELETE")
                        old_path = Path(elem)
                        old_path.unlink()
                else:
                    print(elem)
                    new_name = normalize.normalize(elem.name)
                    name_folder = "others"
                    create_default_folder(path,name_folder)
                    new_path = path/name_folder
                    old_path = Path(elem)
                    shutil.move(old_path, new_path/new_name)
                    Unknown_extensions.append(elem_suffix)


# Видалення папок

def delete_folder(target_folder):
    dir_path = Path(target_folder)
    for elem in dir_path.iterdir():
        if elem.is_dir() and elem.name not in ["archives", "video", "audio", "documents", "images", "others"]:
            delete_folder(elem)
            try:
                elem.rmdir()
            except:
                "Error delet folder"

# Друк назв файлів у папці
                
def print_result(target_folder):
    dir_path = Path(target_folder)
    if dir_path.is_dir():
        print(f"Folder name - {dir_path.name}, name file:")
        for elem in dir_path.iterdir():
            print(elem.name)


if len(sys.argv) != 2:
    print("Not enough parameters")
    quit()
    
target_folder = sys.argv[1]
#target_folder = "Temp"


scan_and_move_and_rename(target_folder,target_folder)
delete_folder(target_folder)

for name in ["archives", "video", "audio", "documents", "images", "others"]:
    new = target_folder+"/"+name
    print_result(new)

print(f"Know extensiond: {Known_extensions}")
print(f"Unknow extensiond: {Unknown_extensions}")


            