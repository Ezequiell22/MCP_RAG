Search

# Monitoring and Management over JMX

Java Management Extensions (JMX) provide a standard mechanism to monitor and manage applications.
By default, this feature is not enabled.
You can turn it on by setting the `spring.jmx.enabled` configuration property to `true`.
Spring Boot exposes the most suitable [`MBeanServer`](https://docs.oracle.com/en/java/javase/17/docs/api/java.management/javax/management/MBeanServer.html) as a bean with an ID of `mbeanServer`.
Any of your beans that are annotated with Spring JMX annotations (`@org.springframework.jmx.export.annotation.ManagedResource`, [`@ManagedAttribute`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jmx/export/annotation/ManagedAttribute.html), or [`@ManagedOperation`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jmx/export/annotation/ManagedOperation.html)) are exposed to it.

If your platform provides a standard [`MBeanServer`](https://docs.oracle.com/en/java/javase/17/docs/api/java.management/javax/management/MBeanServer.html), Spring Boot uses that and defaults to the VM [`MBeanServer`](https://docs.oracle.com/en/java/javase/17/docs/api/java.management/javax/management/MBeanServer.html), if necessary.
If all that fails, a new [`MBeanServer`](https://docs.oracle.com/en/java/javase/17/docs/api/java.management/javax/management/MBeanServer.html) is created.

|  |  |
| --- | --- |
|  | `spring.jmx.enabled` affects only the management beans provided by Spring. Enabling management beans provided by other libraries (for example [Log4j2](https://logging.apache.org/log4j/2.x/manual/jmx.html) or [Quartz](https://javadoc.io/doc/org.quartz-scheduler/quartz/2.5.2/constant-values.html#org.quartz.impl.StdSchedulerFactory.PROP_SCHED_JMX_EXPORT)) is independent. |

See the [`JmxAutoConfiguration`](https://github.com/spring-projects/spring-boot/tree/v4.1.0/core/spring-boot-autoconfigure/src/main/java/org/springframework/boot/autoconfigure/jmx/JmxAutoConfiguration.java) class for more details.

By default, Spring Boot also exposes management endpoints as JMX MBeans under the `org.springframework.boot` domain.
To take full control over endpoint registration in the JMX domain, consider registering your own [`EndpointObjectNameFactory`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/jmx/EndpointObjectNameFactory.html) implementation.

## Customizing MBean Names

The name of the MBean is usually generated from the `id` of the endpoint.
For example, the `health` endpoint is exposed as `org.springframework.boot:type=Endpoint,name=Health`.

If your application contains more than one Spring [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html), you may find that names clash.
To solve this problem, you can set the `spring.jmx.unique-names` property to `true` so that MBean names are always unique.

You can also customize the JMX domain under which endpoints are exposed.
The following settings show an example of doing so in `application.properties`:

* Properties
* YAML

```
spring.jmx.unique-names=true
management.endpoints.jmx.domain=com.example.myapp
```

```
spring:
  jmx:
    unique-names: true
management:
  endpoints:
    jmx:
      domain: "com.example.myapp"
```

## Disabling JMX Endpoints

If you do not want to expose endpoints over JMX, you can set the `management.endpoints.jmx.exposure.exclude` property to `*`, as the following example shows:

* Properties
* YAML

```
management.endpoints.jmx.exposure.exclude=*
```

```
management:
  endpoints:
    jmx:
      exposure:
        exclude: "*"
```