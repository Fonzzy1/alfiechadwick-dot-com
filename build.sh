set -e
pip install \
    matplotlib \
    numpy \
    pandas 

r -e 'blogdown::build_site(build_rmd = TRUE)'

git add .
git commit --amend --no-edit
git push --force-with-lease


