PY?=python3
PIPENV=PIPENV_VENV_IN_PROJECT=1 pipenv
IN_ENV=$(PIPENV) run
PELICAN?=$(IN_ENV) pelican
PELICANOPTS=

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py
PUBLISHCONF=$(BASEDIR)/publishconf.py

BLACK_TARGETS := $(shell find . -name "*.py" -not -path "*/.venv/*" -not -path "*/.vscode/*" -not -path "*/.tox/*")

DEBUG ?= 0
ifeq ($(DEBUG), 1)
	PELICANOPTS += -D
endif

RELATIVE ?= 0
ifeq ($(RELATIVE), 1)
	PELICANOPTS += --relative-urls
endif

help:
	@echo 'Makefile for a pelican Web site                                           '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make html                           (re)generate the web site          '
	@echo '   make clean                          remove the generated files         '
	@echo '   make regenerate                     regenerate files upon modification '
	@echo '   make publish                        generate using production settings '
	@echo '   make serve [PORT=8000]              serve site at http://localhost:8000'
	@echo '   make serve-global [SERVER=0.0.0.0]  serve (as root) to $(SERVER):80    '
	@echo '   make devserver [PORT=8000]          serve and regenerate together      '
	@echo '                                                                          '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html   '
	@echo 'Set the RELATIVE variable to 1 to enable relative urls                    '
	@echo '                                                                          '

setup:  
	$(PIPENV) install --dev

html:
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

format:
	$(IN_ENV) isort --apply
	$(IN_ENV) black $(BLACK_TARGETS)

lint:
	$(IN_ENV) isort --check-only
	$(IN_ENV) black --check $(BLACK_TARGETS)

lint-assets:  
	cat $(THEME)/static/css/main.scss | sass > /dev/null

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

regenerate:
	$(PELICAN) -r $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

serve: publish
ifdef PORT
	$(PELICAN) -v -l $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS) -p $(PORT)
else
	$(PELICAN) -v -l $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)
endif

serve-global:
ifdef SERVER
	$(PELICAN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         -l $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS) -p $(PORT) -b $(SERVER)
else
	$(PELICAN) -v -l $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS) -p $(PORT) -b 0.0.0.0
endif


devserver:
ifdef PORT
	$(PELICAN) -lr $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS) -p $(PORT)
else
	$(PELICAN) -lr $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)
endif

publish:
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS)

publish-demo:
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

migrate_all: migrate_images

migrate_images:
	$(IN_ENV) python management/image_migration.py /Users/antonioferegrino/Documents/GitHub/that-c-sharp-guy/postimages/ /Users/antonioferegrino/Documents/GitHub/yet-another-blog-migration/content/images/

migrate_posts:
	$(IN_ENV) python management/post_migration.py /Users/antonioferegrino/Documents/GitHub/that-c-sharp-guy/en/_posts/ /Users/antonioferegrino/Documents/GitHub/yet-another-blog-migration/content/
	$(IN_ENV) python management/post_migration.py /Users/antonioferegrino/Documents/GitHub/that-c-sharp-guy/es/_posts/ /Users/antonioferegrino/Documents/GitHub/yet-another-blog-migration/content/
	$(IN_ENV) python management/post_migration.py /Users/antonioferegrino/Documents/GitHub/that-c-sharp-guy/tv/_posts/ /Users/antonioferegrino/Documents/GitHub/yet-another-blog-migration/content/tv/ -t template:video


.PHONY: html help clean regenerate serve serve-global devserver stopserver publish test-assets