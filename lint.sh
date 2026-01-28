#!/bin/bash
ruff check binary_database_files
black --check binary_database_files
isort --check binary_database_files