class VMTranslator:
    """Gerencia a tradução do arquivo .vm para .asm."""
    def __init__(self, input_file):
        self.parser = Parser(input_file)
        output_file = input_file.replace(".vm", ".asm")
        self.code_writer = CodeWriter(output_file)

    def translate(self):
        """Realiza a tradução completa do arquivo .vm para .asm."""
        while self.parser.hasMoreCommands():
            self.parser.advance()
            command_type = self.parser.commandType()

            if command_type == "C_ARITHMETIC":
                self.code_writer.writeArithmetic(self.parser.arg1())
            elif command_type == "C_PUSH":
                self.code_writer.writePush(self.parser.arg1(), self.parser.arg2())
            elif command_type == "C_POP":
                self.code_writer.writePop(self.parser.arg1(), self.parser.arg2())

        self.code_writer.close()