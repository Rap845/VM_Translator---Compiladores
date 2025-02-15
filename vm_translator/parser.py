class Parser:
    def __init__(self, filename):
        """Inicializa o parser e carrega os comandos do arquivo .vm."""
        with open(filename, "r") as file:
            self.commands = [
                line.split("//")[0].strip().split()  # Remove comentários e divide tokens
                for line in file.readlines()
                if line.strip() and not line.startswith("//")
            ]
        self.current_command = None

    def hasMoreCommands(self):
        """Retorna True se ainda há comandos a processar."""
        return bool(self.commands)

    def advance(self):
        """Lê o próximo comando e o define como corrente."""
        if self.hasMoreCommands():
            self.current_command = self.commands.pop(0)

    def commandType(self):
        """Retorna o tipo do comando."""
        if self.current_command[0] in {"add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"}:
            return "C_ARITHMETIC"
        elif self.current_command[0] == "push":
            return "C_PUSH"
        elif self.current_command[0] == "pop":
            return "C_POP"
        else:
            raise ValueError(f"Comando desconhecido: {self.current_command[0]}")

    def arg1(self):
        """Retorna o primeiro argumento do comando."""
        if self.commandType() == "C_ARITHMETIC":
            return self.current_command[0]
        return self.current_command[1]

    def arg2(self):
        """Retorna o segundo argumento (apenas para Push, Pop, Function, Call)."""
        if self.commandType() in {"C_PUSH", "C_POP"}:
            return int(self.current_command[2])
        raise ValueError(f"arg2 chamado para comando inválido: {self.current_command}")