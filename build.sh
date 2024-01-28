if [ "$1" = "--init" ]; then
  # Run the commands
  pip install matplotlib numpy catppuccin-matplotlib beautifulsoup4==4.12.3 pandas==2.2.0 Requests==2.31.0 lxml

  R -e 'install.packages(c("devtools", "patchwork","jsonlite"))'
  R -e 'install.packages("xgboost")'
  R -e 'devtools::install_github("albert-ying/catppuccin")'
fi

if ! R -e 'blogdown::build_site(build_rmd = "md5sum")'; then
    exit 1
fi

R -e 'blogdown::serve_site()'


