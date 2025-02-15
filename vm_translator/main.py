import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python VMTranslator.py arquivo.vm")
        sys.exit(1)
    translator = VMTranslator(sys.argv[1])
    translator.translate()
    print("Tradução concluída! Arquivo .asm gerado.")