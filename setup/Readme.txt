Data represented here is found at https://www.genomes2fields.org/resources/
Additionally you will need the file `g2f_2015_agronomic information.csv` which is reformatted to be more easily read in.

Code is to be run using the conda `g2fd` enviroment, which can be built from the "g2fd_env.yml" file provided.
1. create the enviorment from the yml
conda env create -f g2fd_env.yml
2. activate it
conda activate g2fd
3. if changes are made, export the new version
conda env export > g2fd_env.yml

