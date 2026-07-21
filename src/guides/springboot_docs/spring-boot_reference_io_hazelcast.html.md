Search

# Hazelcast

If [Hazelcast](https://hazelcast.com/) is on the classpath and a suitable configuration is found, Spring Boot auto-configures a [`HazelcastInstance`](https://docs.hazelcast.org/docs/5.5.0/javadoc/com/hazelcast/core/HazelcastInstance.html) that you can inject in your application.

Spring Boot first attempts to create a client by checking the following configuration options:

* The presence of a [`ClientConfig`](https://docs.hazelcast.org/docs/5.5.0/javadoc/com/hazelcast/client/config/ClientConfig.html) bean.
* A configuration file defined by the `spring.hazelcast.config` property.
* The presence of the `hazelcast.client.config` system property.
* A `hazelcast-client.xml` in the working directory or at the root of the classpath.
* A `hazelcast-client.yaml` (or `hazelcast-client.yml`) in the working directory or at the root of the classpath.

If a client can not be created, Spring Boot attempts to configure an embedded server.
If you define a [`Config`](https://docs.hazelcast.org/docs/5.5.0/javadoc/com/hazelcast/config/Config.html) bean, Spring Boot uses it at is.
If your configuration defines an instance name, Spring Boot tries to locate an existing instance rather than creating a new one.

You could also specify the Hazelcast configuration file to use through configuration, as shown in the following example:

* Properties
* YAML

```
spring.hazelcast.config=classpath:config/my-hazelcast.xml
```

```
spring:
  hazelcast:
    config: "classpath:config/my-hazelcast.xml"
```

Otherwise, Spring Boot tries to find the Hazelcast configuration from the default locations: `hazelcast.xml` in the working directory or at the root of the classpath, or a YAML counterpart in the same locations.
We also check if the `hazelcast.config` system property is set.
See the [Hazelcast documentation](https://docs.hazelcast.org/docs/latest/manual/html-single/) for more details.

|  |  |
| --- | --- |
|  | By default, [`@SpringAware`](https://docs.hazelcast.org/docs/5.5.0/javadoc/com/hazelcast/spring/context/SpringAware.html) on Hazelcast components is supported. The [`ManagedContext`](https://docs.hazelcast.org/docs/5.5.0/javadoc/com/hazelcast/core/ManagedContext.html) can be overridden by declaring a [`HazelcastConfigCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/hazelcast/autoconfigure/HazelcastConfigCustomizer.html) bean with an [`@Order`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/annotation/Order.html) higher than zero. |

|  |  |
| --- | --- |
|  | Spring Boot also has [explicit caching support for Hazelcast](caching.html#io.caching.provider.hazelcast). If caching is enabled, the [`HazelcastInstance`](https://docs.hazelcast.org/docs/5.5.0/javadoc/com/hazelcast/core/HazelcastInstance.html) is automatically wrapped in a [`CacheManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/CacheManager.html) implementation. |