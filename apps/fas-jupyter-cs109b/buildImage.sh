# exit if a command exits with a non-zero status
set -e

# get the name of current folder to use as image name
imageName=${PWD##*/} 

# compile the requirements into requirements.txt
# echo "Compiling requirements for ${imageName}..."
# pip-compile --resolver=backtracking --output-file requirements.txt requirements.in

# build the image, tagging with parent folder name

echo "Building docker image for ${imageName}"
docker build --platform linux/amd64 -t $imageName . 

# Export the installed packages to a reference file
echo "Exporting requirements for ${imageName}"
docker run --rm --platform linux/amd64 $imageName conda env export -n base > environment.yml
