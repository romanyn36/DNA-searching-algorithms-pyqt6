import sys
import sqlite3
import numpy as np
import pandas as pd
import PyQt6 as qt
from PyQt6.QtCore import Qt 
from PyQt6.uic import loadUi
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication,QDialog,QWidget,QMessageBox,QFileDialog,QLabel
from PyQt6.QtWidgets import  QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
 

from output import Ui_dna_seaching
from BoyerMoore import  boyer_moore_algo
from kmp import KMPSearch
from naive import naive
from suffixAarrays import suffixAarrays
from kmer import find_valid_pairs,compute_suffix_array
from approximate import edit_distance_dp


class UiDnaSeaching(QWidget):
    def __init__(self,) -> None:
        super().__init__()
        print("ui created")
       

        self.ui=Ui_dna_seaching()
        self.ui.setupUi(self)

         # create database object


        # set actions to buttons
        self.ui.btn_browse.clicked.connect(self.browse_file)
        self.ui.btn_apply.clicked.connect(self.apply_algorithm)
        # Set background image


        # Set layout to central widget
        # set background_
        background_label = QLabel(self)
        pixmap = QPixmap("Isolated-DNA-Strand.jpg")  # Replace with the path to your image
        background_label.setPixmap(pixmap)
        # background_label.setGeometry(0, 0, self.width(), self.height())
        background_label.lower()
      

   

        self.show()
    
    def browse_file(self):
        options = QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Select DNA Sequence File", "", "Text Files (*.txt *.fasta);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'r') as file:
                dna_sequence = file.read()
                self.ui.ed_text.setText(dna_sequence)
        pass

    def apply_algorithm(self):
        # Implement your DNA algorithm logic here
        t = self.ui.ed_text.text()
        p=self.ui.ed_pattern.text()
        option = self.ui.cbox_algorithm.currentIndex()
        name=self.ui.cbox_algorithm.currentText()
        print("algorithm : ",option," ",name)
        # Replace the following line with your actual algorithm logic
        if option==0:
            result, alignments = naive(p,t)
            if len(result) >0:
                modified_sequence = f"Pattern found"
                self.ui.lbl_align.setText(str(alignments))
                self.ui.lbl_idx.setText(str(result))
                # self.ui.lbl_skip.setText(str(skips))
            else:
                modified_sequence = f"Pattern not found"

        elif option==1:
      
            result, alignments, skips=boyer_moore_algo(p,t) 
            if len(result) >0:
                modified_sequence = f"Pattern found"
                self.ui.lbl_align.setText(str(alignments))
                self.ui.lbl_idx.setText(str(result))
                self.ui.lbl_skip.setText(str(skips))
            else:
                modified_sequence = f"Pattern not found"
            

        elif option==2:
            result=suffixAarrays(t)
            result = '\n'.join([', '.join(map(str, sublist)) for sublist in result])
            modified_sequence = f"{result}"
            self.ui.lbl_align.setText('')
            self.ui.lbl_idx.setText('')
            self.ui.lbl_skip.setText('')

        elif option==3:
            suffix_arr = compute_suffix_array(t)
            result =find_valid_pairs(suffix_arr, 2)
            result =[', '.join(map(str, sublist)) for sublist in result]
            modified_sequence = f"{result}"
            self.ui.lbl_align.setText('')
            self.ui.lbl_idx.setText('')
            self.ui.lbl_skip.setText('')


        elif option==4:
            result, alignments, skips=KMPSearch(p,t)
            if len(result) >0:
                modified_sequence = f"Pattern found"
                self.ui.lbl_align.setText(str(alignments))
                self.ui.lbl_idx.setText(str(result))
                self.ui.lbl_skip.setText(str(skips))
            else:
                modified_sequence = f"Pattern not found"

        elif option==5:
            result=edit_distance_dp(p, t)
            modified_sequence = f"the distance {result}"
        elif option==6:
            if len(t) >0:
                modified_sequence = f"{t[::-1]}"
            else:
                modified_sequence = f"input a valid sequance!!"
        elif option==7:
            if len(t) >0:
                modified_sequence = f"{self.dna_to_protein(t)}"
            else:
                modified_sequence = f"input a valid sequance!!"


        self.ui.lbl_outputt.setText(modified_sequence)
    
    def dna_to_protein(self,dna_sequence):
        # Define the genetic code mapping codons to amino acids
        genetic_code = {
            'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
            'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
            'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
            'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
            'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
            'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
            'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
            'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
            'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
            'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
            'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
            'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
            'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
            'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
            'TAC': 'Y', 'TAT': 'Y', 'TAA': '*', 'TAG': '*',
            'TGC': 'C', 'TGT': 'C', 'TGA': '*', 'TGG': 'W',
        }

        protein_sequence = ''
        for i in range(0, len(dna_sequence), 3):
            codon = dna_sequence[i:i + 3]
            if codon in genetic_code:
                protein_sequence += genetic_code[codon]
            else:
                # If an unknown codon is encountered, you can handle it accordingly
                protein_sequence += 'X'

        return protein_sequence



    def closeEvent(self, event):# works like destructor
        print("ui deleted")
        #if auto destractor not work , use this
        # self.db.colseConnection()
        event.accept()
 

if __name__=='__main__':
    app=QApplication(sys.argv)

    carsSystem=UiDnaSeaching()
    
    sys.exit(app.exec())

