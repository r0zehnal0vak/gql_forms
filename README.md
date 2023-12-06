```
uvicorn main:app --reload

uvicorn main:app --env-file environment.txt --reload
```

```
pytest --cov-report term-missing --cov=DBDefinitions --cov=GraphTypeDefinitions --cov=utils --log-cli-level=INFO
```

```
python -m pydoc GraphTypeDefinitions
```