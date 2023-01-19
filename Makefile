# usage: make filename.pdf
%.pdf: %.tex
	pdflatex $<
	pdflatex $<
