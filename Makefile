.PHONY: all clean clean_data

SCRIPTS=$(wildcard scripts/*.py)
PLOTS=$(patsubst scripts/%.py,plots/%.png,$(SCRIPTS))

all: $(PLOTS)

clean_data: 
	rm -rf data

clean: 
	rm -rf plots

data:
	mkdir -p data
	wget -P data https://ftp.geogratis.gc.ca/pub/nrcan_rncan/vector/framework_cadre/Atlas_of_Canada_1M/hydrology/AC_1M_Waterbodies.shp.zip
	wget -P data https://ftp.geogratis.gc.ca/pub/nrcan_rncan/vector/framework_cadre/Atlas_of_Canada_1M/hydrology/AC_1M_Rivers.shp.zip 
	cd data; unzip AC_1M_Waterbodies.shp.zip
	cd data; unzip AC_1M_Rivers.shp.zip

plots/%.png: scripts/%.py data
	mkdir -p plots
	python $< data $@