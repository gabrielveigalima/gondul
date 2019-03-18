#!/usr/bin/env bash
cd ~/repo/
echo "["$(date -u +"%Y-%m-%dT%H:%M:%SZ")"][RUNNER] Current Dir:" $(pwd)
pip install -U pip wheel setuptools numba
pip install --user -r pip_requirements.txt

pip install scrapy
cd Gondul
scrapy crawl pciconcursos
scrapy crawl folhadirigida
