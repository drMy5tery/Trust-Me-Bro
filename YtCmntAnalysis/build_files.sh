echo " BUILD START"
python --version
pip3 --version
pip3 install -r requirements.txt
python3.9 manage.py collectstatic --noinput --clear
echo " BUILD END"

