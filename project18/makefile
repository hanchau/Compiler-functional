all:
	mkdir bin comp_files
	cp src/symtab.py bin/
	cp src/parser.py bin/
	cp src/lexer.py bin/
	cp src/tac.py bin/
	cp src/irgen bin/
	cp src/CodeGen.py bin/codegen
	cp src/GlobalVariables.py bin/GlobalVariables.py
	cp src/RegAllocatFunc.py bin/RegAllocatFunc.py
	cp src/TransInstr.py bin/TransInstr.py
	cp src/OCaml.sh bin/ocaml
	chmod 777 bin/*
	chmod +x bin/*
clean:
	rm -r bin/ comp_files/
	rm parser.out assem
	rm parsetab.py
