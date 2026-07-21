Search

# Process Monitoring

In the `spring-boot` module, you can find two classes to create files that are often useful for process monitoring:

* [`ApplicationPidFileWriter`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/ApplicationPidFileWriter.html) creates a file that contains the application PID (by default, in the application directory with a file name of `application.pid`).
* [`WebServerPortFileWriter`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/web/server/context/WebServerPortFileWriter.html) creates a file (or files) that contain the ports of the running web server (by default, in the application directory with a file name of `application.port`).

By default, these writers are not activated, but you can enable them:

* [Extending Configuration](#actuator.process-monitoring.configuration)
* [Programmatically Enabling Process Monitoring](#actuator.process-monitoring.programmatically)

## Extending Configuration

In the `META-INF/spring.factories` file, you can activate the listener (or listeners) that writes a PID file:

```
org.springframework.context.ApplicationListener=\
org.springframework.boot.context.ApplicationPidFileWriter,\
org.springframework.boot.web.server.context.WebServerPortFileWriter
```

## Programmatically Enabling Process Monitoring

You can also activate a listener by invoking the `SpringApplication.addListeners(…​)` method and passing the appropriate [`Writer`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/Writer.html) object.
This method also lets you customize the file name and path in the [`Writer`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/io/Writer.html) constructor.