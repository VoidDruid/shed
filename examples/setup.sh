# Add `shed` package to PYTHONPATH, so it can be called from any directory
export PYTHONPATH=$(pwd)/..:${PYTHONPATH}
alias run-shed="python3 -m shed"
