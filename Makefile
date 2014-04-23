install:
	mkdir -p media/ckeditor
	git clone "https://github.com/cercisanat/django-ajax-forms.git"
	python manage.py syncdb
	python manage.py migrate
	python manage.py collectstatic --noinput
	python manage.py runserver
.PHONY: install
