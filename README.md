Proyecto binance_automation
=================

## Guidelines

------

Determina que parametros han de seguirse para un diseño de código limpio
siguiendo una standarización correcta, así como tambien que direcctrices deben tenerse en cuenta a hora de hacer un commit.

### General

1. Todo elemento que no sea leido por un usuario final debe ir en ingles (Variables, Clases, Modelos, Componentes, Objectos, Contextos, Métodos, Funciones, etc...)

2. Los campos relacionales `many2one` deben poseer un sufijo, '`_id`' al final, si el campo relacional es `many2many` el sufijo sería `_ids`.

    ```python
    country_id = models.ForeignKey(to=Country, ...)
    department_ids = mdoels.ManyToManyField(to=Department, ...)
    ```

3. Bajo ningun motivo debe re-definirse la llave primaria de ningún modelo. Siempre debe ser llamada **`id`**

### Clases

1. Las clases deben ser escritas en CamelCase

    ```python
    class NewModel
    ```

2. Las tablas de la base de datos deben estar escritas en minusculas, separadas por una '**`_`**' y poseer el mismo nombre que su clase.

    ```python
    class NewModel

        def Meta(Meta):
            db_table = 'new_model'
    ```

### Commits

Cada commit realizado debería poseer un tag como prefijo:

* **`[IMP]`** para mejoras.
* **`[FIX]`** para correción de bugs.
* **`[REF]`** para refactorización
* **`[ADD]`** para agregar nuevos recursos
* **`[REM]`** para remover recursos
* **`[MOV]`** para mover archivor, o mover codigo de una archivo a otro.
* **`[MERGE]`** para merge de commits

Luego el mensaje como tal, espeficando la parte del código impactado por los cambios (nombre del modulo, app, libreria, objecto, componentes, etc..) y la descripción del cambio.

* Agregar siempre mensajes con significado, evitar usar una sola palabra como "fix" o "mejoras".
* De ser posible, evitar commits que impacten de modulos o componentes simultaneamente, intentar separarlos en diferentes commits 

    ```git
    [FIX] mailing: corregida recursividad de correo electronico, reemplazado ciclo for por un metodo. 
    ```

## Comandos

**1 - Iniciar Instancias (Todos los servicios):**

```bash
    $ docker-compose -f local.yml up
```

**2 - Iniciar Instancia solo de Django:**

 ```bash
    $ docker rm -f django # Para apagar la ejecución del contenedor de Django si fue ejecutado el paso 1 previmente
    $ docker-compose run --rm --service-ports django
 ```

**3 - Migración de Esquemas:**

```bash
    $ docker-compose run --rm django python manage.py makemigrations
    $ docker-compose run --rm django python manage.py migrate
```

**4 - Crear Superusuario:**

```bash
    $ docker-compose -f local.yml run --rm django python manage.py createsuperuser
```

**5 - Ingresa a la consola de Django desde docker:**

```bash
    $ docker-compose -f local.yml run --rm django python manage.py shell_plus
```

**6 - Reinicio Limpio de backend:**

```bash
    $ docker-compose down # baja y elimina contenedores principales
    $ docker volume rm $(docker volume ls -q) # Borra los volumenes
    $ docker-compose -f local.yml up
```

**7 - Instalar Paquetes de PIP**: _(agregarlo a los requeriments, si es necesarío)_

```bash
    $ docker-compose run --rm django pip <paquete>
```

**8 - Cargar Datos desde un archivo fixtures:**

```bash
    $ docker-compose run --rm django python manage.py loaddata <fixturename>
```

**9 - Cargar todos los datos dede fixtures:** _nota: Agregar nuevos fixtures al archivo run_fixtures.sh, si son creados_

```bash
    $ ./run_fixtures.sh
```

**10 - Aplicar certificados SSL:**

```bash
    $ snap install core; sudo snap refresh core
    $ snap install --classic certbot # Instala certbot
    $ ln -s /snap/bin/certbot /usr/bin/certbot # Prepara certbot
    $ certbot --nginx 
```

**11 - Renovar certificados SSL:**

```bash
    $ certbot renew --dry-run
```

_Nota: El comando para renovar el certbot esta instalado en uno de estos directorios_

- /etc/crontab/
- /etc/cron.*/*
- systemctl list-timers