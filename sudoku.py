from PIL import Image, ImageFilter
import pytesseract
# from wand.image import Image


pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


class sudoku:
    def __init__(self, text=None,file=None,picture=None):
        self.board = [[(i+j)%9+1 for i in range(9)] for j in range(9)]
        if file:
            with open(file,'r') as f:
                text = f.read()
        if text:
            for i,line in enumerate(text.split('\n')):
                self.board[i] = [(int(i) if i != '#' else 0) for i in line.split(' ')]
        if picture:
            im = Image.open(picture)
            # im.crop((36,34,140,68)).show()
            # print(pytesseract.image_to_string(im.crop((36,34,72,68)),config='--psm 6'))
            # print(pytesseract.image_to_string(im,config='--psm 6'))
            # pytesseract.image_to_string
            # im.crop((3.5+31.2,3.5+2*31.2,34.7))
            for j in range(9):
                for i in range(9):
                    cut = im.crop((3.5+31.2*i,3.5+j*31.2,33.4+31.2*i,3+(j+1)*31.2) )
                    # cut.sharpen(radius=8,sigma=4)
                    cut = cut.convert('RGB')
                    # cut = cut.filter(ImageFilter.SMOOTH)
                    # cut = cut.filter(ImageFilter.DETAIL)
                    cut = cut.filter(ImageFilter.SMOOTH_MORE)
                    # cut = cut.filter(ImageFilter.SMOOTH)
                    cut = cut.filter(ImageFilter.SHARPEN)
                    # cut = cut.convert('palette')
                    # cut = cut.filter(ImageFilter.SMOOTH_MORE)
                    # if picture== './test/image3.png':
                    
                    # cut = cut.filter(ImageFilter.SMOOTH)

                    # cut = cut.filter(ImageFilter.BLUR)
                    x = pytesseract.image_to_string(cut,config='--psm 6')
                    if x in ['1','2','3','4','5','6','7','8','9']:
                        print(x,end=" ")
                        self.board[j][i] = int(x)
                    else:
                        self.board[j][i] = 0
                        print(" ",end=" ")
                print()


        
    def printBoard(self):
        print("SUDOKU")
        for j,lines in enumerate(self.board):
            for i,num in enumerate(lines):
                print(num,end=" ")
                if i % 3 == 2 and i != 8:
                    print('|',end="") 
            print()
            if j % 3 == 2 and j != 8:
                print('--------------------')

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


if __name__ == '__main__':
    a = sudoku(picture='./test/image1.png')
    # a.printBoard()
    if a.solve():
        a.printBoard()
    else:
        print("unsolvable")