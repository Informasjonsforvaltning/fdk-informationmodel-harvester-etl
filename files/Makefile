.PHONY: test
all: extract transform load

extract:
	echo "Extracting informationmodels..."
	python3 ./extract_mongodata.py -o ./tmp/

load:
	echo "Loading informationmodels...."
	python3 ./load_informationmodels.py -o ./tmp/

clean:
	rm ./tmp/*.json
