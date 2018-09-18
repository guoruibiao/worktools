#!/usr/bin python
#coding:utf8
import sys

#copy the text from other commands
def pbcopy():
    lines = []
    for line in sys.stdin:
        lines.append(line)
    with open("/tmp/clip.txt", "w") as file:
        file.writelines(lines)
        file.close()


# paste the text to other commands
def pbpaste():
    lines = []
    with open("/tmp/clip.txt", "r") as file:
        lines = file.readlines()
        file.close()
    # remove the last useless line
    print(str("".join(lines)).strip("  ").strip("\n"))

if __name__ == "__main__":
    action = sys.argv[1]
    if action == "copy":
        pbcopy()
    else:
        pbpaste()
