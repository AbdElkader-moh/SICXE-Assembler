# ⚙️ Modified SIC/XE Assembler Project

A complete assembler simulator for a modified SIC/XE architecture, developed as part of the Systems Programming course at the Arab Academy for Science, Technology & Maritime Transport.

This assembler handles both Pass 1 and Pass 2 of the compilation process, generates HTME records, manages memory blocks, supports literals, and introduces a custom **Format 4F** for conditional execution.

---

## 📚 Overview

The project simulates the workflow of a two-pass assembler targeting a customized SIC/XE instruction set. The assembler processes `.txt` input files with assembly-like syntax and outputs:

- Symbol table
- Intermediate code
- Final object code in HTME format (Header, Text, Modification, End)
- Error reports

---

## 🧠 Key Features

- 🔁 **Two-Pass Assembler**:
  - **Pass 1**: Computes memory locations and generates the symbol table.
  - **Pass 2**: Generates object code and HTME records.

- 🧩 **Support for 4 Memory Blocks**:
  - `DEFAULT` (formats 1 & 2)
  - `DEFAULTB` (formats 3, 4, and 4F)
  - `CDATA` (compact data storage)
  - `CBLKS` (larger reserved blocks)

- 🧮 **Format 4F – Conditional Execution**:
  - Adds condition flags (Z, N, C, V)
  - Eliminates need for traditional jump instructions

- 🔍 **Error Handling**:
  - Unrecognized symbols
  - Invalid block names

- 🧾 **Literals Management**:
  - Detects and allocates memory for literals during assembly

---

## 📄 Input & Output

### 🔽 Input:
- `in.txt`: Assembly code using modified SIC/XE format

### 🔼 Outputs:
- `intermediate.txt`: Cleaned assembly for Pass 2
- `symbTable.txt`: Generated symbol table
- `out_pass1.txt`: Location counter for each instruction
- `out_pass2.txt`: Object code line by line
- `HTME.txt`: Final machine-ready code in HTME format

---

## 🛠️ How to Run

If you're on Windows, just double-click the run_all.bat file or run it via the command prompt:

run_all.bat

if you're already in the folder via terminal:

cd path\to\your\project
run_all.bat
