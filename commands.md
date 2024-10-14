```bash
pipenv run python -c "from db import init_db; init_db()"
```

```bash
pipenv run python batch.py
```


```bash
pytest --cache-clear
```

##起動
```bash
pipenv run uvicorn main:app --reload
```

```bash
pipenv run streamlit run streamlit_app.py
```


