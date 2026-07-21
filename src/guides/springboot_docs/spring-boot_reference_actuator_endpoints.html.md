Search

# Endpoints

Actuator endpoints let you monitor and interact with your application.
Spring Boot includes a number of built-in endpoints and lets you add your own.
For example, the `health` endpoint provides basic application health information.

You can [control access](#actuator.endpoints.controlling-access) to each individual endpoint and [expose them (make them remotely accessible) over HTTP or JMX](#actuator.endpoints.exposing).
An endpoint is considered to be available when access to it is permitted and it is exposed.
The built-in endpoints are auto-configured only when they are available.
Most applications choose exposure over HTTP, where the ID of the endpoint and a prefix of `/actuator` is mapped to a URL.
For example, by default, the `health` endpoint is mapped to `/actuator/health`.

|  |  |
| --- | --- |
|  | To learn more about the Actuator’s endpoints and their request and response formats, see the [API documentation](../../api/rest/actuator/index.html). |

The following technology-agnostic endpoints are available:

| ID | Description |
| --- | --- |
| `auditevents` | Exposes audit events information for the current application. Requires an [`AuditEventRepository`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/audit/AuditEventRepository.html) bean. |
| `beans` | Displays a complete list of all the Spring beans in your application. |
| `caches` | Exposes available caches. |
| `conditions` | Shows the conditions that were evaluated on configuration and auto-configuration classes and the reasons why they did or did not match. |
| `configprops` | Displays a collated list of all [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html). Subject to [sanitization](#actuator.endpoints.sanitization). |
| `env` | Exposes properties from Spring’s [`ConfigurableEnvironment`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/env/ConfigurableEnvironment.html). Subject to [sanitization](#actuator.endpoints.sanitization). |
| `flyway` | Shows any Flyway database migrations that have been applied. Requires one or more [`Flyway`](https://javadoc.io/doc/org.flywaydb/flyway-core/12.4.0/org/flywaydb/core/Flyway.html) beans. |
| `health` | Shows application health information. |
| `httpexchanges` | Displays HTTP exchange information (by default, the last 100 HTTP request-response exchanges). Requires an [`HttpExchangeRepository`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/web/exchanges/HttpExchangeRepository.html) bean. |
| `info` | Displays arbitrary application info. |
| `integrationgraph` | Shows the Spring Integration graph. Requires a dependency on `spring-integration-core`. |
| `loggers` | Shows and modifies the configuration of loggers in the application. |
| `liquibase` | Shows any Liquibase database migrations that have been applied. Requires one or more [`Liquibase`](https://javadoc.io/doc/org.liquibase/liquibase-core/5.0.3/liquibase/Liquibase.html) beans. |
| `metrics` | Shows “metrics” information for the current application to diagnose the metrics the application has recorded. |
| `mappings` | Displays a collated list of all [`@RequestMapping`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/bind/annotation/RequestMapping.html) paths. |
| `quartz` | Shows information about Quartz Scheduler jobs. Subject to [sanitization](#actuator.endpoints.sanitization). |
| `scheduledtasks` | Displays the scheduled tasks in your application. |
| `sessions` | Allows retrieval and deletion of user sessions from a Spring Session-backed session store. Requires a servlet-based web application that uses Spring Session. |
| `shutdown` | Lets the application be gracefully shutdown. Only works when using jar packaging. Disabled by default. |
| `startup` | Shows the [startup steps data](../features/spring-application.html#features.spring-application.startup-tracking) collected by the [`ApplicationStartup`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/metrics/ApplicationStartup.html). Requires the [`SpringApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/SpringApplication.html) to be configured with a [`BufferingApplicationStartup`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/metrics/buffering/BufferingApplicationStartup.html). |
| `threaddump` | Performs a thread dump. |

If your application is a web application (Spring MVC, Spring WebFlux, or Jersey), you can use the following additional endpoints:

| ID | Description |
| --- | --- |
| `heapdump` | Returns a heap dump file. On a HotSpot JVM, an `HPROF`-format file is returned. On an OpenJ9 JVM, a `PHD`-format file is returned. |
| `logfile` | Returns the contents of the logfile (if the `logging.file.name` or the `logging.file.path` property has been set). Supports the use of the HTTP `Range` header to retrieve part of the log file’s content. |
| `prometheus` | Exposes metrics in a format that can be scraped by a Prometheus server. Requires a dependency on `micrometer-registry-prometheus`. |

## Controlling Access to Endpoints

By default, access to all endpoints except for `shutdown` and `heapdump` is unrestricted.
To configure the permitted access to an endpoint, use its `management.endpoint.<id>.access` property.
The following example allows unrestricted access to the `shutdown` endpoint:

* Properties
* YAML

```
management.endpoint.shutdown.access=unrestricted
```

```
management:
  endpoint:
    shutdown:
      access: unrestricted
```

If you prefer access to be opt-in rather than opt-out, set the `management.endpoints.access.default` property to `none` and use individual endpoint `access` properties to opt back in.
The following example allows read-only access to the `loggers` endpoint and denies access to all other endpoints:

* Properties
* YAML

```
management.endpoints.access.default=none
management.endpoint.loggers.access=read-only
```

```
management:
  endpoints:
    access:
      default: none
  endpoint:
    loggers:
      access: read-only
```

|  |  |
| --- | --- |
|  | Inaccessible endpoints are removed entirely from the application context. If you want to change only the technologies over which an endpoint is exposed, use the [`include` and `exclude` properties](#actuator.endpoints.exposing) instead. |

### Limiting Access

Application-wide endpoint access can be limited using the `management.endpoints.access.max-permitted` property.
This property takes precedence over the default access or an individual endpoint’s access level.
Set it to `none` to make all endpoints inaccessible.
Set it to `read-only` to only allow read access to endpoints.

For [`@Endpoint`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/annotation/Endpoint.html), [`@JmxEndpoint`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/jmx/annotation/JmxEndpoint.html), and [`@WebEndpoint`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/web/annotation/WebEndpoint.html), read access equates to the endpoint methods annotated with [`@ReadOperation`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/annotation/ReadOperation.html).
For [`@ControllerEndpoint`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/web/annotation/ControllerEndpoint.html) and [`@RestControllerEndpoint`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/web/annotation/RestControllerEndpoint.html), read access equates to request mappings that can handle `GET` and `HEAD` requests.
For [`@ServletEndpoint`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/web/annotation/ServletEndpoint.html), read access equates to `GET` and `HEAD` requests.

## Exposing Endpoints

By default, only the health endpoint is exposed over HTTP and JMX.
Since Endpoints may contain sensitive information, you should carefully consider when to expose them.

To change which endpoints are exposed, use the following technology-specific `include` and `exclude` properties:

| Property | Default |
| --- | --- |
| `management.endpoints.jmx.exposure.exclude` |  |
| `management.endpoints.jmx.exposure.include` | `health` |
| `management.endpoints.web.exposure.exclude` |  |
| `management.endpoints.web.exposure.include` | `health` |

The `include` property lists the IDs of the endpoints that are exposed.
The `exclude` property lists the IDs of the endpoints that should not be exposed.
The `exclude` property takes precedence over the `include` property.
You can configure both the `include` and the `exclude` properties with a list of endpoint IDs.

For example, to only expose the `health` and `info` endpoints over JMX, use the following property:

* Properties
* YAML

```
management.endpoints.jmx.exposure.include=health,info
```

```
management:
  endpoints:
    jmx:
      exposure:
        include: "health,info"
```

`*` can be used to select all endpoints.
For example, to expose everything over HTTP except the `env` and `beans` endpoints, use the following properties:

* Properties
* YAML

```
management.endpoints.web.exposure.include=*
management.endpoints.web.exposure.exclude=env,beans
```

```
management:
  endpoints:
    web:
      exposure:
        include: "*"
        exclude: "env,beans"
```

|  |  |
| --- | --- |
|  | `*` has a special meaning in YAML, so be sure to add quotation marks if you want to include (or exclude) all endpoints. |

|  |  |
| --- | --- |
|  | If your application is exposed publicly, we strongly recommend that you also [secure your endpoints](#actuator.endpoints.security). |

|  |  |
| --- | --- |
|  | If you want to implement your own strategy for when endpoints are exposed, you can register an [`EndpointFilter`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/EndpointFilter.html) bean. |

## Security

For security purposes, only the `/health` endpoint is exposed over HTTP by default.
You can use the `management.endpoints.web.exposure.include` property to configure the endpoints that are exposed.

|  |  |
| --- | --- |
|  | Before setting the `management.endpoints.web.exposure.include`, ensure that the exposed actuators do not contain sensitive information, are secured by placing them behind a firewall, or are secured by something like Spring Security. |

If Spring Security is on the classpath and no other [`SecurityFilterChain`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/web/SecurityFilterChain.html) bean is present, all actuators other than `/health` are secured by Spring Boot auto-configuration.
If you define a custom [`SecurityFilterChain`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/web/SecurityFilterChain.html) bean, Spring Boot auto-configuration backs off and lets you fully control the actuator access rules.

If you wish to configure custom security for HTTP endpoints (for example, to allow only users with a certain role to access them), Spring Boot provides some convenient [`RequestMatcher`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/web/util/matcher/RequestMatcher.html) objects that you can use in combination with Spring Security.

A typical Spring Security configuration might look something like the following example:

* Java
* Kotlin

```
import org.springframework.boot.security.autoconfigure.actuate.web.servlet.EndpointRequest;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

import static org.springframework.security.config.Customizer.withDefaults;

@Configuration(proxyBeanMethods = false)
public class MySecurityConfiguration {

	@Bean
	public SecurityFilterChain securityFilterChain(HttpSecurity http) {
		http.securityMatcher(EndpointRequest.toAnyEndpoint());
		http.authorizeHttpRequests((requests) -> requests.anyRequest().hasRole("ENDPOINT_ADMIN"));
		http.httpBasic(withDefaults());
		return http.build();
	}

}
```

```
import org.springframework.boot.security.autoconfigure.actuate.web.servlet.EndpointRequest
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.security.config.Customizer.withDefaults
import org.springframework.security.config.annotation.web.builders.HttpSecurity
import org.springframework.security.web.SecurityFilterChain

@Configuration(proxyBeanMethods = false)
class MySecurityConfiguration {

	@Bean
	fun securityFilterChain(http: HttpSecurity): SecurityFilterChain {
		http.securityMatcher(EndpointRequest.toAnyEndpoint()).authorizeHttpRequests { requests ->
			requests.anyRequest().hasRole("ENDPOINT_ADMIN")
		}
		http.httpBasic(withDefaults())
		return http.build()
	}

}
```

The preceding example uses `EndpointRequest.toAnyEndpoint()` to match a request to any endpoint and then ensures that all have the `ENDPOINT_ADMIN` role.
Several other matcher methods are also available on [`EndpointRequest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/security/autoconfigure/actuate/web/servlet/EndpointRequest.html).
See the [API documentation](../../api/rest/actuator/index.html) for details.

|  |  |
| --- | --- |
|  | When matching for Actuator endpoints, `EndpointRequest.to("endpoint")` will consider the endpoint root and all its subpaths, effectively matching `"/actuator/endpoint/**"` even if the endpoint does not declare nested routes. |

If you deploy applications behind a firewall, you may prefer that all your actuator endpoints can be accessed without requiring authentication.
You can do so by changing the `management.endpoints.web.exposure.include` property, as follows:

* Properties
* YAML

```
management.endpoints.web.exposure.include=*
```

```
management:
  endpoints:
    web:
      exposure:
        include: "*"
```

Additionally, if Spring Security is present, you would need to add custom security configuration that allows unauthenticated access to the endpoints, as the following example shows:

* Java
* Kotlin

```
import org.springframework.boot.security.autoconfigure.actuate.web.servlet.EndpointRequest;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration(proxyBeanMethods = false)
public class MySecurityConfiguration {

	@Bean
	public SecurityFilterChain securityFilterChain(HttpSecurity http) {
		http.securityMatcher(EndpointRequest.toAnyEndpoint());
		http.authorizeHttpRequests((requests) -> requests.anyRequest().permitAll());
		return http.build();
	}

}
```

```
import org.springframework.boot.security.autoconfigure.actuate.web.servlet.EndpointRequest
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.security.config.annotation.web.builders.HttpSecurity
import org.springframework.security.web.SecurityFilterChain

@Configuration(proxyBeanMethods = false)
class MySecurityConfiguration {

	@Bean
	fun securityFilterChain(http: HttpSecurity): SecurityFilterChain {
		http.securityMatcher(EndpointRequest.toAnyEndpoint()).authorizeHttpRequests { requests ->
			requests.anyRequest().permitAll()
		}
		return http.build()
	}

}
```

|  |  |
| --- | --- |
|  | In both of the preceding examples, the configuration applies only to the actuator endpoints. Since Spring Boot’s security configuration backs off completely in the presence of any [`SecurityFilterChain`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/web/SecurityFilterChain.html) bean, you need to configure an additional [`SecurityFilterChain`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/web/SecurityFilterChain.html) bean with rules that apply to the rest of the application. |

### Cross Site Request Forgery Protection

Since Spring Boot relies on Spring Security’s defaults, CSRF protection is turned on by default.
This means that the actuator endpoints that require a `POST` (shutdown and loggers endpoints), a `PUT`, or a `DELETE` get a 403 (forbidden) error when the default security configuration is in use.

|  |  |
| --- | --- |
|  | We recommend disabling CSRF protection completely only if you are creating a service that is used by non-browser clients. |

You can find additional information about CSRF protection in the [Spring Security Reference Guide](https://docs.spring.io/spring-security/reference/7.1/features/exploits/csrf.html).

## Configuring Endpoints

Endpoints automatically cache responses to read operations that do not take any parameters.
To configure the amount of time for which an endpoint caches a response, use its `cache.time-to-live` property.
The following example sets the time-to-live of the `beans` endpoint’s cache to 10 seconds:

* Properties
* YAML

```
management.endpoint.beans.cache.time-to-live=10s
```

```
management:
  endpoint:
    beans:
      cache:
        time-to-live: "10s"
```

|  |  |
| --- | --- |
|  | The `management.endpoint.<name>` prefix uniquely identifies the endpoint that is being configured. |

## Sanitize Sensitive Values

Information returned by the `/env`, `/configprops` and `/quartz` endpoints can be sensitive, so by default values are always fully sanitized (replaced by `******`).

Values can only be viewed in an unsanitized form when:

* The `show-values` property has been set to something other than `never`
* No custom [`SanitizingFunction`](../../how-to/actuator.html#howto.actuator.customizing-sanitization) beans apply

The `show-values` property can be configured for sanitizable endpoints to one of the following values:

* `never` - values are always fully sanitized (replaced by `******`)
* `always` - values are shown to all users (as long as no [`SanitizingFunction`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/SanitizingFunction.html) bean applies)
* `when-authorized` - values are shown only to authorized users (as long as no [`SanitizingFunction`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/SanitizingFunction.html) bean applies)

For HTTP endpoints, a user is considered to be authorized if they have authenticated and have the roles configured by the endpoint’s roles property.
By default, any authenticated user is authorized.

For JMX endpoints, all users are always authorized.

The following example allows all users with the `admin` role to view values from the `/env` endpoint in their original form.
Unauthorized users, or users without the `admin` role, will see only sanitized values.

* Properties
* YAML

```
management.endpoint.env.show-values=when-authorized
management.endpoint.env.roles=admin
```

```
management:
  endpoint:
    env:
      show-values: when-authorized
      roles: "admin"
```

|  |  |
| --- | --- |
|  | This example assumes that no [`SanitizingFunction`](../../how-to/actuator.html#howto.actuator.customizing-sanitization) beans have been defined. |

## Hypermedia for Actuator Web Endpoints

A “discovery page” is added with links to all the endpoints.
The “discovery page” is available on `/actuator` by default.

To disable the “discovery page”, add the following property to your application properties:

* Properties
* YAML

```
management.endpoints.web.discovery.enabled=false
```

```
management:
  endpoints:
    web:
      discovery:
        enabled: false
```

When a custom management context path is configured, the “discovery page” automatically moves from `/actuator` to the root of the management context.
For example, if the management context path is `/management`, the discovery page is available from `/management`.
When the management context path is set to `/`, the discovery page is disabled to prevent the possibility of a clash with other mappings.

## CORS Support

[Cross-origin resource sharing](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) (CORS) is a [W3C specification](https://www.w3.org/TR/cors/) that lets you specify in a flexible way what kind of cross-domain requests are authorized.
If you use Spring MVC or Spring WebFlux, you can configure Actuator’s web endpoints to support such scenarios.

CORS support is disabled by default and is only enabled once you have set the `management.endpoints.web.cors.allowed-origins` property.
The following configuration permits `GET` and `POST` calls from the `example.com` domain:

* Properties
* YAML

```
management.endpoints.web.cors.allowed-origins=https://example.com
management.endpoints.web.cors.allowed-methods=GET,POST
```

```
management:
  endpoints:
    web:
      cors:
        allowed-origins: "https://example.com"
        allowed-methods: "GET,POST"
```

|  |  |
| --- | --- |
|  | See [`CorsEndpointProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/autoconfigure/endpoint/web/CorsEndpointProperties.html) for a complete list of options. |

## JSON

When working with JSON, Jackson is used for serialization and deserialization.
By default, an isolated [`JsonMapper`](https://javadoc.io/doc/tools.jackson.core/jackson-databind/3.1.4/tools/jackson/databind/json/JsonMapper.html) is used.
This isolation means that it does not share the same configuration as the application’s `JsonMapper` and it is not affected by `spring.jackson.*` properties.
To disable this behavior and configure Actuator to use the application’s `JsonMapper`, set `management.endpoints.jackson.isolated-json-mapper` to `false`.
Alternatively, you can define your own [`EndpointJsonMapper`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/jackson/EndpointJsonMapper.html) bean that produces a `JsonMapper` that meets your needs.
Actuator will then use it for JSON processing.

## Implementing Custom Endpoints

If you add a [`@Bean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Bean.html) annotated with [`@Endpoint`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/annotation/Endpoint.html), any methods annotated with [`@ReadOperation`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/annotation/ReadOperation.html), [`@WriteOperation`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/annotation/WriteOperation.html), or [`@DeleteOperation`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/annotation/DeleteOperation.html) are automatically exposed over JMX and, in a web application, over HTTP as well.
Endpoints can be exposed over HTTP by using Jersey, Spring MVC, or Spring WebFlux.
If both Jersey and Spring MVC are available, Spring MVC is used.

The following example exposes a read operation that returns a custom object:

* Java
* Kotlin

```
	@ReadOperation
	public CustomData getData() {
		return new CustomData("test", 5);
	}
```

```
	@ReadOperation
	fun getData(): CustomData {
		return CustomData("test", 5)
	}
```

You can also write technology-specific endpoints by using [`@JmxEndpoint`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/jmx/annotation/JmxEndpoint.html) or [`@WebEndpoint`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/web/annotation/WebEndpoint.html).
These endpoints are restricted to their respective technologies.
For example, [`@WebEndpoint`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/web/annotation/WebEndpoint.html) is exposed only over HTTP and not over JMX.

You can write technology-specific extensions by using [`@EndpointWebExtension`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/web/annotation/EndpointWebExtension.html) and [`@EndpointJmxExtension`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/jmx/annotation/EndpointJmxExtension.html).
These annotations let you provide technology-specific operations to augment an existing endpoint.
An endpoint may have at most one extension of each type.

Finally, if you need access to web-framework-specific functionality, you can implement servlet or Spring [`@Controller`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Controller.html) and [`@RestController`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/bind/annotation/RestController.html) endpoints at the cost of them not being available over JMX or when using a different web framework.

### Receiving Input

Operations on an endpoint receive input through their parameters.
When exposed over the web, the values for these parameters are taken from the URL’s query parameters and from the JSON request body.
When exposed over JMX, the parameters are mapped to the parameters of the MBean’s operations.
Parameters are required by default.
They can be made optional by annotating them with JSpecify’s [`@Nullable`](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html).
Kotlin null safety is also supported.

You can map each root property in the JSON request body to a parameter of the endpoint.
Consider the following JSON request body:

```
{
	"name": "test",
	"counter": 42
}
```

You can use this to invoke a write operation that takes `String name` and `int counter` parameters, as the following example shows:

* Java
* Kotlin

```
	@WriteOperation
	public void updateData(String name, int counter) {
		// injects "test" and 42
	}
```

```
	@WriteOperation
	fun updateData(name: String?, counter: Int) {
		// injects "test" and 42
	}
```

|  |  |
| --- | --- |
|  | Because endpoints are technology agnostic, only simple types can be specified in the method signature. In particular, declaring a single parameter with a [`CustomData`](https://javadoc.io/doc/org.liquibase/liquibase-core/5.0.3/liquibase/report/CustomData.html) type that defines a `name` and `counter` properties is not supported. |

|  |  |
| --- | --- |
|  | To let the input be mapped to the operation method’s parameters, Java code that implements an endpoint should be compiled with `-parameters`. For Kotlin code, please review [the recommendation](https://docs.spring.io/spring-framework/reference/7.0/languages/kotlin/classes-interfaces.html) of the Spring Framework reference. This will happen automatically if you use Spring Boot’s Gradle plugin or if you use Maven and `spring-boot-starter-parent`. |

#### Input Type Conversion

The parameters passed to endpoint operation methods are, if necessary, automatically converted to the required type.
Before calling an operation method, the input received over JMX or HTTP is converted to the required types by using an instance of [`ApplicationConversionService`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/convert/ApplicationConversionService.html) as well as any [`Converter`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/convert/converter/Converter.html) or [`GenericConverter`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/convert/converter/GenericConverter.html) beans qualified with [`@EndpointConverter`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/annotation/EndpointConverter.html).

### Custom Web Endpoints

Operations on an [`@Endpoint`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/annotation/Endpoint.html), [`@WebEndpoint`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/web/annotation/WebEndpoint.html), or [`@EndpointWebExtension`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/web/annotation/EndpointWebExtension.html) are automatically exposed over HTTP using Jersey, Spring MVC, or Spring WebFlux.
If both Jersey and Spring MVC are available, Spring MVC is used.

#### Web Endpoint Request Predicates

A request predicate is automatically generated for each operation on a web-exposed endpoint.

#### Path

The path of the predicate is determined by the ID of the endpoint and the base path of the web-exposed endpoints.
The default base path is `/actuator`.
For example, an endpoint with an ID of `sessions` uses `/actuator/sessions` as its path in the predicate.

You can further customize the path by annotating one or more parameters of the operation method with [`@Selector`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/annotation/Selector.html).
Such a parameter is added to the path predicate as a path variable.
The variable’s value is passed into the operation method when the endpoint operation is invoked.
If you want to capture all remaining path elements, you can add `@Selector(Match=ALL_REMAINING)` to the last parameter and make it a type that is conversion-compatible with a `String[]`.

#### HTTP method

The HTTP method of the predicate is determined by the operation type, as shown in the following table:

| Operation | HTTP method |
| --- | --- |
| [`@ReadOperation`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/annotation/ReadOperation.html) | `GET` |
| [`@WriteOperation`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/annotation/WriteOperation.html) | `POST` |
| [`@DeleteOperation`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/annotation/DeleteOperation.html) | `DELETE` |

#### Consumes

For a [`@WriteOperation`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/annotation/WriteOperation.html) (HTTP `POST`) that uses the request body, the `consumes` clause of the predicate is `application/vnd.spring-boot.actuator.v2+json, application/json`.
For all other operations, the `consumes` clause is empty.

#### Produces

The `produces` clause of the predicate can be determined by the `produces` attribute of the [`@DeleteOperation`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/annotation/DeleteOperation.html), [`@ReadOperation`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/annotation/ReadOperation.html), and [`@WriteOperation`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/annotation/WriteOperation.html) annotations.
The attribute is optional.
If it is not used, the `produces` clause is determined automatically.

If the operation method returns `void` or [`Void`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Void.html), the `produces` clause is empty.
If the operation method returns a [`Resource`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/io/Resource.html), the `produces` clause is `application/octet-stream`.
For all other operations, the `produces` clause is `application/vnd.spring-boot.actuator.v2+json, application/json`.

#### Web Endpoint Response Status

The default response status for an endpoint operation depends on the operation type (read, write, or delete) and what, if anything, the operation returns.

If a [`@ReadOperation`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/annotation/ReadOperation.html) returns a value, the response status will be 200 (OK).
If it does not return a value, the response status will be 404 (Not Found).

If a [`@WriteOperation`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/annotation/WriteOperation.html) or [`@DeleteOperation`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/annotation/DeleteOperation.html) returns a value, the response status will be 200 (OK).
If it does not return a value, the response status will be 204 (No Content).

If an operation is invoked without a required parameter or with a parameter that cannot be converted to the required type, the operation method is not called, and the response status will be 400 (Bad Request).

#### Web Endpoint Range Requests

You can use an HTTP range request to request part of an HTTP resource.
When using Spring MVC or Spring Web Flux, operations that return a [`Resource`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/io/Resource.html) automatically support range requests.

|  |  |
| --- | --- |
|  | Range requests are not supported when using Jersey. |

#### Web Endpoint Security

An operation on a web endpoint or a web-specific endpoint extension can receive the current [`Principal`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/security/Principal.html) or [`SecurityContext`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/endpoint/SecurityContext.html) as a method parameter.
The former is typically used in conjunction with [`@Nullable`](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html) to provide different behavior for authenticated and unauthenticated users.
The latter is typically used to perform authorization checks by using its `isUserInRole(String)` method.

## Health Information

You can use health information to check the status of your running application.
It is often used by monitoring software to alert someone when a production system goes down.
The information exposed by the `health` endpoint depends on the `management.endpoint.health.show-details` and `management.endpoint.health.show-components` properties, which can be configured with one of the following values:

| Name | Description |
| --- | --- |
| `never` | Details are never shown. |
| `when-authorized` | Details are shown only to authorized users. Authorized roles can be configured by using `management.endpoint.health.roles`. |
| `always` | Details are shown to all users. |

The default value is `never`.
A user is considered to be authorized when they are in one or more of the endpoint’s roles.
If the endpoint has no configured roles (the default), all authenticated users are considered to be authorized.
You can configure the roles by using the `management.endpoint.health.roles` property.

|  |  |
| --- | --- |
|  | If you have secured your application and wish to use `always`, your security configuration must permit access to the health endpoint for both authenticated and unauthenticated users. |

Health information is collected from the content of a [`HealthContributorRegistry`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/registry/HealthContributorRegistry.html) (by default, all [`HealthContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthContributor.html) instances defined in your [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html)).
Spring Boot includes a number of auto-configured [`HealthContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthContributor.html) beans, and you can also write your own.

A [`HealthContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthContributor.html) can be either a [`HealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthIndicator.html) or a [`CompositeHealthContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/CompositeHealthContributor.html).
A [`HealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthIndicator.html) provides actual health information, including a [`Status`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/Status.html).
A [`CompositeHealthContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/CompositeHealthContributor.html) provides a composite of other [`HealthContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthContributor.html) instances.
Taken together, contributors form a tree structure to represent the overall system health.

By default, the final system health is derived by a [`StatusAggregator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/actuate/endpoint/StatusAggregator.html), which sorts the statuses from each [`HealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthIndicator.html) based on an ordered list of statuses.
The first status in the sorted list is used as the overall health status.
If no [`HealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthIndicator.html) returns a status that is known to the [`StatusAggregator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/actuate/endpoint/StatusAggregator.html), an `UNKNOWN` status is used.

|  |  |
| --- | --- |
|  | You can use the [`HealthContributorRegistry`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/registry/HealthContributorRegistry.html) to register and unregister health indicators at runtime. |

### Auto-configured HealthIndicators

When appropriate, Spring Boot auto-configures the [`HealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthIndicator.html) beans listed in the following table.
You can also enable or disable selected indicators by configuring `management.health.key.enabled`,
with the `key` listed in the following table:

| Key | Name | Description |
| --- | --- | --- |
| `cassandra` | [`CassandraDriverHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/cassandra/health/CassandraDriverHealthIndicator.html) | Checks that a Cassandra database is up. |
| `couchbase` | [`CouchbaseHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/couchbase/health/CouchbaseHealthIndicator.html) | Checks that a Couchbase cluster is up. |
| `db` | [`DataSourceHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jdbc/health/DataSourceHealthIndicator.html) | Checks that a connection to [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html) can be obtained. |
| `diskspace` | [`DiskSpaceHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/application/DiskSpaceHealthIndicator.html) | Checks for low disk space. |
| `elasticsearch` | [`ElasticsearchRestClientHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/elasticsearch/health/ElasticsearchRestClientHealthIndicator.html) | Checks that an Elasticsearch cluster is up. |
| `hazelcast` | [`HazelcastHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/hazelcast/health/HazelcastHealthIndicator.html) | Checks that a Hazelcast server is up. |
| `jms` | [`JmsHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jms/health/JmsHealthIndicator.html) | Checks that a JMS broker is up. |
| `ldap` | [`LdapHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/ldap/health/LdapHealthIndicator.html) | Checks that an LDAP server is up. |
| `mail` | [`MailHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/mail/health/MailHealthIndicator.html) | Checks that a mail server is up. |
| `mongo` | [`MongoHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/mongodb/health/MongoHealthIndicator.html) | Checks that a Mongo database is up. |
| `neo4j` | [`Neo4jHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/neo4j/health/Neo4jHealthIndicator.html) | Checks that a Neo4j database is up. |
| `ping` | [`PingHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/PingHealthIndicator.html) | Always responds with `UP`. |
| `rabbit` | [`RabbitHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/amqp/health/RabbitHealthIndicator.html) | Checks that a Rabbit server is up. |
| `redis` | [`DataRedisHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/redis/health/DataRedisHealthIndicator.html) | Checks that a Redis server is up. |
| `ssl` | [`SslHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/application/SslHealthIndicator.html) | Checks that SSL certificates are ok. |

|  |  |
| --- | --- |
|  | You can disable them all by setting the `management.health.defaults.enabled` property. |

|  |  |
| --- | --- |
|  | The `ssl` [`HealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthIndicator.html) has a "warning threshold" property named `management.health.ssl.certificate-validity-warning-threshold`. You can use this threshold to give yourself enough lead time to rotate the soon-to-be-expired certificate. If an SSL certificate will become invalid within the period defined by this threshold, the [`HealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthIndicator.html) will report this in the details section of its response where `details.validChains.certificates.[*].validity.status` will have the value `WILL_EXPIRE_SOON`. |

Additional [`HealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthIndicator.html) beans are enabled by default:

| Key | Name | Description |
| --- | --- | --- |
| `livenessstate` | [`LivenessStateHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/application/LivenessStateHealthIndicator.html) | Exposes the “Liveness” application availability state. |
| `readinessstate` | [`ReadinessStateHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/application/ReadinessStateHealthIndicator.html) | Exposes the “Readiness” application availability state. |

These can be disabled by using the `management.endpoint.health.probes.enabled` configuration property.

### Writing Custom HealthIndicators

To provide custom health information, you can register Spring beans that implement the [`HealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthIndicator.html) interface.
You need to provide an implementation of the `health()` method and return a [`Health`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/Health.html) response.
The [`Health`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/Health.html) response should include a status and can optionally include additional details to be displayed.
The following code shows a sample [`HealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthIndicator.html) implementation:

* Java
* Kotlin

```
import org.springframework.boot.health.contributor.Health;
import org.springframework.boot.health.contributor.HealthIndicator;
import org.springframework.stereotype.Component;

@Component
public class MyHealthIndicator implements HealthIndicator {

	@Override
	public Health health() {
		int errorCode = check();
		if (errorCode != 0) {
			return Health.down().withDetail("Error Code", errorCode).build();
		}
		return Health.up().build();
	}

	private int check() {
		// perform some specific health check
		return ...
	}

}
```

```
import org.springframework.boot.health.contributor.Health
import org.springframework.boot.health.contributor.HealthIndicator
import org.springframework.stereotype.Component

@Component
class MyHealthIndicator : HealthIndicator {

	override fun health(): Health {
		val errorCode = check()
		if (errorCode != 0) {
			return Health.down().withDetail("Error Code", errorCode).build()
		}
		return Health.up().build()
	}

	private fun check(): Int {
		// perform some specific health check
		return  ...
	}

}
```

|  |  |
| --- | --- |
|  | The identifier for a given [`HealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthIndicator.html) is the name of the bean without the [`HealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthIndicator.html) suffix, if it exists. In the preceding example, the health information is available in an entry named `my`. |

|  |  |
| --- | --- |
|  | Health indicators are usually called over HTTP and need to respond before any connection timeouts. Spring Boot will log a warning message for any health indicator that takes longer than 10 seconds to respond. If you want to configure this threshold, you can use the `management.endpoint.health.logging.slow-indicator-threshold` property. |

In addition to Spring Boot’s predefined [`Status`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/Status.html) types, [`Health`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/Health.html) can return a custom [`Status`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/Status.html) that represents a new system state.
In such cases, you also need to provide a custom implementation of the [`StatusAggregator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/actuate/endpoint/StatusAggregator.html) interface, or you must configure the default implementation by using the `management.endpoint.health.status.order` configuration property.

For example, assume a new [`Status`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/Status.html) with a code of `FATAL` is being used in one of your [`HealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthIndicator.html) implementations.
To configure the severity order, add the following property to your application properties:

* Properties
* YAML

```
management.endpoint.health.status.order=fatal,down,out-of-service,unknown,up
```

```
management:
  endpoint:
    health:
      status:
        order: "fatal,down,out-of-service,unknown,up"
```

The HTTP status code in the response reflects the overall health status.
By default, `OUT_OF_SERVICE` and `DOWN` map to 503.
Any unmapped health statuses, including `UP`, map to 200.
You might also want to register custom status mappings if you access the health endpoint over HTTP.
Configuring a custom mapping disables the defaults mappings for `DOWN` and `OUT_OF_SERVICE`.
If you want to retain the default mappings, you must explicitly configure them, alongside any custom mappings.
For example, the following property maps `FATAL` to 503 (service unavailable) and retains the default mappings for `DOWN` and `OUT_OF_SERVICE`:

* Properties
* YAML

```
management.endpoint.health.status.http-mapping.down=503
management.endpoint.health.status.http-mapping.fatal=503
management.endpoint.health.status.http-mapping.out-of-service=503
```

```
management:
  endpoint:
    health:
      status:
        http-mapping:
          down: 503
          fatal: 503
          out-of-service: 503
```

|  |  |
| --- | --- |
|  | If you need more control, you can define your own [`HttpCodeStatusMapper`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/actuate/endpoint/HttpCodeStatusMapper.html) bean. |

The following table shows the default status mappings for the built-in statuses:

| Status | Mapping |
| --- | --- |
| `DOWN` | `SERVICE_UNAVAILABLE` (`503`) |
| `OUT_OF_SERVICE` | `SERVICE_UNAVAILABLE` (`503`) |
| `UP` | No mapping by default, so HTTP status is `200` |
| `UNKNOWN` | No mapping by default, so HTTP status is `200` |

### Reactive Health Indicators

For reactive applications, such as those that use Spring WebFlux, [`ReactiveHealthContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/ReactiveHealthContributor.html) provides a non-blocking contract for getting application health.
Similar to a traditional [`HealthContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthContributor.html), health information is collected from the content of a [`ReactiveHealthContributorRegistry`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/registry/ReactiveHealthContributorRegistry.html) (by default, all [`HealthContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthContributor.html) and [`ReactiveHealthContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/ReactiveHealthContributor.html) instances defined in your [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html)).
Regular [`HealthContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthContributor.html) instances that do not check against a reactive API are executed on the elastic scheduler.

|  |  |
| --- | --- |
|  | In a reactive application, you should use the [`ReactiveHealthContributorRegistry`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/registry/ReactiveHealthContributorRegistry.html) to register and unregister health indicators at runtime. If you need to register a regular [`HealthContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthContributor.html), you should wrap it with `ReactiveHealthContributor#adapt`. |

To provide custom health information from a reactive API, you can register Spring beans that implement the [`ReactiveHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/ReactiveHealthIndicator.html) interface.
The following code shows a sample [`ReactiveHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/ReactiveHealthIndicator.html) implementation:

* Java
* Kotlin

```
import reactor.core.publisher.Mono;

import org.springframework.boot.health.contributor.Health;
import org.springframework.boot.health.contributor.ReactiveHealthIndicator;
import org.springframework.stereotype.Component;

@Component
public class MyReactiveHealthIndicator implements ReactiveHealthIndicator {

	@Override
	public Mono<Health> health() {
		return doHealthCheck().onErrorResume((exception) ->
			Mono.just(new Health.Builder().down(exception).build()));
	}

	private Mono<Health> doHealthCheck() {
		// perform some specific health check
		return ...
	}

}
```

```
import org.springframework.boot.health.contributor.Health
import org.springframework.boot.health.contributor.ReactiveHealthIndicator
import org.springframework.stereotype.Component
import reactor.core.publisher.Mono

@Component
class MyReactiveHealthIndicator : ReactiveHealthIndicator {

	override fun health(): Mono<Health> {
		return doHealthCheck().onErrorResume { exception: Throwable ->
			Mono.just(Health.Builder().down(exception).build())
		}
	}

	private fun doHealthCheck(): Mono<Health> {
		// perform some specific health check
		return  ...
	}

}
```

|  |  |
| --- | --- |
|  | To handle the error automatically, consider extending from [`AbstractReactiveHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/AbstractReactiveHealthIndicator.html). |

### Auto-configured ReactiveHealthIndicators

When appropriate, Spring Boot auto-configures the following [`ReactiveHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/ReactiveHealthIndicator.html) beans:

| Key | Name | Description |
| --- | --- | --- |
| `cassandra` | [`CassandraDriverReactiveHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/cassandra/health/CassandraDriverReactiveHealthIndicator.html) | Checks that a Cassandra database is up. |
| `couchbase` | [`CouchbaseReactiveHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/couchbase/health/CouchbaseReactiveHealthIndicator.html) | Checks that a Couchbase cluster is up. |
| `elasticsearch` | [`DataElasticsearchReactiveHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/elasticsearch/health/DataElasticsearchReactiveHealthIndicator.html) | Checks that an Elasticsearch cluster is up. |
| `mongo` | [`MongoReactiveHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/mongodb/health/MongoReactiveHealthIndicator.html) | Checks that a Mongo database is up. |
| `neo4j` | [`Neo4jReactiveHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/neo4j/health/Neo4jReactiveHealthIndicator.html) | Checks that a Neo4j database is up. |
| `redis` | [`DataRedisReactiveHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/redis/health/DataRedisReactiveHealthIndicator.html) | Checks that a Redis server is up. |

|  |  |
| --- | --- |
|  | If necessary, reactive indicators replace the regular ones. Also, any [`HealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthIndicator.html) that is not handled explicitly is wrapped automatically. |

### Health Groups

It is sometimes useful to organize health indicators into groups that you can use for different purposes.

To create a health indicator group, you can use the `management.endpoint.health.group.<name>` property and specify a list of health indicator IDs to `include` or `exclude`.
For example, to create a group that includes only database indicators you can define the following:

* Properties
* YAML

```
management.endpoint.health.group.custom.include=db
```

```
management:
  endpoint:
    health:
      group:
        custom:
          include: "db"
```

You can then check the result by hitting `localhost:8080/actuator/health/custom`.

Similarly, to create a group that excludes the database indicators from the group and includes all the other indicators, you can define the following:

* Properties
* YAML

```
management.endpoint.health.group.custom.exclude=db
```

```
management:
  endpoint:
    health:
      group:
        custom:
          exclude: "db"
```

By default, startup will fail if a health group includes or excludes a health indicator that does not exist.
To disable this behavior set `management.endpoint.health.validate-group-membership` to `false`.

By default, groups inherit the same [`StatusAggregator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/actuate/endpoint/StatusAggregator.html) and [`HttpCodeStatusMapper`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/actuate/endpoint/HttpCodeStatusMapper.html) settings as the system health.
However, you can also define these on a per-group basis.
You can also override the `show-details` and `roles` properties if required:

* Properties
* YAML

```
management.endpoint.health.group.custom.show-details=when-authorized
management.endpoint.health.group.custom.roles=admin
management.endpoint.health.group.custom.status.order=fatal,up
management.endpoint.health.group.custom.status.http-mapping.fatal=500
management.endpoint.health.group.custom.status.http-mapping.out-of-service=500
```

```
management:
  endpoint:
    health:
      group:
        custom:
          show-details: "when-authorized"
          roles: "admin"
          status:
            order: "fatal,up"
            http-mapping:
              fatal: 500
              out-of-service: 500
```

|  |  |
| --- | --- |
|  | You can use `@Qualifier("groupname")` if you need to register custom [`StatusAggregator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/actuate/endpoint/StatusAggregator.html) or [`HttpCodeStatusMapper`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/actuate/endpoint/HttpCodeStatusMapper.html) beans for use with the group. |

A health group can also include/exclude a [`CompositeHealthContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/CompositeHealthContributor.html).
You can also include/exclude only a certain component of a [`CompositeHealthContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/CompositeHealthContributor.html).
This can be done using the fully qualified name of the component as follows:

```
management.endpoint.health.group.custom.include="test/primary"
management.endpoint.health.group.custom.exclude="test/primary/b"
```

In the example above, the `custom` group will include the [`HealthContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthContributor.html) with the name `primary` which is a component of the composite `test`.
Here, `primary` itself is a composite and the [`HealthContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/contributor/HealthContributor.html) with the name `b` will be excluded from the `custom` group.

Health groups can be made available at an additional path on either the main or management port.
This is useful in cloud environments such as Kubernetes, where it is quite common to use a separate management port for the actuator endpoints for security purposes.
Having a separate port could lead to unreliable health checks because the main application might not work properly even if the health check is successful.
The health group can be configured with an additional path as follows:

```
management.endpoint.health.group.live.additional-path="server:/healthz"
```

This would make the `live` health group available on the main server port at `/healthz`.
The prefix is mandatory and must be either `server:` (represents the main server port) or `management:` (represents the management port, if configured.)
The path must be a single path segment.

### DataSource Health

The [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html) health indicator shows the health of both standard data sources and routing data source beans.
The health of a routing data source includes the health of each of its target data sources.
In the health endpoint’s response, each of a routing data source’s targets is named by using its routing key.
If you prefer not to include routing data sources in the indicator’s output, set `management.health.db.ignore-routing-data-sources` to `true`.

## Kubernetes Probes

Applications deployed on Kubernetes can provide information about their internal state with [Container Probes](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-probes).
Depending on [your Kubernetes configuration](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/), the kubelet calls those probes and reacts to the result.

By default, Spring Boot manages your [Application Availability](../features/spring-application.html#features.spring-application.application-availability) state.
If deployed in a Kubernetes environment, actuator gathers the “Liveness” and “Readiness” information from the [`ApplicationAvailability`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/availability/ApplicationAvailability.html) interface and uses that information in dedicated [health indicators](#actuator.endpoints.health.auto-configured-health-indicators): [`LivenessStateHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/application/LivenessStateHealthIndicator.html) and [`ReadinessStateHealthIndicator`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/health/application/ReadinessStateHealthIndicator.html).
These indicators are shown on the global health endpoint (`"/actuator/health"`).
They are also exposed as separate HTTP Probes by using [health groups](#actuator.endpoints.health.groups): `"/actuator/health/liveness"` and `"/actuator/health/readiness"`.

You can then configure your Kubernetes infrastructure with the following endpoint information:

```
livenessProbe:
  httpGet:
    path: "/actuator/health/liveness"
    port: <actuator-port>
  failureThreshold: ...
  periodSeconds: ...

readinessProbe:
  httpGet:
    path: "/actuator/health/readiness"
    port: <actuator-port>
  failureThreshold: ...
  periodSeconds: ...
```

|  |  |
| --- | --- |
|  | `<actuator-port>` should be set to the port that the actuator endpoints are available on. It could be the main web server port or a separate management port if the `"management.server.port"` property has been set. |

These health groups are automatically enabled.
You can disable them by using the `management.endpoint.health.probes.enabled` configuration property.

|  |  |
| --- | --- |
|  | If an application takes longer to start than the configured liveness period, Kubernetes [mentions the `"startupProbe"` as a possible solution](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#when-should-you-use-a-startup-probe). Generally speaking, the `"startupProbe"` is not necessarily needed here as the `"readinessProbe"` fails until all startup tasks are done. This means your application will not receive traffic until it is ready. However, if your application takes a long time to start, consider [configuring a `"startupProbe"`](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-startup-probes) that uses the liveness HTTP probe to make sure that Kubernetes won’t kill your application while it is in the process of starting. See the section that describes [how probes behave during the application lifecycle](#actuator.endpoints.kubernetes-probes.lifecycle). |

If your Actuator endpoints are deployed on a separate management context, the endpoints do not use the same web infrastructure (port, connection pools, framework components) as the main application.
In this case, a probe check could be successful even if the main application does not work properly (for example, it cannot accept new connections).
For this reason, it is a good idea to make the `liveness` and `readiness` health groups available on the main server port.
This can be done by setting the following property:

```
management.endpoint.health.probes.add-additional-paths=true
```

This would make the `liveness` group available at `/livez` and the `readiness` group available at `/readyz` on the main server port.
Paths can be customized using the `additional-path` property on each group, see [health groups](#actuator.endpoints.health.groups) for details.

### Checking External State With Kubernetes Probes

Actuator configures the “liveness” and “readiness” probes as Health Groups.
This means that all the [health groups features](#actuator.endpoints.health.groups) are available for them.
You can, for example, configure additional Health Indicators:

* Properties
* YAML

```
management.endpoint.health.group.readiness.include=readinessState,customCheck
```

```
management:
  endpoint:
    health:
      group:
        readiness:
          include: "readinessState,customCheck"
```

By default, Spring Boot does not add other health indicators to these groups.

The “liveness” probe should not depend on health checks for external systems.
If the [liveness state of an application](../features/spring-application.html#features.spring-application.application-availability.liveness) is broken, Kubernetes tries to solve that problem by restarting the application instance.
This means that if an external system (such as a database, a Web API, or an external cache) fails, Kubernetes might restart all application instances and create cascading failures.

As for the “readiness” probe, the choice of checking external systems must be made carefully by the application developers.
For this reason, Spring Boot does not include any additional health checks in the readiness probe.
If the [readiness state of an application instance](../features/spring-application.html#features.spring-application.application-availability.readiness) is unready, Kubernetes does not route traffic to that instance.
Some external systems might not be shared by application instances, in which case they could be included in a readiness probe.
Other external systems might not be essential to the application (the application could have circuit breakers and fallbacks), in which case they definitely should not be included.
Unfortunately, an external system that is shared by all application instances is common, and you have to make a judgement call: Include it in the readiness probe and expect that the application is taken out of service when the external service is down or leave it out and deal with failures higher up the stack, perhaps by using a circuit breaker in the caller.

|  |  |
| --- | --- |
|  | If all instances of an application are unready, a Kubernetes Service with `type=ClusterIP` or `NodePort` does not accept any incoming connections. There is no HTTP error response (503 and so on), since there is no connection. A service with `type=LoadBalancer` might or might not accept connections, depending on the provider. A service that has an explicit [ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) also responds in a way that depends on the implementation — the ingress service itself has to decide how to handle the “connection refused” from downstream. HTTP 503 is quite likely in the case of both load balancer and ingress. |

Also, if an application uses Kubernetes [autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/), it may react differently to applications being taken out of the load-balancer, depending on its autoscaler configuration.

### Application Lifecycle and Probe States

An important aspect of the Kubernetes Probes support is its consistency with the application lifecycle.
There is a significant difference between the [`AvailabilityState`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/availability/AvailabilityState.html) (which is the in-memory, internal state of the application)
and the actual probe (which exposes that state).
Depending on the phase of application lifecycle, the probe might not be available.

Spring Boot publishes [application events during startup and shutdown](../features/spring-application.html#features.spring-application.application-events-and-listeners),
and probes can listen to such events and expose the [`AvailabilityState`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/availability/AvailabilityState.html) information.

The following tables show the [`AvailabilityState`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/availability/AvailabilityState.html) and the state of HTTP connectors at different stages.

When a Spring Boot application starts:

| Startup phase | LivenessState | ReadinessState | HTTP server | Notes |
| --- | --- | --- | --- | --- |
| Starting | `BROKEN` | `REFUSING_TRAFFIC` | Not started | Kubernetes checks the "liveness" Probe and restarts the application if it takes too long. |
| Started | `CORRECT` | `REFUSING_TRAFFIC` | Refuses requests | The application context is refreshed. The application performs startup tasks and does not receive traffic yet. |
| Ready | `CORRECT` | `ACCEPTING_TRAFFIC` | Accepts requests | Startup tasks are finished. The application is receiving traffic. |

When a Spring Boot application shuts down:

| Shutdown phase | Liveness State | Readiness State | HTTP server | Notes |
| --- | --- | --- | --- | --- |
| Running | `CORRECT` | `ACCEPTING_TRAFFIC` | Accepts requests | Shutdown has been requested. |
| Graceful shutdown | `CORRECT` | `REFUSING_TRAFFIC` | New requests are rejected | If enabled, [graceful shutdown processes in-flight requests](../web/graceful-shutdown.html). HTTP probes also stop accepting traffic, so the availability states are not readily available externally. |
| Shutdown complete | N/A | N/A | Server is shut down | The application context is closed and the application is shut down. |

|  |  |
| --- | --- |
|  | See [Kubernetes Container Lifecycle](../../how-to/deployment/cloud.html#howto.deployment.cloud.kubernetes.container-lifecycle) for more information about Kubernetes deployment. In particular, it describes how to use the `preStop` hook to give your application time to shut down gracefully before Kubernetes kills it. |

## Application Information

Application information exposes various information collected from all [`InfoContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/info/InfoContributor.html) beans defined in your [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html).
Spring Boot includes a number of auto-configured [`InfoContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/info/InfoContributor.html) beans, and you can write your own.

### Auto-configured InfoContributors

When appropriate, Spring auto-configures the following [`InfoContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/info/InfoContributor.html) beans:

| ID | Name | Description | Prerequisites |
| --- | --- | --- | --- |
| `build` | [`BuildInfoContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/info/BuildInfoContributor.html) | Exposes build information. | A `META-INF/build-info.properties` resource. |
| `env` | [`EnvironmentInfoContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/info/EnvironmentInfoContributor.html) | Exposes any property from the [`Environment`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/env/Environment.html) whose name starts with `info.`. | None. |
| `git` | [`GitInfoContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/info/GitInfoContributor.html) | Exposes git information. | A `git.properties` resource. |
| `java` | [`JavaInfoContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/info/JavaInfoContributor.html) | Exposes Java runtime information. | None. |
| `os` | [`OsInfoContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/info/OsInfoContributor.html) | Exposes Operating System information. | None. |
| `process` | [`ProcessInfoContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/info/ProcessInfoContributor.html) | Exposes process information. | None. |
| `ssl` | [`SslInfoContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/info/SslInfoContributor.html) | Exposes SSL certificate information. | An [SSL Bundle](../features/ssl.html#features.ssl.bundles) configured. |

Whether an individual contributor is enabled is controlled by its `management.info.<id>.enabled` property.
Different contributors have different defaults for this property, depending on their prerequisites and the nature of the information that they expose.

With no prerequisites to indicate that they should be enabled, the `env`, `java`, `os`, and `process` contributors are disabled by default. The `ssl` contributor has a prerequisite of having an [SSL Bundle](../features/ssl.html#features.ssl.bundles) configured but it is disabled by default.
Each can be enabled by setting its `management.info.<id>.enabled` property to `true`.

The `build` and `git` info contributors are enabled by default.
Each can be disabled by setting its `management.info.<id>.enabled` property to `false`.
Alternatively, to disable every contributor that is usually enabled by default, set the `management.info.defaults.enabled` property to `false`.

### Custom Application Information

When the `env` contributor is enabled, you can customize the data exposed by the `info` endpoint by setting `info.*` Spring properties.
All [`Environment`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/env/Environment.html) properties under the `info` key are automatically exposed.
For example, you could add the following settings to your `application.properties` file:

* Properties
* YAML

```
info.app.encoding=UTF-8
info.app.java.source=17
info.app.java.target=17
```

```
info:
  app:
    encoding: "UTF-8"
    java:
      source: "17"
      target: "17"
```

|  |  |
| --- | --- |
|  | Rather than hardcoding those values, you could also [expand info properties at build time](../../how-to/properties-and-configuration.html#howto.properties-and-configuration.expand-properties).  Assuming you use Maven, you could rewrite the preceding example as follows:  * Properties * YAML  ``` [email protected]@ [email protected]@ [email protected]@ ```  ``` info:   app:     encoding: "@project.build.sourceEncoding@"     java:       source: "@java.version@"       target: "@java.version@" ``` |

### Git Commit Information

Another useful feature of the `info` endpoint is its ability to publish information about the state of your `git` source code repository when the project was built.
If a [`GitProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/info/GitProperties.html) bean is available, you can use the `info` endpoint to expose these properties.

|  |  |
| --- | --- |
|  | A [`GitProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/info/GitProperties.html) bean is auto-configured if a `git.properties` file is available at the root of the classpath. See [Generate Git Information](../../how-to/build.html#howto.build.generate-git-info) for more detail. |

By default, the endpoint exposes `git.branch`, `git.commit.id`, and `git.commit.time` properties, if present.
If you do not want any of these properties in the endpoint response, they need to be excluded from the `git.properties` file.
If you want to display the full git information (that is, the full content of `git.properties`), use the `management.info.git.mode` property, as follows:

* Properties
* YAML

```
management.info.git.mode=full
```

```
management:
  info:
    git:
      mode: "full"
```

To disable the git commit information from the `info` endpoint completely, set the `management.info.git.enabled` property to `false`, as follows:

* Properties
* YAML

```
management.info.git.enabled=false
```

```
management:
  info:
    git:
      enabled: false
```

### Build Information

If a [`BuildProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/info/BuildProperties.html) bean is available, the `info` endpoint can also publish information about your build.
This happens if a `META-INF/build-info.properties` file is available in the classpath.

|  |  |
| --- | --- |
|  | The Maven and Gradle plugins can both generate that file. See [Generate Build Information](../../how-to/build.html#howto.build.generate-info) for more details. |

### Java Information

The `info` endpoint publishes information about your Java runtime environment, see [`JavaInfo`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/info/JavaInfo.html) for more details.

### OS Information

The `info` endpoint publishes information about your Operating System, see [`OsInfo`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/info/OsInfo.html) for more details.

### Process Information

The `info` endpoint publishes information about your process, see [`ProcessInfo`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/info/ProcessInfo.html) for more details.

### SSL Information

The `info` endpoint publishes information about your SSL certificates (that are configured through [SSL Bundles](../features/ssl.html#features.ssl.bundles)), see [`SslInfo`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/info/SslInfo.html) for more details.

### Writing Custom InfoContributors

To provide custom application information, you can register Spring beans that implement the [`InfoContributor`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/info/InfoContributor.html) interface.

The following example contributes an `example` entry with a single value:

* Java
* Kotlin

```
import java.util.Collections;

import org.springframework.boot.actuate.info.Info;
import org.springframework.boot.actuate.info.InfoContributor;
import org.springframework.stereotype.Component;

@Component
public class MyInfoContributor implements InfoContributor {

	@Override
	public void contribute(Info.Builder builder) {
		builder.withDetail("example", Collections.singletonMap("key", "value"));
	}

}
```

```
import org.springframework.boot.actuate.info.Info
import org.springframework.boot.actuate.info.InfoContributor
import org.springframework.stereotype.Component
import java.util.Collections

@Component
class MyInfoContributor : InfoContributor {

	override fun contribute(builder: Info.Builder) {
		builder.withDetail("example", Collections.singletonMap("key", "value"))
	}

}
```

If you reach the `info` endpoint, you should see a response that contains the following additional entry:

```
{
	"example": {
		"key" : "value"
	}
}
```

## Software Bill of Materials (SBOM)

The `sbom` endpoint exposes the [Software Bill of Materials](https://en.wikipedia.org/wiki/Software_supply_chain).
CycloneDX SBOMs can be auto-detected, but other formats can be manually configured, too.

The `sbom` actuator endpoint will then expose an SBOM called "application", which describes the contents of your application.

|  |  |
| --- | --- |
|  | To automatically generate a CycloneDX SBOM at project build time, please see the [Generate a CycloneDX SBOM](../../how-to/build.html#howto.build.generate-cyclonedx-sbom) section. |

### Other SBOM formats

If you want to publish an SBOM in a different format, there are some configuration properties which you can use.

The configuration property `management.endpoint.sbom.application.location` sets the location for the application SBOM.
For example, setting this to `classpath:sbom.json` will use the contents of the `/sbom.json` resource on the classpath.

The media type for SBOMs in CycloneDX, SPDX and Syft format is detected automatically.
To override the auto-detected media type, use the configuration property `management.endpoint.sbom.application.media-type`.

### Additional SBOMs

The actuator endpoint can handle multiple SBOMs.
To add SBOMs, use the configuration property `management.endpoint.sbom.additional`, as shown in this example:

* Properties
* YAML

```
management.endpoint.sbom.additional.system.location=optional:file:/system.spdx.json
management.endpoint.sbom.additional.system.media-type=application/spdx+json
```

```
management:
  endpoint:
    sbom:
      additional:
        system:
          location: "optional:file:/system.spdx.json"
          media-type: "application/spdx+json"
```

This will add an SBOM called "system", which is stored in `/system.spdx.json`.
The `optional:` prefix can be used to prevent a startup failure if the file doesn’t exist.