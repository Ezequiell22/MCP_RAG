Search

# Reactive Web Applications

Spring Boot simplifies development of reactive web applications by providing auto-configuration for Spring Webflux.

## The “Spring WebFlux Framework”

Spring WebFlux is the new reactive web framework introduced in Spring Framework 5.0.
Unlike Spring MVC, it does not require the servlet API, is fully asynchronous and non-blocking, and implements the [Reactive Streams](https://www.reactive-streams.org/) specification through [the Reactor project](https://projectreactor.io/).

Spring WebFlux comes in two flavors: functional and annotation-based.
The annotation-based one is quite close to the Spring MVC model, as shown in the following example:

* Java
* Kotlin

```
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/users")
public class MyRestController {

	private final UserRepository userRepository;

	private final CustomerRepository customerRepository;

	public MyRestController(UserRepository userRepository, CustomerRepository customerRepository) {
		this.userRepository = userRepository;
		this.customerRepository = customerRepository;
	}

	@GetMapping("/{userId}")
	public Mono<User> getUser(@PathVariable Long userId) {
		return this.userRepository.findById(userId);
	}

	@GetMapping("/{userId}/customers")
	public Flux<Customer> getUserCustomers(@PathVariable Long userId) {
		return this.userRepository.findById(userId).flatMapMany(this.customerRepository::findByUser);
	}

	@DeleteMapping("/{userId}")
	public Mono<Void> deleteUser(@PathVariable Long userId) {
		return this.userRepository.deleteById(userId);
	}

}
```

```
import org.springframework.web.bind.annotation.DeleteMapping
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import reactor.core.publisher.Flux
import reactor.core.publisher.Mono

@RestController
@RequestMapping("/users")
class MyRestController(private val userRepository: UserRepository, private val customerRepository: CustomerRepository) {

	@GetMapping("/{userId}")
	fun getUser(@PathVariable userId: Long): Mono<User> {
		return userRepository.findById(userId)
	}

	@GetMapping("/{userId}/customers")
	fun getUserCustomers(@PathVariable userId: Long): Flux<Customer> {
		return userRepository.findById(userId).flatMapMany { user: User ->
			customerRepository.findByUser(user)
		}
	}

	@DeleteMapping("/{userId}")
	fun deleteUser(@PathVariable userId: Long): Mono<Void> {
		return userRepository.deleteById(userId)
	}

}
```

WebFlux is part of the Spring Framework and detailed information is available in its [reference documentation](https://docs.spring.io/spring-framework/reference/7.0/web/webflux.html).

“WebFlux.fn”, the functional variant, separates the routing configuration from the actual handling of the requests, as shown in the following example:

* Java
* Kotlin

```
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.function.server.RequestPredicate;
import org.springframework.web.reactive.function.server.RouterFunction;
import org.springframework.web.reactive.function.server.ServerResponse;

import static org.springframework.web.reactive.function.server.RequestPredicates.accept;
import static org.springframework.web.reactive.function.server.RouterFunctions.route;

@Configuration(proxyBeanMethods = false)
public class MyRoutingConfiguration {

	private static final RequestPredicate ACCEPT_JSON = accept(MediaType.APPLICATION_JSON);

	@Bean
	public RouterFunction<ServerResponse> monoRouterFunction(MyUserHandler userHandler) {
		return route()
				.GET("/{user}", ACCEPT_JSON, userHandler::getUser)
				.GET("/{user}/customers", ACCEPT_JSON, userHandler::getUserCustomers)
				.DELETE("/{user}", ACCEPT_JSON, userHandler::deleteUser)
				.build();
	}

}
```

```
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.http.MediaType
import org.springframework.web.reactive.function.server.RequestPredicates.DELETE
import org.springframework.web.reactive.function.server.RequestPredicates.GET
import org.springframework.web.reactive.function.server.RequestPredicates.accept
import org.springframework.web.reactive.function.server.RouterFunction
import org.springframework.web.reactive.function.server.RouterFunctions
import org.springframework.web.reactive.function.server.ServerResponse

@Configuration(proxyBeanMethods = false)
class MyRoutingConfiguration {

	@Bean
	fun monoRouterFunction(userHandler: MyUserHandler): RouterFunction<ServerResponse> {
		return RouterFunctions.route(
			GET("/{user}").and(ACCEPT_JSON), userHandler::getUser).andRoute(
			GET("/{user}/customers").and(ACCEPT_JSON), userHandler::getUserCustomers).andRoute(
			DELETE("/{user}").and(ACCEPT_JSON), userHandler::deleteUser)
	}

	companion object {
		private val ACCEPT_JSON = accept(MediaType.APPLICATION_JSON)
	}

}
```

* Java
* Kotlin

```
import reactor.core.publisher.Mono;

import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;

@Component
public class MyUserHandler {

	public Mono<ServerResponse> getUser(ServerRequest request) {
		...
	}

	public Mono<ServerResponse> getUserCustomers(ServerRequest request) {
		...
	}

	public Mono<ServerResponse> deleteUser(ServerRequest request) {
		...
	}

}
```

```
import org.springframework.stereotype.Component
import org.springframework.web.reactive.function.server.ServerRequest
import org.springframework.web.reactive.function.server.ServerResponse
import reactor.core.publisher.Mono

@Component
class MyUserHandler {

	fun getUser(request: ServerRequest?): Mono<ServerResponse> {
		...
	}

	fun getUserCustomers(request: ServerRequest?): Mono<ServerResponse> {
		...
	}

	fun deleteUser(request: ServerRequest?): Mono<ServerResponse> {
		...
	}

}
```

“WebFlux.fn” is part of the Spring Framework and detailed information is available in its [reference documentation](https://docs.spring.io/spring-framework/reference/7.0/web/webflux-functional.html).

|  |  |
| --- | --- |
|  | You can define as many [`RouterFunction`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/server/RouterFunction.html) beans as you like to modularize the definition of the router. Beans can be ordered if you need to apply a precedence. |

To get started, add the `spring-boot-starter-webflux` module to your application.

|  |  |
| --- | --- |
|  | Adding both `spring-boot-starter-web` and `spring-boot-starter-webflux` modules in your application results in Spring Boot auto-configuring Spring MVC, not WebFlux. This behavior has been chosen because many Spring developers add `spring-boot-starter-webflux` to their Spring MVC application to use the reactive [`WebClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/WebClient.html). You can still enforce your choice by setting the chosen application type to `SpringApplication.setWebApplicationType(WebApplicationType.REACTIVE)`. |

### Spring WebFlux Auto-configuration

Spring Boot provides auto-configuration for Spring WebFlux that works well with most applications.

The auto-configuration adds the following features on top of Spring’s defaults:

* Configuring codecs for [`HttpMessageReader`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/http/codec/HttpMessageReader.html) and [`HttpMessageWriter`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/http/codec/HttpMessageWriter.html) instances (described [later in this document](#web.reactive.webflux.httpcodecs)).
* Support for serving static resources, including support for WebJars (described [later in this document](servlet.html#web.servlet.spring-mvc.static-content)).

If you want to keep Spring Boot WebFlux features and you want to add additional [WebFlux configuration](https://docs.spring.io/spring-framework/reference/7.0/web/webflux/config.html), you can add your own [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) class of type [`WebFluxConfigurer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/config/WebFluxConfigurer.html) but **without** [`@EnableWebFlux`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/config/EnableWebFlux.html).

If you want to add additional customization to the auto-configured [`HttpHandler`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/http/server/reactive/HttpHandler.html), you can define beans of type [`WebHttpHandlerBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webflux/autoconfigure/WebHttpHandlerBuilderCustomizer.html) and use them to modify the [`WebHttpHandlerBuilder`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/server/adapter/WebHttpHandlerBuilder.html).

If you want to take complete control of Spring WebFlux, you can add your own [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) annotated with [`@EnableWebFlux`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/config/EnableWebFlux.html).

### Spring WebFlux Conversion Service

If you want to customize the [`ConversionService`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/convert/ConversionService.html) used by Spring WebFlux, you can provide a [`WebFluxConfigurer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/config/WebFluxConfigurer.html) bean with an `addFormatters` method.

Conversion can also be customized using the `spring.webflux.format.*` configuration properties.
When not configured, the following defaults are used:

| Property | `DateTimeFormatter` | Formats |
| --- | --- | --- |
| `spring.webflux.format.date` | `ofLocalizedDate(FormatStyle.SHORT)` | `java.util.Date` and [`LocalDate`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/LocalDate.html) |
| `spring.webflux.format.time` | `ofLocalizedTime(FormatStyle.SHORT)` | java.time’s [`LocalTime`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/LocalTime.html) and [`OffsetTime`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/OffsetTime.html) |
| `spring.webflux.format.date-time` | `ofLocalizedDateTime(FormatStyle.SHORT)` | java.time’s [`LocalDateTime`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/LocalDateTime.html), [`OffsetDateTime`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/OffsetDateTime.html), and [`ZonedDateTime`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/ZonedDateTime.html) |

### HTTP Codecs with HttpMessageReaders and HttpMessageWriters

Spring WebFlux uses the [`HttpMessageReader`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/http/codec/HttpMessageReader.html) and [`HttpMessageWriter`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/http/codec/HttpMessageWriter.html) interfaces to convert HTTP requests and responses.
They are configured with [`CodecConfigurer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/http/codec/CodecConfigurer.html) to have sensible defaults by looking at the libraries available in your classpath.

Spring Boot provides dedicated configuration properties for codecs, `spring.http.codecs.*`.
It also applies further customization by using [`CodecCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/http/codec/CodecCustomizer.html) instances.
For example, `spring.jackson.*` configuration keys are applied to the Jackson codec.

If you need to add or customize codecs, you can create a custom [`CodecCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/http/codec/CodecCustomizer.html) component, as shown in the following example:

* Java
* Kotlin

```
import org.springframework.boot.http.codec.CodecCustomizer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.codec.ServerSentEventHttpMessageReader;

@Configuration(proxyBeanMethods = false)
public class MyCodecsConfiguration {

	@Bean
	public CodecCustomizer myCodecCustomizer() {
		return (configurer) -> {
			configurer.registerDefaults(false);
			configurer.customCodecs().register(new ServerSentEventHttpMessageReader());
			// ...
		};
	}

}
```

```
import org.springframework.boot.http.codec.CodecCustomizer
import org.springframework.context.annotation.Bean
import org.springframework.http.codec.CodecConfigurer
import org.springframework.http.codec.ServerSentEventHttpMessageReader

class MyCodecsConfiguration {

	@Bean
	fun myCodecCustomizer(): CodecCustomizer {
		return CodecCustomizer { configurer: CodecConfigurer ->
			configurer.registerDefaults(false)
			configurer.customCodecs().register(ServerSentEventHttpMessageReader())
		}
	}

}
```

You can also leverage [Boot’s custom JSON serializers and deserializers](../features/json.html#features.json.jackson.custom-serializers-and-deserializers).

### Static Content

By default, Spring Boot serves static content from a directory called `/static` (or `/public` or `/resources` or `/META-INF/resources`) in the classpath.
It uses the [`ResourceWebHandler`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/resource/ResourceWebHandler.html) from Spring WebFlux so that you can modify that behavior by adding your own [`WebFluxConfigurer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/config/WebFluxConfigurer.html) and overriding the `addResourceHandlers` method.

By default, resources are mapped on `/**`, but you can tune that by setting the `spring.webflux.static-path-pattern` property.
For instance, relocating all resources to `/resources/**` can be achieved as follows:

* Properties
* YAML

```
spring.webflux.static-path-pattern=/resources/**
```

```
spring:
  webflux:
    static-path-pattern: "/resources/**"
```

You can also customize the static resource locations by using `spring.web.resources.static-locations`.
Doing so replaces the default values with a list of directory locations.
If you do so, the default welcome page detection switches to your custom locations.
So, if there is an `index.html` in any of your locations on startup, it is the home page of the application.

In addition to the “standard” static resource locations listed earlier, a special case is made for [Webjars content](https://www.webjars.org/).
By default, any resources with a path in `/webjars/**` are served from jar files if they are packaged in the Webjars format.
The path can be customized with the `spring.webflux.webjars-path-pattern` property.

|  |  |
| --- | --- |
|  | Spring WebFlux applications do not strictly depend on the servlet API, so they cannot be deployed as war files and do not use the `src/main/webapp` directory. |

### Welcome Page

Spring Boot supports both static and templated welcome pages.
It first looks for an `index.html` file in the configured static content locations.
If one is not found, it then looks for an `index` template.
If either is found, it is automatically used as the welcome page of the application.

This only acts as a fallback for actual index routes defined by the application.
The ordering is defined by the order of [`HandlerMapping`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/HandlerMapping.html) beans which is by default the following:

|  |  |
| --- | --- |
| `org.springframework.web.reactive.function.server.support.RouterFunctionMapping` | Endpoints declared with [`RouterFunction`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/server/RouterFunction.html) beans |
| `org.springframework.web.reactive.result.method.annotation.RequestMappingHandlerMapping` | Endpoints declared in [`@Controller`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Controller.html) beans |
| `RouterFunctionMapping` for the Welcome Page | The welcome page support |

### Template Engines

As well as REST web services, you can also use Spring WebFlux to serve dynamic HTML content.
Spring WebFlux supports a variety of templating technologies, including Thymeleaf, FreeMarker, and Mustache.

Spring Boot includes auto-configuration support for the following templating engines:

* [FreeMarker](https://freemarker.apache.org/docs/)
* [Thymeleaf](https://www.thymeleaf.org)
* [Mustache](https://mustache.github.io/)

|  |  |
| --- | --- |
|  | Not all FreeMarker features are supported with WebFlux. For more details, check the description of each property. |

When you use one of these templating engines with the default configuration, your templates are picked up automatically from `src/main/resources/templates`.

### Error Handling

Spring Boot provides a [`WebExceptionHandler`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/server/WebExceptionHandler.html) that handles all errors in a sensible way.
Its position in the processing order is immediately before the handlers provided by WebFlux, which are considered last.
For machine clients, it produces a JSON response with details of the error, the HTTP status, and the exception message.
For browser clients, there is a “whitelabel” error handler that renders the same data in HTML format.
You can also provide your own HTML templates to display errors (see the [next section](#web.reactive.webflux.error-handling.error-pages)).

Before customizing error handling in Spring Boot directly, you can leverage the [RFC 9457 Problem Details](https://docs.spring.io/spring-framework/reference/7.0/web/webflux/ann-rest-exceptions.html) support in Spring WebFlux.
Spring WebFlux can produce custom error messages with the `application/problem+json` media type, like:

```
{
	"type": "https://example.org/problems/unknown-project",
	"title": "Unknown project",
	"status": 404,
	"detail": "No project found for id 'spring-unknown'",
	"instance": "/projects/spring-unknown"
}
```

This support can be enabled by setting `spring.webflux.problemdetails.enabled` to `true`.

The first step to customizing this feature often involves using the existing mechanism but replacing or augmenting the error contents.
For that, you can add a bean of type [`ErrorAttributes`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webflux/error/ErrorAttributes.html).

To change the error handling behavior, you can implement [`ErrorWebExceptionHandler`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webflux/error/ErrorWebExceptionHandler.html) and register a bean definition of that type.
Because an [`ErrorWebExceptionHandler`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webflux/error/ErrorWebExceptionHandler.html) is quite low-level, Spring Boot also provides a convenient [`AbstractErrorWebExceptionHandler`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webflux/autoconfigure/error/AbstractErrorWebExceptionHandler.html) to let you handle errors in a WebFlux functional way, as shown in the following example:

* Java
* Kotlin

```
import reactor.core.publisher.Mono;

import org.springframework.boot.autoconfigure.web.WebProperties;
import org.springframework.boot.webflux.autoconfigure.error.AbstractErrorWebExceptionHandler;
import org.springframework.boot.webflux.error.ErrorAttributes;
import org.springframework.context.ApplicationContext;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.codec.ServerCodecConfigurer;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.server.RouterFunction;
import org.springframework.web.reactive.function.server.RouterFunctions;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import org.springframework.web.reactive.function.server.ServerResponse.BodyBuilder;

@Component
public class MyErrorWebExceptionHandler extends AbstractErrorWebExceptionHandler {

	public MyErrorWebExceptionHandler(ErrorAttributes errorAttributes, WebProperties webProperties,
			ApplicationContext applicationContext, ServerCodecConfigurer serverCodecConfigurer) {
		super(errorAttributes, webProperties.getResources(), applicationContext);
		setMessageReaders(serverCodecConfigurer.getReaders());
		setMessageWriters(serverCodecConfigurer.getWriters());
	}

	@Override
	protected RouterFunction<ServerResponse> getRoutingFunction(ErrorAttributes errorAttributes) {
		return RouterFunctions.route(this::acceptsXml, this::handleErrorAsXml);
	}

	private boolean acceptsXml(ServerRequest request) {
		return request.headers().accept().contains(MediaType.APPLICATION_XML);
	}

	public Mono<ServerResponse> handleErrorAsXml(ServerRequest request) {
		BodyBuilder builder = ServerResponse.status(HttpStatus.INTERNAL_SERVER_ERROR);
		// ... additional builder calls
		return builder.build();
	}

}
```

```
import org.springframework.boot.autoconfigure.web.WebProperties
import org.springframework.boot.webflux.error.ErrorAttributes
import org.springframework.boot.webflux.autoconfigure.error.AbstractErrorWebExceptionHandler
import org.springframework.context.ApplicationContext
import org.springframework.http.HttpStatus
import org.springframework.http.MediaType
import org.springframework.http.codec.ServerCodecConfigurer
import org.springframework.stereotype.Component
import org.springframework.web.reactive.function.server.RouterFunction
import org.springframework.web.reactive.function.server.RouterFunctions
import org.springframework.web.reactive.function.server.ServerRequest
import org.springframework.web.reactive.function.server.ServerResponse
import reactor.core.publisher.Mono

@Component
class MyErrorWebExceptionHandler(
		errorAttributes: ErrorAttributes, webProperties: WebProperties,
		applicationContext: ApplicationContext, serverCodecConfigurer: ServerCodecConfigurer
) : AbstractErrorWebExceptionHandler(errorAttributes, webProperties.resources, applicationContext) {

	init {
		setMessageReaders(serverCodecConfigurer.readers)
		setMessageWriters(serverCodecConfigurer.writers)
	}

	override fun getRoutingFunction(errorAttributes: ErrorAttributes): RouterFunction<ServerResponse> {
		return RouterFunctions.route(this::acceptsXml, this::handleErrorAsXml)
	}

	private fun acceptsXml(request: ServerRequest): Boolean {
		return request.headers().accept().contains(MediaType.APPLICATION_XML)
	}

	fun handleErrorAsXml(request: ServerRequest): Mono<ServerResponse> {
		val builder = ServerResponse.status(HttpStatus.INTERNAL_SERVER_ERROR)
		// ... additional builder calls
		return builder.build()
	}

}
```

For a more complete picture, you can also subclass [`DefaultErrorWebExceptionHandler`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webflux/autoconfigure/error/DefaultErrorWebExceptionHandler.html) directly and override specific methods.

In some cases, errors handled at the controller level are not recorded by web observations or the [metrics infrastructure](../actuator/metrics.html#actuator.metrics.supported.spring-webflux).
Applications can ensure that such exceptions are recorded with the observations by [setting the handled exception on the observation context](https://docs.spring.io/spring-framework/reference/7.0/integration/observability.html#observability.http-server.reactive).

#### Custom Error Pages

If you want to display a custom HTML error page for a given status code, you can add views that resolve from `error/*`, for example by adding files to a `/error` directory.
Error pages can either be static HTML (that is, added under any of the static resource directories) or built with templates.
The name of the file should be the exact status code, a status code series mask, or `error` for a default if nothing else matches.
Note that the path to the default error view is `error/error`, whereas with Spring MVC the default error view is `error`.

For example, to map `404` to a static HTML file, your directory structure would be as follows:

```
src/
 +- main/
     +- java/
     |   + <source code>
     +- resources/
         +- public/
             +- error/
             |   +- 404.html
             +- <other public assets>
```

To map all `5xx` errors by using a Mustache template, your directory structure would be as follows:

```
src/
 +- main/
     +- java/
     |   + <source code>
     +- resources/
         +- templates/
             +- error/
             |   +- 5xx.mustache
             +- <other templates>
```

### Web Filters

Spring WebFlux provides a [`WebFilter`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/server/WebFilter.html) interface that can be implemented to filter HTTP request-response exchanges.
[`WebFilter`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/server/WebFilter.html) beans found in the application context will be automatically used to filter each exchange.

Where the order of the filters is important they can implement [`Ordered`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/Ordered.html) or be annotated with [`@Order`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/annotation/Order.html).
Spring Boot auto-configuration may configure web filters for you.
When it does so, the orders shown in the following table will be used:

| Web Filter | Order |
| --- | --- |
| [`WebFilterChainProxy`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/web/server/WebFilterChainProxy.html) (Spring Security) | `-100` |
| [`HttpExchangesWebFilter`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webflux/actuate/web/exchanges/HttpExchangesWebFilter.html) | `Ordered.LOWEST_PRECEDENCE - 10` |

### API Versioning

Spring WebFlux supports API versioning which can be used to evolve an HTTP API over time.
The same `@Controller` path can be mapped multiple times to support different versions of the API.

For more details see [Spring Framework’s reference documentation](https://docs.spring.io/spring-framework/reference/7.0/web/webflux/controller/ann-requestmapping.html#webflux-ann-requestmapping-version).

Once mappings have been added, you additionally need to configure Spring WebFlux so that it is able to use any version information sent with a request.
Typically, versions are sent as HTTP headers, query parameters, media type parameters, or as part of the path.

To configure Spring WebFlux, you can either use a [`WebFluxConfigurer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/config/WebFluxConfigurer.html) bean and override the `configureApiVersioning(…​)` method, or you can use properties.

For example, the following will use an `X-Version` HTTP header to obtain version information and default to `1.0.0` when no header is sent.

* Properties
* YAML

```
spring.webflux.apiversion.default=1.0.0
spring.webflux.apiversion.use.header=X-Version
```

```
spring:
  webflux:
    apiversion:
      default: 1.0.0
      use:
        header: X-Version
```

|  |  |
| --- | --- |
|  | If your setup requires multiple strategies, such as header and query parameter, consider declaring the order programmatically by overriding the `configureApiVersioning` method. |

For more complete control, you can also define [`ApiVersionResolver`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/accept/ApiVersionResolver.html), [`ApiVersionParser`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/accept/ApiVersionParser.html) and [`ApiVersionDeprecationHandler`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/accept/ApiVersionDeprecationHandler.html) beans which will be injected into the auto-configured Spring WebFlux configuration.

|  |  |
| --- | --- |
|  | API versioning is also supported on the client-side with both `WebClient` and `RestClient`. See [API Versioning](../io/rest-client.html#io.rest-client.apiversioning) for details. |

## Embedded Reactive Server Support

Spring Boot includes support for the following embedded reactive web servers: Reactor Netty, Tomcat, and Jetty.
Most developers use the appropriate starter to obtain a fully configured instance.
By default, the embedded server listens for HTTP requests on port 8080.

### Customizing Reactive Servers

Common reactive web server settings can be configured by using Spring [`Environment`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/env/Environment.html) properties.
Usually, you would define the properties in your `application.properties` or `application.yaml` file.

Common server settings include:

* Network settings: Listen port for incoming HTTP requests (`server.port`), interface address to bind to (`server.address`), and so on.
* Error management: Location of the error page (`spring.web.error.path`) and so on.
* [SSL](../../how-to/webserver.html#howto.webserver.configure-ssl)
* [HTTP compression](../../how-to/webserver.html#howto.webserver.enable-response-compression)

Spring Boot tries as much as possible to expose common settings, but this is not always possible.
For those cases, dedicated namespaces such as `server.netty.*` offer server-specific customizations.

|  |  |
| --- | --- |
|  | See the [`ServerProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/web/server/autoconfigure/ServerProperties.html) class for a complete list. |

#### Programmatic Customization

If you need to programmatically configure your reactive web server, you can register a Spring bean that implements the [`WebServerFactoryCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/web/server/WebServerFactoryCustomizer.html) interface.
[`WebServerFactoryCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/web/server/WebServerFactoryCustomizer.html) provides access to the [`ConfigurableReactiveWebServerFactory`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/web/server/reactive/ConfigurableReactiveWebServerFactory.html), which includes numerous customization setter methods.
The following example shows programmatically setting the port:

* Java
* Kotlin

```
import org.springframework.boot.web.server.WebServerFactoryCustomizer;
import org.springframework.boot.web.server.reactive.ConfigurableReactiveWebServerFactory;
import org.springframework.stereotype.Component;

@Component
public class MyWebServerFactoryCustomizer implements WebServerFactoryCustomizer<ConfigurableReactiveWebServerFactory> {

	@Override
	public void customize(ConfigurableReactiveWebServerFactory server) {
		server.setPort(9000);
	}

}
```

```
import org.springframework.boot.web.server.WebServerFactoryCustomizer
import org.springframework.boot.web.server.reactive.ConfigurableReactiveWebServerFactory
import org.springframework.stereotype.Component

@Component
class MyWebServerFactoryCustomizer : WebServerFactoryCustomizer<ConfigurableReactiveWebServerFactory> {

	override fun customize(server: ConfigurableReactiveWebServerFactory) {
		server.setPort(9000)
	}

}
```

[`JettyReactiveWebServerFactory`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jetty/reactive/JettyReactiveWebServerFactory.html), [`NettyReactiveWebServerFactory`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/reactor/netty/NettyReactiveWebServerFactory.html), and [`TomcatReactiveWebServerFactory`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/tomcat/reactive/TomcatReactiveWebServerFactory.html) are dedicated variants of [`ConfigurableReactiveWebServerFactory`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/web/server/reactive/ConfigurableReactiveWebServerFactory.html) that have additional customization setter methods for Jetty, Reactor Netty, and Tomcat respectively.
The following example shows how to customize [`NettyReactiveWebServerFactory`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/reactor/netty/NettyReactiveWebServerFactory.html) that provides access to Reactor Netty-specific configuration options:

* Java
* Kotlin

```
import java.time.Duration;

import org.springframework.boot.reactor.netty.NettyReactiveWebServerFactory;
import org.springframework.boot.web.server.WebServerFactoryCustomizer;
import org.springframework.stereotype.Component;

@Component
public class MyNettyWebServerFactoryCustomizer implements WebServerFactoryCustomizer<NettyReactiveWebServerFactory> {

	@Override
	public void customize(NettyReactiveWebServerFactory factory) {
		factory.addServerCustomizers((server) -> server.idleTimeout(Duration.ofSeconds(20)));
	}

}
```

```
import org.springframework.boot.web.server.WebServerFactoryCustomizer
import org.springframework.boot.reactor.netty.NettyReactiveWebServerFactory
import org.springframework.stereotype.Component
import java.time.Duration

@Component
class MyNettyWebServerFactoryCustomizer : WebServerFactoryCustomizer<NettyReactiveWebServerFactory> {

	override fun customize(factory: NettyReactiveWebServerFactory) {
		factory.addServerCustomizers({ server -> server.idleTimeout(Duration.ofSeconds(20)) })
	}

}
```

#### Customizing ConfigurableReactiveWebServerFactory Directly

For more advanced use cases that require you to extend from [`ReactiveWebServerFactory`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/web/server/reactive/ReactiveWebServerFactory.html), you can expose a bean of such type yourself.

Setters are provided for many configuration options.
Several protected method “hooks” are also provided should you need to do something more exotic.
See the [`ConfigurableReactiveWebServerFactory`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/web/server/reactive/ConfigurableReactiveWebServerFactory.html) API documentation for details.

|  |  |
| --- | --- |
|  | Auto-configured customizers are still applied on your custom factory, so use that option carefully. |

## Reactive Server Resources Configuration

When auto-configuring a Reactor Netty or Jetty server, Spring Boot will create specific beans that will provide HTTP resources to the server instance: [`ReactorResourceFactory`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/http/client/ReactorResourceFactory.html) or [`JettyResourceFactory`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/http/client/reactive/JettyResourceFactory.html).

By default, those resources will be also shared with the Reactor Netty and Jetty clients for optimal performances, given:

* the same technology is used for server and client
* the client instance is built using the [`WebClient.Builder`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/WebClient.Builder.html) bean auto-configured by Spring Boot

Developers can override the resource configuration for Jetty and Reactor Netty by providing a custom [`ReactorResourceFactory`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/http/client/ReactorResourceFactory.html) or [`JettyResourceFactory`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/http/client/reactive/JettyResourceFactory.html) bean - this will be applied to both clients and servers.

You can learn more about the resource configuration on the client side in the [WebClient Runtime](../io/rest-client.html#io.rest-client.webclient.runtime) section.