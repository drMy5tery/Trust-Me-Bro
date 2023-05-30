echo " BUILD START"
python --version
pip --version
python -m pip install -r requirements.txt
python3.9 manage.py collectstatic --noinput --clear
echo " BUILD END"

