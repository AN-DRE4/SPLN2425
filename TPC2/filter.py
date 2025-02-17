#!/usr/bin/env python3

import os
from jjcli import * 
'''
Repetidas - Remove linhas repetidas num programa. 
Usage - 
    repetidas options file*
Options: 
    - s  fix me keep spaces 
    - e remove empty lines 

'''

def remove_linhas_repetidas(cl): 
    output_dir = os.path.expanduser("~/home/user/.local/bin")
    # output_dir = os.path.join(os.path.dirname(__file__), "output") # for testing purposes
    os.makedirs(output_dir, exist_ok=True)

    if not cl.args:
        # Handle stdin
        linhas_vistas = set()
        output_text = ""
        lines = cl.input()
        for i, linha in enumerate(lines):
            if linha == "\n":
                if "-e" in cl.opt:
                    output_text += "\n"
                elif "-p" in cl.opt:
                    output_text += "#" + "\n"
                else:
                    output_text += ""
            else:
                if "-s" not in cl.opt:
                    ln = linha.strip()
                    if i < len(lines) - 1:  # Except the last line
                        ln += "\n"
                else:
                    ln = linha
                if ln not in linhas_vistas:
                    output_text += ln
                    linhas_vistas.add(ln)
        
        output_path = os.path.join(output_dir, "filtered_stdin.txt")
        with open(output_path, "w") as f:
            f.write(output_text)
    else:
        # Handle files
        for input_file in cl.args:
            linhas_vistas = set()
            output_text = ""
            
            # Create output filename based on input filename
            base_name = os.path.basename(input_file)
            output_path = os.path.join(output_dir, f"filtered_{base_name}")
            
            with open(input_file, 'r') as f:
                lines = f.readlines()
                for i, linha in enumerate(lines):
                    if linha == "\n":
                        if "-e" in cl.opt:
                            output_text += "\n"
                        elif "-p" in cl.opt:
                            output_text += "#" + "\n"
                        else:
                            output_text += ""
                    else:
                        if "-s" not in cl.opt:
                            ln = linha.strip()
                            if i < len(lines) - 1:  # Except the last line
                                ln += "\n"
                        else:
                            ln = linha
                        if ln not in linhas_vistas:
                            output_text += ln
                            linhas_vistas.add(ln)
            with open(output_path, "w") as f:
                f.write(output_text)

def main (): 
    cl = clfilter(opt="s,e,p", man=__doc__)
    remove_linhas_repetidas(cl)

if __name__ == '__main__': 
    main()
