#!/usr/bin/make -f

CP=cp
RM=rm -f
TARG=main
#TARG=main_latexdiff
#TARG=main_latexupdate

.PHONY: all clean

all:$(TARG).pdf

.SUFFIXES: .pdf .tex .aux .bbl

.tex.pdf:
	@\
	aux=$(<:%.tex=%.aux);\
	$(CP) $$aux $$aux-;\
	pdflatex $<;\
	echo ========;\
	diff -q $$aux $$aux- > /dev/null;\
	if [ $$? -eq 0 ]; then\
		echo No need for second compile.;\
	else\
		bibtex $$aux;\
		echo ========;\
		$(CP) $$aux $$aux-;\
		pdflatex $<;\
		echo ========;\
		diff -q $$aux $$aux- > /dev/null;\
		if [ $$? -eq 0 ]; then\
			echo No need for third compile.;\
		else\
			pdflatex $<;\
		fi;\
	fi;\
	$(RM) $$aux-
	$(RM) $(TARG).{aux,bbl,log,blg,cut,out,xcp,gz,xcp}

clean:
	$(RM) $(TARG).{pdf,aux,bbl,log,blg,cut,out,xcp,gz,xcp}
