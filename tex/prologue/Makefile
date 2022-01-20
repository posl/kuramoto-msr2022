FILE_NAME := prologue
TEMP_FILES := \
    $(FILE_NAME).aux \
    $(FILE_NAME).bbl \
    $(FILE_NAME).log \
    $(FILE_NAME).blg \
    $(FILE_NAME).brf \
    $(FILE_NAME).dvi \
    $(FILE_NAME).out \
	$(FILE_NAME).fls \
	$(FILE_NAME).fdb_latexmk \
	$(FILE_NAME).lol \
	$(FILE_NAME).toc \
	$(FILE_NAME).log
DEBUG=no
ifneq '$(DEBUG)' 'yes'
LATEX_FLAGS="-interaction=batchmode --file-line-error --synctex=1"
endif
LATEX_FLAG_ENC="-kanji=utf8"
OPEN ?= open
.DELETE_ON_ERROR:
################################################################################
# Main paper building
################################################################################
$(FILE_NAME).pdf:
	platex $(FILE_NAME)
	dvipdfmx $(FILE_NAME)
	rm -f $(TEMP_FILES) $(SUBDIR)/*.aux missfont.log
.PHONY: clean view
clean:
	rm -f $(TEMP_FILES) $(GEN_FIGURES) $(FILE_NAME).pdf $(SUBDIR)/*.aux missfont.log
view: $(FILE_NAME).pdf
	$(OPEN) $(FILE_NAME).pdf
