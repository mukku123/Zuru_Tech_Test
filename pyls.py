import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Union

class File:
    def __init__(self, name: str, size: int, time_modified: int, permissions: str):
        self.name = name
        self.size = size
        self.time_modified = time_modified
        self.permissions = permissions

    def __repr__(self):
        return f"{self.permissions} {self.size} {datetime.utcfromtimestamp(self.time_modified).strftime('%b %d %H:%M')} {self.name}"

class Directory:
    def __init__(self, name: str, size: int, time_modified: int, permissions: str, contents: List[Union['File', 'Directory']]):
        self.name = name
        self.size = size
        self.time_modified = time_modified
        self.permissions = permissions
        self.contents = contents

    def __repr__(self):
        return self.name

def parse_json(json_data: Dict) -> List[Union[File, Directory]]:
    contents = json_data.get('contents', [])
    result = []
    for item in contents:
        if 'contents' in item:
            subdir = Directory(item['name'], item['size'], item['time_modified'], item['permissions'], parse_json(item))
            result.append(subdir)
        else:
            file = File(item['name'], item['size'], item['time_modified'], item['permissions'])
            result.append(file)
    return result

def filter_contents(contents: List[Union[File, Directory]], show_hidden: bool) -> List[Union[File, Directory]]:
    if show_hidden:
        return contents
    else:
        return [item for item in contents if not item.name.startswith('.')]

def sort_contents(contents: List[Union[File, Directory]], by_time: bool, reverse: bool) -> List[Union[File, Directory]]:
    if by_time:
        return sorted(contents, key=lambda item: item.time_modified, reverse=reverse)
    else:
        return sorted(contents, key=lambda item: item.name, reverse=reverse)

def human_readable_size(size: int) -> str:
    suffixes = ['B', 'KB', 'MB', 'GB']
    suffix_index = 0
    while size > 1024 and suffix_index < len(suffixes) - 1:
        size /= 1024
        suffix_index += 1
    return f"{size:.1f}{suffixes[suffix_index]}"

def print_contents(contents: List[Union[File, Directory]], long_format: bool, human_readable: bool, path: str, is_path_exist: bool):
    if '/' in path:
        f_name = path.split('/')[-1]
    else:
        f_name = path
    for item in contents:
        if path:
            if item.name in path:
                is_path_exist = True
                if item.name == f_name:
                    if isinstance(item, File):
                        print_contents([item], long_format, human_readable, '', is_path_exist)
                    else:
                        print_contents(item.contents, long_format, human_readable, '', is_path_exist)
                else:
                    if isinstance(item, File):
                        print_contents([item], long_format, human_readable, f_name, is_path_exist)
                    else:
                        print_contents(item.contents, long_format, human_readable, f_name, is_path_exist)
        else:
            if isinstance(item, File):
                if long_format:
                    if human_readable:
                        size = human_readable_size(item.size)
                    else:
                        size = str(item.size)
                    print(f"{item.permissions} {size} {datetime.utcfromtimestamp(item.time_modified).strftime('%b %d %H:%M')} {item.name}")
                else:
                    print(item.name, end=' ')
            else:
                if long_format:
                    size = str(item.size)
                    print(f"{item.permissions} {size} {datetime.utcfromtimestamp(item.time_modified).strftime('%b %d %H:%M')} {item.name}")
                else:
                    print(item.name, end=' ')
    return is_path_exist

def main():
    parser = argparse.ArgumentParser(description="List files and directories in JSON format similar to ls")
    parser.add_argument("path", nargs='?', default='', help="Path to the JSON file or directory (default: current directory)")
    parser.add_argument("-A", "--all", action="store_true", help="Do not ignore entries starting with .")
    parser.add_argument("-l", "--long", action="store_true", help="Use a long listing format")
    parser.add_argument("-r", "--reverse", action="store_true", help="Reverse order while sorting")
    parser.add_argument("-t", "--sort-by-time", action="store_true", help="Sort by modification time, newest first")
    parser.add_argument("-H", "--human-readable", action="store_true", help="With -l, print sizes in human readable format (e.g., 1K, 234M)")
    parser.add_argument("--filter", choices=['file', 'dir'], help="Filter by type (file or dir)")
    args = parser.parse_args()
    
    path = 'structure.json'
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"error: cannot access '{path}': No such file or directory")
        sys.exit(1)
    
    contents = parse_json(data)
    contents = filter_contents(contents, args.all)
    contents = sort_contents(contents, args.sort_by_time, args.reverse)

    if args.filter:
        if args.filter == 'file':
            contents = [item for item in contents if isinstance(item, File)]
        elif args.filter == 'dir':
            contents = [item for item in contents if isinstance(item, Directory)]
    
    is_path_exist = print_contents(contents, args.long, args.human_readable, args.path, False)
    if not is_path_exist and args.path:
        print(f"error: cannot access '{args.path}': No such file or directory")
    return True

if __name__ == "__main__":
    main()
