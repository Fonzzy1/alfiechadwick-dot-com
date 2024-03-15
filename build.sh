for arg in "$@"
do
    if [ "$arg" = "--init" ]; then
        # Run the initialisation commands
        pip install matplotlib numpy catppuccin-matplotlib beautifulsoup4==4.12.3 pandas==2.2.0 Requests==2.31.0 lxml

        R -e 'install.packages(c("devtools", "patchwork","jsonlite"))'
        R -e 'install.packages("xgboost")'
        R -e 'devtools::install_github("albert-ying/catppuccin")'
    fi
done

R -e 'blogdown::build_site(build_rmd = "md5sum")'

for arg in "$@"
do
    if [ "$arg" = "--serve" ]; then
        R -e 'blogdown::serve_site()'
    fi
done
