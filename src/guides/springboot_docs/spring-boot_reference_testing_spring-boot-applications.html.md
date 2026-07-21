Search

# Testing Spring Boot Applications

A Spring Boot application is a Spring [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html), so nothing very special has to be done to test it beyond what you would normally do with a vanilla Spring context.

|  |  |
| --- | --- |
|  | External properties, logging, and other features of Spring Boot are installed in the context by default only if you use [`SpringApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/SpringApplication.html) to create it. |

Spring Boot provides a [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html) annotation, which can be used as an alternative to the standard `spring-test` [`@ContextConfiguration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/context/ContextConfiguration.html) annotation when you need Spring Boot features.
The annotation works by [creating the [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html) used in your tests through [`SpringApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/SpringApplication.html)](#testing.spring-boot-applications.detecting-configuration).
In addition to [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html) a number of other annotations are also provided for [testing more specific slices](#testing.spring-boot-applications.autoconfigured-tests) of an application.

|  |  |
| --- | --- |
|  | If you are using JUnit 4, do not forget to also add `@RunWith(SpringRunner.class)` to your test, otherwise the annotations will be ignored. If you are using JUnit 6, there is no need to add the equivalent `@ExtendWith(SpringExtension.class)` as [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html) and the other `@…​Test` annotations are already annotated with it. |

By default, [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html) will not start a server.
You can use the `webEnvironment` attribute of [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html) to further refine how your tests run:

* `MOCK`(Default) : Loads a web [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html) and provides a mock web environment.
  Embedded servers are not started when using this annotation.
  If a web environment is not available on your classpath, this mode transparently falls back to creating a regular non-web [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html).
  It can be used in conjunction with [`@AutoConfigureMockMvc`](#testing.spring-boot-applications.with-mock-environment), or [`@AutoConfigureWebTestClient`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webtestclient/autoconfigure/AutoConfigureWebTestClient.html)] for mock-based testing of your web application.
* `RANDOM_PORT`: Loads a [`WebServerApplicationContext`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/web/server/context/WebServerApplicationContext.html) and provides a real web environment.
  Embedded servers are started and listen on a random port.
* `DEFINED_PORT`: Loads a [`WebServerApplicationContext`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/web/server/context/WebServerApplicationContext.html) and provides a real web environment.
  Embedded servers are started and listen on a defined port (from your `application.properties`) or on the default port of `8080`.
* `NONE`: Loads an [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html) by using [`SpringApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/SpringApplication.html) but does not provide *any* web environment (mock or otherwise).

|  |  |
| --- | --- |
|  | If your test is [`@Transactional`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/transaction/annotation/Transactional.html), it rolls back the transaction at the end of each test method by default. However, as using this arrangement with either `RANDOM_PORT` or `DEFINED_PORT` implicitly provides a real servlet environment, the HTTP client and server run in separate threads and, thus, in separate transactions. Any transaction initiated on the server does not roll back in this case. |

|  |  |
| --- | --- |
|  | [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html) with `webEnvironment = WebEnvironment.RANDOM_PORT` will also start the management server on a separate random port if your application uses a different port for the management server. |

## Detecting Web Application Type

If Spring MVC is available, a regular MVC-based application context is configured.
If you have only Spring WebFlux, we will detect that and configure a WebFlux-based application context instead.

If both are present, Spring MVC takes precedence.
If you want to test a reactive web application in this scenario, you must set the `spring.main.web-application-type` property:

* Java
* Kotlin

```
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest(properties = "spring.main.web-application-type=reactive")
class MyWebFluxTests {

	// ...

}
```

```
import org.springframework.boot.test.context.SpringBootTest

@SpringBootTest(properties = ["spring.main.web-application-type=reactive"])
class MyWebFluxTests {

	// ...

}
```

## Detecting Test Configuration

If you are familiar with the Spring Test Framework, you may be used to using `@ContextConfiguration(classes=…​)` in order to specify which Spring [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) to load.
Alternatively, you might have often used nested [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) classes within your test.

When testing Spring Boot applications, this is often not required.
Spring Boot’s `@*Test` annotations search for your primary configuration automatically whenever you do not explicitly define one.

The search algorithm works up from the package that contains the test until it finds a class annotated with [`@SpringBootApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/SpringBootApplication.html) or [`@SpringBootConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/SpringBootConfiguration.html).
As long as you [structured your code](../using/structuring-your-code.html) in a sensible way, your main configuration is usually found.

|  |  |
| --- | --- |
|  | If you use a [test annotation to test a more specific slice of your application](#testing.spring-boot-applications.autoconfigured-tests), you should avoid adding configuration settings that are specific to a particular area on the [main method’s application class](#testing.spring-boot-applications.user-configuration-and-slicing).  The underlying component scan configuration of [`@SpringBootApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/SpringBootApplication.html) defines exclude filters that are used to make sure slicing works as expected. If you are using an explicit [`@ComponentScan`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/ComponentScan.html) directive on your [`@SpringBootApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/SpringBootApplication.html)-annotated class, be aware that those filters will be disabled. If you are using slicing, you should define them again. |

If you want to customize the primary configuration, you can use a nested [`@TestConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/TestConfiguration.html) class.
Unlike a nested [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) class, which would be used instead of your application’s primary configuration, a nested [`@TestConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/TestConfiguration.html) class is used in addition to your application’s primary configuration.

|  |  |
| --- | --- |
|  | Spring’s test framework caches application contexts between tests. Therefore, as long as your tests share the same configuration (no matter how it is discovered), the potentially time-consuming process of loading the context happens only once. |

## Using the Test Configuration Main Method

Typically the test configuration discovered by [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html) will be your main [`@SpringBootApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/SpringBootApplication.html).
In most well structured applications, this configuration class will also include the `main` method used to launch the application.

For example, the following is a very common code pattern for a typical Spring Boot application:

* Java
* Kotlin

```
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class MyApplication {

	public static void main(String[] args) {
		SpringApplication.run(MyApplication.class, args);
	}

}
```

```
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.docs.using.structuringyourcode.locatingthemainclass.MyApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class MyApplication

fun main(args: Array<String>) {
	runApplication<MyApplication>(*args)
}
```

In the example above, the `main` method doesn’t do anything other than delegate to [`SpringApplication.run(Class, String...)`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/SpringApplication.html#run(java.lang.Class,java.lang.String...)).
It is, however, possible to have a more complex `main` method that applies customizations before calling [`SpringApplication.run(Class, String...)`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/SpringApplication.html#run(java.lang.Class,java.lang.String...)).

For example, here is an application that changes the banner mode and sets additional profiles:

* Java
* Kotlin

```
import org.springframework.boot.Banner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class MyApplication {

	public static void main(String[] args) {
		SpringApplication application = new SpringApplication(MyApplication.class);
		application.setBannerMode(Banner.Mode.OFF);
		application.setAdditionalProfiles("myprofile");
		application.run(args);
	}

}
```

```
import org.springframework.boot.Banner
import org.springframework.boot.runApplication
import org.springframework.boot.autoconfigure.SpringBootApplication

@SpringBootApplication
class MyApplication

fun main(args: Array<String>) {
	runApplication<MyApplication>(*args) {
		setBannerMode(Banner.Mode.OFF)
		setAdditionalProfiles("myprofile")
	}
}
```

Since customizations in the `main` method can affect the resulting [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html), it’s possible that you might also want to use the `main` method to create the [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html) used in your tests.
By default, [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html) will not call your `main` method, and instead the class itself is used directly to create the [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html)

If you want to change this behavior, you can change the `useMainMethod` attribute of [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html) to [`SpringBootTest.UseMainMethod.ALWAYS`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.UseMainMethod.html#ALWAYS) or [`SpringBootTest.UseMainMethod.WHEN_AVAILABLE`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.UseMainMethod.html#WHEN_AVAILABLE).
When set to `ALWAYS`, the test will fail if no `main` method can be found.
When set to `WHEN_AVAILABLE` the `main` method will be used if it is available, otherwise the standard loading mechanism will be used.

For example, the following test will invoke the `main` method of `MyApplication` in order to create the [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html).
If the main method sets additional profiles then those will be active when the [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html) starts.

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.SpringBootTest.UseMainMethod;

@SpringBootTest(useMainMethod = UseMainMethod.ALWAYS)
class MyApplicationTests {

	@Test
	void exampleTest() {
		// ...
	}

}
```

```
import org.junit.jupiter.api.Test
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.boot.test.context.SpringBootTest.UseMainMethod

@SpringBootTest(useMainMethod = UseMainMethod.ALWAYS)
class MyApplicationTests {

	@Test
	fun exampleTest() {
		// ...
	}

}
```

## Excluding Test Configuration

If your application uses component scanning (for example, if you use [`@SpringBootApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/SpringBootApplication.html) or [`@ComponentScan`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/ComponentScan.html)), you may find top-level configuration classes that you created only for specific tests accidentally get picked up everywhere.

As we [have seen earlier](#testing.spring-boot-applications.detecting-configuration), [`@TestConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/TestConfiguration.html) can be used on an inner class of a test to customize the primary configuration.
[`@TestConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/TestConfiguration.html) can also be used on a top-level class. Doing so indicates that the class should not be picked up by scanning.
You can then import the class explicitly where it is required, as shown in the following example:

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Import;

@SpringBootTest
@Import(MyTestsConfiguration.class)
class MyTests {

	@Test
	void exampleTest() {
		// ...
	}

}
```

```
import org.junit.jupiter.api.Test
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.context.annotation.Import

@SpringBootTest
@Import(MyTestsConfiguration::class)
class MyTests {

	@Test
	fun exampleTest() {
		// ...
	}

}
```

|  |  |
| --- | --- |
|  | If you directly use [`@ComponentScan`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/ComponentScan.html) (that is, not through [`@SpringBootApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/SpringBootApplication.html)) you need to register the [`TypeExcludeFilter`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/TypeExcludeFilter.html) with it. See the [`TypeExcludeFilter`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/TypeExcludeFilter.html) API documentation for details. |

|  |  |
| --- | --- |
|  | An imported [`@TestConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/TestConfiguration.html) is processed earlier than an inner-class [`@TestConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/TestConfiguration.html) and an imported [`@TestConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/TestConfiguration.html) will be processed before any configuration found through component scanning. Generally speaking, this difference in ordering has no noticeable effect but it is something to be aware of if you’re relying on bean overriding. |

## Using Application Arguments

If your application expects [arguments](../features/spring-application.html#features.spring-application.application-arguments), you can
have [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html) inject them using the `args` attribute.

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.test.context.SpringBootTest;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(args = "--app.test=one")
class MyApplicationArgumentTests {

	@Test
	void applicationArgumentsPopulated(@Autowired ApplicationArguments args) {
		assertThat(args.getOptionNames()).containsOnly("app.test");
		assertThat(args.getOptionValues("app.test")).containsOnly("one");
	}

}
```

```
import org.assertj.core.api.Assertions.assertThat
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.ApplicationArguments
import org.springframework.boot.test.context.SpringBootTest

@SpringBootTest(args = ["--app.test=one"])
class MyApplicationArgumentTests {

	@Test
	fun applicationArgumentsPopulated(@Autowired args: ApplicationArguments) {
		assertThat(args.optionNames).containsOnly("app.test")
		assertThat(args.getOptionValues("app.test")).containsOnly("one")
	}

}
```

## Testing With a Mock Environment

By default, [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html) does not start the server but instead sets up a mock environment for testing web endpoints.

With Spring MVC, we can query our web endpoints using [`MockMvc`](https://docs.spring.io/spring-framework/reference/7.0/testing/mockmvc.html).
The following integrations are available:

* The regular [`MockMvc`](https://docs.spring.io/spring-framework/reference/7.0/testing/mockmvc/hamcrest.html) that uses Hamcrest.
* [`MockMvcTester`](https://docs.spring.io/spring-framework/reference/7.0/testing/mockmvc/assertj.html) that wraps [`MockMvc`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/servlet/MockMvc.html) and uses AssertJ.
* [`RestTestClient`](https://docs.spring.io/spring-framework/reference/7.0/testing/resttestclient.html) where [`MockMvc`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/servlet/MockMvc.html) is plugged in as the server to handle requests with.
* [`WebTestClient`](https://docs.spring.io/spring-framework/reference/7.0/testing/webtestclient.html) where [`MockMvc`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/servlet/MockMvc.html) is plugged in as the server to handle requests with.

The following example showcases the available integrations:

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.resttestclient.autoconfigure.AutoConfigureRestTestClient;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.boot.webtestclient.autoconfigure.AutoConfigureWebTestClient;
import org.springframework.test.web.reactive.server.WebTestClient;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.assertj.MockMvcTester;
import org.springframework.test.web.servlet.client.RestTestClient;
import org.springframework.test.web.servlet.client.RestTestClient.ResponseSpec;
import org.springframework.test.web.servlet.client.assertj.RestTestClientResponse;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@AutoConfigureRestTestClient
@AutoConfigureWebTestClient
class MyMockMvcTests {

	@Test
	void testWithMockMvc(@Autowired MockMvc mvc) throws Exception {
		mvc.perform(get("/"))
				.andExpect(status().isOk())
				.andExpect(content().string("Hello World"));
	}

	@Test // If AssertJ is on the classpath, you can use MockMvcTester
	void testWithMockMvcTester(@Autowired MockMvcTester mvc) {
		assertThat(mvc.get().uri("/"))
				.hasStatusOk()
				.hasBodyTextEqualTo("Hello World");
	}

	@Test
	void testWithRestTestClient(@Autowired RestTestClient restClient) {
		restClient
				.get().uri("/")
				.exchange()
				.expectStatus().isOk()
				.expectBody(String.class).isEqualTo("Hello World");
	}

	@Test // If you prefer AssertJ, dedicated assertions are available
	void testWithRestTestClientAssertJ(@Autowired RestTestClient restClient) {
		ResponseSpec spec = restClient.get().uri("/").exchange();
		RestTestClientResponse response = RestTestClientResponse.from(spec);
		assertThat(response).hasStatusOk()
				.bodyText().isEqualTo("Hello World");
	}

	@Test // If Spring WebFlux is on the classpath
	void testWithWebTestClient(@Autowired WebTestClient webClient) {
		webClient
				.get().uri("/")
				.exchange()
				.expectStatus().isOk()
				.expectBody(String.class).isEqualTo("Hello World");
	}

}
```

```
import org.assertj.core.api.Assertions.assertThat
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.resttestclient.autoconfigure.AutoConfigureRestTestClient
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc
import org.springframework.boot.webtestclient.autoconfigure.AutoConfigureWebTestClient
import org.springframework.test.web.reactive.server.WebTestClient
import org.springframework.test.web.reactive.server.expectBody
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.assertj.MockMvcTester
import org.springframework.test.web.servlet.client.RestTestClient
import org.springframework.test.web.servlet.client.assertj.RestTestClientResponse
import org.springframework.test.web.servlet.client.expectBody
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get
import org.springframework.test.web.servlet.result.MockMvcResultMatchers.content
import org.springframework.test.web.servlet.result.MockMvcResultMatchers.status

@SpringBootTest
@AutoConfigureMockMvc
@AutoConfigureRestTestClient
@AutoConfigureWebTestClient
class MyMockMvcTests {

	@Test
	fun testWithMockMvc(@Autowired mvc: MockMvc) {
		mvc.perform(get("/"))
			.andExpect(status().isOk())
			.andExpect(content().string("Hello World"))
	}

	@Test // If AssertJ is on the classpath, you can use MockMvcTester
	fun testWithMockMvcTester(@Autowired mvc: MockMvcTester) {
		assertThat(mvc.get().uri("/")).hasStatusOk()
			.hasBodyTextEqualTo("Hello World")
	}

	@Test
	fun testWithRestTestClient(@Autowired webClient: RestTestClient) {
		webClient
			.get().uri("/")
			.exchange()
			.expectStatus().isOk
			.expectBody<String>().isEqualTo("Hello World")
	}

	@Test // If you prefer AssertJ, dedicated assertions are available
	fun testWithRestTestClientAssertJ(@Autowired webClient: RestTestClient) {
		val spec = webClient.get().uri("/").exchange()
		val response = RestTestClientResponse.from(spec)
		assertThat(response).hasStatusOk().bodyText().isEqualTo("Hello World")
	}

	@Test // If Spring WebFlux is on the classpath
	fun testWithWebTestClient(@Autowired webClient: WebTestClient) {
		webClient
			.get().uri("/")
			.exchange()
			.expectStatus().isOk
			.expectBody<String>().isEqualTo("Hello World")
	}

}
```

|  |  |
| --- | --- |
|  | If you want to focus only on the web layer and not start a complete [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html), consider [using [`@WebMvcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webmvc/test/autoconfigure/WebMvcTest.html) instead](#testing.spring-boot-applications.spring-mvc-tests). |

With Spring WebFlux endpoints, you can use [`WebTestClient`](https://docs.spring.io/spring-framework/reference/7.0/testing/webtestclient.html) as shown in the following example:

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webtestclient.autoconfigure.AutoConfigureWebTestClient;
import org.springframework.test.web.reactive.server.WebTestClient;

@SpringBootTest
@AutoConfigureWebTestClient
class MyMockWebTestClientTests {

	@Test
	void exampleTest(@Autowired WebTestClient webClient) {
		webClient
			.get().uri("/")
			.exchange()
			.expectStatus().isOk()
			.expectBody(String.class).isEqualTo("Hello World");
	}

}
```

```
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.boot.webtestclient.autoconfigure.AutoConfigureWebTestClient
import org.springframework.test.web.reactive.server.WebTestClient
import org.springframework.test.web.reactive.server.expectBody

@SpringBootTest
@AutoConfigureWebTestClient
class MyMockWebTestClientTests {

	@Test
	fun exampleTest(@Autowired webClient: WebTestClient) {
		webClient
			.get().uri("/")
			.exchange()
			.expectStatus().isOk
			.expectBody<String>().isEqualTo("Hello World")
	}

}
```

|  |  |
| --- | --- |
|  | Testing within a mocked environment is usually faster than running with a full servlet container. However, since mocking occurs at the Spring MVC layer, code that relies on lower-level servlet container behavior cannot be directly tested with MockMvc.  For example, Spring Boot’s error handling is based on the “error page” support provided by the servlet container. This means that, whilst you can test your MVC layer throws and handles exceptions as expected, you cannot directly test that a specific [custom error page](../web/servlet.html#web.servlet.spring-mvc.error-handling.error-pages) is rendered. If you need to test these lower-level concerns, you can start a fully running server as described in the next section. |

## Testing With a Running Server

If you need to start a full running server, we recommend that you use random ports.
If you use `@SpringBootTest(webEnvironment=WebEnvironment.RANDOM_PORT)`, an available port is picked at random each time your test runs.

The [`@LocalServerPort`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/web/server/LocalServerPort.html) annotation can be used to [inject the actual port used](../../how-to/webserver.html#howto.webserver.discover-port) into your test.

Tests that need to make REST calls to the started server can autowire a
[`RestTestClient`](https://docs.spring.io/spring-framework/reference/7.0/testing/resttestclient.html) by annotating the test class with [`@AutoConfigureRestTestClient`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/resttestclient/autoconfigure/AutoConfigureRestTestClient.html).

The configured client resolves relative links to the running server and comes with a dedicated API for verifying responses, as shown in the following example:

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.resttestclient.autoconfigure.AutoConfigureRestTestClient;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment;
import org.springframework.test.web.servlet.client.RestTestClient;

@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureRestTestClient
class MyRandomPortRestTestClientTests {

	@Test
	void exampleTest(@Autowired RestTestClient restClient) {
		restClient
			.get().uri("/")
			.exchange()
			.expectStatus().isOk()
			.expectBody(String.class).isEqualTo("Hello World");
	}

}
```

```
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.resttestclient.autoconfigure.AutoConfigureRestTestClient
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment
import org.springframework.test.web.servlet.client.RestTestClient
import org.springframework.test.web.servlet.client.expectBody

@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureRestTestClient
class MyRandomPortRestTestClientTests {

	@Test
	fun exampleTest(@Autowired webClient: RestTestClient) {
		webClient
			.get().uri("/")
			.exchange()
			.expectStatus().isOk
			.expectBody<String>().isEqualTo("Hello World")
	}

}
```

If you prefer to use AssertJ, dedicated assertions are available from [`RestTestClientResponse`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/servlet/client/assertj/RestTestClientResponse.html), as shown in the following example:

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.resttestclient.autoconfigure.AutoConfigureRestTestClient;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment;
import org.springframework.test.web.servlet.client.RestTestClient;
import org.springframework.test.web.servlet.client.RestTestClient.ResponseSpec;
import org.springframework.test.web.servlet.client.assertj.RestTestClientResponse;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureRestTestClient
class MyRandomPortRestTestClientAssertJTests {

	@Test
	void exampleTest(@Autowired RestTestClient restClient) {
		ResponseSpec spec = restClient.get().uri("/").exchange();
		RestTestClientResponse response = RestTestClientResponse.from(spec);
		assertThat(response).hasStatusOk().bodyText().isEqualTo("Hello World");
	}

}
```

```
import org.assertj.core.api.Assertions.assertThat
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.resttestclient.autoconfigure.AutoConfigureRestTestClient
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment
import org.springframework.test.web.servlet.client.RestTestClient
import org.springframework.test.web.servlet.client.assertj.RestTestClientResponse

@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureRestTestClient
class MyRandomPortRestTestClientAssertJTests {

	@Test
	fun exampleTest(@Autowired webClient: RestTestClient) {
		val exchange = webClient.get().uri("/").exchange()
		val response = RestTestClientResponse.from(exchange)
		assertThat(response).hasStatusOk()
			.bodyText().isEqualTo("Hello World")
	}

}
```

If you have `spring-webflux` on the classpath, you can also autowire a [`WebTestClient`](https://docs.spring.io/spring-framework/reference/7.0/testing/webtestclient.html) by annotating the test class with [`@AutoConfigureWebTestClient`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webtestclient/autoconfigure/AutoConfigureWebTestClient.html).

`WebTestClient` provides a similar API, as shown in the following example:

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment;
import org.springframework.boot.webtestclient.autoconfigure.AutoConfigureWebTestClient;
import org.springframework.test.web.reactive.server.WebTestClient;

@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureWebTestClient
class MyRandomPortWebTestClientTests {

	@Test
	void exampleTest(@Autowired WebTestClient webClient) {
		webClient
			.get().uri("/")
			.exchange()
			.expectStatus().isOk()
			.expectBody(String.class).isEqualTo("Hello World");
	}

}
```

```
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment
import org.springframework.boot.webtestclient.autoconfigure.AutoConfigureWebTestClient
import org.springframework.test.web.reactive.server.WebTestClient
import org.springframework.test.web.reactive.server.expectBody

@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureWebTestClient
class MyRandomPortWebTestClientTests {

	@Test
	fun exampleTest(@Autowired webClient: WebTestClient) {
		webClient
			.get().uri("/")
			.exchange()
			.expectStatus().isOk
			.expectBody<String>().isEqualTo("Hello World")
	}

}
```

|  |  |
| --- | --- |
|  | [`WebTestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/reactive/server/WebTestClient.html) can also be used with a [mock environment](#testing.spring-boot-applications.with-mock-environment), removing the need for a running server, by annotating your test class with [`@AutoConfigureWebTestClient`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webtestclient/autoconfigure/AutoConfigureWebTestClient.html) from `spring-boot-webflux-test`. |

|  |  |
| --- | --- |
|  | For certain [sliced tests](#testing.spring-boot-applications.autoconfigured-tests) you may need to use the [`@AutoConfigureWebServer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/web/server/test/AutoConfigureWebServer.html) annotation to auto-configure an embedded web server. |

The `spring-boot-resttestclient` module also provides a [`TestRestTemplate`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/resttestclient/TestRestTemplate.html) facility:

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.resttestclient.TestRestTemplate;
import org.springframework.boot.resttestclient.autoconfigure.AutoConfigureTestRestTemplate;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureTestRestTemplate
class MyRandomPortTestRestTemplateTests {

	@Test
	void exampleTest(@Autowired TestRestTemplate restTemplate) {
		String body = restTemplate.getForObject("/", String.class);
		assertThat(body).isEqualTo("Hello World");
	}

}
```

```
import org.assertj.core.api.Assertions.assertThat
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment
import org.springframework.boot.resttestclient.TestRestTemplate
import org.springframework.boot.resttestclient.autoconfigure.AutoConfigureTestRestTemplate

@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureTestRestTemplate
class MyRandomPortTestRestTemplateTests {

	@Test
	fun exampleTest(@Autowired restTemplate: TestRestTemplate) {
		val body = restTemplate.getForObject("/", String::class.java)
		assertThat(body).isEqualTo("Hello World")
	}

}
```

To use `TestRestTemplate` a dependency on `spring-boot-restclient` is also required.
Take care when adding this dependency as it will enable auto-configuration for `RestClient.Builder`.
If your main code uses `RestClient.Builder`, declare the `spring-boot-restclient` dependency so that it is on your application’s main classpath and not only on its test classpath.

## Customizing RestTestClient

To customize the [`RestTestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/servlet/client/RestTestClient.html) bean, configure a [`RestTestClientBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/resttestclient/autoconfigure/RestTestClientBuilderCustomizer.html) bean.
Any such beans are called with the [`RestTestClient.Builder`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/servlet/client/RestTestClient.Builder.html) that is used to create the [`RestTestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/servlet/client/RestTestClient.html).

## Customizing WebTestClient

To customize the [`WebTestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/reactive/server/WebTestClient.html) bean, configure a [`WebTestClientBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webtestclient/autoconfigure/WebTestClientBuilderCustomizer.html) bean.
Any such beans are called with the [`WebTestClient.Builder`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/reactive/server/WebTestClient.Builder.html) that is used to create the [`WebTestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/reactive/server/WebTestClient.html).

## Using JMX

As the test context framework caches context, JMX is disabled by default to prevent identical components to register on the same domain.
If such test needs access to an [`MBeanServer`](https://docs.oracle.com/en/java/javase/17/docs/api/java.management/javax/management/MBeanServer.html), consider marking it dirty as well:

* Java
* Kotlin

```
import javax.management.MBeanServer;

import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.DirtiesContext;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(properties = "spring.jmx.enabled=true")
@DirtiesContext
class MyJmxTests {

	@Autowired
	private MBeanServer mBeanServer;

	@Test
	void exampleTest() {
		assertThat(this.mBeanServer.getDomains()).contains("java.lang");
		// ...
	}

}
```

```
import javax.management.MBeanServer

import org.assertj.core.api.Assertions.assertThat
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.test.annotation.DirtiesContext

@SpringBootTest(properties = ["spring.jmx.enabled=true"])
@DirtiesContext
class MyJmxTests(@Autowired val mBeanServer: MBeanServer) {

	@Test
	fun exampleTest() {
		assertThat(mBeanServer.domains).contains("java.lang")
		// ...
	}

}
```

## Using Observations

If you annotate [a sliced test](#testing.spring-boot-applications.autoconfigured-tests) with [`@AutoConfigureTracing`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/micrometer/tracing/test/autoconfigure/AutoConfigureTracing.html) from `spring-boot-micrometer-tracing-test` or with [`@AutoConfigureMetrics`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/micrometer/metrics/test/autoconfigure/AutoConfigureMetrics.html) from `spring-boot-micrometer-metrics-test`, it auto-configures an [`ObservationRegistry`](https://javadoc.io/doc/io.micrometer/micrometer-observation/1.17.0/io/micrometer/observation/ObservationRegistry.html).

## Using Metrics

Regardless of your classpath, meter registries, except the in-memory backed, are not auto-configured when using [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html).

If you need to export metrics to a different backend as part of an integration test, annotate it with [`@AutoConfigureMetrics`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/micrometer/metrics/test/autoconfigure/AutoConfigureMetrics.html).

If you annotate [a sliced test](#testing.spring-boot-applications.autoconfigured-tests) with [`@AutoConfigureMetrics`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/micrometer/metrics/test/autoconfigure/AutoConfigureMetrics.html), it auto-configures an in-memory [`MeterRegistry`](https://javadoc.io/doc/io.micrometer/micrometer-core/1.17.0/io/micrometer/core/instrument/MeterRegistry.html).
Data exporting in sliced tests is not supported with the [`@AutoConfigureMetrics`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/micrometer/metrics/test/autoconfigure/AutoConfigureMetrics.html) annotation.

## Using Tracing

Regardless of your classpath, tracing components which are reporting data are not auto-configured when using [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html).

If you need those components as part of an integration test, annotate the test with [`@AutoConfigureTracing`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/micrometer/tracing/test/autoconfigure/AutoConfigureTracing.html).

If you have created your own reporting components (e.g. a custom [`SpanExporter`](https://javadoc.io/doc/io.opentelemetry/opentelemetry-sdk-trace/1.62.0/io/opentelemetry/sdk/trace/export/SpanExporter.html) or `brave.handler.SpanHandler`) and you don’t want them to be active in tests, you can use the [`@ConditionalOnEnabledTracingExport`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/micrometer/tracing/autoconfigure/ConditionalOnEnabledTracingExport.html) annotation to disable them.

If you annotate [a sliced test](#testing.spring-boot-applications.autoconfigured-tests) with [`@AutoConfigureTracing`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/micrometer/tracing/test/autoconfigure/AutoConfigureTracing.html) , it auto-configures a no-op [`Tracer`](https://javadoc.io/doc/io.micrometer/micrometer-tracing/1.7.0/io/micrometer/tracing/Tracer.html).
Data exporting in sliced tests is not supported with the [`@AutoConfigureTracing`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/micrometer/tracing/test/autoconfigure/AutoConfigureTracing.html) annotation.

## Mocking and Spying Beans

When running tests, it is sometimes necessary to mock certain components within your application context.
For example, you may have a facade over some remote service that is unavailable during development.
Mocking can also be useful when you want to simulate failures that might be hard to trigger in a real environment.

Spring Framework includes a [`@MockitoBean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/context/bean/override/mockito/MockitoBean.html) annotation that can be used to define a Mockito mock for a bean inside your [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html).
Additionally, [`@MockitoSpyBean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/context/bean/override/mockito/MockitoSpyBean.html) can be used to define a Mockito spy.
Learn more about these features in the [Spring Framework documentation](https://docs.spring.io/spring-framework/reference/7.0/testing/annotations/integration-spring/annotation-mockitobean.html).

## Auto-configured Tests

Spring Boot’s auto-configuration system works well for applications but can sometimes be a little too much for tests.
It often helps to load only the parts of the configuration that are required to test a “slice” of your application.
For example, you might want to test that Spring MVC controllers are mapping URLs correctly, and you do not want to involve database calls in those tests, or you might want to test JPA entities, and you are not interested in the web layer when those tests run.

When combined with `spring-boot-test-autoconfigure`, Spring Boot’s [test modules](test-modules.html) include a number of annotations that can be used to automatically configure such “slices”.
Each of them works in a similar way, providing a `@…​Test` annotation that loads the [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html) and one or more `@AutoConfigure…​` annotations that can be used to customize auto-configuration settings.

|  |  |
| --- | --- |
|  | Each slice restricts component scan to appropriate components and loads a very restricted set of auto-configuration classes. If you need to exclude one of them, most `@…​Test` annotations provide an `excludeAutoConfiguration` attribute. Alternatively, you can use `@ImportAutoConfiguration#exclude`. |

|  |  |
| --- | --- |
|  | Including multiple “slices” by using several `@…​Test` annotations in one test is not supported. If you need multiple “slices”, pick one of the `@…​Test` annotations and include the `@AutoConfigure…​` annotations of the other “slices” by hand. |

|  |  |
| --- | --- |
|  | It is also possible to use the `@AutoConfigure…​` annotations with the standard [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html) annotation. You can use this combination if you are not interested in “slicing” your application but you want some of the auto-configured test beans. |

## Auto-configured JSON Tests

To test that object JSON serialization and deserialization is working as expected, you can use the [`@JsonTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/autoconfigure/json/JsonTest.html) annotation from the `spring-boot-test-autoconfigure` module.
[`@JsonTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/autoconfigure/json/JsonTest.html) auto-configures the available supported JSON mapper, which can be one of the following libraries:

* Jackson [`JsonMapper`](https://javadoc.io/doc/tools.jackson.core/jackson-databind/3.1.4/tools/jackson/databind/json/JsonMapper.html), any [`@JacksonComponent`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jackson/JacksonComponent.html) beans and any Jackson [`JacksonModule`](https://javadoc.io/doc/tools.jackson.core/jackson-databind/3.1.4/tools/jackson/databind/JacksonModule.html)
* Jackson 2 (deprecated) [`ObjectMapper`](https://javadoc.io/doc/com.fasterxml.jackson.core/jackson-databind/2.21.4/com/fasterxml/jackson/databind/ObjectMapper.html), any [`@JsonComponent`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jackson2/JsonComponent.html) beans and any Jackson [`Module`](https://javadoc.io/doc/com.fasterxml.jackson.core/jackson-databind/2.21.4/com/fasterxml/jackson/databind/Module.html)
* `Gson`
* `Jsonb`

|  |  |
| --- | --- |
|  | A list of the auto-configurations that are enabled by [`@JsonTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/autoconfigure/json/JsonTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

If you need to configure elements of the auto-configuration, you can use the [`@AutoConfigureJsonTesters`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/autoconfigure/json/AutoConfigureJsonTesters.html) annotation.

Spring Boot includes AssertJ-based helpers that work with the JSONAssert and JsonPath libraries to check that JSON appears as expected.
The [`JacksonTester`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/json/JacksonTester.html), [`GsonTester`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/json/GsonTester.html), [`JsonbTester`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/json/JsonbTester.html), and [`BasicJsonTester`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/json/BasicJsonTester.html) classes can be used for Jackson, Gson, Jsonb, and Strings respectively.
Any helper fields on the test class can be [`@Autowired`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/beans/factory/annotation/Autowired.html) when using [`@JsonTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/autoconfigure/json/JsonTest.html).
The following example shows a test class for Jackson:

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.json.JsonTest;
import org.springframework.boot.test.json.JacksonTester;

import static org.assertj.core.api.Assertions.assertThat;

@JsonTest
class MyJsonTests {

	@Autowired
	private JacksonTester<VehicleDetails> json;

	@Test
	void serialize() throws Exception {
		VehicleDetails details = new VehicleDetails("Honda", "Civic");
		// Assert against a `.json` file in the same package as the test
		assertThat(this.json.write(details)).isEqualToJson("expected.json");
		// Or use JSON path based assertions
		assertThat(this.json.write(details)).hasJsonPathStringValue("@.make");
		assertThat(this.json.write(details)).extractingJsonPathStringValue("@.make").isEqualTo("Honda");
	}

	@Test
	void deserialize() throws Exception {
		String content = "{\"make\":\"Ford\",\"model\":\"Focus\"}";
		assertThat(this.json.parse(content)).isEqualTo(new VehicleDetails("Ford", "Focus"));
		assertThat(this.json.parseObject(content).getMake()).isEqualTo("Ford");
	}

}
```

```
import org.assertj.core.api.Assertions.assertThat
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.json.JsonTest
import org.springframework.boot.test.json.JacksonTester

@JsonTest
class MyJsonTests(@Autowired val json: JacksonTester<VehicleDetails>) {

	@Test
	fun serialize() {
		val details = VehicleDetails("Honda", "Civic")
		// Assert against a `.json` file in the same package as the test
		assertThat(json.write(details)).isEqualToJson("expected.json")
		// Or use JSON path based assertions
		assertThat(json.write(details)).hasJsonPathStringValue("@.make")
		assertThat(json.write(details)).extractingJsonPathStringValue("@.make").isEqualTo("Honda")
	}

	@Test
	fun deserialize() {
		val content = "{\"make\":\"Ford\",\"model\":\"Focus\"}"
		assertThat(json.parse(content)).isEqualTo(VehicleDetails("Ford", "Focus"))
		assertThat(json.parseObject(content).make).isEqualTo("Ford")
	}

}
```

|  |  |
| --- | --- |
|  | JSON helper classes can also be used directly in standard unit tests. To do so, call the `initFields` method of the helper in your [`@BeforeEach`](https://junit.org/junit5/docs/6.0.3/api/org.junit.jupiter.api/org/junit/jupiter/api/BeforeEach.html) method if you do not use [`@JsonTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/autoconfigure/json/JsonTest.html). |

If you use Spring Boot’s AssertJ-based helpers to assert on a number value at a given JSON path, you might not be able to use `isEqualTo` depending on the type.
Instead, you can use AssertJ’s `satisfies` to assert that the value matches the given condition.
For instance, the following example asserts that the actual number is a float value close to `0.15` within an offset of `0.01`.

* Java
* Kotlin

```
	@Test
	void someTest() throws Exception {
		SomeObject value = new SomeObject(0.152f);
		assertThat(this.json.write(value)).extractingJsonPathNumberValue("@.test.numberValue")
			.satisfies((number) -> assertThat(number.floatValue()).isCloseTo(0.15f, within(0.01f)));
	}
```

```
	@Test
	fun someTest() {
		val value = SomeObject(0.152f)
		assertThat(json.write(value)).extractingJsonPathNumberValue("@.test.numberValue")
			.satisfies(ThrowingConsumer { number ->
				assertThat(number.toFloat()).isCloseTo(0.15f, within(0.01f))
			})
	}
```

## Auto-configured Spring MVC Tests

To test whether Spring MVC controllers are working as expected, use the [`@WebMvcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webmvc/test/autoconfigure/WebMvcTest.html) annotation from the `spring-boot-webmvc-test` module.
[`@WebMvcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webmvc/test/autoconfigure/WebMvcTest.html) auto-configures the Spring MVC infrastructure and limits scanned beans to [`@Controller`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Controller.html), [`@ControllerAdvice`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/bind/annotation/ControllerAdvice.html), [`@JacksonComponent`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jackson/JacksonComponent.html), [`@JsonComponent`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jackson2/JsonComponent.html) (deprecated), [`Converter`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/convert/converter/Converter.html), [`GenericConverter`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/convert/converter/GenericConverter.html), [`Filter`](https://jakarta.ee/specifications/servlet/6.1/apidocs/jakarta.servlet/jakarta/servlet/Filter.html), [`HandlerInterceptor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/servlet/HandlerInterceptor.html), [`WebMvcConfigurer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/servlet/config/annotation/WebMvcConfigurer.html), [`WebMvcRegistrations`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webmvc/autoconfigure/WebMvcRegistrations.html), and [`HandlerMethodArgumentResolver`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/method/support/HandlerMethodArgumentResolver.html).
Regular [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html) and [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans are not scanned when the [`@WebMvcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webmvc/test/autoconfigure/WebMvcTest.html) annotation is used.
[`@EnableConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/EnableConfigurationProperties.html) can be used to include [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans.

|  |  |
| --- | --- |
|  | A list of the auto-configuration settings that are enabled by [`@WebMvcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webmvc/test/autoconfigure/WebMvcTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

|  |  |
| --- | --- |
|  | If you need to register extra components, such as a [`JacksonModule`](https://javadoc.io/doc/tools.jackson.core/jackson-databind/3.1.4/tools/jackson/databind/JacksonModule.html), you can import additional configuration classes by using [`@Import`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Import.html) on your test. |

Often, [`@WebMvcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webmvc/test/autoconfigure/WebMvcTest.html) is limited to a single controller and is used in combination with [`@MockitoBean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/context/bean/override/mockito/MockitoBean.html) to provide mock implementations for required collaborators.

[`@WebMvcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webmvc/test/autoconfigure/WebMvcTest.html) also auto-configures [`MockMvc`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/servlet/MockMvc.html).
Mock MVC offers a powerful way to quickly test MVC controllers without needing to start a full HTTP server.
If AssertJ is available, the AssertJ support provided by [`MockMvcTester`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/servlet/assertj/MockMvcTester.html) is auto-configured as well.
If you’d like to use [`RestTestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/servlet/client/RestTestClient.html) in your tests, annotate your test class with [`@AutoConfigureRestTestClient`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/resttestclient/autoconfigure/AutoConfigureRestTestClient.html).
A `RestTestClient` that uses the Mock MVC infrastructure will then be auto-configured.

|  |  |
| --- | --- |
|  | You can also auto-configure [`MockMvc`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/servlet/MockMvc.html) and [`MockMvcTester`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/servlet/assertj/MockMvcTester.html) in a non-`@WebMvcTest` (such as [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html)) by annotating it with [`@AutoConfigureMockMvc`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webmvc/test/autoconfigure/AutoConfigureMockMvc.html). The following example uses [`MockMvcTester`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/servlet/assertj/MockMvcTester.html): |

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.assertj.MockMvcTester;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.BDDMockito.given;

@WebMvcTest(UserVehicleController.class)
class MyControllerTests {

	@Autowired
	private MockMvcTester mvc;

	@MockitoBean
	private UserVehicleService userVehicleService;

	@Test
	void testExample() {
		given(this.userVehicleService.getVehicleDetails("sboot"))
			.willReturn(new VehicleDetails("Honda", "Civic"));
		assertThat(this.mvc.get().uri("/sboot/vehicle").accept(MediaType.TEXT_PLAIN))
			.hasStatusOk()
			.hasBodyTextEqualTo("Honda Civic");
	}

}
```

```
import org.assertj.core.api.Assertions.assertThat
import org.junit.jupiter.api.Test
import org.mockito.BDDMockito.given
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest
import org.springframework.http.MediaType
import org.springframework.test.context.bean.override.mockito.MockitoBean
import org.springframework.test.web.servlet.assertj.MockMvcTester

@WebMvcTest(UserVehicleController::class)
class MyControllerTests(@Autowired val mvc: MockMvcTester) {

	@MockitoBean
	lateinit var userVehicleService: UserVehicleService

	@Test
	fun testExample() {
		given(userVehicleService.getVehicleDetails("sboot"))
				.willReturn(VehicleDetails("Honda", "Civic"))
		assertThat(mvc.get().uri("/sboot/vehicle").accept(MediaType.TEXT_PLAIN))
				.hasStatusOk().hasBodyTextEqualTo("Honda Civic")
	}

}
```

|  |  |
| --- | --- |
|  | If you need to configure elements of the auto-configuration (for example, when servlet filters should be applied) you can use attributes in the [`@AutoConfigureMockMvc`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webmvc/test/autoconfigure/AutoConfigureMockMvc.html) annotation. |

If you use HtmlUnit and Selenium, auto-configuration also provides an HtmlUnit [`WebClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/WebClient.html) bean and/or a Selenium [`WebDriver`](https://www.selenium.dev/selenium/docs/api/java/org/openqa/selenium/WebDriver.html) bean.
The following example uses HtmlUnit:

* Java
* Kotlin

```
import org.htmlunit.WebClient;
import org.htmlunit.html.HtmlPage;
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.BDDMockito.given;

@WebMvcTest(UserVehicleController.class)
class MyHtmlUnitTests {

	@Autowired
	private WebClient webClient;

	@MockitoBean
	private UserVehicleService userVehicleService;

	@Test
	void testExample() throws Exception {
		given(this.userVehicleService.getVehicleDetails("sboot")).willReturn(new VehicleDetails("Honda", "Civic"));
		HtmlPage page = this.webClient.getPage("/sboot/vehicle.html");
		assertThat(page.getBody().getTextContent()).isEqualTo("Honda Civic");
	}

}
```

```
import org.assertj.core.api.Assertions.assertThat
import org.htmlunit.WebClient
import org.htmlunit.html.HtmlPage
import org.junit.jupiter.api.Test
import org.mockito.BDDMockito.given
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest
import org.springframework.test.context.bean.override.mockito.MockitoBean

@WebMvcTest(UserVehicleController::class)
class MyHtmlUnitTests(@Autowired val webClient: WebClient) {

	@MockitoBean
	lateinit var userVehicleService: UserVehicleService

	@Test
	fun testExample() {
		given(userVehicleService.getVehicleDetails("sboot")).willReturn(VehicleDetails("Honda", "Civic"))
		val page = webClient.getPage<HtmlPage>("/sboot/vehicle.html")
		assertThat(page.body.textContent).isEqualTo("Honda Civic")
	}

}
```

|  |  |
| --- | --- |
|  | By default, Spring Boot puts [`WebDriver`](https://www.selenium.dev/selenium/docs/api/java/org/openqa/selenium/WebDriver.html) beans in a special “scope” to ensure that the driver exits after each test and that a new instance is injected. If you do not want this behavior, you can add `@Scope(ConfigurableBeanFactory.SCOPE_SINGLETON)` to your [`WebDriver`](https://www.selenium.dev/selenium/docs/api/java/org/openqa/selenium/WebDriver.html) [`@Bean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Bean.html) definition. |

|  |  |
| --- | --- |
|  | The `webDriver` scope created by Spring Boot will replace any user defined scope of the same name. If you define your own `webDriver` scope you may find it stops working when you use [`@WebMvcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webmvc/test/autoconfigure/WebMvcTest.html). |

If you have Spring Security on the classpath, [`@WebMvcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webmvc/test/autoconfigure/WebMvcTest.html) will also scan [`WebSecurityConfigurer`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/config/annotation/web/WebSecurityConfigurer.html) beans.
Instead of disabling security completely for such tests, you can use Spring Security’s test support.
More details on how to use Spring Security’s [`MockMvc`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/servlet/MockMvc.html) support can be found in this [Testing With Spring Security](../../how-to/testing.html#howto.testing.with-spring-security) “How-to Guides” section.

|  |  |
| --- | --- |
|  | Sometimes writing Spring MVC tests is not enough; Spring Boot can help you run [full end-to-end tests with an actual server](#testing.spring-boot-applications.with-running-server). |

## Auto-configured Spring WebFlux Tests

To test that [Spring WebFlux](https://docs.spring.io/spring-framework/reference/7.0/web-reactive.html) controllers are working as expected, you can use the [`@WebFluxTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webflux/test/autoconfigure/WebFluxTest.html) annotation from the `spring-boot-webflux-test` module.
[`@WebFluxTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webflux/test/autoconfigure/WebFluxTest.html) auto-configures the Spring WebFlux infrastructure and limits scanned beans to [`@Controller`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Controller.html), [`@ControllerAdvice`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/bind/annotation/ControllerAdvice.html), [`@JacksonComponent`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jackson/JacksonComponent.html), [`@JsonComponent`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jackson2/JsonComponent.html) (deprecated), [`Converter`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/convert/converter/Converter.html), [`GenericConverter`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/convert/converter/GenericConverter.html) and [`WebFluxConfigurer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/config/WebFluxConfigurer.html).
Regular [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html) and [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans are not scanned when the [`@WebFluxTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webflux/test/autoconfigure/WebFluxTest.html) annotation is used.
[`@EnableConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/EnableConfigurationProperties.html) can be used to include [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans.

|  |  |
| --- | --- |
|  | A list of the auto-configurations that are enabled by [`@WebFluxTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webflux/test/autoconfigure/WebFluxTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

|  |  |
| --- | --- |
|  | If you need to register extra components, such as a [`JacksonModule`](https://javadoc.io/doc/tools.jackson.core/jackson-databind/3.1.4/tools/jackson/databind/JacksonModule.html), you can import additional configuration classes using [`@Import`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Import.html) on your test. |

Often, [`@WebFluxTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webflux/test/autoconfigure/WebFluxTest.html) is limited to a single controller and used in combination with the [`@MockitoBean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/context/bean/override/mockito/MockitoBean.html) annotation to provide mock implementations for required collaborators.

[`@WebFluxTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webflux/test/autoconfigure/WebFluxTest.html) also auto-configures [`WebTestClient`](https://docs.spring.io/spring-framework/reference/7.0/testing/webtestclient.html), which offers a powerful way to quickly test WebFlux controllers without needing to start a full HTTP server.

|  |  |
| --- | --- |
|  | You can also auto-configure [`WebTestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/reactive/server/WebTestClient.html) in a non-`@WebFluxTest` (such as [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html)) by annotating it with [`@AutoConfigureWebTestClient`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webtestclient/autoconfigure/AutoConfigureWebTestClient.html). |

The following example shows a class that uses both [`@WebFluxTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webflux/test/autoconfigure/WebFluxTest.html) and a [`WebTestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/reactive/server/WebTestClient.html):

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webflux.test.autoconfigure.WebFluxTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.reactive.server.WebTestClient;

import static org.mockito.BDDMockito.given;

@WebFluxTest(UserVehicleController.class)
class MyControllerTests {

	@Autowired
	private WebTestClient webClient;

	@MockitoBean
	private UserVehicleService userVehicleService;

	@Test
	void testExample() {
		given(this.userVehicleService.getVehicleDetails("sboot"))
			.willReturn(new VehicleDetails("Honda", "Civic"));
		this.webClient.get().uri("/sboot/vehicle").accept(MediaType.TEXT_PLAIN).exchange()
			.expectStatus().isOk()
			.expectBody(String.class).isEqualTo("Honda Civic");
	}

}
```

```
import org.junit.jupiter.api.Test
import org.mockito.BDDMockito.given
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.webflux.test.autoconfigure.WebFluxTest
import org.springframework.http.MediaType
import org.springframework.test.context.bean.override.mockito.MockitoBean
import org.springframework.test.web.reactive.server.WebTestClient
import org.springframework.test.web.reactive.server.expectBody

@WebFluxTest(UserVehicleController::class)
class MyControllerTests(@Autowired val webClient: WebTestClient) {

	@MockitoBean
	lateinit var userVehicleService: UserVehicleService

	@Test
	fun testExample() {
		given(userVehicleService.getVehicleDetails("sboot"))
			.willReturn(VehicleDetails("Honda", "Civic"))
		webClient.get().uri("/sboot/vehicle").accept(MediaType.TEXT_PLAIN).exchange()
			.expectStatus().isOk
			.expectBody<String>().isEqualTo("Honda Civic")
	}

}
```

|  |  |
| --- | --- |
|  | This setup is only supported by WebFlux applications as using [`WebTestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/reactive/server/WebTestClient.html) in a mocked web application only works with WebFlux at the moment. |

|  |  |
| --- | --- |
|  | [`@WebFluxTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webflux/test/autoconfigure/WebFluxTest.html) cannot detect routes registered through the functional web framework. For testing [`RouterFunction`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/server/RouterFunction.html) beans in the context, consider importing your [`RouterFunction`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/server/RouterFunction.html) yourself by using [`@Import`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Import.html) or by using [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html). |

|  |  |
| --- | --- |
|  | [`@WebFluxTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webflux/test/autoconfigure/WebFluxTest.html) cannot detect custom security configuration registered as a [`@Bean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Bean.html) of type [`SecurityWebFilterChain`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/web/server/SecurityWebFilterChain.html). To include that in your test, you will need to import the configuration that registers the bean by using [`@Import`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Import.html) or by using [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html). |

|  |  |
| --- | --- |
|  | Sometimes writing Spring WebFlux tests is not enough; Spring Boot can help you run [full end-to-end tests with an actual server](#testing.spring-boot-applications.with-running-server). |

## Auto-configured Spring GraphQL Tests

Spring GraphQL offers a dedicated testing support module; you’ll need to add it to your project:

Maven

```
<dependencies>
	<dependency>
		<groupId>org.springframework.graphql</groupId>
		<artifactId>spring-graphql-test</artifactId>
		<scope>test</scope>
	</dependency>
	<!-- Unless already present in the compile scope -->
	<dependency>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-webflux</artifactId>
		<scope>test</scope>
	</dependency>
</dependencies>
```

Gradle

```
dependencies {
	testImplementation("org.springframework.graphql:spring-graphql-test")
	// Unless already present in the implementation configuration
	testImplementation("org.springframework.boot:spring-boot-starter-webflux")
}
```

This testing module ships the [GraphQlTester](https://docs.spring.io/spring-graphql/reference/2.0/testing.html#testing.graphqltester).
The tester is heavily used in test, so be sure to become familiar with using it.
There are [`GraphQlTester`](https://docs.spring.io/spring-graphql/docs/2.0.x/api/org/springframework/graphql/test/tester/GraphQlTester.html) variants and Spring Boot will auto-configure them depending on the type of tests:

* the [`ExecutionGraphQlServiceTester`](https://docs.spring.io/spring-graphql/docs/2.0.x/api/org/springframework/graphql/test/tester/ExecutionGraphQlServiceTester.html) performs tests on the server side, without a client nor a transport
* the [`HttpGraphQlTester`](https://docs.spring.io/spring-graphql/docs/2.0.x/api/org/springframework/graphql/test/tester/HttpGraphQlTester.html) performs tests with a client that connects to a server, with or without a live server

Spring Boot helps you to test your [Spring GraphQL Controllers](https://docs.spring.io/spring-graphql/reference/2.0/controllers.html) with the [`@GraphQlTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/graphql/test/autoconfigure/GraphQlTest.html) annotation from the `spring-boot-graphql-test` module.
[`@GraphQlTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/graphql/test/autoconfigure/GraphQlTest.html) auto-configures the Spring GraphQL infrastructure, without any transport nor server being involved.
This limits scanned beans to [`@Controller`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Controller.html), [`@ControllerAdvice`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/bind/annotation/ControllerAdvice.html), [`RuntimeWiringConfigurer`](https://docs.spring.io/spring-graphql/docs/2.0.x/api/org/springframework/graphql/execution/RuntimeWiringConfigurer.html), [`JacksonComponent`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jackson/JacksonComponent.html), [`@JsonComponent`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jackson2/JsonComponent.html) (deprecated), [`Converter`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/convert/converter/Converter.html), [`GenericConverter`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/convert/converter/GenericConverter.html), [`DataFetcherExceptionResolver`](https://docs.spring.io/spring-graphql/docs/2.0.x/api/org/springframework/graphql/execution/DataFetcherExceptionResolver.html), [`Instrumentation`](https://javadoc.io/doc/com.graphql-java/graphql-java/25.0/graphql/execution/instrumentation/Instrumentation.html) and [`GraphQlSourceBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/graphql/autoconfigure/GraphQlSourceBuilderCustomizer.html).
Regular [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html) and [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans are not scanned when the [`@GraphQlTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/graphql/test/autoconfigure/GraphQlTest.html) annotation is used.
[`@EnableConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/EnableConfigurationProperties.html) can be used to include [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans.

|  |  |
| --- | --- |
|  | A list of the auto-configurations that are enabled by [`@GraphQlTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/graphql/test/autoconfigure/GraphQlTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

Often, [`@GraphQlTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/graphql/test/autoconfigure/GraphQlTest.html) is limited to a set of controllers and used in combination with the [`@MockitoBean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/context/bean/override/mockito/MockitoBean.html) annotation to provide mock implementations for required collaborators.

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.docs.web.graphql.runtimewiring.GreetingController;
import org.springframework.boot.graphql.test.autoconfigure.GraphQlTest;
import org.springframework.graphql.test.tester.GraphQlTester;

@GraphQlTest(GreetingController.class)
class GreetingControllerTests {

	@Autowired
	private GraphQlTester graphQlTester;

	@Test
	void shouldGreetWithSpecificName() {
		this.graphQlTester.document("{ greeting(name: \"Alice\") } ")
			.execute()
			.path("greeting")
			.entity(String.class)
			.isEqualTo("Hello, Alice!");
	}

	@Test
	void shouldGreetWithDefaultName() {
		this.graphQlTester.document("{ greeting } ")
			.execute()
			.path("greeting")
			.entity(String.class)
			.isEqualTo("Hello, Spring!");
	}

}
```

```
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.docs.web.graphql.runtimewiring.GreetingController
import org.springframework.boot.graphql.test.autoconfigure.GraphQlTest
import org.springframework.graphql.test.tester.GraphQlTester

@GraphQlTest(GreetingController::class)
internal class GreetingControllerTests {

	@Autowired
	lateinit var graphQlTester: GraphQlTester

	@Test
	fun shouldGreetWithSpecificName() {
		graphQlTester.document("{ greeting(name: \"Alice\") } ").execute().path("greeting").entity(String::class.java)
				.isEqualTo("Hello, Alice!")
	}

	@Test
	fun shouldGreetWithDefaultName() {
		graphQlTester.document("{ greeting } ").execute().path("greeting").entity(String::class.java)
				.isEqualTo("Hello, Spring!")
	}

}
```

[`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html) tests are full integration tests and involve the entire application.
A [`HttpGraphQlTester`](https://docs.spring.io/spring-graphql/docs/2.0.x/api/org/springframework/graphql/test/tester/HttpGraphQlTester.html) bean can be added by annotating your test class with [`@AutoConfigureHttpGraphQlTester`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/graphql/test/autoconfigure/tester/AutoConfigureHttpGraphQlTester.html) from the `spring-boot-graphql-test` module:

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.graphql.test.autoconfigure.tester.AutoConfigureHttpGraphQlTester;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment;
import org.springframework.graphql.test.tester.HttpGraphQlTester;

@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureHttpGraphQlTester
class GraphQlIntegrationTests {

	@Test
	void shouldGreetWithSpecificName(@Autowired HttpGraphQlTester graphQlTester) {
		HttpGraphQlTester authenticatedTester = graphQlTester.mutate()
			.webTestClient((client) -> client.defaultHeaders((headers) -> headers.setBasicAuth("admin", "ilovespring")))
			.build();
		authenticatedTester.document("{ greeting(name: \"Alice\") } ")
			.execute()
			.path("greeting")
			.entity(String.class)
			.isEqualTo("Hello, Alice!");
	}

}
```

```
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.graphql.test.autoconfigure.tester.AutoConfigureHttpGraphQlTester
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment
import org.springframework.graphql.test.tester.HttpGraphQlTester
import org.springframework.http.HttpHeaders
import org.springframework.test.web.reactive.server.WebTestClient

@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@AutoConfigureHttpGraphQlTester
class GraphQlIntegrationTests {

	@Test
	fun shouldGreetWithSpecificName(@Autowired graphQlTester: HttpGraphQlTester) {
		val authenticatedTester = graphQlTester.mutate()
			.webTestClient { client: WebTestClient.Builder ->
				client.defaultHeaders { headers: HttpHeaders ->
					headers.setBasicAuth("admin", "ilovespring")
				}
			}.build()
		authenticatedTester.document("{ greeting(name: \"Alice\") } ").execute()
			.path("greeting").entity(String::class.java).isEqualTo("Hello, Alice!")
	}
}
```

The [`HttpGraphQlTester`](https://docs.spring.io/spring-graphql/docs/2.0.x/api/org/springframework/graphql/test/tester/HttpGraphQlTester.html) bean uses the relevant transport of the integration test.
When using a random or defined port, the tester is configured against the live server.
To bind the tester to `MockMvc`, make sure to annotate your test class with [`@AutoConfigureMockMvc`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webmvc/test/autoconfigure/AutoConfigureMockMvc.html).

## Auto-configured Data Cassandra Tests

You can use [`@DataCassandraTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/cassandra/test/autoconfigure/DataCassandraTest.html) from the `spring-boot-data-cassandra-test` module to test Data Cassandra applications.
By default, it configures a [`CassandraTemplate`](https://docs.spring.io/spring-data/cassandra/docs/5.1.x/api/org/springframework/data/cassandra/core/CassandraTemplate.html), scans for [`@Table`](https://docs.spring.io/spring-data/cassandra/docs/5.1.x/api/org/springframework/data/cassandra/core/mapping/Table.html) classes, and configures Spring Data Cassandra repositories.
Regular [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html) and [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans are not scanned when the [`@DataCassandraTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/cassandra/test/autoconfigure/DataCassandraTest.html) annotation is used.
[`@EnableConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/EnableConfigurationProperties.html) can be used to include [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans.
(For more about using Cassandra with Spring Boot, see [Cassandra](../data/nosql.html#data.nosql.cassandra).)

|  |  |
| --- | --- |
|  | A list of the auto-configuration settings that are enabled by [`@DataCassandraTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/cassandra/test/autoconfigure/DataCassandraTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

The following example shows a typical setup for using Cassandra tests in Spring Boot:

* Java
* Kotlin

```
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.cassandra.test.autoconfigure.DataCassandraTest;

@DataCassandraTest
class MyDataCassandraTests {

	@Autowired
	private SomeRepository repository;

}
```

```
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.data.cassandra.test.autoconfigure.DataCassandraTest

@DataCassandraTest
class MyDataCassandraTests(@Autowired val repository: SomeRepository)
```

## Auto-configured Data Couchbase Tests

You can use [`@DataCouchbaseTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/couchbase/test/autoconfigure/DataCouchbaseTest.html) from the `spring-boot-data-couchbase-test` module to test Data Couchbase applications.
By default, it configures a [`CouchbaseTemplate`](https://docs.spring.io/spring-data/couchbase/docs/6.1.x/api/org/springframework/data/couchbase/core/CouchbaseTemplate.html) or [`ReactiveCouchbaseTemplate`](https://docs.spring.io/spring-data/couchbase/docs/6.1.x/api/org/springframework/data/couchbase/core/ReactiveCouchbaseTemplate.html), scans for [`@Document`](https://docs.spring.io/spring-data/couchbase/docs/6.1.x/api/org/springframework/data/couchbase/core/mapping/Document.html) classes, and configures Spring Data Couchbase repositories.
Regular [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html) and [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans are not scanned when the [`@DataCouchbaseTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/couchbase/test/autoconfigure/DataCouchbaseTest.html) annotation is used.
[`@EnableConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/EnableConfigurationProperties.html) can be used to include [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans.
(For more about using Couchbase with Spring Boot, see [Couchbase](../data/nosql.html#data.nosql.couchbase), earlier in this chapter.)

|  |  |
| --- | --- |
|  | A list of the auto-configuration settings that are enabled by [`@DataCouchbaseTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/couchbase/test/autoconfigure/DataCouchbaseTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

The following example shows a typical setup for using Couchbase tests in Spring Boot:

* Java
* Kotlin

```
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.couchbase.test.autoconfigure.DataCouchbaseTest;

@DataCouchbaseTest
class MyDataCouchbaseTests {

	@Autowired
	private SomeRepository repository;

	// ...

}
```

```
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.data.couchbase.test.autoconfigure.DataCouchbaseTest

@DataCouchbaseTest
class MyDataCouchbaseTests(@Autowired val repository: SomeRepository) {

	// ...

}
```

## Auto-configured Data Elasticsearch Tests

You can use [`@DataElasticsearchTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/elasticsearch/test/autoconfigure/DataElasticsearchTest.html) from the `spring-boot-data-elasticsearch-test` module to test Data Elasticsearch applications.
By default, it configures an [`ElasticsearchTemplate`](https://docs.spring.io/spring-data/elasticsearch/docs/6.1.x/api/org/springframework/data/elasticsearch/client/elc/ElasticsearchTemplate.html), scans for [`@Document`](https://docs.spring.io/spring-data/elasticsearch/docs/6.1.x/api/org/springframework/data/elasticsearch/annotations/Document.html) classes, and configures Spring Data Elasticsearch repositories.
Regular [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html) and [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans are not scanned when the [`@DataElasticsearchTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/elasticsearch/test/autoconfigure/DataElasticsearchTest.html) annotation is used.
[`@EnableConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/EnableConfigurationProperties.html) can be used to include [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans.
(For more about using Elasticsearch with Spring Boot, see [Elasticsearch](../data/nosql.html#data.nosql.elasticsearch), earlier in this chapter.)

|  |  |
| --- | --- |
|  | A list of the auto-configuration settings that are enabled by [`@DataElasticsearchTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/elasticsearch/test/autoconfigure/DataElasticsearchTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

The following example shows a typical setup for using Elasticsearch tests in Spring Boot:

* Java
* Kotlin

```
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.elasticsearch.test.autoconfigure.DataElasticsearchTest;

@DataElasticsearchTest
class MyDataElasticsearchTests {

	@Autowired
	private SomeRepository repository;

	// ...

}
```

```
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.data.elasticsearch.test.autoconfigure.DataElasticsearchTest

@DataElasticsearchTest
class MyDataElasticsearchTests(@Autowired val repository: SomeRepository) {

	// ...

}
```

## Auto-configured Data JPA Tests

You can use the [`@DataJpaTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/jpa/test/autoconfigure/DataJpaTest.html) annotation from the `spring-boot-data-jpa-test` module to test Data JPA applications.
By default, it scans for [`@Entity`](https://jakarta.ee/specifications/persistence/3.2/apidocs/jakarta.persistence/jakarta/persistence/Entity.html) classes and configures Spring Data JPA repositories.
If an embedded database is available on the classpath, it configures one as well.
SQL queries are logged by default by setting the `spring.jpa.show-sql` property to `true`.
This can be disabled using the `showSql` attribute of the annotation.

Regular [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html) and [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans are not scanned when the [`@DataJpaTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/jpa/test/autoconfigure/DataJpaTest.html) annotation is used.
[`@EnableConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/EnableConfigurationProperties.html) can be used to include [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans.

|  |  |
| --- | --- |
|  | A list of the auto-configuration settings that are enabled by [`@DataJpaTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/jpa/test/autoconfigure/DataJpaTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

By default, data JPA tests are transactional and roll back at the end of each test.
See the [relevant section](https://docs.spring.io/spring-framework/reference/7.0/testing/testcontext-framework/tx.html#testcontext-tx-enabling-transactions) in the Spring Framework Reference Documentation for more details.
If that is not what you want, you can disable transaction management for a test or for the whole class as follows:

* Java
* Kotlin

```
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

@DataJpaTest
@Transactional(propagation = Propagation.NOT_SUPPORTED)
class MyNonTransactionalTests {

	// ...

}
```

```
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest
import org.springframework.transaction.annotation.Propagation
import org.springframework.transaction.annotation.Transactional

@DataJpaTest
@Transactional(propagation = Propagation.NOT_SUPPORTED)
class MyNonTransactionalTests {

	// ...

}
```

Data JPA tests may also inject a [`TestEntityManager`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jpa/test/autoconfigure/TestEntityManager.html) bean, which provides an alternative to the standard JPA [`EntityManager`](https://jakarta.ee/specifications/persistence/3.2/apidocs/jakarta.persistence/jakarta/persistence/EntityManager.html) that is specifically designed for tests.

|  |  |
| --- | --- |
|  | [`TestEntityManager`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jpa/test/autoconfigure/TestEntityManager.html) can also be auto-configured to any of your Spring-based test class by adding [`@AutoConfigureTestEntityManager`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jpa/test/autoconfigure/AutoConfigureTestEntityManager.html). When doing so, make sure that your test is running in a transaction, for instance by adding [`@Transactional`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/transaction/annotation/Transactional.html) on your test class or method. |

A [`JdbcTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jdbc/core/JdbcTemplate.html) is also available if you need that.
The following example shows the [`@DataJpaTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/jpa/test/autoconfigure/DataJpaTest.html) annotation in use:

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import org.springframework.boot.jpa.test.autoconfigure.TestEntityManager;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
class MyRepositoryTests {

	@Autowired
	private TestEntityManager entityManager;

	@Autowired
	private UserRepository repository;

	@Test
	void testExample() {
		this.entityManager.persist(new User("sboot", "1234"));
		User user = this.repository.findByUsername("sboot");
		assertThat(user.getUsername()).isEqualTo("sboot");
		assertThat(user.getEmployeeNumber()).isEqualTo("1234");
	}

}
```

```
import org.assertj.core.api.Assertions.assertThat
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest
import org.springframework.boot.jpa.test.autoconfigure.TestEntityManager

@DataJpaTest
class MyRepositoryTests(@Autowired val entityManager: TestEntityManager, @Autowired val repository: UserRepository) {

	@Test
	fun testExample() {
		entityManager.persist(User("sboot", "1234"))
		val user = repository.findByUsername("sboot")
		assertThat(user?.username).isEqualTo("sboot")
		assertThat(user?.employeeNumber).isEqualTo("1234")
	}

}
```

In-memory embedded databases generally work well for tests, since they are fast and do not require any installation.
If, however, you prefer to run tests against a real database you can use the [`@AutoConfigureTestDatabase`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jdbc/test/autoconfigure/AutoConfigureTestDatabase.html) annotation, as shown in the following example:

* Java
* Kotlin

```
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import org.springframework.boot.jdbc.test.autoconfigure.AutoConfigureTestDatabase;
import org.springframework.boot.jdbc.test.autoconfigure.AutoConfigureTestDatabase.Replace;

@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
class MyRepositoryTests {

	// ...

}
```

```
import org.springframework.boot.jdbc.test.autoconfigure.AutoConfigureTestDatabase
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest

@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class MyRepositoryTests {

	// ...

}
```

## Auto-configured JDBC Tests

[`@JdbcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jdbc/test/autoconfigure/JdbcTest.html) from the `spring-boot-jdbc-test` module is similar to [`@DataJdbcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/jdbc/test/autoconfigure/DataJdbcTest.html) but is for tests that only require a [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html) and do not use Spring Data JDBC.
By default, it configures an in-memory embedded database and a [`JdbcTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jdbc/core/JdbcTemplate.html).
Regular [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html) and [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans are not scanned when the [`@JdbcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jdbc/test/autoconfigure/JdbcTest.html) annotation is used.
[`@EnableConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/EnableConfigurationProperties.html) can be used to include [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans.

|  |  |
| --- | --- |
|  | A list of the auto-configurations that are enabled by [`@JdbcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jdbc/test/autoconfigure/JdbcTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

By default, JDBC tests are transactional and roll back at the end of each test.
See the [relevant section](https://docs.spring.io/spring-framework/reference/7.0/testing/testcontext-framework/tx.html#testcontext-tx-enabling-transactions) in the Spring Framework Reference Documentation for more details.
If that is not what you want, you can disable transaction management for a test or for the whole class, as follows:

* Java
* Kotlin

```
import org.springframework.boot.jdbc.test.autoconfigure.JdbcTest;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

@JdbcTest
@Transactional(propagation = Propagation.NOT_SUPPORTED)
class MyTransactionalTests {

}
```

```
import org.springframework.boot.jdbc.test.autoconfigure.JdbcTest
import org.springframework.transaction.annotation.Propagation
import org.springframework.transaction.annotation.Transactional

@JdbcTest
@Transactional(propagation = Propagation.NOT_SUPPORTED)
class MyTransactionalTests
```

If you prefer your test to run against a real database, you can use the [`@AutoConfigureTestDatabase`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jdbc/test/autoconfigure/AutoConfigureTestDatabase.html) annotation in the same way as for [`@DataJpaTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/jpa/test/autoconfigure/DataJpaTest.html).
(See [Auto-configured Data JPA Tests](#testing.spring-boot-applications.autoconfigured-spring-data-jpa).)

## Auto-configured Data JDBC Tests

[`@DataJdbcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/jdbc/test/autoconfigure/DataJdbcTest.html) from the `spring-boot-data-jdbc-test` module is similar to [`@JdbcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jdbc/test/autoconfigure/JdbcTest.html) but is for tests that use Spring Data JDBC repositories.
By default, it configures an in-memory embedded database, a [`JdbcTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jdbc/core/JdbcTemplate.html), and Spring Data JDBC repositories.
Only [`AbstractJdbcConfiguration`](https://docs.spring.io/spring-data/jdbc/docs/4.1.x/api/org/springframework/data/jdbc/repository/config/AbstractJdbcConfiguration.html) subclasses are scanned when the [`@DataJdbcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/jdbc/test/autoconfigure/DataJdbcTest.html) annotation is used, regular [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html) and [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans are not scanned.
[`@EnableConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/EnableConfigurationProperties.html) can be used to include [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans.

|  |  |
| --- | --- |
|  | A list of the auto-configurations that are enabled by [`@DataJdbcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/jdbc/test/autoconfigure/DataJdbcTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

By default, Data JDBC tests are transactional and roll back at the end of each test.
See the [relevant section](https://docs.spring.io/spring-framework/reference/7.0/testing/testcontext-framework/tx.html#testcontext-tx-enabling-transactions) in the Spring Framework Reference Documentation for more details.
If that is not what you want, you can disable transaction management for a test or for the whole test class as [shown in the JDBC example](#testing.spring-boot-applications.autoconfigured-jdbc).

If you prefer your test to run against a real database, you can use the [`@AutoConfigureTestDatabase`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jdbc/test/autoconfigure/AutoConfigureTestDatabase.html) annotation in the same way as for [`@DataJpaTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/jpa/test/autoconfigure/DataJpaTest.html).
(See [Auto-configured Data JPA Tests](#testing.spring-boot-applications.autoconfigured-spring-data-jpa).)

## Auto-configured Data R2DBC Tests

[`@DataR2dbcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/r2dbc/test/autoconfigure/DataR2dbcTest.html) from the `spring-boot-data-r2dbc-test` module is similar to [`@DataJdbcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/jdbc/test/autoconfigure/DataJdbcTest.html) but is for tests that use Spring Data R2DBC repositories.
By default, it configures an in-memory embedded database, an [`R2dbcEntityTemplate`](https://docs.spring.io/spring-data/r2dbc/docs/4.1.x/api/org/springframework/data/r2dbc/core/R2dbcEntityTemplate.html), and Spring Data R2DBC repositories.
Regular [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html) and [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans are not scanned when the [`@DataR2dbcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/r2dbc/test/autoconfigure/DataR2dbcTest.html) annotation is used.
[`@EnableConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/EnableConfigurationProperties.html) can be used to include [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans.

|  |  |
| --- | --- |
|  | A list of the auto-configurations that are enabled by [`@DataR2dbcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/r2dbc/test/autoconfigure/DataR2dbcTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

By default, Data R2DBC tests are not transactional.

If you prefer your test to run against a real database, you can use the [`@AutoConfigureTestDatabase`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jdbc/test/autoconfigure/AutoConfigureTestDatabase.html) annotation in the same way as for [`@DataJpaTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/jpa/test/autoconfigure/DataJpaTest.html).
(See [Auto-configured Data JPA Tests](#testing.spring-boot-applications.autoconfigured-spring-data-jpa).)

## Auto-configured jOOQ Tests

You can use [`@JooqTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jooq/test/autoconfigure/JooqTest.html) from `spring-boot-jooq-test` in a similar fashion as [`@JdbcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jdbc/test/autoconfigure/JdbcTest.html) but for jOOQ-related tests.
As jOOQ relies heavily on a Java-based schema that corresponds with the database schema, the existing [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html) is used.
If you want to replace it with an in-memory database, you can use [`@AutoConfigureTestDatabase`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jdbc/test/autoconfigure/AutoConfigureTestDatabase.html) to override those settings.
(For more about using jOOQ with Spring Boot, see [Using jOOQ](../data/sql.html#data.sql.jooq).)
Regular [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html) and [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans are not scanned when the [`@JooqTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jooq/test/autoconfigure/JooqTest.html) annotation is used.
[`@EnableConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/EnableConfigurationProperties.html) can be used to include [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans.

|  |  |
| --- | --- |
|  | A list of the auto-configurations that are enabled by [`@JooqTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jooq/test/autoconfigure/JooqTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

[`@JooqTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jooq/test/autoconfigure/JooqTest.html) configures a [`DSLContext`](https://www.jooq.org/javadoc/3.21.5/org/jooq/DSLContext.html).
The following example shows the [`@JooqTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jooq/test/autoconfigure/JooqTest.html) annotation in use:

* Java
* Kotlin

```
import org.jooq.DSLContext;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.jooq.test.autoconfigure.JooqTest;

@JooqTest
class MyJooqTests {

	@Autowired
	private DSLContext dslContext;

	// ...

}
```

```
import org.jooq.DSLContext
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.jooq.test.autoconfigure.JooqTest

@JooqTest
class MyJooqTests(@Autowired val dslContext: DSLContext) {

	// ...

}
```

JOOQ tests are transactional and roll back at the end of each test by default.
If that is not what you want, you can disable transaction management for a test or for the whole test class as [shown in the JDBC example](#testing.spring-boot-applications.autoconfigured-jdbc).

## Auto-configured Data MongoDB Tests

You can use [`@DataMongoTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/mongodb/test/autoconfigure/DataMongoTest.html) from the `spring-boot-data-mongodb-test` module to test MongoDB applications.
By default, it configures a [`MongoTemplate`](https://docs.spring.io/spring-data/mongodb/docs/5.1.x/api/org/springframework/data/mongodb/core/MongoTemplate.html), scans for [`@Document`](https://docs.spring.io/spring-data/mongodb/docs/5.1.x/api/org/springframework/data/mongodb/core/mapping/Document.html) classes, and configures Spring Data MongoDB repositories.
Regular [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html) and [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans are not scanned when the [`@DataMongoTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/mongodb/test/autoconfigure/DataMongoTest.html) annotation is used.
[`@EnableConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/EnableConfigurationProperties.html) can be used to include [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans.
(For more about using MongoDB with Spring Boot, see [MongoDB](../data/nosql.html#data.nosql.mongodb).)

|  |  |
| --- | --- |
|  | A list of the auto-configuration settings that are enabled by [`@DataMongoTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/mongodb/test/autoconfigure/DataMongoTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

The following class shows the [`@DataMongoTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/mongodb/test/autoconfigure/DataMongoTest.html) annotation in use:

* Java
* Kotlin

```
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.mongodb.test.autoconfigure.DataMongoTest;
import org.springframework.data.mongodb.core.MongoTemplate;

@DataMongoTest
class MyDataMongoDbTests {

	@Autowired
	private MongoTemplate mongoTemplate;

	// ...

}
```

```
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.data.mongodb.test.autoconfigure.DataMongoTest
import org.springframework.data.mongodb.core.MongoTemplate

@DataMongoTest
class MyDataMongoDbTests(@Autowired val mongoTemplate: MongoTemplate) {

	// ...

}
```

## Auto-configured Data Neo4j Tests

You can use [`@DataNeo4jTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/neo4j/test/autoconfigure/DataNeo4jTest.html) from the `spring-boot-data-neo4j-test` module to test Neo4j applications.
By default, it scans for [`@Node`](https://docs.spring.io/spring-data/neo4j/docs/8.1.x/api/org/springframework/data/neo4j/core/schema/Node.html) classes, and configures Spring Data Neo4j repositories.
Regular [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html) and [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans are not scanned when the [`@DataNeo4jTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/neo4j/test/autoconfigure/DataNeo4jTest.html) annotation is used.
[`@EnableConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/EnableConfigurationProperties.html) can be used to include [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans.
(For more about using Neo4J with Spring Boot, see [Neo4j](../data/nosql.html#data.nosql.neo4j).)

|  |  |
| --- | --- |
|  | A list of the auto-configuration settings that are enabled by [`@DataNeo4jTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/neo4j/test/autoconfigure/DataNeo4jTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

The following example shows a typical setup for using Neo4J tests in Spring Boot:

* Java
* Kotlin

```
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.neo4j.test.autoconfigure.DataNeo4jTest;

@DataNeo4jTest
class MyDataNeo4jTests {

	@Autowired
	private SomeRepository repository;

	// ...

}
```

```
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.data.neo4j.test.autoconfigure.DataNeo4jTest

@DataNeo4jTest
class MyDataNeo4jTests(@Autowired val repository: SomeRepository) {

	// ...

}
```

By default, Data Neo4j tests are transactional and roll back at the end of each test.
See the [relevant section](https://docs.spring.io/spring-framework/reference/7.0/testing/testcontext-framework/tx.html#testcontext-tx-enabling-transactions) in the Spring Framework Reference Documentation for more details.
If that is not what you want, you can disable transaction management for a test or for the whole class, as follows:

* Java
* Kotlin

```
import org.springframework.boot.data.neo4j.test.autoconfigure.DataNeo4jTest;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

@DataNeo4jTest
@Transactional(propagation = Propagation.NOT_SUPPORTED)
class MyDataNeo4jTests {

}
```

```
import org.springframework.boot.data.neo4j.test.autoconfigure.DataNeo4jTest
import org.springframework.transaction.annotation.Propagation
import org.springframework.transaction.annotation.Transactional

@DataNeo4jTest
@Transactional(propagation = Propagation.NOT_SUPPORTED)
class MyDataNeo4jTests
```

|  |  |
| --- | --- |
|  | Transactional tests are not supported with reactive access. If you are using this style, you must configure [`@DataNeo4jTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/neo4j/test/autoconfigure/DataNeo4jTest.html) tests as described above. |

## Auto-configured Data Redis Tests

You can use [`@DataRedisTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/redis/test/autoconfigure/DataRedisTest.html) from the `spring-boot-data-redis-test` module to test Data Redis applications.
By default, it scans for [`@RedisHash`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/core/RedisHash.html) classes and configures Spring Data Redis repositories.
Regular [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html) and [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans are not scanned when the [`@DataRedisTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/redis/test/autoconfigure/DataRedisTest.html) annotation is used.
[`@EnableConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/EnableConfigurationProperties.html) can be used to include [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans.
(For more about using Redis with Spring Boot, see [Redis](../data/nosql.html#data.nosql.redis).)

|  |  |
| --- | --- |
|  | A list of the auto-configuration settings that are enabled by [`@DataRedisTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/redis/test/autoconfigure/DataRedisTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

The following example shows the [`@DataRedisTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/redis/test/autoconfigure/DataRedisTest.html) annotation in use:

* Java
* Kotlin

```
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.redis.test.autoconfigure.DataRedisTest;

@DataRedisTest
class MyDataRedisTests {

	@Autowired
	private SomeRepository repository;

	// ...

}
```

```
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.data.redis.test.autoconfigure.DataRedisTest

@DataRedisTest
class MyDataRedisTests(@Autowired val repository: SomeRepository) {

	// ...

}
```

## Auto-configured Data LDAP Tests

You can use [`@DataLdapTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/ldap/test/autoconfigure/DataLdapTest.html) to test Data LDAP applications.
By default, it configures an in-memory embedded LDAP (if available), configures an [`LdapTemplate`](https://docs.spring.io/spring-ldap/docs/4.1.x/api/org/springframework/ldap/core/LdapTemplate.html), scans for [`@Entry`](https://docs.spring.io/spring-ldap/docs/4.1.x/api/org/springframework/ldap/odm/annotations/Entry.html) classes, and configures Spring Data LDAP repositories.
Regular [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html) and [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans are not scanned when the [`@DataLdapTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/ldap/test/autoconfigure/DataLdapTest.html) annotation is used.
[`@EnableConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/EnableConfigurationProperties.html) can be used to include [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans.
(For more about using LDAP with Spring Boot, see [LDAP](../data/nosql.html#data.nosql.ldap).)

|  |  |
| --- | --- |
|  | A list of the auto-configuration settings that are enabled by [`@DataLdapTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/ldap/test/autoconfigure/DataLdapTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

The following example shows the [`@DataLdapTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/ldap/test/autoconfigure/DataLdapTest.html) annotation in use:

* Java
* Kotlin

```
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.ldap.test.autoconfigure.DataLdapTest;
import org.springframework.ldap.core.LdapTemplate;

@DataLdapTest
class MyDataLdapTests {

	@Autowired
	private LdapTemplate ldapTemplate;

	// ...

}
```

```
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.data.ldap.test.autoconfigure.DataLdapTest
import org.springframework.ldap.core.LdapTemplate

@DataLdapTest
class MyDataLdapTests(@Autowired val ldapTemplate: LdapTemplate) {

	// ...

}
```

In-memory embedded LDAP generally works well for tests, since it is fast and does not require any developer installation.
If, however, you prefer to run tests against a real LDAP server, you should exclude the embedded LDAP auto-configuration, as shown in the following example:

* Java
* Kotlin

```
import org.springframework.boot.data.ldap.test.autoconfigure.DataLdapTest;
import org.springframework.boot.ldap.autoconfigure.embedded.EmbeddedLdapAutoConfiguration;

@DataLdapTest(excludeAutoConfiguration = EmbeddedLdapAutoConfiguration.class)
class MyDataLdapTests {

	// ...

}
```

```
import org.springframework.boot.ldap.autoconfigure.embedded.EmbeddedLdapAutoConfiguration
import org.springframework.boot.data.ldap.test.autoconfigure.DataLdapTest

@DataLdapTest(excludeAutoConfiguration = [EmbeddedLdapAutoConfiguration::class])
class MyDataLdapTests {

	// ...

}
```

## Auto-configured REST Clients

You can use the [`@RestClientTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/test/autoconfigure/RestClientTest.html) annotation from the `spring-boot-restclient-test` module to test REST clients.
By default, it auto-configures Jackson, GSON, and Jsonb support, configures a [`RestTemplateBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/RestTemplateBuilder.html) and a [`RestClient.Builder`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestClient.Builder.html), and adds support for [`MockRestServiceServer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/client/MockRestServiceServer.html).
Regular [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html) and [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans are not scanned when the [`@RestClientTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/test/autoconfigure/RestClientTest.html) annotation is used.
[`@EnableConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/EnableConfigurationProperties.html) can be used to include [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans.

|  |  |
| --- | --- |
|  | A list of the auto-configuration settings that are enabled by [`@RestClientTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/test/autoconfigure/RestClientTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

The specific beans that you want to test should be specified by using the `value` or `components` attribute of [`@RestClientTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/test/autoconfigure/RestClientTest.html).

When using a [`RestTemplateBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/RestTemplateBuilder.html) in the beans under test and `RestTemplateBuilder.rootUri(String rootUri)` has been called when building the [`RestTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestTemplate.html), then the root URI should be omitted from the [`MockRestServiceServer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/client/MockRestServiceServer.html) expectations as shown in the following example:

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.restclient.test.autoconfigure.RestClientTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.client.MockRestServiceServer;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.requestTo;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withSuccess;

@RestClientTest(org.springframework.boot.docs.testing.springbootapplications.autoconfiguredrestclient.RemoteVehicleDetailsService.class)
class MyRestTemplateServiceTests {

	@Autowired
	private RemoteVehicleDetailsService service;

	@Autowired
	private MockRestServiceServer server;

	@Test
	void getVehicleDetailsWhenResultIsSuccessShouldReturnDetails() {
		this.server.expect(requestTo("/greet/details")).andRespond(withSuccess("hello", MediaType.TEXT_PLAIN));
		String greeting = this.service.callRestService();
		assertThat(greeting).isEqualTo("hello");
	}

}
```

```
import org.assertj.core.api.Assertions.assertThat
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.restclient.test.autoconfigure.RestClientTest
import org.springframework.http.MediaType
import org.springframework.test.web.client.MockRestServiceServer
import org.springframework.test.web.client.match.MockRestRequestMatchers
import org.springframework.test.web.client.response.MockRestResponseCreators

@RestClientTest(RemoteVehicleDetailsService::class)
class MyRestTemplateServiceTests(
	@Autowired val service: RemoteVehicleDetailsService,
	@Autowired val server: MockRestServiceServer) {

	@Test
	fun getVehicleDetailsWhenResultIsSuccessShouldReturnDetails() {
		server.expect(MockRestRequestMatchers.requestTo("/greet/details"))
			.andRespond(MockRestResponseCreators.withSuccess("hello", MediaType.TEXT_PLAIN))
		val greeting = service.callRestService()
		assertThat(greeting).isEqualTo("hello")
	}

}
```

When using a [`RestClient.Builder`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestClient.Builder.html) in the beans under test, or when using a [`RestTemplateBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/RestTemplateBuilder.html) without calling `rootUri(String rootURI)`, the full URI must be used in the [`MockRestServiceServer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/client/MockRestServiceServer.html) expectations as shown in the following example:

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.restclient.test.autoconfigure.RestClientTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.client.MockRestServiceServer;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.requestTo;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withSuccess;

@RestClientTest(RemoteVehicleDetailsService.class)
class MyRestClientServiceTests {

	@Autowired
	private RemoteVehicleDetailsService service;

	@Autowired
	private MockRestServiceServer server;

	@Test
	void getVehicleDetailsWhenResultIsSuccessShouldReturnDetails() {
		this.server.expect(requestTo("https://example.com/greet/details"))
			.andRespond(withSuccess("hello", MediaType.TEXT_PLAIN));
		String greeting = this.service.callRestService();
		assertThat(greeting).isEqualTo("hello");
	}

}
```

```
import org.assertj.core.api.Assertions.assertThat
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.restclient.test.autoconfigure.RestClientTest
import org.springframework.http.MediaType
import org.springframework.test.web.client.MockRestServiceServer
import org.springframework.test.web.client.match.MockRestRequestMatchers
import org.springframework.test.web.client.response.MockRestResponseCreators

@RestClientTest(RemoteVehicleDetailsService::class)
class MyRestClientServiceTests(
	@Autowired val service: RemoteVehicleDetailsService,
	@Autowired val server: MockRestServiceServer) {

	@Test
	fun getVehicleDetailsWhenResultIsSuccessShouldReturnDetails() {
		server.expect(MockRestRequestMatchers.requestTo("https://example.com/greet/details"))
			.andRespond(MockRestResponseCreators.withSuccess("hello", MediaType.TEXT_PLAIN))
		val greeting = service.callRestService()
		assertThat(greeting).isEqualTo("hello")
	}

}
```

## Auto-configured Web Clients

You can use the [`@WebClientTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webclient/test/autoconfigure/WebClientTest.html) annotation from the `spring-boot-webclient-test` module to test code that uses `WebClient`.
By default, it auto-configures Jackson, GSON, and Jsonb support, and configures a [`WebClient.Builder`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/WebClient.Builder.html).
Regular [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html) and [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans are not scanned when the [`@WebClientTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webclient/test/autoconfigure/WebClientTest.html) annotation is used.
[`@EnableConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/EnableConfigurationProperties.html) can be used to include [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans.

|  |  |
| --- | --- |
|  | A list of the auto-configuration settings that are enabled by [`@WebClientTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webclient/test/autoconfigure/WebClientTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

The specific beans that you want to test should be specified by using the `value` or `components` attribute of [`@WebClientTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webclient/test/autoconfigure/WebClientTest.html).

## Auto-configured Spring REST Docs Tests

You can use the [`@AutoConfigureRestDocs`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restdocs/test/autoconfigure/AutoConfigureRestDocs.html) annotation from the `spring-boot-restdocs- module to use [Spring REST Docs](https://spring.io/projects/spring-restdocs) in your tests with Mock MVC or WebTestClient.
It removes the need for the JUnit extension in Spring REST Docs.

[`@AutoConfigureRestDocs`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restdocs/test/autoconfigure/AutoConfigureRestDocs.html) can be used to override the default output directory (`target/generated-snippets` if you are using Maven or `build/generated-snippets` if you are using Gradle).
It can also be used to configure the host, scheme, and port that appears in any documented URIs.

### Auto-configured Spring REST Docs Tests With Mock MVC

[`@AutoConfigureRestDocs`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restdocs/test/autoconfigure/AutoConfigureRestDocs.html) customizes the [`MockMvc`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/servlet/MockMvc.html) bean to use Spring REST Docs when testing servlet-based web applications.
You can inject it by using [`@Autowired`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/beans/factory/annotation/Autowired.html) and use it in your tests as you normally would when using Mock MVC and Spring REST Docs, as shown in the following example:

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.restdocs.test.autoconfigure.AutoConfigureRestDocs;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.assertj.MockMvcTester;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.restdocs.mockmvc.MockMvcRestDocumentation.document;

@WebMvcTest(UserController.class)
@AutoConfigureRestDocs
class MyUserDocumentationTests {

	@Autowired
	private MockMvcTester mvc;

	@Test
	void listUsers() {
		assertThat(this.mvc.get().uri("/users").accept(MediaType.TEXT_PLAIN)).hasStatusOk()
			.apply(document("list-users"));
	}

}
```

If you prefer to use the AssertJ integration, [`MockMvcTester`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/servlet/assertj/MockMvcTester.html) is available as well, as shown in the following example:

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.restdocs.test.autoconfigure.AutoConfigureRestDocs;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.assertj.MockMvcTester;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.restdocs.mockmvc.MockMvcRestDocumentation.document;

@WebMvcTest(UserController.class)
@AutoConfigureRestDocs
class MyUserDocumentationTests {

	@Autowired
	private MockMvcTester mvc;

	@Test
	void listUsers() {
		assertThat(this.mvc.get().uri("/users").accept(MediaType.TEXT_PLAIN)).hasStatusOk()
			.apply(document("list-users"));
	}

}
```

Both reuses the same [`MockMvc`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/servlet/MockMvc.html) instance behind the scenes so any configuration to it applies to both.

If you require more control over Spring REST Docs configuration than offered by the attributes of [`@AutoConfigureRestDocs`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restdocs/test/autoconfigure/AutoConfigureRestDocs.html), you can use a [`RestDocsMockMvcConfigurationCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restdocs/test/autoconfigure/RestDocsMockMvcConfigurationCustomizer.html) bean, as shown in the following example:

* Java
* Kotlin

```
import org.springframework.boot.restdocs.test.autoconfigure.RestDocsMockMvcConfigurationCustomizer;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.restdocs.mockmvc.MockMvcRestDocumentationConfigurer;
import org.springframework.restdocs.templates.TemplateFormats;

@TestConfiguration(proxyBeanMethods = false)
public class MyRestDocsConfiguration implements RestDocsMockMvcConfigurationCustomizer {

	@Override
	public void customize(MockMvcRestDocumentationConfigurer configurer) {
		configurer.snippets().withTemplateFormat(TemplateFormats.markdown());
	}

}
```

```
import org.springframework.boot.restdocs.test.autoconfigure.RestDocsMockMvcConfigurationCustomizer
import org.springframework.boot.test.context.TestConfiguration
import org.springframework.restdocs.mockmvc.MockMvcRestDocumentationConfigurer
import org.springframework.restdocs.templates.TemplateFormats

@TestConfiguration(proxyBeanMethods = false)
class MyRestDocsConfiguration : RestDocsMockMvcConfigurationCustomizer {

	override fun customize(configurer: MockMvcRestDocumentationConfigurer) {
		configurer.snippets().withTemplateFormat(TemplateFormats.markdown())
	}

}
```

If you want to make use of Spring REST Docs support for a parameterized output directory, you can create a [`RestDocumentationResultHandler`](https://docs.spring.io/spring-restdocs/docs/4.0.x/api/org/springframework/restdocs/mockmvc/RestDocumentationResultHandler.html) bean.
The auto-configuration calls `alwaysDo` with this result handler, thereby causing each [`MockMvc`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/servlet/MockMvc.html) call to automatically generate the default snippets.
The following example shows a [`RestDocumentationResultHandler`](https://docs.spring.io/spring-restdocs/docs/4.0.x/api/org/springframework/restdocs/mockmvc/RestDocumentationResultHandler.html) being defined:

* Java
* Kotlin

```
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.restdocs.mockmvc.MockMvcRestDocumentation;
import org.springframework.restdocs.mockmvc.RestDocumentationResultHandler;

@TestConfiguration(proxyBeanMethods = false)
public class MyResultHandlerConfiguration {

	@Bean
	public RestDocumentationResultHandler restDocumentation() {
		return MockMvcRestDocumentation.document("{method-name}");
	}

}
```

```
import org.springframework.boot.test.context.TestConfiguration
import org.springframework.context.annotation.Bean
import org.springframework.restdocs.mockmvc.MockMvcRestDocumentation
import org.springframework.restdocs.mockmvc.RestDocumentationResultHandler

@TestConfiguration(proxyBeanMethods = false)
class MyResultHandlerConfiguration {

	@Bean
	fun restDocumentation(): RestDocumentationResultHandler {
		return MockMvcRestDocumentation.document("{method-name}")
	}

}
```

### Auto-configured Spring REST Docs Tests With WebTestClient

[`@AutoConfigureRestDocs`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restdocs/test/autoconfigure/AutoConfigureRestDocs.html) can also be used with [`WebTestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/web/reactive/server/WebTestClient.html) when testing reactive web applications.
You can inject it by using [`@Autowired`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/beans/factory/annotation/Autowired.html) and use it in your tests as you normally would when using [`@WebFluxTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webflux/test/autoconfigure/WebFluxTest.html) and Spring REST Docs, as shown in the following example:

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.restdocs.test.autoconfigure.AutoConfigureRestDocs;
import org.springframework.boot.webflux.test.autoconfigure.WebFluxTest;
import org.springframework.test.web.reactive.server.WebTestClient;

import static org.springframework.restdocs.webtestclient.WebTestClientRestDocumentation.document;

@WebFluxTest
@AutoConfigureRestDocs
class MyUsersDocumentationTests {

	@Autowired
	private WebTestClient webTestClient;

	@Test
	void listUsers() {
		this.webTestClient
			.get().uri("/")
		.exchange()
		.expectStatus()
			.isOk()
		.expectBody()
			.consumeWith(document("list-users"));
	}

}
```

```
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.restdocs.test.autoconfigure.AutoConfigureRestDocs
import org.springframework.boot.webflux.test.autoconfigure.WebFluxTest
import org.springframework.restdocs.webtestclient.WebTestClientRestDocumentation
import org.springframework.test.web.reactive.server.WebTestClient

@WebFluxTest
@AutoConfigureRestDocs
class MyUsersDocumentationTests(@Autowired val webTestClient: WebTestClient) {

	@Test
	fun listUsers() {
		webTestClient
			.get().uri("/")
			.exchange()
			.expectStatus()
			.isOk
			.expectBody()
			.consumeWith(WebTestClientRestDocumentation.document("list-users"))
	}

}
```

If you require more control over Spring REST Docs configuration than offered by the attributes of [`@AutoConfigureRestDocs`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restdocs/test/autoconfigure/AutoConfigureRestDocs.html), you can use a [`RestDocsWebTestClientConfigurationCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restdocs/test/autoconfigure/RestDocsWebTestClientConfigurationCustomizer.html) bean, as shown in the following example:

* Java
* Kotlin

```
import org.springframework.boot.restdocs.test.autoconfigure.RestDocsWebTestClientConfigurationCustomizer;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.restdocs.webtestclient.WebTestClientRestDocumentationConfigurer;

@TestConfiguration(proxyBeanMethods = false)
public class MyRestDocsConfiguration implements RestDocsWebTestClientConfigurationCustomizer {

	@Override
	public void customize(WebTestClientRestDocumentationConfigurer configurer) {
		configurer.snippets().withEncoding("UTF-8");
	}

}
```

```
import org.springframework.boot.restdocs.test.autoconfigure.RestDocsWebTestClientConfigurationCustomizer
import org.springframework.boot.test.context.TestConfiguration
import org.springframework.restdocs.webtestclient.WebTestClientRestDocumentationConfigurer

@TestConfiguration(proxyBeanMethods = false)
class MyRestDocsConfiguration : RestDocsWebTestClientConfigurationCustomizer {

	override fun customize(configurer: WebTestClientRestDocumentationConfigurer) {
		configurer.snippets().withEncoding("UTF-8")
	}

}
```

If you want to make use of Spring REST Docs support for a parameterized output directory, you can use a [`WebTestClientBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webtestclient/autoconfigure/WebTestClientBuilderCustomizer.html) to configure a consumer for every entity exchange result.
The following example shows such a [`WebTestClientBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webtestclient/autoconfigure/WebTestClientBuilderCustomizer.html) being defined:

* Java
* Kotlin

```
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.boot.webtestclient.autoconfigure.WebTestClientBuilderCustomizer;
import org.springframework.context.annotation.Bean;

import static org.springframework.restdocs.webtestclient.WebTestClientRestDocumentation.document;

@TestConfiguration(proxyBeanMethods = false)
public class MyWebTestClientBuilderCustomizerConfiguration {

	@Bean
	public WebTestClientBuilderCustomizer restDocumentation() {
		return (builder) -> builder.entityExchangeResultConsumer(document("{method-name}"));
	}

}
```

```
import org.springframework.boot.test.context.TestConfiguration
import org.springframework.boot.webtestclient.autoconfigure.WebTestClientBuilderCustomizer
import org.springframework.context.annotation.Bean
import org.springframework.restdocs.webtestclient.WebTestClientRestDocumentation
import org.springframework.test.web.reactive.server.WebTestClient

@TestConfiguration(proxyBeanMethods = false)
class MyWebTestClientBuilderCustomizerConfiguration {

	@Bean
	fun restDocumentation(): WebTestClientBuilderCustomizer {
		return WebTestClientBuilderCustomizer { builder: WebTestClient.Builder ->
			builder.entityExchangeResultConsumer(
				WebTestClientRestDocumentation.document("{method-name}")
			)
		}
	}

}
```

## Auto-configured Spring Web Services Tests

### Auto-configured Spring Web Services Client Tests

You can use [`@WebServiceClientTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webservices/test/autoconfigure/client/WebServiceClientTest.html) from the `spring-boot-webservices-test` module to test applications that call web services using the Spring Web Services project.
By default, it configures a [`MockWebServiceServer`](https://docs.spring.io/spring-ws/docs/5.0.x/api/org/springframework/ws/test/client/MockWebServiceServer.html) bean and automatically customizes your [`WebServiceTemplateBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webservices/client/WebServiceTemplateBuilder.html).
(For more about using Web Services with Spring Boot, see [Web Services](../io/webservices.html).)

|  |  |
| --- | --- |
|  | A list of the auto-configuration settings that are enabled by [`@WebServiceClientTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webservices/test/autoconfigure/client/WebServiceClientTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

The following example shows the [`@WebServiceClientTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webservices/test/autoconfigure/client/WebServiceClientTest.html) annotation in use:

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webservices.test.autoconfigure.client.WebServiceClientTest;
import org.springframework.ws.test.client.MockWebServiceServer;
import org.springframework.xml.transform.StringSource;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.ws.test.client.RequestMatchers.payload;
import static org.springframework.ws.test.client.ResponseCreators.withPayload;

@WebServiceClientTest(SomeWebService.class)
class MyWebServiceClientTests {

	@Autowired
	private MockWebServiceServer server;

	@Autowired
	private SomeWebService someWebService;

	@Test
	void mockServerCall() {
		this.server
			.expect(payload(new StringSource("<request/>")))
			.andRespond(withPayload(new StringSource("<response><status>200</status></response>")));
		assertThat(this.someWebService.test())
			.extracting(Response::getStatus)
			.isEqualTo(200);
	}

}
```

```
import org.assertj.core.api.Assertions.assertThat
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.webservices.test.autoconfigure.client.WebServiceClientTest
import org.springframework.ws.test.client.MockWebServiceServer
import org.springframework.ws.test.client.RequestMatchers
import org.springframework.ws.test.client.ResponseCreators
import org.springframework.xml.transform.StringSource

@WebServiceClientTest(SomeWebService::class)
class MyWebServiceClientTests(
		@Autowired val server: MockWebServiceServer, @Autowired val someWebService: SomeWebService) {

	@Test
	fun mockServerCall() {
		server
			.expect(RequestMatchers.payload(StringSource("<request/>")))
			.andRespond(ResponseCreators.withPayload(StringSource("<response><status>200</status></response>")))
		assertThat(this.someWebService.test()).extracting(Response::status).isEqualTo(200)
	}

}
```

### Auto-configured Spring Web Services Server Tests

You can use [`@WebServiceServerTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webservices/test/autoconfigure/server/WebServiceServerTest.html) from the `spring-boot-webservices-test` module to test applications that implement web services using the Spring Web Services project.
By default, it configures a [`MockWebServiceClient`](https://docs.spring.io/spring-ws/docs/5.0.x/api/org/springframework/ws/test/server/MockWebServiceClient.html) bean that can be used to call your web service endpoints.
(For more about using Web Services with Spring Boot, see [Web Services](../io/webservices.html).)

|  |  |
| --- | --- |
|  | A list of the auto-configuration settings that are enabled by [`@WebServiceServerTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webservices/test/autoconfigure/server/WebServiceServerTest.html) can be [found in the appendix](../../appendix/test-auto-configuration/index.html). |

The following example shows the [`@WebServiceServerTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webservices/test/autoconfigure/server/WebServiceServerTest.html) annotation in use:

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webservices.test.autoconfigure.server.WebServiceServerTest;
import org.springframework.ws.test.server.MockWebServiceClient;
import org.springframework.ws.test.server.RequestCreators;
import org.springframework.ws.test.server.ResponseMatchers;
import org.springframework.xml.transform.StringSource;

@WebServiceServerTest(ExampleEndpoint.class)
class MyWebServiceServerTests {

	@Autowired
	private MockWebServiceClient client;

	@Test
	void mockServerCall() {
		this.client
			.sendRequest(RequestCreators.withPayload(new StringSource("<ExampleRequest/>")))
			.andExpect(ResponseMatchers.payload(new StringSource("<ExampleResponse>42</ExampleResponse>")));
	}

}
```

```
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.webservices.test.autoconfigure.server.WebServiceServerTest
import org.springframework.ws.test.server.MockWebServiceClient
import org.springframework.ws.test.server.RequestCreators
import org.springframework.ws.test.server.ResponseMatchers
import org.springframework.xml.transform.StringSource

@WebServiceServerTest(ExampleEndpoint::class)
class MyWebServiceServerTests(@Autowired val client: MockWebServiceClient) {

	@Test
	fun mockServerCall() {
		client
			.sendRequest(RequestCreators.withPayload(StringSource("<ExampleRequest/>")))
			.andExpect(ResponseMatchers.payload(StringSource("<ExampleResponse>42</ExampleResponse>")))
	}

}
```

## Additional Auto-configuration and Slicing

Each slice provides one or more `@AutoConfigure…​` annotations that namely defines the auto-configurations that should be included as part of a slice.
Additional auto-configurations can be added on a test-by-test basis by creating a custom `@AutoConfigure…​` annotation or by adding [`@ImportAutoConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/ImportAutoConfiguration.html) to the test as shown in the following example:

* Java
* Kotlin

```
import org.springframework.boot.autoconfigure.ImportAutoConfiguration;
import org.springframework.boot.integration.autoconfigure.IntegrationAutoConfiguration;
import org.springframework.boot.jdbc.test.autoconfigure.JdbcTest;

@JdbcTest
@ImportAutoConfiguration(IntegrationAutoConfiguration.class)
class MyJdbcTests {

}
```

```
import org.springframework.boot.autoconfigure.ImportAutoConfiguration
import org.springframework.boot.integration.autoconfigure.IntegrationAutoConfiguration
import org.springframework.boot.jdbc.test.autoconfigure.JdbcTest

@JdbcTest
@ImportAutoConfiguration(IntegrationAutoConfiguration::class)
class MyJdbcTests
```

|  |  |
| --- | --- |
|  | Make sure to not use the regular [`@Import`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Import.html) annotation to import auto-configurations as they are handled in a specific way by Spring Boot. |

Alternatively, additional auto-configurations can be added for any use of a slice annotation by registering them in a file stored in `META-INF/spring` as shown in the following example:

META-INF/spring/org.springframework.boot.jdbc.test.autoconfigure.JdbcTest.imports

```
com.example.IntegrationAutoConfiguration
```

In this example, the `com.example.IntegrationAutoConfiguration` is enabled on every test annotated with [`@JdbcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jdbc/test/autoconfigure/JdbcTest.html).

|  |  |
| --- | --- |
|  | You can use comments with `#` in this file. |

|  |  |
| --- | --- |
|  | A slice or `@AutoConfigure…​` annotation can be customized this way as long as it is meta-annotated with [`@ImportAutoConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/ImportAutoConfiguration.html). |

## User Configuration and Slicing

If you [structure your code](../using/structuring-your-code.html) in a sensible way, your [`@SpringBootApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/SpringBootApplication.html) class is [used by default](#testing.spring-boot-applications.detecting-configuration) as the configuration of your tests.

It then becomes important not to litter the application’s main class with configuration settings that are specific to a particular area of its functionality.

Assume that you are using Spring Data MongoDB, you rely on the auto-configuration for it, and you have enabled auditing.
You could define your [`@SpringBootApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/SpringBootApplication.html) as follows:

* Java
* Kotlin

```
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.mongodb.config.EnableMongoAuditing;

@SpringBootApplication
@EnableMongoAuditing
public class MyApplication {

	// ...

}
```

```
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.data.mongodb.config.EnableMongoAuditing

@SpringBootApplication
@EnableMongoAuditing
class MyApplication {

	// ...

}
```

Because this class is the source configuration for the test, any slice test actually tries to enable Mongo auditing, which is definitely not what you want to do.
A recommended approach is to move that area-specific configuration to a separate [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) class at the same level as your application, as shown in the following example:

* Java
* Kotlin

```
import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.config.EnableMongoAuditing;

@Configuration(proxyBeanMethods = false)
@EnableMongoAuditing
public class MyMongoConfiguration {

	// ...

}
```

```
import org.springframework.context.annotation.Configuration
import org.springframework.data.mongodb.config.EnableMongoAuditing

@Configuration(proxyBeanMethods = false)
@EnableMongoAuditing
class MyMongoConfiguration {

	// ...

}
```

|  |  |
| --- | --- |
|  | Depending on the complexity of your application, you may either have a single [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) class for your customizations or one class per domain area. The latter approach lets you enable it in one of your tests, if necessary, with the [`@Import`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Import.html) annotation. See [this how-to section](../../how-to/testing.html#howto.testing.slice-tests) for more details on when you might want to enable specific [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) classes for slice tests. |

Test slices exclude [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) classes from scanning.
For example, for a [`@WebMvcTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webmvc/test/autoconfigure/WebMvcTest.html), the following configuration will not include the given [`WebMvcConfigurer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/servlet/config/annotation/WebMvcConfigurer.html) bean in the application context loaded by the test slice:

* Java
* Kotlin

```
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration(proxyBeanMethods = false)
public class MyWebConfiguration {

	@Bean
	public WebMvcConfigurer testConfigurer() {
		return new WebMvcConfigurer() {
			// ...
		};
	}

}
```

```
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer

@Configuration(proxyBeanMethods = false)
class MyWebConfiguration {

	@Bean
	fun testConfigurer(): WebMvcConfigurer {
		return object : WebMvcConfigurer {
			// ...
		}
	}

}
```

The configuration below will, however, cause the custom [`WebMvcConfigurer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/servlet/config/annotation/WebMvcConfigurer.html) to be loaded by the test slice.

* Java
* Kotlin

```
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Component
public class MyWebMvcConfigurer implements WebMvcConfigurer {

	// ...

}
```

```
import org.springframework.stereotype.Component
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer

@Component
class MyWebMvcConfigurer : WebMvcConfigurer {

	// ...

}
```

Another source of confusion is classpath scanning.
Assume that, while you structured your code in a sensible way, you need to scan an additional package.
Your application may resemble the following code:

* Java
* Kotlin

```
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@ComponentScan({ "com.example.app", "com.example.another" })
public class MyApplication {

	// ...

}
```

```
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.context.annotation.ComponentScan

@SpringBootApplication
@ComponentScan("com.example.app", "com.example.another")
class MyApplication {

	// ...

}
```

Doing so effectively overrides the default component scan directive with the side effect of scanning those two packages regardless of the slice that you chose.
For instance, a [`@DataJpaTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/jpa/test/autoconfigure/DataJpaTest.html) seems to suddenly scan components and user configurations of your application.
Again, moving the custom directive to a separate class is a good way to fix this issue.

|  |  |
| --- | --- |
|  | If this is not an option for you, you can create a [`@SpringBootConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/SpringBootConfiguration.html) somewhere in the hierarchy of your test so that it is used instead. Alternatively, you can specify a source for your test, which disables the behavior of finding a default one. |

## Using Spock to Test Spring Boot Applications

Spock 2.4 or later can be used to test a Spring Boot application.
To do so, add a dependency on a `-groovy-5.0` version of Spock’s `spock-spring` module to your application’s build.
`spock-spring` integrates Spring’s test framework into Spock.
See [the documentation for Spock’s Spring module](https://spockframework.org/spock/docs/2.4/modules.html#spring-module) for further details.