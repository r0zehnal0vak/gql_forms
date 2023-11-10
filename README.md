```
uvicorn main:app --reload
```

```
pytest --cov-report term-missing --cov=DBDefinitions --cov=GraphTypeDefinitions --cov=utils --log-cli-level=INFO
```