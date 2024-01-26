pip install \
    matplotlib \
    numpy \
    pandas \
    catppuccin-matplotlib

R -e 'install.packages("devtools")'
R -e 'devtools::install_github("albert-ying/catppuccin")'
R -e 'install.packages("patchwork")'

if ! R -e 'blogdown::build_site(build_rmd = "md5sum")'; then
    exit 1
fi

R -e 'blogdown::serve_site()'


