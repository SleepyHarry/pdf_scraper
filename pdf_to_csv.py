"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Harry Vane"
__author_github__ = "https://github.com/SleepyHarry"

import os
import sys
import glob
import re
import csv

import PyPDF2 as pdf

from tkinter import *

block_row_seat = re.compile((r"Section:([0-9]+)Row([A-Z]+)Seat([0-9]+)"
                             r"(.{19}).{19}$"))

def pdf_to_csv(in_filename, writer):
    reader = pdf.pdf.PdfFileReader(in_filename)

    pretty_filename = os.path.split(in_filename)[-1]

    for page_num in range(reader.getNumPages()):
        raw_text = reader.getPage(page_num).extractText()
        block, row, seat, barcode = block_row_seat.search(raw_text).groups()
        barcode = ''.join(barcode.split())

        writer.writerow((pretty_filename, block, row, seat, barcode))

def set_source_dir():
    chosen_dir = filedialog.Directory().show()
    in_dirname.set(chosen_dir)

def set_out_file():
    chosen_file = filedialog.SaveAs().show()
    out_filename.set(chosen_file)

def go():
    try:
        out_fileobj = open(out_filename.get(), 'a', newline='')
    except OSError:
        error_str.set("ERROR: Select a valid out_file")
        out_file_choose.focus()
        return
    
    writer = csv.writer(out_fileobj)

    in_dir = in_dirname.get()
    if not in_dir:
        error_str.set("ERROR: Select a valid in_directory")
        in_dir_choose.focus()
        return

    pdf_filenames = glob.glob(os.path.join(in_dirname.get(), "*.pdf"))
    num_pdfs = len(pdf_filenames)

    for filename in pdf_filenames:
        try:
            pdf_to_csv(filename, writer)
        except Exception as e:
            print(e, "({})".format(filename))

    error_str.set("Complete!")

    out_fileobj.close()

root = Tk()
root.title("Bespoke PDF scraper")

main_frame = Frame(root)
main_frame.grid(column=3, row=4)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)

in_dirname = StringVar()
in_dirname_box = Entry(main_frame, width=60, textvariable=in_dirname)
in_dirname_box.grid(column=0, row=0)
in_dir_choose = Button(main_frame, text="Choose source directory",
                       command=set_source_dir)
in_dir_choose.grid(column=1, row=0)

out_filename = StringVar()
out_filename_box = Entry(main_frame, width=60, textvariable=out_filename)
out_filename_box.grid(column=0, row=2)
out_file_choose = Button(main_frame, text="Choose destination CSV",
                         command=set_out_file)
out_file_choose.grid(column=1, row=2)

error_str = StringVar()
error_notice = Label(main_frame, textvariable=error_str)
error_notice.grid(column=0, row=3, sticky=E)

go_button = Button(main_frame, text="Scrape", command=go)
go_button.grid(column=1, row=3, sticky=E)

for child in main_frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
