Search

# Spring Security

If [Spring Security](https://spring.io/projects/spring-security) is on the classpath, then web applications are secured by default.
This includes securing Spring Boot’s `/error` endpoint.
Spring Boot relies on Spring Security’s content-negotiation strategy to determine whether to use `httpBasic` or `formLogin`.
To add method-level security to a web application, you can also add [`@EnableMethodSecurity`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/config/annotation/method/configuration/EnableMethodSecurity.html) with your desired settings.
Additional information can be found in the [Spring Security Reference Guide](https://docs.spring.io/spring-security/reference/7.1/servlet/authorization/method-security.html).

The default [`UserDetailsService`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/core/userdetails/UserDetailsService.html) has a single user.
The user name is `user`, and the password is random and is printed at WARN level when the application starts, as shown in the following example:

```
Using generated security password: 78fa095d-3f4c-48b1-ad50-e24c31d5cf35

This generated password is for development use only. Your security configuration must be updated before running your application in production.
```

|  |  |
| --- | --- |
|  | If you fine-tune your logging configuration, ensure that the `org.springframework.boot.security.autoconfigure` category is set to log `WARN`-level messages. Otherwise, the default password is not printed. |

You can change the username and password by providing a `spring.security.user.name` and `spring.security.user.password`.

The basic features you get by default in a web application are:

* A [`UserDetailsService`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/core/userdetails/UserDetailsService.html) (or [`ReactiveUserDetailsService`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/core/userdetails/ReactiveUserDetailsService.html) in case of a WebFlux application) bean with in-memory store and a single user with a generated password (see [`SecurityProperties.User`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/security/autoconfigure/SecurityProperties.User.html) for the properties of the user).
* Form-based login or HTTP Basic security (depending on the `Accept` header in the request) for the entire application (including actuator endpoints if actuator is on the classpath).
* A [`DefaultAuthenticationEventPublisher`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/authentication/DefaultAuthenticationEventPublisher.html) for publishing authentication events.

You can provide a different [`AuthenticationEventPublisher`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/authentication/AuthenticationEventPublisher.html) by adding a bean for it.

## MVC Security

The default security configuration is implemented in [`SecurityAutoConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/security/autoconfigure/SecurityAutoConfiguration.html) and [`UserDetailsServiceAutoConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/security/autoconfigure/UserDetailsServiceAutoConfiguration.html).
[`SecurityAutoConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/security/autoconfigure/SecurityAutoConfiguration.html) imports `SpringBootWebSecurityConfiguration` for web security and [`UserDetailsServiceAutoConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/security/autoconfigure/UserDetailsServiceAutoConfiguration.html) for authentication.

To completely switch off the default web application security configuration, including Actuator security, or to combine multiple Spring Security components such as OAuth2 Client and Resource Server, add a bean of type [`SecurityFilterChain`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/web/SecurityFilterChain.html) (doing so does not disable the [`UserDetailsService`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/core/userdetails/UserDetailsService.html) configuration).
To also switch off the [`UserDetailsService`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/core/userdetails/UserDetailsService.html) configuration, add a bean of type [`UserDetailsService`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/core/userdetails/UserDetailsService.html), [`AuthenticationProvider`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/authentication/AuthenticationProvider.html), or [`AuthenticationManager`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/authentication/AuthenticationManager.html).

The auto-configuration of a [`UserDetailsService`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/core/userdetails/UserDetailsService.html) will also back off when any of the following Spring Security modules is on the classpath:

* `spring-security-oauth2-client`
* `spring-security-oauth2-resource-server`
* `spring-security-saml2-service-provider`

To use [`UserDetailsService`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/core/userdetails/UserDetailsService.html) in addition to one or more of these dependencies, define your own [`InMemoryUserDetailsManager`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/provisioning/InMemoryUserDetailsManager.html) bean.

Access rules can be overridden by adding a custom [`SecurityFilterChain`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/web/SecurityFilterChain.html) bean.
Spring Boot provides convenience methods that can be used to override access rules for actuator endpoints and static resources.
[`EndpointRequest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/security/autoconfigure/actuate/web/servlet/EndpointRequest.html) can be used to create a [`RequestMatcher`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/web/util/matcher/RequestMatcher.html) that is based on the `management.endpoints.web.base-path` property.
[`PathRequest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/security/autoconfigure/web/servlet/PathRequest.html) can be used to create a [`RequestMatcher`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/web/util/matcher/RequestMatcher.html) for resources in commonly used locations.

## WebFlux Security

Similar to Spring MVC applications, you can secure your WebFlux applications by adding the `spring-boot-starter-security` dependency.
The default security configuration is implemented in [`ReactiveWebSecurityAutoConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/security/autoconfigure/web/reactive/ReactiveWebSecurityAutoConfiguration.html) and [`ReactiveUserDetailsServiceAutoConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/security/autoconfigure/ReactiveUserDetailsServiceAutoConfiguration.html).
In addition to reactive web applications, the latter is also auto-configured when RSocket is in use.
[`ReactiveWebSecurityAutoConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/security/autoconfigure/web/reactive/ReactiveWebSecurityAutoConfiguration.html) imports `WebFluxSecurityConfiguration` for web security.
[`ReactiveUserDetailsServiceAutoConfiguration`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/security/autoconfigure/ReactiveUserDetailsServiceAutoConfiguration.html) auto-configures authentication.

To completely switch off the default web application security configuration, including Actuator security, add a bean of type [`WebFilterChainProxy`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/web/server/WebFilterChainProxy.html) (doing so does not disable the [`ReactiveUserDetailsService`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/core/userdetails/ReactiveUserDetailsService.html) configuration).
To also switch off the [`ReactiveUserDetailsService`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/core/userdetails/ReactiveUserDetailsService.html) configuration, add a bean of type [`ReactiveUserDetailsService`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/core/userdetails/ReactiveUserDetailsService.html) or [`ReactiveAuthenticationManager`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/authentication/ReactiveAuthenticationManager.html).

The auto-configuration will also back off when any of the following Spring Security modules is on the classpath:

* `spring-security-oauth2-client`
* `spring-security-oauth2-resource-server`

To use [`ReactiveUserDetailsService`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/core/userdetails/ReactiveUserDetailsService.html) in addition to one or more of these dependencies, define your own [`MapReactiveUserDetailsService`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/core/userdetails/MapReactiveUserDetailsService.html) bean.

Access rules and the use of multiple Spring Security components such as OAuth 2 Client and Resource Server can be configured by adding a custom [`SecurityWebFilterChain`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/web/server/SecurityWebFilterChain.html) bean.
Spring Boot provides convenience methods that can be used to override access rules for actuator endpoints and static resources.
[`EndpointRequest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/security/autoconfigure/actuate/web/reactive/EndpointRequest.html) can be used to create a [`ServerWebExchangeMatcher`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/web/server/util/matcher/ServerWebExchangeMatcher.html) that is based on the `management.endpoints.web.base-path` property.

[`PathRequest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/security/autoconfigure/web/reactive/PathRequest.html) can be used to create a [`ServerWebExchangeMatcher`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/web/server/util/matcher/ServerWebExchangeMatcher.html) for resources in commonly used locations.

For example, you can customize your security configuration by adding something like:

```
import org.springframework.boot.security.autoconfigure.web.reactive.PathRequest;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.web.server.ServerHttpSecurity;
import org.springframework.security.web.server.SecurityWebFilterChain;

import static org.springframework.security.config.Customizer.withDefaults;

@Configuration(proxyBeanMethods = false)
public class MyWebFluxSecurityConfiguration {

	@Bean
	public SecurityWebFilterChain springSecurityFilterChain(ServerHttpSecurity http) {
		http.authorizeExchange((exchange) -> {
			exchange.matchers(PathRequest.toStaticResources().atCommonLocations()).permitAll();
			exchange.pathMatchers("/foo", "/bar").authenticated();
		});
		http.formLogin(withDefaults());
		return http.build();
	}

}
```

## OAuth2

[OAuth2](https://oauth.net/2/) is a widely used authorization framework.
For details of how to configure and use OAuth2 with your web applications, see the [“OAuth2” section](../security/oauth2.html#security.oauth2) of under “Security”.

## SAML 2.0

[SAML v2.0](https://docs.oasis-open.org/security/saml/Post2.0/sstc-saml-tech-overview-2.0.html) is a widely adopted framework for exchanging security information between online business partners.
For details of how to configure and use SAML 2.0 with your web applications, see the [“SAML 2.0” section](../security/saml2.html#security.saml2) under “Security”.