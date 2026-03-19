# Laboratorio Blue-Green Deployment con Monitoreo usando Docker

## Objetivo

Simular una arquitectura Blue-Green Deployment en entorno local utilizando Docker, separando la infraestructura de monitoreo mediante Prometheus y Grafana.

Este laboratorio permite validar el monitoreo de múltiples instancias antes de implementar la solución en producción.

---

## Arquitectura del laboratorio

Se simulan tres componentes principales:

* Instancia Blue: versión actual de la aplicación
* Instancia Green: nueva versión de la aplicación
* Instancia de monitoreo: servicios de observabilidad

### Servicios desplegados

* Blue → Node Exporter (simulación de aplicación)
* Green → Node Exporter (simulación de aplicación)
* Prometheus → recolección de métricas
* Grafana → visualización de métricas

Prometheus monitorea simultáneamente ambas instancias.

---

## Estructura del proyecto

Crear una carpeta:

```
lab-blue-green/
```

Dentro de ella crear:

* docker-compose.yml
* prometheus.yml

---

## docker-compose.yml

```
version: "3.8"

services:

  blue:
    image: prom/node-exporter
    container_name: blue_app
    ports:
      - "9100:9100"

  green:
    image: prom/node-exporter
    container_name: green_app
    ports:
      - "9200:9100"

  prometheus:
    image: prom/prometheus
    container_name: prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    depends_on:
      - blue
      - green

  grafana:
    image: grafana/grafana
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  prometheus_data:
  grafana_data:
```

---

## prometheus.yml

```
global:
  scrape_interval: 3s

scrape_configs:
  - job_name: "blue"
    static_configs:
      - targets: ["blue:9100"]

  - job_name: "green"
    static_configs:
      - targets: ["green:9100"]
```

---

## Levantar el laboratorio

Ejecutar:

```
docker compose up -d
```

Verificar contenedores:

```
docker ps
```

Deben aparecer:

* blue_app
* green_app
* prometheus
* grafana

---

## Accesos locales

Prometheus:

```
http://localhost:9090
```

Targets:

```
http://localhost:9090/targets
```

Grafana:

```
http://localhost:3000
```

Usuario inicial:

* user: admin
* password: Siempreunelefante07

---

## Configurar Grafana

1. Ir a Connections → Data Sources
2. Add Data Source → Prometheus
3. URL:

```
http://prometheus:9090
```

Guardar configuración.

---

## Crear Dashboard

Crear un panel nuevo y usar query:

```
up
```

Esto permite visualizar el estado de cada instancia monitoreada.

---

## Simular caída de una instancia

Detener instancia Blue:

```
docker stop blue_app
```

Luego verificar en:

```
http://localhost:9090/targets
```

La instancia debe aparecer como DOWN.

Esto simula una falla real en producción.

---

## Prueba de persistencia

Reiniciar todos los servicios:

```
docker compose restart
```

Las métricas deben mantenerse gracias a los volúmenes persistentes configurados.

---

## Conclusión

Este laboratorio permite validar una arquitectura donde la infraestructura de monitoreo está desacoplada del entorno de despliegue Blue-Green.

Prometheus y Grafana se ejecutan en un entorno independiente, permitiendo monitorear múltiples instancias sin reiniciarse durante cambios de versión o despliegues.

Esta práctica facilita la detección de fallos, mejora la observabilidad del sistema y permite realizar rollback de forma segura en entornos productivos.
