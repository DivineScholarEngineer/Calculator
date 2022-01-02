import os
import tkinter as tk
from tkinter.filedialog import askopenfile as aof
from tkinter.filedialog import asksaveasfile as asf
# import win32com.client
from PIL import Image, ImageTk # as it
import PyPDF2

background_color = '#0099FF' # hef value for the color light blue
text_font_style = ("Raleway", 16)

class PDFtoText:
    def __init__(self):
        # calculator details / body
        self.window = tk.Tk()
        TK = self.window
        TK.resizable(0,0)      # calculator app size can't be changed
        TK.title('PDF To Document') # PDF converter title

        TK.canvas = tk.Canvas(TK, width=600,height=300)
        # it splits the canvas to 3 invisible identical, to place elements in columns
        TK.canvas.grid(columnspan=3,rowspan=3)

        #Add Image Logo
        TK.logo = Image.open('pdfLogo.png')
        TK.logo = ImageTk.PhotoImage(self.window.logo)
        TK.logo_label = tk.Label(image=self.window.logo)
        TK.logo_label.image = self.window.logo
        TK.logo_label.grid(column=1,row=0)

        # labels - instructions
        TK.instructions = tk.Label(self.window, text='Select a PDF File to Text', font=text_font_style)
        TK.instructions.grid(columnspan=3,column=0, row=1)

        # browse button
        TK.browseText = tk.StringVar()
        TK.browsebtn = tk.Button(TK, textvariable=TK.browseText,font=text_font_style,
                                 bg=background_color, fg='white', height=2,width=15,command=lambda:self.openFile(TK))
        TK.browseText.set('Browse')
        TK.browsebtn.grid(column=1, row=2)

        # change size when buttons is pressed
        TK.canvas = tk.Canvas(TK, width=600, height=250)
        # it splits the canvas to 3 invisible identical, to place elements in columns
        TK.canvas.grid(columnspan=3)

        # exit button
        self.exit_button = tk.Button(self.window, text='Exit', width=6, command=self.exit_click).grid(row=7, column=0,

                                                                                                sticky=tk.W)

    def openFile(self, TK):
        TK.browseText.set('loading...')

        TK.file = aof(parent=self.window,mode='rb',title='Choose a file',filetype=[('PDF file', '*.pdf')])
        dir = self.getDir(TK)

        # dir_wt_fileexten = self.getdir_wt_fileexten(dir)
        # print(dir_wt_fileexten)
        # PDF_name = self.getPDF_name_wiithout_exten(dir)
        # folder_name = self.dir_without_file(dir)

        # page_content = self.pdf_to_text(dir_wt_fileexten, folder_name, PDF_name)
        page_content = self.pdf_to_text(dir)

        self.put_text_box(TK, page_content)

        self.save_files(page_content)
        # self.save_files(PDF_name_w_extension)

        TK.browseText.set('Browse')

    def getdir_wt_fileexten(self, dir):
        dir_st_exten = dir.split('.')
        dir_extension = f'.{dir_st_exten[-1]}'
        dir_wt_exten = dir.replace(dir_extension, '')
        return dir_wt_exten

    def getPDF_name_wiithout_exten(self, dir):
        PDF_name = self.getPDF_name(dir)
        PDF_name_w_extension = PDF_name[:-4]
        return PDF_name_w_extension

    # def pdf_to_text(self, dir, folder_dir, PDF_name):
    #     word = win32com.client.Dispatch("Word.Application")
    #     word.visible = 1
    #     # os.chdir(self.dir_without_file(dir))
    #     pdfdoc = f'{dir}.pdf'
    #     todocx = f'{folder_dir}{PDF_name}.docx'
    #     # todocx = f'NewDoc.docx'
    #     wb1 = word.Documents.Open(pdfdoc)
    #     wb1.SaveAs(todocx, FileFormat=16)  # file format for docx
    #     wb1.Close()
    #     word.Quit()
    #     return todocx

    def dir_without_file(self, dir):
        dir_split = dir.split('/')
        dir_wt_file = dir.replace(dir_split[-1], '')
        # dir_wt_slash = dir_wt_file.replace(dir_wt_file[-1], '')
        return str(dir_wt_file)

    def pdf_to_text(self, dir):
        pdfFileObject = open(dir, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
        print(" No. Of Pages :", pdfReader.numPages)

        pageObject = pdfReader.getPage(0)
        PDF_text = pageObject.extractText()
        pdfFileObject.close()

        return PDF_text

    def save_files(self, textContent):
        # file = asf(defaultextension=".docx")
        files = [('Microsoft Files', '*.docx'),
                          ('Text Document', '*.txt')]
        file = asf(filetypes=files, defaultextension=files)
        file_text = file.write(textContent)
        return file_text

    def put_text_box(self, TK, page_content):
        # Text Box
        TK.textBox = tk.Text(TK, height=10, width=50, padx=15, pady=15)
        TK.textBox.insert(1.0, page_content)

        # make the text to the center
        TK.textBox.tag_config('center', justify='center')
        TK.textBox.tag_add('center', 1.0, 'end')

        # put on grid
        TK.textBox.grid(column=1, row=3)

    def exit_click(self):
        self.window.destroy()
        exit()

    def getPDF_name(self, dir):
        dirlist = dir.split('/')
        PDF_name = dirlist[-1]
        return PDF_name

    def getDir(self, TK):
        TK.file_dir = str(TK.file)
        TK.file_dir = TK.file_dir[26:]
        TK.file_dir = TK.file_dir[:-2]
        return TK.file_dir

    def run(self):
        self.window.mainloop()