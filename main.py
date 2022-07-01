import os
import sys


class Node:
    def __init__(self, where, what):
        self.where = where
        self.what = what


class fswalker:
    def __init__(self, target_folder):
        self.__target_folder = target_folder
        self.__files = self.walk(self.__target_folder)

    def __str_to_list(self, text):
        text_list = []
        if type(text).__name__ == "str":
            text_list.append(text)
        else:
            text_list = text

        return text_list

    def walk(self, folder_path):
        result_files = []
        folders = [fldr for fldr in os.listdir(folder_path) if os.path.isdir(f"{folder_path}/{fldr}")]
        files = [file for file in os.listdir(folder_path) if not os.path.isdir(f"{folder_path}/{file}")]

        for file in files:
            result_files.append(f"{folder_path}/{file}")

        for folder in folders:
            result_files = result_files + self.walk(f"{folder_path}/{folder}")

        return result_files

    def search(self, search_texts, to_print=False):

        search_text = self.__str_to_list(search_texts)

        search_results = []

        for fpath in self.__files:
            with open(fpath, "r", encoding='utf-8') as file:
                content_lines = file.readlines()
                for stxt in search_text:
                    search_results += [Node(fpath + ":" + str(line.find(stxt)), line.strip()) for line in content_lines if line.find(stxt) > -1]
                file.close()

        if(to_print):
            self.__print(search_results)

        return search_results

    def replace(self, search_texts, replace_text, to_print = False):

        search_text = self.__str_to_list(search_texts)

        replace_results = list([])
        for stxt in search_text:
            replace_results += [Node(file.where, file.what.replace(stxt, replace_text)) for file in self.search(stxt)]

        for fpath in self.__files:
            with open(fpath, "r", encoding='utf-8') as file:
                content = file.read()
                for txt in search_text:
                    content = content.replace(txt, replace_text)
                file.close()

            with open(fpath, "w", encoding='utf-8') as file:
                file.write(content)
                file.close()

        if (to_print):
            self.__print(replace_results)

        return replace_results

    def __print(self, results):
        for result in results:
            print(f"{result.where}\t{result.what}")


if __name__ == '__main__':

    getargind = lambda arg: sys.argv.index(arg)
    getargval = lambda arg: sys.argv[getargind(arg) + 1]

    print(sys.argv)
    if "-h" in sys.argv:
        print("-r replace\n\t-o old strings\n\t-n new string\n-s search\n-f folder\n")
    elif "-s" in sys.argv and "-f" in sys.argv:
        fswalk = fswalker(getargval("-f"))
        fswalk.search(getargval("-s"), True)
    elif "-r" in sys.argv and "-o" in sys.argv and "-n" in sys.argv and "-f" in sys.argv:
        fswalk = fswalker(getargval("-f"))
        fswalk.replace(sys.argv[getargind("-o")+1:getargind("-n")], getargval("-n"), True)
    else:
        print("something wrong")
