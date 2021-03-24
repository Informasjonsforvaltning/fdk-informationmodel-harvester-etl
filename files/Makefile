.PHONY: test
all: extract transform load

extract:
	echo "Extracting informationmodels..."
	python3 ./extract_informationmodels.py -o ./tmp/

transform:
	echo "Transforming informationmodels...."
	python3 -u ./transform_informationmodels.py -o ./tmp/

delete:
	echo "Deleting informationmodels...."
	python3 ./delete_informationmodels.py -o ./tmp/

clean:
	rm ./tmp/*.json
