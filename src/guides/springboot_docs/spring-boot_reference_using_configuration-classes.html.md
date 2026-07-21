Search

# Configuration Classes

Spring Boot favors Java-based configuration.
Although it is possible to use [`SpringApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/SpringApplication.html) with XML sources, we generally recommend that your primary source be a single [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) class.
Usually the class that defines the `main` method is a good candidate as the primary [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html).

|  |  |
| --- | --- |
|  | Many Spring configuration examples have been published on the Internet that use XML configuration. If possible, always try to use the equivalent Java-based configuration. Searching for `Enable*` annotations can be a good starting point. |

## Importing Additional Configuration Classes

You need not put all your [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) into a single class.
The [`@Import`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Import.html) annotation can be used to import additional configuration classes.
Alternatively, you can use [`@ComponentScan`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/ComponentScan.html) to automatically pick up all Spring components, including [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) classes.

## Importing XML Configuration

If you absolutely must use XML based configuration, we recommend that you still start with a [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) class.
You can then use an [`@ImportResource`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/ImportResource.html) annotation to load XML configuration files.