for file in *
do
    if [[ $file == "." ]]
    then
        echo ""
    elif [[ $file == ".." ]]
    then
        echo ""
    elif [[ $file == "aux.sh" ]]
    then
        echo ""
    elif [[ $file == "__pycache__" ]]
    then
        echo ""
    else
        echo $file
        pyside6-uic "$file" -o "${file%???}.py"
    fi
done