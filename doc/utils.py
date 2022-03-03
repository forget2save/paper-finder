import re
from typing import Tuple

# class MDpaper:
#     def __init__(self, raw) -> None:
#         self.raw = raw


def is_title(line: str):
    return line[0] == "-"


def has_link(line: str) -> Tuple[bool, str, str]:
    k1 = line.find("[")
    k2 = line.find("]", k1)
    k3 = line.find("(", k2)
    k4 = line.find(")", k3)
    if k1 == -1 or k2 == -1 or k3 == -1 or k4 == -1:
        return False, line[2:].strip(), ""
    else:
        return True, line[k1 + 1:k2], line[k3 + 1:k4]


def make_link(title):
    title = filter_invalid_char(title)
    return f"- [{title}](./{title}.pdf)"


def filter_invalid_char(filename: str):
    return re.sub('[\\\/:*?"<>|]', "", filename)


def sort_md(file_path: str):
    lines = []
    with open(file_path, "r", encoding="utf-8") as f:
        tmp = f.readlines()
        buf = ""
        for line in tmp:
            if not is_title(line):
                buf += line
            else:
                if len(buf) > 5:
                    lines.append(buf)
                flag, title, _ = has_link(line)
                if not flag:
                    buf = make_link(title)
                else:
                    buf = line
        if len(buf) > 5:
            lines.append(buf)
    lines.sort()
    print(len(lines))
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)


if __name__ == "__main__":
    md_file = r"G:\AD-papers\summary.md"
    sort_md(md_file)
