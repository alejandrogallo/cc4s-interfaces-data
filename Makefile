figs_py = \
abinit/LiH_molecule/plot_lih_molecule.py \
abinit/LiH_bulk/extrap_nvirtuals.py \
abinit/LiH_bulk/extrap_volumes.py \
abinit/He/abinit_he_atom_inv.py \
abinit/He/abinit_he_atom.py \
exciting/solid.py \
exciting/he-vs-alpha.py \
exciting/he-vs-rmt.py \
vasp/He/vasp_he_atom.py \
mrcc/molgw_he_atom.py \
vasp/He/vasp_he_atom_alternative.py


FIGS = $(patsubst %.py,%.pdf,$(figs_py)) main.pdf

all: $(FIGS)

%.pdf: %.py
	@printf "\n\n\n-----> FIG: %s\n\n" $(notdir $<)
	cd $(dir $<) && python $(notdir $<)


LATEX_FORCE = -f -interaction=nonstopmode
LATEX = latexmk -synctex=1 -pdf -shell-escape
%.pdf: %.tex
	$(LATEX) $(LATEX_FORCE) -outdir=build/$* $<
	ln -sf build/$*/$*.pdf
