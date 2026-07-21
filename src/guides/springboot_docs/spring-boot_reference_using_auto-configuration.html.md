Search

# Auto-configuration

Spring Boot auto-configuration attempts to automatically configure your Spring application based on the jar dependencies that you have added.
For example, if `HSQLDB` is on your classpath, and you have not manually configured any database connection beans, then Spring Boot auto-configures an in-memory database.

You need to opt-in to auto-configuration by adding the [`@EnableAutoConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/EnableAutoConfiguration.html) or [`@SpringBootApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/SpringBootApplication.html) annotations to one of your [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) classes.

|  |  |
| --- | --- |
|  | You should only ever add one [`@SpringBootApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/SpringBootApplication.html) or [`@EnableAutoConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/EnableAutoConfiguration.html) annotation. We generally recommend that you add one or the other to your primary [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) class only. |

## Gradually Replacing Auto-configuration

Auto-configuration is non-invasive.
At any point, you can start to define your own configuration to replace specific parts of the auto-configuration.
For example, if you add your own [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html) bean, the default embedded database support backs away.

If you need to find out what auto-configuration is currently being applied, and why, start your application with the `--debug` switch.
Doing so enables debug logs for a selection of core loggers and logs a conditions report to the console.

## Disabling Specific Auto-configuration Classes

If you find that specific auto-configuration classes that you do not want are being applied, you can use the exclude attribute of [`@SpringBootApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/SpringBootApplication.html) to disable them, as shown in the following example:

* Java
* Kotlin

```
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration;

@SpringBootApplication(exclude = { DataSourceAutoConfiguration.class })
public class MyApplication {

}
```

```
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration

@SpringBootApplication(exclude = [DataSourceAutoConfiguration::class])
class MyApplication
```

If the class is not on the classpath, you can use the `excludeName` attribute of the annotation and specify the fully qualified name instead.
If you prefer to use [`@EnableAutoConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/EnableAutoConfiguration.html) rather than [`@SpringBootApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/SpringBootApplication.html), `exclude` and `excludeName` are also available.
Finally, you can also control the list of auto-configuration classes to exclude by using the `spring.autoconfigure.exclude` property.

|  |  |
| --- | --- |
|  | You can define exclusions both at the annotation level and by using the property. |

|  |  |
| --- | --- |
|  | Even though auto-configuration classes are `public`, the only aspect of the class that is considered public API is the name of the class which can be used for disabling the auto-configuration. The actual contents of those classes, such as nested configuration classes or bean methods are for internal use only and we do not recommend using those directly. |

## Auto-configuration Packages

Auto-configuration packages are the packages that various auto-configured features look in by default when scanning for things such as entities and Spring Data repositories.
The [`@EnableAutoConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/EnableAutoConfiguration.html) annotation (either directly or through its presence on [`@SpringBootApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/SpringBootApplication.html)) determines the default auto-configuration package.
Additional packages can be configured using the [`@AutoConfigurationPackage`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/AutoConfigurationPackage.html) annotation.