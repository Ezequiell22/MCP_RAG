Search

# Using the @SpringBootApplication Annotation

Many Spring Boot developers like their apps to use auto-configuration, component scan and be able to define extra configuration on their "application class".
A single [`@SpringBootApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/SpringBootApplication.html) annotation can be used to enable those three features, that is:

* [`@EnableAutoConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/EnableAutoConfiguration.html): enable [Spring Boot’s auto-configuration mechanism](auto-configuration.html)
* [`@ComponentScan`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/ComponentScan.html): enable [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html) scan on the package where the application is located (see [the best practices](structuring-your-code.html))
* [`@SpringBootConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/SpringBootConfiguration.html): enable registration of extra beans in the context or the import of additional configuration classes.
  An alternative to Spring’s standard [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) that aids [configuration detection](../testing/spring-boot-applications.html#testing.spring-boot-applications.detecting-configuration) in your integration tests.

* Java
* Kotlin

```
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

// Same as @SpringBootConfiguration @EnableAutoConfiguration @ComponentScan
@SpringBootApplication
public class MyApplication {

	public static void main(String[] args) {
		SpringApplication.run(MyApplication.class, args);
	}

}
```

```
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

// Same as @SpringBootConfiguration @EnableAutoConfiguration @ComponentScan
@SpringBootApplication
class MyApplication

fun main(args: Array<String>) {
	runApplication<MyApplication>(*args)
}
```

|  |  |
| --- | --- |
|  | [`@SpringBootApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/SpringBootApplication.html) also provides aliases to customize the attributes of [`@EnableAutoConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/EnableAutoConfiguration.html) and [`@ComponentScan`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/ComponentScan.html). |

|  |  |
| --- | --- |
|  | None of these features are mandatory and you may choose to replace this single annotation by any of the features that it enables. For instance, you may not want to use component scan or configuration properties scan in your application:  * Java * Kotlin  ``` import org.springframework.boot.SpringApplication; import org.springframework.boot.SpringBootConfiguration; import org.springframework.boot.autoconfigure.EnableAutoConfiguration; import org.springframework.context.annotation.Import;  @SpringBootConfiguration(proxyBeanMethods = false) @EnableAutoConfiguration @Import({ SomeConfiguration.class, AnotherConfiguration.class }) public class MyApplication {  	public static void main(String[] args) { 		SpringApplication.run(MyApplication.class, args); 	}  } ```  ``` import org.springframework.boot.SpringBootConfiguration import org.springframework.boot.autoconfigure.EnableAutoConfiguration import org.springframework.boot.docs.using.structuringyourcode.locatingthemainclass.MyApplication import org.springframework.boot.runApplication import org.springframework.context.annotation.Import  @SpringBootConfiguration(proxyBeanMethods = false) @EnableAutoConfiguration @Import(SomeConfiguration::class, AnotherConfiguration::class) class MyApplication  fun main(args: Array<String>) { 	runApplication<MyApplication>(*args) } ```  In this example, `MyApplication` is just like any other Spring Boot application except that [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html)-annotated classes and [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html)-annotated classes are not detected automatically and the user-defined beans are imported explicitly (see [`@Import`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Import.html)). |