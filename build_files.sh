echo " BUILD START"

python3.9 --version
python3.9 -m ensurepip # não aparece nos tutoriais internacionais
python3.9 -m pip install -r requirements.txt

echo " MAKE MIGRATIONS..."
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput


python3.9 manage.py collectstatic --noinput --clear
echo " BUILD END"