FILE=$1
if [[ "$#" -ne 1 ]] 
then
	echo "You must enter exactly 1 command line argument. Usage: ./validate.sh <FILE_TO_VALIDATE>"
else
	python ./validator.py $FILE
fi