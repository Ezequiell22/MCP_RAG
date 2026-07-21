Search

# Validation

The method validation feature supported by Bean Validation 1.1 is automatically enabled as long as a JSR-303 implementation (such as Hibernate Validator, typically provided by `spring-boot-starter-validation`) is on the classpath.
This lets bean methods be annotated with `jakarta.validation` constraints on their parameters and/or on their return value.
Target classes with such annotated methods need to be annotated with the [`@Validated`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/validation/annotation/Validated.html) annotation at the type level for their methods to be searched for inline constraint annotations.

For instance, the following service triggers the validation of the first argument, making sure its size is between 8 and 10:

* Java
* Kotlin

```
import jakarta.validation.constraints.Size;

import org.springframework.stereotype.Service;
import org.springframework.validation.annotation.Validated;

@Service
@Validated
public class MyBean {

	public Archive findByCodeAndAuthor(@Size(min = 8, max = 10) String code, Author author) {
		return ...
	}

}
```

```
import jakarta.validation.constraints.Size
import org.springframework.stereotype.Service
import org.springframework.validation.annotation.Validated

@Service
@Validated
class MyBean {

	fun findByCodeAndAuthor(code: @Size(min = 8, max = 10) String?, author: Author?): Archive? {
		return null
	}

}
```

The application’s [`MessageSource`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/MessageSource.html) is used when resolving `{parameters}` in constraint messages.
This allows you to use [your application’s `messages.properties` files](../features/internationalization.html) for Bean Validation messages.
Once the parameters have been resolved, message interpolation is completed using Bean Validation’s default interpolator.

To customize the [`Configuration`](https://jakarta.ee/specifications/bean-validation/3.1/apidocs/jakarta/validation/Configuration.html) used to build the [`ValidatorFactory`](https://jakarta.ee/specifications/bean-validation/3.1/apidocs/jakarta/validation/ValidatorFactory.html), define a [`ValidationConfigurationCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/validation/autoconfigure/ValidationConfigurationCustomizer.html) bean.
When multiple customizer beans are defined, they are called in order based on their [`@Order`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/annotation/Order.html) annotation or [`Ordered`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/Ordered.html) implementation.