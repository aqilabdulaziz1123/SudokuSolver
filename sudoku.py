from PIL import Image, ImageFilter, ImageOps
import pytesseract
import numpy as np
from sys import argv
# from wand.image import Image


pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


class sudoku:
    def __init__(self, text=None,filename=None,picture=None):
        self.board = [[0 for i in range(9)] for j in range(9)]
        if filename:
            with open(filename,'r') as f:
                text = f.read()
        if text:
            for i,line in enumerate(text.split('\n')):
                self.board[i] = [(int(i) if i != '#' else 0) for i in line.split(' ')]
        if picture:
            im = Image.open(picture)
            for j in range(9):
                for i in range(9):
                    cut = im.crop((3.5+31.2*i,3.5+j*31.2,33.4+31.2*i,3+(j+1)*31.2))
                    np_img = np.array(cut)
                    if (np_img.mean() > 20):
                        cut = cut.convert('RGB')
                        cut = cut.filter(ImageFilter.SMOOTH_MORE)
                        x = pytesseract.image_to_string(cut,config='--psm 6')
                        if len(x) > 1:
                            for k in x:
                                if k in ['1','2','3','4','5','6','7','8','9']:
                                    x = k
                                    break
                        x = x.replace('S','5')
                        print(x,end=" ")
                        self.board[j][i] = int(x)
                    else:
                        print(' ',end=' ')
                        self.board[j][i] = 0
                print()
        if picture:
            name = picture.split('\n')[-1]
        if filename:
            name = filename.split('\n')[-1]
        self.writeFile(name)
        


        
    def printBoard(self):
        # print("SUDOKU")
        for j,lines in enumerate(self.board):
            for i,num in enumerate(lines):
                print(num,end=" ")
                if i % 3 == 2 and i != 8:
                    print('|',end="") 
            print()
            if j % 3 == 2 and j != 8:
                print('--------------------')
    
    def writeFile(self,filename):
        name = filename.split('/')
        f = open("./result/"+name[-1]+".jawaban",'w')
        print("SUDOKU",file=f)
        for j,lines in enumerate(self.board):
            for i,num in enumerate(lines):
                print(num,end=" ",file=f)
                if i % 3 == 2 and i != 8:
                    print('|',end="",file=f) 
            print("",file=f)
            if j % 3 == 2 and j != 8:
                print('--------------------',file=f)
        print("Lokasi para 5 : ",end="",file=f)
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 5:
                    print(f"({i},{j})",end=" ",file=f)
        f.close()

    def isi(self,row,col,x):
        self.board[row][col] = x
    
    def findEmpty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i,j
        return 0

    def validPlacing(self,num,row,col):
        for i in range(9):
            if self.board[row][i] == num and col != i:
                return False
            if self.board[i][col] == num and row != i:
                return False

        boxx = col // 3
        boxy = row // 3

        for i in range(boxy*3, boxy*3 + 3):
            for j in range(boxx * 3, boxx*3 + 3):
                if self.board[i][j] == num and i != row and j != col:
                    return False

        return True
    
    #backtrack
    def solve(self):
        find = self.findEmpty()
        if not find:
            return True
        else:
            row, col = find

        for i in range(9):
            if self.validPlacing(i+1, row, col):
                self.board[row][col] = i+1

                if self.solve():
                    return True

                self.board[row][col] = 0

        return False
    
    def print5(self):
        print("Lokasi para 5 : ",end="")
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 5:
                    print(f"({i},{j})",end=" ")


if __name__ == '__main__':
    if len(argv) < 2:
        print("USAGE : py sudoku.py [NAMAFILESUDOKU]")
    else:
        if 'png' in argv[1] or 'jpg' in argv[1]:
            a = sudoku(picture=argv[1])
        else:
            a = sudoku(filename=argv[1])
        print("Awal : ")
        a.printBoard()
        if a.solve():
            print("Jawaban : ")
            a.printBoard()
            a.print5()
            a.writeFile(argv[1])
        else:
            print('Unsolvably unbelievable')

    # a = sudoku(picture='./test/image1.png')
    # if a.solve():
    #     a.printBoard()
    # else:
        # print("unsolvable")
    # a = sudoku(picture='./test/image2.png')
    # if a.solve():
    #     a.printBoard()
    # else:
    #     print("unsolvable")
    # a = sudoku(picture='./test/image3.png')
    # if a.solve():
    #     a.printBoard()
    # else:
    #     print("unsolvable")
    # a = sudoku(picture='./test/image4.png')
    # # a.printBoard()
    # if a.solve():
    #     a.printBoard()
    # else:
    #     print("unsolvable")