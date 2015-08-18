#coding=utf-8
import sys

class Atext():
    def a(self):
        print("python is a")

    def b(self):
        print("b")

if __name__ == '__main__':
    for i in sys.argv:
        asd = Atext()
        if i =="--debug":
            asd.a()
        if i =="--b":
            asd.b()
        if i =="--help":
            print (u"命令参数：\n--debug\t调试模式\n--b\t执行模式\n--help\t帮助文档")

