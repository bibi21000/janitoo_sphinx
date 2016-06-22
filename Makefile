# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = ../docs

# User-friendly check for sphinx-build
#~ ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
#~ $(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH. If you don't have Sphinx installed, grab it from http://sphinx-doc.org/)
#~ endif

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) source
# the i18n builder cannot share the environment and doctrees with the others
I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) source

ARCHBASE      = archive
BUILDPKGDIR   = /tmp/janitoo_sphinx_build
DISTDIR       = dists
NOSE          = $(shell which nosetests)
NOSEOPTS      = --verbosity=2
PYLINT        = $(shell which pylint)
PYLINTOPTS    = --max-line-length=140 --max-args=9 --extension-pkg-whitelist=zmq --ignored-classes=zmq --min-public-methods=0

ifndef PYTHON_EXEC
PYTHON_EXEC=python
endif

ifndef message
message="Auto-commit"
endif

ifdef VIRTUAL_ENV
python_version_full := $(wordlist 2,4,$(subst ., ,$(shell ${VIRTUAL_ENV}/bin/${PYTHON_EXEC} --version 2>&1)))
else
python_version_full := $(wordlist 2,4,$(subst ., ,$(shell ${PYTHON_EXEC} --version 2>&1)))
endif

janitoo_version := $(shell ${PYTHON_EXEC} _version.py 2>/dev/null)

python_version_major = $(word 1,${python_version_full})
python_version_minor = $(word 2,${python_version_full})
python_version_patch = $(word 3,${python_version_full})

PIP_EXEC=pip
ifeq (${python_version_major},3)
	PIP_EXEC=pip3
endif

MODULENAME   = $(shell basename `pwd`)
DOCKERNAME   = $(shell echo ${MODULENAME}|sed -e "s|janitoo_||g")
NOSEMODULES  = janitoo,janitoo_factory,janitoo_db
MOREMODULES  = janitoo_factory_ext

DEBIANDEPS := $(shell [ -f debian.deps ] && cat debian.deps)
BASHDEPS := $(shell [ -f bash.deps ] && echo "bash.deps")
JANITOODEPS := $(shell [ -f janitoo.deps ] && echo janitoo.deps)
BOWERDEPS := $(shell [ -f bower.deps ] && cat bower.deps)

TAGGED := $(shell git tag | grep -c v${janitoo_version} )

-include Makefile.local

NOSECOVER     = --cover-package=${MODULENAME} --with-coverage --cover-inclusive --cover-html --cover-html-dir=${BUILDDIR}/html/tools/coverage --with-html --html-file=${BUILDDIR}/html/tools/nosetests/index.html
NOSEDOCKER     = --cover-package=${NOSEMODULES},${MODULENAME},${MOREMODULES} --with-coverage --cover-inclusive --with-xunit --xunit-testsuite-name=${MODULENAME}

.PHONY: help clean html dirhtml singlehtml pickle json htmlhelp qthelp devhelp epub latex latexpdf text man changes linkcheck doctest gettext tests

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"
	@echo "  dirhtml    to make HTML files named index.html in directories"
	@echo "  singlehtml to make a single large HTML file"
	@echo "  pickle     to make pickle files"
	@echo "  json       to make JSON files"
	@echo "  htmlhelp   to make HTML files and a HTML help project"
	@echo "  qthelp     to make HTML files and a qthelp project"
	@echo "  devhelp    to make HTML files and a Devhelp project"
	@echo "  epub       to make an epub"
	@echo "  latex      to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
	@echo "  latexpdf   to make LaTeX files and run them through pdflatex"
	@echo "  latexpdfja to make LaTeX files and run them through platex/dvipdfmx"
	@echo "  text       to make text files"
	@echo "  man        to make manual pages"
	@echo "  texinfo    to make Texinfo files"
	@echo "  info       to make Texinfo files and run them through makeinfo"
	@echo "  gettext    to make PO message catalogs"
	@echo "  changes    to make an overview of all changed/added/deprecated items"
	@echo "  xml        to make Docutils-native XML files"
	@echo "  pseudoxml  to make pseudoxml-XML files for display purposes"
	@echo "  linkcheck  to check all external links for integrity"
	@echo "  doctest    to run all doctests embedded in the documentation (if enabled)"

