import pygsheets
import numpy as np

gc = pygsheets.authorize()

# # Open spreadsheet and then worksheet
# sh = gc.open('testSheet')
# wks = sh.sheet1
#
# # Update a cell with value (just to let him know values is updated ;) )
# wks.update_value('A1', "Hey yank this numpy array")
# my_nparray = np.random.randint(10, size=(3, 4))
#
# # update the sheet with array
# wks.update_values('A2', my_nparray.tolist())
#
# # share the sheet with your friend
# sh.share("morel.israel@mail.huji.ac.il")


def copyDoc():
    gc = pygsheets.authorize(outh_file='client_secret.json')
    sh = gc.open('testSheet')
    gc.create("")
    wks = sh.add_worksheet("Sheet2", src_worksheet=sh.worksheet_by_title("Sheet1"))

copyDoc()