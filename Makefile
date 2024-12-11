install:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

run:
	. venv/bin/activate && flask run --host=0.0.0.0 --port=3000

test:
	PYTHONPATH=. . venv/bin/activate && pytest --maxfail=1 --disable-warnings -v
