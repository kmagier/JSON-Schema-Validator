Simple JSON Schema Validator created for Formal Languages and Compilers classes.Validator works as finite automata matching tokens with corresponding groups. To check if JSON schema is valid, schema should be put inside a txt file, and name of file should be given as parameter to a validate.sh script, which runs the validator written in Python:

```
./validate.sh NAME_OF_TXT_FILE.txt
```
