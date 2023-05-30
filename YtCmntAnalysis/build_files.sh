echo " BUILD START"
python -m pip install -r requirements.txt
mkdir staticfiles_build/static
python manage.py collectstatic --noinput --clear
echo " BUILD END"

