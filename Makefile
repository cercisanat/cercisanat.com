install:
	mkdir -p media/ckeditor
	python manage.py syncdb --noinput
	python manage.py migrate
	python manage.py collectstatic --noinput

.PHONY: install