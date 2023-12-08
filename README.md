```
uvicorn main:app --env-file environment.txt --port 8002 --reload
```

```
pytest --cov-report term-missing --cov=DBDefinitions --cov=GraphTypeDefinitions --cov=utils --log-cli-level=INFO
```


```
python -m pydoc GraphTypeDefinitions
```