# **Reserva de Horas - Aplicación en Flask**

Bienvenido a **Reserva de Horas**, una sencilla pero potente aplicación web construida con **Flask** que permite gestionar reservas de horarios de manera eficiente y dinámica. Este proyecto proporciona una **interfaz intuitiva** tanto para usuarios como para administradores, con un sistema de gestión de reservas que incluye notificaciones por correo electrónico para cada acción realizada.

## **Características principales** ✨

### **Funcionalidad para Usuarios**:
- **Registro y Login**: Diferencia entre **usuarios** y **administradores** mediante un sistema de autenticación basado en roles.
- **Solicitar Reservas**: Los usuarios pueden solicitar una o varias horas de su elección en el calendario disponible.
- **Gestión de Solicitudes**: Cada solicitud enviada por un usuario será notificada al administrador para su revisión.

### **Funcionalidad para Administradores**:
- **Aceptar o Denegar Solicitudes**: Los administradores tienen la capacidad de gestionar las solicitudes de los usuarios, aceptando o denegando las reservas según sea necesario.
- **Notificaciones por Correo**: Cada acción tomada, ya sea una aceptación o un rechazo de solicitud, es seguida de una **alerta por correo electrónico** tanto para el usuario como para el administrador.

---

## **Tecnologías utilizadas** ⚙️

- **Flask**: Framework principal para desarrollar la aplicación.
- **SQLAlchemy**: ORM utilizado para la gestión de la base de datos.
- **Bootstrap**: Para una interfaz de usuario moderna y responsive.
- **Correo Electrónico (SMTP)**: Para el envío de alertas y notificaciones.

---

## **Cómo Ejecutar la Aplicación** 🚀

1. **Clona este repositorio**:
   ```bash
   git clone https://github.com/tu_usuario/reserva-de-horas.git
   ```
2. **Instala las dependencias**:
   ```bash
   pip install flask flask_sqlalchemy flask_login sqlalchemy flask_mail
   ```
3. **Ejecuta la aplicación**: Para correr la aplicación en tu máquina, solo necesitas ejecutar el siguiente comando (con privilegios de administrador si es necesario):
   ```bash
   python app.py
   ```
La aplicación estará disponible en http://127.0.0.1:5000.

## Estructura de Archivos 📁
   ```bash
   /Reserva-de-Horas
   │
   ├── /templates               # Archivos HTML para las vistas
   ├── /static                  # Archivos estáticos como CSS, JS, imágenes
   ├── app.py                   # Archivo principal para iniciar la app
   ├── models.py                # Definición de la base de datos
   ├── requirements.txt         # Librerías necesarias para el proyecto
   └── README.md                # Documentación del proyecto
   ```

## Contribuciones ✍️
Si deseas contribuir a este proyecto, siéntete libre de realizar un fork y enviar tus pull requests. Todas las sugerencias y mejoras son bienvenidas.




