echo " BUILD START"
python -m pip install -r requirements.txt
mkdir staticfiles_build/
python manage.py collectstatic --noinput --clear
echo " BUILD END"

