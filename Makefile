include Makeconf

.PHONY: clean

all: clean po sis-unsigned

clean:
	-rm -rf $(BUILD_DIR)

po:
	for l in $(SRC_CLI_LOCALES); do \
		cd $(SRC_CLI_DIR)/locale/$$l/LC_MESSAGES  ; \
		pocompile pytriloquist.po -o pytriloquist.mo ; \
	done

sis:
	-mkdir $(BUILD_DIR)
	cd $(PYS60_DIR) ; \
	python ensymble.py py2sis --icon="$(SIS_ICON)" --version="$(PROJECT_VERSION)"          \
	--appname="$(SIS_APPNAME)" --caption="$(SIS_CAPTION)" --shortcaption="$(SIS_SCAPTION)" \
	--vendor="$(SIS_VENDOR)" --uid="$(SIS_UID)" --lang="$(SIS_LANG)" --caps="$(SIS_CAPS)"  \
	"$(SRC_CLI_DIR)" "$(SIS_FILE).sis"

sis-unsigned: sis
	cp $(SIS_FILE).sis $(SIS_FILE)-unsigned.sis
	cd $(PYS60_DIR) ; \
	python ensymble.py signsis --unsign "$(SIS_FILE)-unsigned.sis"
