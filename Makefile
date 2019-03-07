# Makefile for building and compressing things for the workshop

SERPENT_EXE=./sss2
SERPENT_OPTS=-omp 4

SERPENT_INPUTS=simple dep det hist sens
SERPENT_RESULTS:=coe.coe
SERPENT_RESULTS:=$(addsuffix _res.m,$(SERPENT_INPUTS))

serpent : $(SERPENT_RESULTS)

files.zip : serpent
	zip $@ $(SERPENT_RESULTS) depmtx_fuelpfpr10.m

files.tgz : serpent
	tar czvf $@ $(SERPENT_RESULTS) depmtx_fuelpfpr10.m

files.sha256: files.zip files.tgz
	sha256sum $^ > $@

files.md5: files.zip files.tgz
	md5sum $^ > $@

%_res.m : %
	$(SERPENT_EXE) $(SERPENT_OPTS) $< > $<.txt

%.coe : %
	$(SERPENT_EXE) $(SERPENT_OPTS) $< > $<.txt

clean:
	$(RM) *seed *out *txt *.dep *.wrk *.m *png
