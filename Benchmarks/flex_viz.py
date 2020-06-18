import os
import re
import webbrowser


def fileSrch(path='./'):
    """
    Returns list of files to examine.

    Parameter
    ----------
    path : str, optional, default './'
        Path to search for files.
    """
    file_list = {}

    for root, dirs, files in os.walk(path):
        match_list = [
            i for i in files if re.search(r"[\w]+\.html|[\w]+\.pstats", i)
        ]

        if match_list:
            file_list[root] = match_list

    return file_list


def fileView(path, f_name):
    cmd = f"cd {path}"
    os.system(cmd)

    if re.search(r"[\w]+\.pstats", f_name):
        cmd = f"gprof2dot -f pstats {os.path.join(path, f_name)} | dot -Tpng -o output.png && eog output.png"
        os.system(cmd)

        cmd = f"snakeviz {os.path.join(path, f_name)}"
        os.system(cmd)

    elif re.search(r"[\w]+\.html", f_name):
        webbrowser.open(os.path.join(path, f_name), new=2)


if __name__ == "__main__":
    path = input(
        "Enter the path you wish to search files for: (default enter ./) \n")

    file_list = fileSrch(path)

    print("""The files that can be examined are:

    1 - .pstats file(cProfile)
                    -> Snakeviz Visualization
                    -> gprof2dot chart

    2 - .html file(pyInstrument)
                    -> Statistical Profiler Visualization
    \n""")
    for k, v in file_list.items():
        print(f"{k} -> ")
        for i in v:
            print(i)

    while 1:
        f_name = input("\nEnter the file name you wish to examine:")

        for root, file in file_list.items():
            if f_name in file:
                f_path = root

        try:
            fileView(f_path, f_name)
        except NameError:
            print("Enter a valid file name")

        if input("Do you wish to analyze another file: (Y/N)") == 'N':
            break