clean:
	rm -rf $(BUILDDIR)/*

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

dirhtml:
	$(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/dirhtml
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/dirhtml."

singlehtml:
	$(SPHINXBUILD) -b singlehtml $(ALLSPHINXOPTS) $(BUILDDIR)/singlehtml
	@echo
	@echo "Build finished. The HTML page is in $(BUILDDIR)/singlehtml."

pickle:
	$(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) $(BUILDDIR)/pickle
	@echo
	@echo "Build finished; now you can process the pickle files."

json:
	$(SPHINXBUILD) -b json $(ALLSPHINXOPTS) $(BUILDDIR)/json
	@echo
	@echo "Build finished; now you can process the JSON files."

htmlhelp:
	$(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) $(BUILDDIR)/htmlhelp
	@echo
	@echo "Build finished; now you can run HTML Help Workshop with the" \
	      ".hhp project file in $(BUILDDIR)/htmlhelp."

qthelp:
	$(SPHINXBUILD) -b qthelp $(ALLSPHINXOPTS) $(BUILDDIR)/qthelp
	@echo
	@echo "Build finished; now you can run "qcollectiongenerator" with the" \
	      ".qhcp project file in $(BUILDDIR)/qthelp, like this:"
	@echo "# qcollectiongenerator $(BUILDDIR)/qthelp/JanitOO.qhcp"
	@echo "To view the help file:"
	@echo "# assistant -collectionFile $(BUILDDIR)/qthelp/JanitOO.qhc"

devhelp:
	$(SPHINXBUILD) -b devhelp $(ALLSPHINXOPTS) $(BUILDDIR)/devhelp
	@echo
	@echo "Build finished."
	@echo "To view the help file:"
	@echo "# mkdir -p $$HOME/.local/share/devhelp/JanitOO"
	@echo "# ln -s $(BUILDDIR)/devhelp $$HOME/.local/share/devhelp/JanitOO"
	@echo "# devhelp"

epub:
	$(SPHINXBUILD) -b epub $(ALLSPHINXOPTS) $(BUILDDIR)/epub
	@echo
	@echo "Build finished. The epub file is in $(BUILDDIR)/epub."

latex:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo
	@echo "Build finished; the LaTeX files are in $(BUILDDIR)/latex."
	@echo "Run \`make' in that directory to run these through (pdf)latex" \
	      "(use \`make latexpdf' here to do that automatically)."

latexpdf:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo "Running LaTeX files through pdflatex..."
	$(MAKE) -C $(BUILDDIR)/latex all-pdf
	@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex."

latexpdfja:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo "Running LaTeX files through platex and dvipdfmx..."
	$(MAKE) -C $(BUILDDIR)/latex all-pdf-ja
	@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex."

text:
	$(SPHINXBUILD) -b text $(ALLSPHINXOPTS) $(BUILDDIR)/text
	@echo
	@echo "Build finished. The text files are in $(BUILDDIR)/text."

man:
	$(SPHINXBUILD) -b man $(ALLSPHINXOPTS) $(BUILDDIR)/man
	@echo
	@echo "Build finished. The manual pages are in $(BUILDDIR)/man."

texinfo:
	$(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(BUILDDIR)/texinfo
	@echo
	@echo "Build finished. The Texinfo files are in $(BUILDDIR)/texinfo."
	@echo "Run \`make' in that directory to run these through makeinfo" \
	      "(use \`make info' here to do that automatically)."

info:
	$(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(BUILDDIR)/texinfo
	@echo "Running Texinfo files through makeinfo..."
	make -C $(BUILDDIR)/texinfo info
	@echo "makeinfo finished; the Info files are in $(BUILDDIR)/texinfo."

gettext:
	$(SPHINXBUILD) -b gettext $(I18NSPHINXOPTS) $(BUILDDIR)/locale
	@echo
	@echo "Build finished. The message catalogs are in $(BUILDDIR)/locale."

changes:
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) $(BUILDDIR)/changes
	@echo
	@echo "The overview file is in $(BUILDDIR)/changes."

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

doctest:
	$(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) $(BUILDDIR)/doctest
	@echo "Testing of doctests in the sources finished, look at the " \
	      "results in $(BUILDDIR)/doctest/output.txt."

xml:
	$(SPHINXBUILD) -b xml $(ALLSPHINXOPTS) $(BUILDDIR)/xml
	@echo
	@echo "Build finished. The XML files are in $(BUILDDIR)/xml."

pseudoxml:
	$(SPHINXBUILD) -b pseudoxml $(ALLSPHINXOPTS) $(BUILDDIR)/pseudoxml
	@echo
	@echo "Build finished. The pseudo-XML files are in $(BUILDDIR)/pseudoxml."

rst:
	$(SPHINXBUILD) -b rst $(ALLSPHINXOPTS) $(BUILDDIR)/rst
	@echo
	@echo "Build finished. The ReST files are in $(BUILDDIR)/rst."

deps:
ifneq ('${BASHDEPS}','')
	bash ${BASHDEPS}
endif
ifneq ('${DEBIANDEPS}','')
	sudo apt-get install -y ${DEBIANDEPS}
endif
	@echo
	@echo "Dependencies for ${MODULENAME} finished."

install:
	${PYTHON_EXEC} setup.py install
	#~ pip install -r requirements.txt
	@echo
	@echo "Installation finished."

develop:
	${PYTHON_EXEC} setup.py develop
	#~ pip install -r requirements.txt
	@echo
	@echo "Installation for developpers of ${MODULENAME} finished."

directories:
	-sudo mkdir /opt/janitoo
	-sudo chown -Rf ${USER}:${USER} /opt/janitoo
	-for dir in cache cache/janitoo_manager home log run etc init; do mkdir /opt/janitoo/$$dir; done

docker-deps:
	-test -d docker/config && cp -rf docker/config/* /opt/janitoo/etc/
	-test -d docker/supervisor.conf.d && cp -rf docker/supervisor.conf.d/* /etc/supervisor/janitoo.conf.d/
	-test -d docker/supervisor-tests.conf.d && cp -rf docker/supervisor-tests.conf.d/* /etc/supervisor/janitoo-tests.conf.d/
	-test -d docker/nginx && cp -rf docker/nginx/* /etc/nginx/conf.d/
	true
	@echo
	@echo "Docker dependencies for ${MODULENAME} installed."

travis-deps:
	sudo apt-get install -y python-pip
	pip install git+git://github.com/bibi21000/janitoo_nosetests@master
	pip install git+git://github.com/bibi21000/janitoo_nosetests_flask@master
	pip install coveralls
	@echo
	@echo "Travis dependencies for ${MODULENAME} installed."

docker-tests:
	@echo
	@echo "Docker tests for ${MODULENAME} start."
	[ -f tests/test_docker.py ] && $(NOSE) $(NOSEOPTS) $(NOSEDOCKER) tests/test_docker.py
	@echo
	@echo "Docker tests for ${MODULENAME} finished."

docker-local-pull:
	@echo
	@echo "Pull local docker for ${MODULENAME}."
	docker pull bibi21000/${MODULENAME}
	@echo
	@echo "Docker local for ${MODULENAME} pulled."

docker-local-store: docker-local-pull
	@echo
	@echo "Create docker local store for ${MODULENAME}."
	docker create -v /root/.ssh/ -v /opt/janitoo/etc/ --name ${DOCKERNAME}_store bibi21000/${MODULENAME} /bin/true
	@echo
	@echo "Docker local store for ${MODULENAME} created."

docker-local-running: docker-local-pull
	@echo
	@echo "Update local docker for ${MODULENAME}."
	-docker stop ${DOCKERNAME}_running
	-docker rm ${DOCKERNAME}_running
	docker create --volumes-from ${DOCKERNAME}_store -p 8885:22 --name ${DOCKERNAME}_running bibi21000/${MODULENAME}
	docker ps -a|grep ${DOCKERNAME}_running
	docker start ${DOCKERNAME}_running
	docker ps|grep ${DOCKERNAME}_running
	@echo
	@echo "Docker local for ${MODULENAME} updated."
	@echo "Docker tests for ${MODULENAME} finished."

tests:
	-mkdir -p ${BUILDPKGDIR}/docs/html/tools/coverage
	-mkdir -p ${BUILDPKGDIR}/docs/html/tools/nosetests
	#~ export NOSESKIP=False && $(NOSE) $(NOSEOPTS) $(NOSECOVER) tests ; unset NOSESKIP
	#~ $(NOSE) $(NOSEOPTS) $(NOSECOVER) tests
	@echo
	@echo "Tests for ${MODULENAME} finished."

build:
	${PYTHON_EXEC} setup.py build --build-base $(BUILDPKGDIR)

egg:
	-mkdir -p $(BUILDPKGDIR)
	-mkdir -p $(DISTDIR)
	${PYTHON_EXEC} setup.py bdist_egg --bdist-dir $(BUILDPKGDIR) --dist-dir $(DISTDIR)

tar:
	-mkdir -p $(DISTDIR)
	tar cvjf $(DISTDIR)/${MODULENAME}-${janitoo_version}.tar.bz2 -h --exclude=\*.pyc --exclude=\*.egg-info --exclude=janidoc --exclude=.git* --exclude=$(BUILDDIR) --exclude=$(DISTDIR) --exclude=$(ARCHBASE) .
	@echo
	@echo "Archive for ${MODULENAME} version ${janitoo_version} created"

commit:
	git commit -m "$(message)" -a && git push
	@echo
	@echo "Commits for branch master pushed on github."

pull:
	git pull
	@echo
	@echo "Commits from branch master pulled from github."

status:
	git status

clean-doc:
	-rm -Rf ${BUILDPKGDIR}/docs
	-rm -Rf ${BUILDPKGDIR}/janidoc
	-rm -f objects.inv
	-rm -f generated_doc
	-rm -f janidoc

janidoc:
	-mkdir -p ${BUILDPKGDIR}/janidoc
	-cp -Rf .${BUILDPKGDIR}/janidoc

apidoc:
	-rm -rf ${BUILDPKGDIR}/janidoc/source/api
	-mkdir -p ${BUILDPKGDIR}/janidoc/source/api
	cp -Rf . ${BUILDPKGDIR}/janidoc/
	cd ${BUILDPKGDIR}/janidoc/source/api && sphinx-apidoc --force --no-toc -o . ../../src/
	cd ${BUILDPKGDIR}/janidoc/source/api && mv ${MODULENAME}.rst index.rst

doc: janidoc apidoc
	- [ -f transitions_graph.py ] && python transitions_graph.py
	-cp -Rf rst/* ${BUILDPKGDIR}/janidoc/source
	sed -i -e "s/MODULE_NAME/${MODULENAME}/g" ${BUILDPKGDIR}/janidoc/source/tools/index.rst
	make -C ${BUILDPKGDIR}/janidoc html
	cp ${BUILDPKGDIR}/janidoc/source/README.rst README.rst
	-ln -s $(BUILDPKGDIR)/docs/html generated_doc
	@echo
	@echo "Documentation finished."

doc-commit: doc
	git checkout gh-pages
	cp -Rf ${BUILDPKGDIR}/docs/html/* .
	git add *.html
	git add *.js
	git add tools/
	git add api/
	-git add _images/
	-git add _modules/
	-git add _sources/
	-git add _static/
	git commit -m "Auto-commit documentation" -a
	git push origin gh-pages
	git checkout master
	@echo
	@echo "Documentation published to github.io."

github.io:
	git checkout --orphan gh-pages
	git rm -rf .
	touch .nojekyll
	git add .nojekyll
	git commit -m "Initial import" -a
	git push origin gh-pages
	git checkout master
	@echo
	@echo "github.io branch initialised."
