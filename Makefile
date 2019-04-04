# Makefile for building and compressing things for the workshop

SERPENT_EXE=./sss2
SERPENT_OPTS=-omp 4

SERPENT_RESULTS=coe.coe simple_res.m dep_dep.m det_det0.m hist_his0.m sens_sens0.m
ARCHIVE=dep_res.m depmtx_fuelpfpr10.m ${SERPENT_RESULTS}

# LaTeX
# Maybe need to change this to pdflatex
LATEX_BUILDER=pdflatex

slides: ans19-serpentTools.pdf

serpent : $(SERPENT_RESULTS)

archive : files.sha256 files.md5

files.zip : serpent
	zip $@ $(ARCHIVE)

files.tgz : serpent
	tar czvf $@ $(ARCHIVE)

files.sha256: files.zip files.tgz
	sha256sum $^ > $@

files.md5: files.zip files.tgz
	md5sum $^ > $@

%_res.m : %
	$(SERPENT_EXE) $(SERPENT_OPTS) $< > $<.txt

%.coe : %
	$(SERPENT_EXE) $(SERPENT_OPTS) $< > $<.txt

%_dep.m : %
	$(SERPENT_EXE) $(SERPENT_OPTS) $< > $<.txt

%_det0.m : %
	$(SERPENT_EXE) $(SERPENT_OPTS) $< > $<.txt

%_sens0.m : %
	$(SERPENT_EXE) $(SERPENT_OPTS) $< > $<.txt

%_his0.m : %
	$(SERPENT_EXE) $(SERPENT_OPTS) $< > $<.txt

clean:
	$(RM) *aux *log *blg *toc *snm *nav *seed *out *txt *.dep *.wrk *.m *png files.sha256 files.md5 *pdf

%.pdf : %.tex
	$(LATEX_BUILDER) $<
