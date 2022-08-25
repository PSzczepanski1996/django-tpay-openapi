rm -rf build
rm -rf dist
python3 setup.py sdist bdist_wheel
echo -e "\e[32mProject rebuilt, now PyPi server is hosted on \e[96m\e[1mhttp://localhost:8421\e[0m"
pypi-server run -p 8421 ./dist
