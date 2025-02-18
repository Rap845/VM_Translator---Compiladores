package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

// Tipos de comandos possíveis
type CommandType int

const (
	Arithmetic CommandType = iota
	Push
	Pop
	Label
	Goto
	If
	Function
	Return
	Call
)

// Parser estrutura
type Parser struct {
	lines  []string
	index  int
	tokens []string
}

// Novo Parser
func NewParser(filename string) (*Parser, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := strings.Split(scanner.Text(), "//")[0] // Remove comentários
		line = strings.TrimSpace(line)                 // Remove espaços extras
		if line != "" {
			lines = append(lines, line)
		}
	}

	return &Parser{lines: lines, index: -1}, scanner.Err()
}

// Verifica se há mais comandos
func (p *Parser) HasMoreCommands() bool {
	return p.index < len(p.lines)-1
}

// Avança para o próximo comando
func (p *Parser) Advance() {
	if p.HasMoreCommands() {
		p.index++
		p.tokens = strings.Fields(p.lines[p.index])
	}
}

// Retorna o tipo do comando atual
func (p *Parser) CommandType() CommandType {
	switch p.tokens[0] {
	case "push":
		return Push
	case "pop":
		return Pop
	case "label":
		return Label
	case "goto":
		return Goto
	case "if-goto":
		return If
	case "function":
		return Function
	case "return":
		return Return
	case "call":
		return Call
	default:
		return Arithmetic
	}
}

// Retorna o primeiro argumento do comando
func (p *Parser) Arg1() string {
	if p.CommandType() == Arithmetic {
		return p.tokens[0]
	}
	return p.tokens[1]
}

// Retorna o segundo argumento (apenas para Push, Pop, Function, Call)
func (p *Parser) Arg2() int {
	if cmdType := p.CommandType(); cmdType == Push || cmdType == Pop || cmdType == Function || cmdType == Call {
		var index int
		fmt.Sscanf(p.tokens[2], "%d", &index)
		return index
	}
	return -1
}
