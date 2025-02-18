package main

import (
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Uso: go run main.go arquivo.vm")
		return
	}

	inputFile := os.Args[1]
	outputFile := filepath.Base(inputFile[:len(inputFile)-3]) + ".asm"

	parser, err := NewParser(inputFile)
	if err != nil {
		fmt.Println("Erro ao abrir o arquivo:", err)
		return
	}

	codeWriter, err := NewCodeWriter(outputFile)
	if err != nil {
		fmt.Println("Erro ao criar arquivo de saída:", err)
		return
	}
	defer codeWriter.Close()

	for parser.HasMoreCommands() {
		parser.Advance()
		cmdType := parser.CommandType()

		switch cmdType {
		case Arithmetic:
			codeWriter.WriteArithmetic(parser.Arg1())
		case Push:
			codeWriter.WritePush(parser.Arg1(), parser.Arg2())
		case Pop:
			codeWriter.WritePop(parser.Arg1(), parser.Arg2())
		}
	}
}
