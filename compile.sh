search_dir=source
for entry in "$search_dir"/*
do
    python compiler.py "$entry"
done