
# Useful Commands

### Run the entire APP
```bash
# cur dir: /
npm run dev
```

## Backend

### Run
```bash
# cur dir: /backend
fastapi dev
```

### Format
```bash
# cur dir: /backend
black .
```

### Run unit test
```bash
# cur dir: /backend
python -m unittest -vs
```

### Generate frontend schemas
Generate TS codes in frontend to unify APIs.
```bash
# cur dir: /
chmod +x ./tools/sync-schemas.sh
./tools/sync-schemas.sh
```


## Frontend

### Run
```bash
# cur dir: /frontend
npm run dev
```

