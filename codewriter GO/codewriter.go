package main

import (
	"fmt"
	"os"
)

// Variável global para contar labels únicos
var staticLabelCount int

// Estrutura do CodeWriter
type CodeWriter struct {
	file *os.File
}

// Cria um novo CodeWriter
func NewCodeWriter(filename string) (*CodeWriter, error) {
	file, err := os.Create(filename)
	if err != nil {
		return nil, err
	}
	return &CodeWriter{file: file}, nil
}

// Escreve um comando aritmético
func (cw *CodeWriter) WriteArithmetic(command string) {
	assembly := fmt.Sprintf("// %s\n", command)

	switch command {
	case "add":
		assembly += "@SP\nAM=M-1\nD=M\nA=A-1\nM=M+D\n"
	case "sub":
		assembly += "@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n"
	case "neg":
		assembly += "@SP\nA=M-1\nM=-M\n"
	case "eq":
		assembly += generateComparison("JEQ")
	case "gt":
		assembly += generateComparison("JGT")
	case "lt":
		assembly += generateComparison("JLT")
	case "and":
		assembly += "@SP\nAM=M-1\nD=M\nA=A-1\nM=M&D\n"
	case "or":
		assembly += "@SP\nAM=M-1\nD=M\nA=A-1\nM=M|D\n"
	case "not":
		assembly += "@SP\nA=M-1\nM=!M\n"
	}

	cw.file.WriteString(assembly)
}

// Escreve um comando de Push
func (cw *CodeWriter) WritePush(segment string, index int) {
	assembly := fmt.Sprintf("// push %s %d\n", segment, index)
	switch segment {
	case "constant":
		assembly += fmt.Sprintf("@%d\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n", index)
	}
	cw.file.WriteString(assembly)
}

// Escreve um comando de Pop
func (cw *CodeWriter) WritePop(segment string, index int) {
	assembly := fmt.Sprintf("// pop %s %d\n", segment, index)
	cw.file.WriteString(assembly)
}

// Fecha o arquivo
func (cw *CodeWriter) Close() {
	cw.file.Close()
}

// Função auxiliar para gerar código de comparação
func generateComparison(jumpType string) string {
	staticLabelCount++ // Incrementa para criar labels únicos
	labelTrue := fmt.Sprintf("TRUE_%d", staticLabelCount)
	labelEnd := fmt.Sprintf("END_%d", staticLabelCount)

	return fmt.Sprintf(`@SP
AM=M-1
D=M
A=A-1
D=M-D
@%s
D;%s
@SP
A=M-1
M=0
@%s
0;JMP
(%s)
@SP
A=M-1
M=-1
(%s)
`, labelTrue, jumpType, labelEnd, labelTrue, labelEnd)
}
