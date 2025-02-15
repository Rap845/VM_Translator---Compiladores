class CodeWriter:
    def __init__(self, filename):
        """Abre o arquivo de saída e inicializa o CodeWriter."""
        self.file = open(filename, "w")
        self.label_count = 0

    def writeArithmetic(self, command):
        """Escreve código assembly para comandos aritméticos."""
        if command in {"add", "sub", "and", "or"}:
            op = {"add": "+", "sub": "-", "and": "&", "or": "|"}[command]
            asm_code = "@SP\nAM=M-1\nD=M\nA=A-1\nM=M" + op + "D\n"
        elif command in {"neg", "not"}:
            op = {"neg": "-", "not": "!"}[command]
            asm_code = "@SP\nA=M-1\nM=" + op + "M\n"
        elif command in {"eq", "gt", "lt"}:
            jump = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}[command]
            label_true = f"TRUE_{self.label_count}"
            label_end = f"END_{self.label_count}"
            asm_code = (
                "@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n"
                f"@{label_true}\nD;{jump}\n"
                "@SP\nA=M-1\nM=0\n"
                f"@{label_end}\n0;JMP\n"
                f"({label_true})\n@SP\nA=M-1\nM=-1\n"
                f"({label_end})\n"
            )
            self.label_count += 1
        else:
            raise ValueError(f"Comando aritmético inválido: {command}")

        self.file.write(asm_code)

    def writePush(self, segment, index):
        """Escreve código assembly para comando push."""
        segment_map = {
            "constant": f"@{index}\nD=A\n",
            "local": f"@LCL\nD=M\n@{index}\nA=D+A\nD=M\n",
            "argument": f"@ARG\nD=M\n@{index}\nA=D+A\nD=M\n",
            "this": f"@THIS\nD=M\n@{index}\nA=D+A\nD=M\n",
            "that": f"@THAT\nD=M\n@{index}\nA=D+A\nD=M\n",
            "temp": f"@{5 + index}\nD=M\n",
            "pointer": f"@{'THIS' if index == 0 else 'THAT'}\nD=M\n",
            "static": f"@Static.{index}\nD=M\n"
        }

        if segment not in segment_map:
            raise ValueError(f"Segmento inválido: {segment}")

        asm_code = segment_map[segment] + "@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        self.file.write(asm_code)

    def writePop(self, segment, index):
        """Escreve código assembly para comando pop."""
        if segment == "constant":
            raise ValueError("Pop não pode ser usado com constant.")

        segment_map = {
            "local": "@LCL",
            "argument": "@ARG",
            "this": "@THIS",
            "that": "@THAT",
            "temp": f"@{5 + index}",
            "pointer": "@THIS" if index == 0 else "@THAT",
            "static": f"@Static.{index}"
        }

        if segment not in segment_map:
            raise ValueError(f"Segmento inválido: {segment}")

        if segment in {"temp", "pointer", "static"}:
            asm_code = "@SP\nAM=M-1\nD=M\n" + segment_map[segment] + "\nM=D\n"
        else:
            asm_code = (
                f"@{index}\nD=A\n"
                + segment_map[segment]
                + "\nD=M+D\n@R13\nM=D\n"
                "@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n"
            )

        self.file.write(asm_code)

    def close(self):
        """Fecha o arquivo de saída."""
        self.file.close()