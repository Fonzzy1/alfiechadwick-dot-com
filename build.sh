if [[ $(git status --porcelain) ]]; then
    echo "There are uncommitted or unpushed changes. Please commit or push your changes before running this script."
    exit 1
fi

pip install \
    matplotlib \
    numpy \
    pandas

if ! R -e 'blogdown::build_site(build_rmd = TRUE)'; then
    exit 1
fi

if ! R -e 'blogdown::serve_site()'; then


