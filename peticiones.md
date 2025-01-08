## MONGO

```bash
curl -X POST http://localhost:5000/mongo \
-H "Content-Type: application/json" \
-d '{"nombre": "Juan", "edad": 30}'
```

```bash
curl -X GET http://localhost:5000/mongo
```

## REDIS

```bash
curl -X POST http://localhost:5000/redis \
-H "Content-Type: application/json" \
-d '{"clave1": "valor1", "clave2": "valor2"}'
```

```bash
curl -X GET http://localhost:5000/redis/clave1
```

## ELASTICSEARCH

```bash
curl -X POST http://localhost:5000/elasticsearch \
-H "Content-Type: application/json" \
-d '{"nombre": "Documento", "descripcion": "Prueba de Elastic"}'
```

```bash
curl -X GET http://localhost:5000/elasticsearch
```
