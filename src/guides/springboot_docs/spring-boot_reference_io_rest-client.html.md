Search

# Calling REST Services

Spring Boot provides various convenient ways to call remote REST services.
If you are developing a non-blocking reactive application and you’re using Spring WebFlux, then you can use [`WebClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/WebClient.html).
If you prefer imperative APIs then you can use [`RestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestClient.html) or [`RestTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestTemplate.html).

## WebClient

If you have Spring WebFlux on your classpath we recommend that you use [`WebClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/WebClient.html) to call remote REST services.
The [`WebClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/WebClient.html) interface provides a functional style API and is fully reactive.
You can learn more about the [`WebClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/WebClient.html) in the dedicated [section in the Spring Framework docs](https://docs.spring.io/spring-framework/reference/7.0/web/webflux-webclient.html).

|  |  |
| --- | --- |
|  | If you are not writing a reactive Spring WebFlux application you can use the [`RestClient`](#io.rest-client.restclient) instead of a [`WebClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/WebClient.html). This provides a similar functional API, but is imperative rather than reactive. |

Spring Boot creates and pre-configures a prototype [`WebClient.Builder`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/WebClient.Builder.html) bean for you.
It is strongly advised to inject it in your components and use it to create [`WebClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/WebClient.html) instances.
Spring Boot is configuring that builder to share HTTP resources and reflect codecs setup in the same fashion as the server ones (see [WebFlux HTTP codecs auto-configuration](../web/reactive.html#web.reactive.webflux.httpcodecs)), and more.

The following code shows a typical example:

* Java
* Kotlin

```
import reactor.core.publisher.Mono;

import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@Service
public class MyService {

	private final WebClient webClient;

	public MyService(WebClient.Builder webClientBuilder) {
		this.webClient = webClientBuilder.baseUrl("https://example.org").build();
	}

	public Mono<Details> someRestCall(String name) {
		return this.webClient.get().uri("/{name}/details", name).retrieve().bodyToMono(Details.class);
	}

}
```

```
import org.springframework.stereotype.Service
import org.springframework.web.reactive.function.client.WebClient
import reactor.core.publisher.Mono

@Service
class MyService(webClientBuilder: WebClient.Builder) {

	private val webClient: WebClient

	init {
		webClient = webClientBuilder.baseUrl("https://example.org").build()
	}

	fun someRestCall(name: String): Mono<Details> {
		return webClient.get().uri("/{name}/details", name)
				.retrieve().bodyToMono(Details::class.java)
	}

}
```

### WebClient Runtime

Spring Boot will auto-detect which [`ClientHttpConnector`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/http/client/reactive/ClientHttpConnector.html) to use to drive [`WebClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/WebClient.html) depending on the libraries available on the application classpath.
In order of preference, the following clients are supported:

1. Reactor Netty
2. Jetty RS client
3. Apache HttpClient
4. JDK HttpClient

If multiple clients are available on the classpath, the most preferred client will be used.

The `spring-boot-starter-webflux` starter depends on `io.projectreactor.netty:reactor-netty` by default, which brings both server and client implementations.
If you choose to use Jetty as a reactive server instead, you should add a dependency on the Jetty Reactive HTTP client library, `org.eclipse.jetty:jetty-reactive-httpclient`.
Using the same technology for server and client has its advantages, as it will automatically share HTTP resources between client and server.

Developers can override the resource configuration for Jetty and Reactor Netty by providing a custom [`ReactorResourceFactory`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/http/client/ReactorResourceFactory.html) or [`JettyResourceFactory`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/http/client/reactive/JettyResourceFactory.html) bean - this will be applied to both clients and servers.

If you wish to override that choice for the client, you can define your own [`ClientHttpConnector`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/http/client/reactive/ClientHttpConnector.html) bean and have full control over the client configuration.

You can learn more about the [`WebClient` configuration options in the Spring Framework reference documentation](https://docs.spring.io/spring-framework/reference/7.0/web/webflux-webclient/client-builder.html).

### Global HTTP Connector Configuration

If the auto-detected [`ClientHttpConnector`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/http/client/reactive/ClientHttpConnector.html) does not meet your needs, you can use the `spring.http.clients.reactive.connector` property to pick a specific connector.
For example, if you have Reactor Netty on your classpath, but you prefer Jetty’s [`HttpClient`](https://javadoc.jetty.org/jetty-12/org/eclipse/jetty/client/HttpClient.html) you can add the following:

* Properties
* YAML

```
spring.http.clients.reactive.connector=jetty
```

```
spring:
  http:
    clients:
      reactive:
        connector: jetty
```

|  |  |
| --- | --- |
|  | You can also use [global configuration properties](#io.rest-client.global-configuration) which apply to all HTTP clients. |

For more complex customizations, you can use [`ClientHttpConnectorBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/http/client/autoconfigure/reactive/ClientHttpConnectorBuilderCustomizer.html) or declare your own [`ClientHttpConnectorBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/http/client/reactive/ClientHttpConnectorBuilder.html) bean which will cause auto-configuration to back off.
This can be useful when you need to customize some of the internals of the underlying HTTP library.

For example, the following will use a JDK client configured with a specific [`ProxySelector`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/net/ProxySelector.html):

* Java
* Kotlin

```
import java.net.ProxySelector;

import org.springframework.boot.http.client.reactive.ClientHttpConnectorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration(proxyBeanMethods = false)
public class MyConnectorHttpConfiguration {

	@Bean
	ClientHttpConnectorBuilder<?> clientHttpConnectorBuilder(ProxySelector proxySelector) {
		return ClientHttpConnectorBuilder.jdk().withHttpClientCustomizer((builder) -> builder.proxy(proxySelector));
	}

}
```

```
import org.springframework.boot.http.client.reactive.ClientHttpConnectorBuilder
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import java.net.ProxySelector

@Configuration(proxyBeanMethods = false)
class MyConnectorHttpConfiguration {

	@Bean
	fun clientHttpConnectorBuilder(proxySelector: ProxySelector): ClientHttpConnectorBuilder<*> {
		return ClientHttpConnectorBuilder.jdk().withHttpClientCustomizer { builder -> builder.proxy(proxySelector) }
	}

}
```

### WebClient Customization

There are three main approaches to [`WebClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/WebClient.html) customization, depending on how broadly you want the customizations to apply.

To make the scope of any customizations as narrow as possible, inject the auto-configured [`WebClient.Builder`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/WebClient.Builder.html) and then call its methods as required.
[`WebClient.Builder`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/WebClient.Builder.html) instances are stateful: Any change on the builder is reflected in all clients subsequently created with it.
If you want to create several clients with the same builder, you can also consider cloning the builder with `WebClient.Builder other = builder.clone();`.

To make an application-wide, additive customization to all [`WebClient.Builder`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/WebClient.Builder.html) instances, you can declare [`WebClientCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webclient/WebClientCustomizer.html) beans and change the [`WebClient.Builder`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/WebClient.Builder.html) locally at the point of injection.

Finally, you can fall back to the original API and use `WebClient.create()`.
In that case, no auto-configuration or [`WebClientCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webclient/WebClientCustomizer.html) is applied.

### WebClient SSL Support

If you need custom SSL configuration on the [`ClientHttpConnector`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/http/client/reactive/ClientHttpConnector.html) used by the [`WebClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/WebClient.html), you can inject a [`WebClientSsl`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webclient/autoconfigure/WebClientSsl.html) instance that can be used with the builder’s `apply` method.

The [`WebClientSsl`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/webclient/autoconfigure/WebClientSsl.html) interface provides access to any [SSL bundles](../features/ssl.html#features.ssl.bundles) that you have defined in your `application.properties` or `application.yaml` file.

The following code shows a typical example:

* Java
* Kotlin

```
import reactor.core.publisher.Mono;

import org.springframework.boot.webclient.autoconfigure.WebClientSsl;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@Service
public class MyService {

	private final WebClient webClient;

	public MyService(WebClient.Builder webClientBuilder, WebClientSsl ssl) {
		this.webClient = webClientBuilder.baseUrl("https://example.org").apply(ssl.fromBundle("mybundle")).build();
	}

	public Mono<Details> someRestCall(String name) {
		return this.webClient.get().uri("/{name}/details", name).retrieve().bodyToMono(Details.class);
	}

}
```

```
import org.springframework.boot.webclient.autoconfigure.WebClientSsl
import org.springframework.stereotype.Service
import org.springframework.web.reactive.function.client.WebClient
import reactor.core.publisher.Mono

@Service
class MyService(webClientBuilder: WebClient.Builder, ssl: WebClientSsl) {

	private val webClient: WebClient

	init {
		webClient = webClientBuilder.baseUrl("https://example.org")
				.apply(ssl.fromBundle("mybundle")).build()
	}

	fun someRestCall(name: String): Mono<Details> {
		return webClient.get().uri("/{name}/details", name)
				.retrieve().bodyToMono(Details::class.java)
	}

}
```

## RestClient

If you are not using Spring WebFlux or Project Reactor in your application we recommend that you use [`RestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestClient.html) to call remote REST services.

The [`RestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestClient.html) interface provides a functional style imperative API.

Spring Boot creates and pre-configures a prototype [`RestClient.Builder`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestClient.Builder.html) bean for you.
It is strongly advised to inject it in your components and use it to create [`RestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestClient.html) instances.
Spring Boot is configuring that builder with [`HttpMessageConverters`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/http/converter/autoconfigure/HttpMessageConverters.html) and an appropriate [`ClientHttpRequestFactory`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/http/client/ClientHttpRequestFactory.html).

The following code shows a typical example:

* Java
* Kotlin

```
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service
public class MyService {

	private final RestClient restClient;

	public MyService(RestClient.Builder restClientBuilder) {
		this.restClient = restClientBuilder.baseUrl("https://example.org").build();
	}

	public Details someRestCall(String name) {
		return this.restClient.get().uri("/{name}/details", name).retrieve().body(Details.class);
	}

}
```

```
import org.springframework.boot.docs.io.restclient.restclient.ssl.Details
import org.springframework.stereotype.Service
import org.springframework.web.client.RestClient

@Service
class MyService(restClientBuilder: RestClient.Builder) {

	private val restClient: RestClient

	init {
		restClient = restClientBuilder.baseUrl("https://example.org").build()
	}

	fun someRestCall(name: String): Details {
		return restClient.get().uri("/{name}/details", name)
				.retrieve().body(Details::class.java)!!
	}

}
```

### RestClient Customization

There are three main approaches to [`RestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestClient.html) customization, depending on how broadly you want the customizations to apply.

To make the scope of any customizations as narrow as possible, inject the auto-configured [`RestClient.Builder`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestClient.Builder.html) and then call its methods as required.
[`RestClient.Builder`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestClient.Builder.html) instances are stateful: Any change on the builder is reflected in all clients subsequently created with it.
If you want to create several clients with the same builder, you can also consider cloning the builder with `RestClient.Builder other = builder.clone();`.

To make an application-wide, additive customization to all [`RestClient.Builder`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestClient.Builder.html) instances, you can declare [`RestClientCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/RestClientCustomizer.html) beans and change the [`RestClient.Builder`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestClient.Builder.html) locally at the point of injection.

Finally, you can fall back to the original API and use `RestClient.create()`.
In that case, no auto-configuration or [`RestClientCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/RestClientCustomizer.html) is applied.

|  |  |
| --- | --- |
|  | You can also change the [global HTTP client configuration](#io.rest-client.clienthttprequestfactory.configuration). |

### RestClient SSL Support

If you need custom SSL configuration on the [`ClientHttpRequestFactory`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/http/client/ClientHttpRequestFactory.html) used by the [`RestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestClient.html), you can inject a [`RestClientSsl`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/autoconfigure/RestClientSsl.html) instance that can be used with the builder’s `apply` method.

The [`RestClientSsl`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/autoconfigure/RestClientSsl.html) interface provides access to any [SSL bundles](../features/ssl.html#features.ssl.bundles) that you have defined in your `application.properties` or `application.yaml` file.

The following code shows a typical example:

* Java
* Kotlin

```
import org.springframework.boot.restclient.autoconfigure.RestClientSsl;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service
public class MyService {

	private final RestClient restClient;

	public MyService(RestClient.Builder restClientBuilder, RestClientSsl ssl) {
		this.restClient = restClientBuilder.baseUrl("https://example.org").apply(ssl.fromBundle("mybundle")).build();
	}

	public Details someRestCall(String name) {
		return this.restClient.get().uri("/{name}/details", name).retrieve().body(Details.class);
	}

}
```

```
import org.springframework.boot.docs.io.restclient.restclient.ssl.settings.Details
import org.springframework.boot.restclient.autoconfigure.RestClientSsl
import org.springframework.stereotype.Service
import org.springframework.web.client.RestClient

@Service
class MyService(restClientBuilder: RestClient.Builder, ssl: RestClientSsl) {

	private val restClient: RestClient

	init {
		restClient = restClientBuilder.baseUrl("https://example.org")
				.apply(ssl.fromBundle("mybundle")).build()
	}

	fun someRestCall(name: String): Details {
		return restClient.get().uri("/{name}/details", name)
				.retrieve().body(Details::class.java)!!
	}

}
```

If you need to apply other customization in addition to an SSL bundle, you can use the [`HttpClientSettings`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/http/client/HttpClientSettings.html) class with [`ClientHttpRequestFactoryBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/http/client/ClientHttpRequestFactoryBuilder.html):

* Java
* Kotlin

```
import java.time.Duration;

import org.springframework.boot.http.client.ClientHttpRequestFactoryBuilder;
import org.springframework.boot.http.client.HttpClientSettings;
import org.springframework.boot.ssl.SslBundles;
import org.springframework.http.client.ClientHttpRequestFactory;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service
public class MyService {

	private final RestClient restClient;

	public MyService(RestClient.Builder restClientBuilder, SslBundles sslBundles) {
		HttpClientSettings settings = HttpClientSettings.ofSslBundle(sslBundles.getBundle("mybundle"))
			.withReadTimeout(Duration.ofMinutes(2));
		ClientHttpRequestFactory requestFactory = ClientHttpRequestFactoryBuilder.detect().build(settings);
		this.restClient = restClientBuilder.baseUrl("https://example.org").requestFactory(requestFactory).build();
	}

	public Details someRestCall(String name) {
		return this.restClient.get().uri("/{name}/details", name).retrieve().body(Details.class);
	}

}
```

```
import org.springframework.boot.http.client.ClientHttpRequestFactoryBuilder;
import org.springframework.boot.http.client.HttpClientSettings
import org.springframework.boot.ssl.SslBundles
import org.springframework.stereotype.Service
import org.springframework.web.client.RestClient
import java.time.Duration

@Service
class MyService(restClientBuilder: RestClient.Builder, sslBundles: SslBundles) {

	private val restClient: RestClient

	init {
		val settings = HttpClientSettings.defaults()
				.withReadTimeout(Duration.ofMinutes(2))
				.withSslBundle(sslBundles.getBundle("mybundle"))
		val requestFactory = ClientHttpRequestFactoryBuilder.detect().build(settings);
		restClient = restClientBuilder
				.baseUrl("https://example.org")
				.requestFactory(requestFactory).build()
	}

	fun someRestCall(name: String): Details {
		return restClient.get().uri("/{name}/details", name).retrieve().body(Details::class.java)!!
	}

}
```

## RestTemplate

Spring Framework’s [`RestTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestTemplate.html) class predates [`RestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestClient.html) and is the classic way that many applications use to call remote REST services.
You might choose to use [`RestTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestTemplate.html) when you have existing code that you don’t want to migrate to [`RestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestClient.html), or because you’re already familiar with the [`RestTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestTemplate.html) API.

Since [`RestTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestTemplate.html) instances often need to be customized before being used, Spring Boot does not provide any single auto-configured [`RestTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestTemplate.html) bean.
It does, however, auto-configure a [`RestTemplateBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/RestTemplateBuilder.html), which can be used to create [`RestTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestTemplate.html) instances when needed.
The auto-configured [`RestTemplateBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/RestTemplateBuilder.html) ensures that sensible [`HttpMessageConverters`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/http/converter/autoconfigure/HttpMessageConverters.html) and an appropriate [`ClientHttpRequestFactory`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/http/client/ClientHttpRequestFactory.html) are applied to [`RestTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestTemplate.html) instances.

The following code shows a typical example:

* Java
* Kotlin

```
import org.springframework.boot.restclient.RestTemplateBuilder;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class MyService {

	private final RestTemplate restTemplate;

	public MyService(RestTemplateBuilder restTemplateBuilder) {
		this.restTemplate = restTemplateBuilder.build();
	}

	public Details someRestCall(String name) {
		return this.restTemplate.getForObject("/{name}/details", Details.class, name);
	}

}
```

```
import org.springframework.boot.restclient.RestTemplateBuilder
import org.springframework.stereotype.Service
import org.springframework.web.client.RestTemplate

@Service
class MyService(restTemplateBuilder: RestTemplateBuilder) {

	private val restTemplate: RestTemplate

	init {
		restTemplate = restTemplateBuilder.build()
	}

	fun someRestCall(name: String): Details {
		return restTemplate.getForObject("/{name}/details", Details::class.java, name)!!
	}

}
```

[`RestTemplateBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/RestTemplateBuilder.html) includes a number of useful methods that can be used to quickly configure a [`RestTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestTemplate.html).
For example, to add BASIC authentication support, you can use `builder.basicAuthentication("user", "password").build()`.

### RestTemplate Customization

There are three main approaches to [`RestTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestTemplate.html) customization, depending on how broadly you want the customizations to apply.

To make the scope of any customizations as narrow as possible, inject the auto-configured [`RestTemplateBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/RestTemplateBuilder.html) and then call its methods as required.
Each method call returns a new [`RestTemplateBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/RestTemplateBuilder.html) instance, so the customizations only affect this use of the builder.

To make an application-wide, additive customization, use a [`RestTemplateCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/RestTemplateCustomizer.html) bean.
All such beans are automatically registered with the auto-configured [`RestTemplateBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/RestTemplateBuilder.html) and are applied to any templates that are built with it.

The following example shows a customizer that configures the use of a proxy for all hosts except `192.168.0.5`:

* Java
* Kotlin

```
import org.apache.hc.client5.http.classic.HttpClient;
import org.apache.hc.client5.http.impl.classic.HttpClientBuilder;
import org.apache.hc.client5.http.impl.routing.DefaultProxyRoutePlanner;
import org.apache.hc.client5.http.routing.HttpRoutePlanner;
import org.apache.hc.core5.http.HttpException;
import org.apache.hc.core5.http.HttpHost;
import org.apache.hc.core5.http.protocol.HttpContext;

import org.springframework.boot.restclient.RestTemplateCustomizer;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.web.client.RestTemplate;

public class MyRestTemplateCustomizer implements RestTemplateCustomizer {

	@Override
	public void customize(RestTemplate restTemplate) {
		HttpRoutePlanner routePlanner = new CustomRoutePlanner(new HttpHost("proxy.example.com"));
		HttpClient httpClient = HttpClientBuilder.create().setRoutePlanner(routePlanner).build();
		restTemplate.setRequestFactory(new HttpComponentsClientHttpRequestFactory(httpClient));
	}

	static class CustomRoutePlanner extends DefaultProxyRoutePlanner {

		CustomRoutePlanner(HttpHost proxy) {
			super(proxy);
		}

		@Override
		protected HttpHost determineProxy(HttpHost target, HttpContext context) throws HttpException {
			if (target.getHostName().equals("192.168.0.5")) {
				return null;
			}
			return super.determineProxy(target, context);
		}

	}

}
```

```
import org.apache.hc.client5.http.classic.HttpClient
import org.apache.hc.client5.http.impl.classic.HttpClientBuilder
import org.apache.hc.client5.http.impl.routing.DefaultProxyRoutePlanner
import org.apache.hc.client5.http.routing.HttpRoutePlanner
import org.apache.hc.core5.http.HttpException
import org.apache.hc.core5.http.HttpHost
import org.apache.hc.core5.http.protocol.HttpContext
import org.springframework.boot.restclient.RestTemplateCustomizer
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory
import org.springframework.web.client.RestTemplate

class MyRestTemplateCustomizer : RestTemplateCustomizer {

	override fun customize(restTemplate: RestTemplate) {
		val routePlanner: HttpRoutePlanner = CustomRoutePlanner(HttpHost("proxy.example.com"))
		val httpClient: HttpClient = HttpClientBuilder.create().setRoutePlanner(routePlanner).build()
		restTemplate.requestFactory = HttpComponentsClientHttpRequestFactory(httpClient)
	}

	internal class CustomRoutePlanner(proxy: HttpHost?) : DefaultProxyRoutePlanner(proxy) {

		@Throws(HttpException::class)
		public override fun determineProxy(target: HttpHost, context: HttpContext): HttpHost? {
			if (target.hostName == "192.168.0.5") {
				return null
			}
			return  super.determineProxy(target, context)
		}

	}

}
```

Finally, you can define your own [`RestTemplateBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/RestTemplateBuilder.html) bean.
Doing so will replace the auto-configured builder.
If you want any [`RestTemplateCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/RestTemplateCustomizer.html) beans to be applied to your custom builder, as the auto-configuration would have done, configure it using a [`RestTemplateBuilderConfigurer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/autoconfigure/RestTemplateBuilderConfigurer.html).
The following example exposes a [`RestTemplateBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/RestTemplateBuilder.html) that matches what Spring Boot’s auto-configuration would have done, except that custom connect and read timeouts are also specified:

* Java
* Kotlin

```
import java.time.Duration;

import org.springframework.boot.restclient.RestTemplateBuilder;
import org.springframework.boot.restclient.autoconfigure.RestTemplateBuilderConfigurer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration(proxyBeanMethods = false)
public class MyRestTemplateBuilderConfiguration {

	@Bean
	public RestTemplateBuilder restTemplateBuilder(RestTemplateBuilderConfigurer configurer) {
		return configurer.configure(new RestTemplateBuilder())
			.connectTimeout(Duration.ofSeconds(5))
			.readTimeout(Duration.ofSeconds(2));
	}

}
```

```
import org.springframework.boot.restclient.autoconfigure.RestTemplateBuilderConfigurer
import org.springframework.boot.restclient.RestTemplateBuilder
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import java.time.Duration

@Configuration(proxyBeanMethods = false)
class MyRestTemplateBuilderConfiguration {

	@Bean
	fun restTemplateBuilder(configurer: RestTemplateBuilderConfigurer): RestTemplateBuilder {
		return configurer.configure(RestTemplateBuilder()).connectTimeout(Duration.ofSeconds(5))
			.readTimeout(Duration.ofSeconds(2))
	}

}
```

The most extreme (and rarely used) option is to create your own [`RestTemplateBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/RestTemplateBuilder.html) bean without using a configurer.
In addition to replacing the auto-configured builder, this also prevents any [`RestTemplateCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/RestTemplateCustomizer.html) beans from being used.

|  |  |
| --- | --- |
|  | You can also change the [global HTTP client configuration](#io.rest-client.clienthttprequestfactory.configuration). |

### RestTemplate SSL Support

If you need custom SSL configuration on the [`RestTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestTemplate.html), you can apply an [SSL bundle](../features/ssl.html#features.ssl.bundles) to the [`RestTemplateBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/restclient/RestTemplateBuilder.html) as shown in this example:

* Java
* Kotlin

```
import org.springframework.boot.docs.io.restclient.resttemplate.Details;
import org.springframework.boot.restclient.RestTemplateBuilder;
import org.springframework.boot.ssl.SslBundles;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class MyService {

	private final RestTemplate restTemplate;

	public MyService(RestTemplateBuilder restTemplateBuilder, SslBundles sslBundles) {
		this.restTemplate = restTemplateBuilder.sslBundle(sslBundles.getBundle("mybundle")).build();
	}

	public Details someRestCall(String name) {
		return this.restTemplate.getForObject("/{name}/details", Details.class, name);
	}

}
```

```
import org.springframework.boot.docs.io.restclient.resttemplate.Details
import org.springframework.boot.ssl.SslBundles
import org.springframework.boot.restclient.RestTemplateBuilder
import org.springframework.stereotype.Service
import org.springframework.web.client.RestTemplate

@Service
class MyService(restTemplateBuilder: RestTemplateBuilder, sslBundles: SslBundles) {

    private val restTemplate: RestTemplate

    init {
        restTemplate = restTemplateBuilder.sslBundle(sslBundles.getBundle("mybundle")).build()
    }

    fun someRestCall(name: String): Details {
        return restTemplate.getForObject("/{name}/details", Details::class.java, name)!!
    }

}
```

## HTTP Client Detection for RestClient and RestTemplate

Spring Boot will auto-detect which HTTP client to use with [`RestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestClient.html) and [`RestTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestTemplate.html) depending on the libraries available on the application classpath.
In order of preference, the following clients are supported:

1. Apache HttpClient
2. Jetty HttpClient
3. Reactor Netty HttpClient
4. JDK client (`java.net.http.HttpClient`)
5. Simple JDK client (`java.net.HttpURLConnection`)

If multiple clients are available on the classpath, and no global configuration is provided, the most preferred client will be used.

### Global HTTP Client Configuration

If the auto-detected HTTP client does not meet your needs, you can use the `spring.http.clients.imperative.factory` property to pick a specific factory.
For example, if you have Apache HttpClient on your classpath, but you prefer Jetty’s [`HttpClient`](https://javadoc.jetty.org/jetty-12/org/eclipse/jetty/client/HttpClient.html) you can add the following:

* Properties
* YAML

```
spring.http.clients.imperative.factory=jetty
```

```
spring:
  http:
    clients:
      imperative:
        factory: jetty
```

|  |  |
| --- | --- |
|  | You can also use [global configuration properties](#io.rest-client.global-configuration) which apply to all HTTP clients. |

For more complex customizations, you can use [`ClientHttpRequestFactoryBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/http/client/autoconfigure/ClientHttpRequestFactoryBuilderCustomizer.html) or declare your own [`ClientHttpRequestFactoryBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/http/client/ClientHttpRequestFactoryBuilder.html) bean which will cause auto-configuration to back off.
This can be useful when you need to customize some of the internals of the underlying HTTP library.

For example, the following will use a JDK client configured with a specific [`ProxySelector`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/net/ProxySelector.html):

* Java
* Kotlin

```
import java.net.ProxySelector;

import org.springframework.boot.http.client.ClientHttpRequestFactoryBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration(proxyBeanMethods = false)
public class MyClientHttpConfiguration {

	@Bean
	ClientHttpRequestFactoryBuilder<?> clientHttpRequestFactoryBuilder(ProxySelector proxySelector) {
		return ClientHttpRequestFactoryBuilder.jdk()
			.withHttpClientCustomizer((builder) -> builder.proxy(proxySelector));
	}

}
```

```
import org.springframework.boot.http.client.ClientHttpRequestFactoryBuilder
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import java.net.ProxySelector

@Configuration(proxyBeanMethods = false)
class MyClientHttpConfiguration {

	@Bean
	fun clientHttpRequestFactoryBuilder(proxySelector: ProxySelector): ClientHttpRequestFactoryBuilder<*> {
		return ClientHttpRequestFactoryBuilder.jdk()
				.withHttpClientCustomizer { builder -> builder.proxy(proxySelector) }
	}

}
```

## API Versioning

Both `WebClient` and `RestClient` support making versioned remote HTTP calls so that APIs can be evolved over time.
Commonly this involves sending an HTTP header, a query parameter or URL path segment that indicates the version of the API that should be used.

You can configure API versioning using methods on `WebClient.Builder` or `RestClient.Builder`.

|  |  |
| --- | --- |
|  | API versioning is also supported on the server-side. See the [Spring MVC](../web/servlet.html#web.servlet.spring-mvc.api-versioning) and [Spring WebFlux](../web/reactive.html#web.reactive.webflux.api-versioning) sections for details. |

|  |  |
| --- | --- |
|  | The server-side API versioning configuration is not taken into account to auto-configure the client. Clients that should use an API versioning strategy, typically for testing, need to configure it explicitly. |

## HTTP Service Interface Clients

Instead of directly using a [`RestClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/RestClient.html) or [`WebClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/WebClient.html) to call an HTTP service, it’s also possible to call them using annotated Java interfaces.

HTTP Service interfaces defines a service contract by using methods that are annotated with [`@HttpExchange`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/service/annotation/HttpExchange.html), or more typically the method specific variants ([`@GetExchange`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/service/annotation/GetExchange.html), [`@PostExchange`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/service/annotation/PostExchange.html), [`@DeleteExchange`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/service/annotation/DeleteExchange.html), etc).

For example, the following code defines an HTTP Service for an “echo” API that will return a JSON object containing an echo of the request.

* Java
* Kotlin

```
import java.util.Map;

import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.service.annotation.HttpExchange;
import org.springframework.web.service.annotation.PostExchange;

@HttpExchange(url = "https://echo.zuplo.io")
public interface EchoService {

	@PostExchange
	Map<?, ?> echo(@RequestBody Map<String, String> message);

}
```

```
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.service.annotation.HttpExchange
import org.springframework.web.service.annotation.PostExchange

@HttpExchange(url = "https://echo.zuplo.io")
interface EchoService {

	@PostExchange
	fun echo(@RequestBody message: Map<String, String>): Map<*, *>

}
```

More details about how to develop HTTP Service interface clients can be found in the [Spring Framework reference documentation](https://docs.spring.io/spring-framework/reference/7.0/integration/rest-clients.html#rest-http-service-client).

### Importing HTTP Services

In order to use an HTTP Service interface as client you need to import it.
One way to achieve this is to use the [`@ImportHttpServices`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/service/registry/ImportHttpServices.html) annotation, typically on your main application class.
You can use the annotation to import specific classes, or scan for classes to import from specific packages.

For example, the following configuration will scan for HTTP Service interfaces in the `com.example.myclients` package:

* Java
* Kotlin

```
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.service.registry.ImportHttpServices;

@SpringBootApplication
@ImportHttpServices(basePackages = "com.example.myclients")
public class MyApplication {

	public static void main(String[] args) {
		SpringApplication.run(MyApplication.class, args);
	}

}
```

```
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.web.service.registry.ImportHttpServices

@SpringBootApplication
@ImportHttpServices(basePackages = ["com.example.myclients"])
class MyApplication

fun main(args: Array<String>) {
	runApplication<MyApplication>(*args)
}
```

### Service Client Groups

Hard-coding absolute URLs in [`@HttpExchange`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/service/annotation/HttpExchange.html) annotations is often not ideal in production applications.
Instead, you will typically want to give the HTTP Service client a logical name in your code, and then lookup a URL from a property based on that name.

HTTP Service clients allow you to do this by registering them into named groups.
An HTTP Service group is a collection of HTTP Service interfaces that all share common features.

For example, we may want to define an “echo” group to use for HTTP Service clients that call `https://echo.zuplo.io`.

|  |  |
| --- | --- |
|  | HTTP Service groups can be used to define more than just URLs. For example, your group could define connection timeouts and SSL settings. You can also associate client customization logic to a group, such as adding code to insert required authorization headers. |

To associate an HTTP Service interface with a group when using [`@ImportHttpServices`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/service/registry/ImportHttpServices.html) you can use the `group` attribute.

For example, if we assume our example above is organized in such a way that all HTTP Service interfaces in the `com.example.myclients` package belong to the `echo` group.
We first remove the hardcoded URL from the service interface:

* Java
* Kotlin

```
import java.util.Map;

import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.service.annotation.PostExchange;

public interface EchoService {

	@PostExchange
	Map<?, ?> echo(@RequestBody Map<String, String> message);

}
```

```
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.service.annotation.HttpExchange
import org.springframework.web.service.annotation.PostExchange

interface EchoService {

	@PostExchange
	fun echo(@RequestBody message: Map<String, String>): Map<*, *>

}
```

We can then write:

* Java
* Kotlin

```
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.service.registry.ImportHttpServices;

@SpringBootApplication
@ImportHttpServices(group = "echo", basePackages = "com.example.myclients")
public class MyApplication {

	public static void main(String[] args) {
		SpringApplication.run(MyApplication.class, args);
	}

}
```

```
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.web.service.registry.ImportHttpServices

@SpringBootApplication
@ImportHttpServices(group = "echo", basePackages = ["com.example.myclients"])
class MyApplication

fun main(args: Array<String>) {
	runApplication<MyApplication>(*args)
}
```

And finally we can then use a `base-url` property to link the `echo` group to an actual URL:

* Properties
* YAML

```
spring.http.serviceclient.echo.base-url=https://echo.zuplo.io
```

```
spring:
  http:
    serviceclient:
      echo:
        base-url: "https://echo.zuplo.io"
```

|  |  |
| --- | --- |
|  | HTTP Service clients will be associated with a group named “default” if you don’t specify a group. |

|  |  |
| --- | --- |
|  | If you have multiple HTTP Service interfaces in the same package that need to be associated with different groups you can list them individually. The [`@ImportHttpServices`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/service/registry/ImportHttpServices.html) is repeatable and the `types` attributes allows you to import individual classes.  For example:  * Java * Kotlin  ``` import org.springframework.boot.SpringApplication; import org.springframework.boot.autoconfigure.SpringBootApplication; import org.springframework.web.service.registry.ImportHttpServices;  @SpringBootApplication @ImportHttpServices(group = "echo", types = EchoService.class) @ImportHttpServices(group = "other", types = OtherService.class) public class MyApplication {  	public static void main(String[] args) { 		SpringApplication.run(MyApplication.class, args); 	}  } ```  ``` import org.springframework.boot.autoconfigure.SpringBootApplication import org.springframework.boot.runApplication import org.springframework.web.service.registry.ImportHttpServices  @SpringBootApplication @ImportHttpServices(group = "echo", types = [EchoService::class]) @ImportHttpServices(group = "other", types = [OtherService::class]) class MyApplication  fun main(args: Array<String>) { 	runApplication<MyApplication>(*args) } ``` |

### Configuration Properties

Configuration properties for HTTP Services can be specified under `spring.http.serviceclient.<group-name>`:

You can use properties to configure aspects such as:

* The base URL.
* Any default headers that should be sent.
* API versioning configuration.
* Redirect settings.
* Connection and read timeouts.
* SSL bundles to use.

|  |  |
| --- | --- |
|  | You can also use [global configuration properties](#io.rest-client.global-configuration) which apply to all HTTP clients. |

For example, the properties below will:

* Configure all HTTP clients to use a one second connect timeout (unless otherwise overridden).
* Configure HTTP Service clients in the “echo” group to:

  + Use a specific base URL.
  + Have a one-second connect timeout.
  + Have a two-second read timeout.

* Properties
* YAML

```
spring.http.clients.connect-timeout=1s
spring.http.serviceclient.echo.base-url=https://echo.zuplo.io
spring.http.serviceclient.echo.connect-timeout=2s
spring.http.serviceclient.echo.read-timeout=2s
```

```
spring:
  http:
    clients:
      connect-timeout: 1s
    serviceclient:
      echo:
        base-url: "https://echo.zuplo.io"
        connect-timeout: 2s
        read-timeout: 2s
```

### Customization

If you need to customize HTTP Service clients beyond basic properties, you can use an HTTP Service group configurer.
For `RestClient` backed HTTP Service clients, you can declare a bean that implements [`RestClientHttpServiceGroupConfigurer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/client/support/RestClientHttpServiceGroupConfigurer.html).
For `WebClient` backed HTTP Service clients you can declare a bean that implements [`WebClientHttpServiceGroupConfigurer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/reactive/function/client/support/WebClientHttpServiceGroupConfigurer.html).

Both work in the same way and will be automatically applied by Spring Boot’s auto-configuration.

For example, the following configuration would add a group customizer that adds an HTTP header to each outgoing request containing the group name:

* Java
* Kotlin

```
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.support.RestClientHttpServiceGroupConfigurer;

@Configuration(proxyBeanMethods = false)
public class MyHttpServiceGroupConfiguration {

	@Bean
	RestClientHttpServiceGroupConfigurer myHttpServiceGroupConfigurer() {
		return (groups) -> groups.forEachClient((group, clientBuilder) -> {
			String groupName = group.name();
			clientBuilder.defaultHeader("service-group", groupName);
		});
	}

}
```

```
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.web.client.support.RestClientHttpServiceGroupConfigurer

@Configuration(proxyBeanMethods = false)
class MyHttpServiceGroupConfiguration {

	@Bean
	fun myHttpServiceGroupConfigurer(): RestClientHttpServiceGroupConfigurer {
		return RestClientHttpServiceGroupConfigurer { groups ->
			groups.forEachClient { group, clientBuilder ->
				val groupName = group.name()
				clientBuilder.defaultHeader("service-group", groupName)
			}
		}
	}

}
```

### Advanced Configuration

As well as the [`@ImportHttpServices`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/service/registry/ImportHttpServices.html) annotation, Spring Framework also offers an [`AbstractHttpServiceRegistrar`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/web/service/registry/AbstractHttpServiceRegistrar.html) class.
You can [`@Import`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Import.html) your own extension of this class to perform programmatic configuration.
For more details, see [Spring Framework reference documentation](https://docs.spring.io/spring-framework/reference/7.0/integration/rest-clients.html#rest-http-service-client-group-config).

Regardless of which method you use to register HTTP Service clients, Spring Boot’s support remains the same.

## Applying Global Configuration to All HTTP Clients

Regardless of the underlying technology being used, all HTTP clients have common settings that can be configured.

These include:

* Connection Timeouts.
* Read Timeouts.
* How HTTP redirects should be handled.
* Which SSL bundle should be used when connecting.

These common settings are represented by the [`HttpClientSettings`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/http/client/HttpClientSettings.html) class which can be passed into the `build(…​)` methods of [`ClientHttpConnectorBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/http/client/reactive/ClientHttpConnectorBuilder.html) and [`ClientHttpRequestFactoryBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/http/client/ClientHttpRequestFactoryBuilder.html).

If you want to apply the same configuration to all auto-configured clients, you can use `spring.http.clients` properties to do so:

* Properties
* YAML

```
spring.http.clients.connect-timeout=2s
spring.http.clients.read-timeout=1s
spring.http.clients.redirects=dont-follow
```

```
spring:
  http:
    clients:
      connect-timeout: 2s
      read-timeout: 1s
      redirects: dont-follow
```

### InetAddress Filtering and SSRF Protection

It’s sometimes useful to limit the remote addresses that an HTTP client is permitted to call.
This technique can be especially useful when hardening your application against Server-Side Request Forgery (SSRF) attacks.

To limit the address that a client can call, you can use an [`InetAddressFilter`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/http/client/InetAddressFilter.html) which will only allow outgoing calls to addresses that match the filter.
The filter is a functional interface and you can either create your own implementation, or use one of the convenient factory methods.

Filters may be applied to the [`HttpClientSettings`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/http/client/HttpClientSettings.html) you used when building a client:

* Java
* Kotlin

```
import org.springframework.boot.http.client.ClientHttpRequestFactoryBuilder;
import org.springframework.boot.http.client.HttpClientSettings;
import org.springframework.boot.http.client.InetAddressFilter;
import org.springframework.http.client.ClientHttpRequestFactory;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service
public class MyService {

	private final RestClient restClient;

	public MyService() {
		InetAddressFilter onlyExternalAddresses = InetAddressFilter.externalAddresses();
		HttpClientSettings settings = HttpClientSettings.defaults().withInetAddressFilter(onlyExternalAddresses);
		ClientHttpRequestFactory requestFactory = ClientHttpRequestFactoryBuilder.jdk().build(settings);
		this.restClient = RestClient.builder().requestFactory(requestFactory).baseUrl("https://example.org").build();
	}

	public Details someRestCall(String name) {
		return this.restClient.get().uri("/{name}/details", name).retrieve().body(Details.class);
	}

}
```

```
import org.springframework.boot.http.client.ClientHttpRequestFactoryBuilder
import org.springframework.boot.http.client.HttpClientSettings
import org.springframework.boot.http.client.InetAddressFilter
import org.springframework.http.client.ClientHttpRequestFactory
import org.springframework.stereotype.Service
import org.springframework.web.client.RestClient

@Service
class MyService {

	private val restClient: RestClient

	init {
		val onlyExternalAddresses = InetAddressFilter.externalAddresses()
		val settings = HttpClientSettings.defaults().withInetAddressFilter(onlyExternalAddresses)
		val requestFactory: ClientHttpRequestFactory = ClientHttpRequestFactoryBuilder.jdk().build(settings)
		restClient = RestClient.builder().requestFactory(requestFactory).baseUrl("https://example.org").build()
	}

	fun someRestCall(name: String?): Details {
		return restClient.get().uri("/{name}/details", name)
			.retrieve().body(Details::class.java)!!
	}

}
```

Or you can also define one as a [`@Bean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Bean.html) if you want to apply it to all auto-configured HTTP client builders:

* Java
* Kotlin

```
import org.springframework.boot.http.client.InetAddressFilter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration(proxyBeanMethods = false)
public class MyHttpClientConfiguration {

	@Bean
	public InetAddressFilter httpClientInetAddressFilter() {
		return InetAddressFilter.of("192.168.1.0/24").andNot("192.168.1.1", "192.168.1.10");
	}

}
```

```
import org.springframework.boot.http.client.InetAddressFilter
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration

@Configuration(proxyBeanMethods = false)
class MyHttpClientConfiguration {

	@Bean
	fun httpClientInetAddressFilter(): InetAddressFilter {
		return InetAddressFilter.of("192.168.1.0/24").andNot("192.168.1.1", "192.168.1.10")
	}

}
```