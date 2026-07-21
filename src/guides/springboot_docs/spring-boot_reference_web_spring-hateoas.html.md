Search

# Spring HATEOAS

If you develop a RESTful API that makes use of hypermedia, Spring Boot provides auto-configuration for Spring HATEOAS that works well with most applications.
The auto-configuration replaces the need to use [`@EnableHypermediaSupport`](https://docs.spring.io/spring-hateoas/docs/3.1.x/api/org/springframework/hateoas/config/EnableHypermediaSupport.html) and registers a number of beans to ease building hypermedia-based applications, including a [`LinkDiscoverers`](https://docs.spring.io/spring-hateoas/docs/3.1.x/api/org/springframework/hateoas/client/LinkDiscoverers.html) (for client side support) and an [`JsonMapper`](https://javadoc.io/doc/tools.jackson.core/jackson-databind/3.1.4/tools/jackson/databind/json/JsonMapper.html) configured to correctly marshal responses into the desired representation.
The [`JsonMapper`](https://javadoc.io/doc/tools.jackson.core/jackson-databind/3.1.4/tools/jackson/databind/json/JsonMapper.html) is customized by setting the various `spring.jackson.*` properties or, if any exist, the [`JsonMapperBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jackson/autoconfigure/JsonMapperBuilderCustomizer.html) beans.

You can take control of Spring HATEOAS’s configuration by using [`@EnableHypermediaSupport`](https://docs.spring.io/spring-hateoas/docs/3.1.x/api/org/springframework/hateoas/config/EnableHypermediaSupport.html).
Note that doing so disables the [`JsonMapper`](https://javadoc.io/doc/tools.jackson.core/jackson-databind/3.1.4/tools/jackson/databind/json/JsonMapper.html) customization described earlier.

|  |  |
| --- | --- |
|  | `spring-boot-starter-hateoas` is specific to Spring MVC and should not be combined with Spring WebFlux. In order to use Spring HATEOAS with Spring WebFlux, you can add a direct dependency on `org.springframework.hateoas:spring-hateoas` along with `spring-boot-starter-webflux`. |

By default, requests that accept `application/json` will receive an `application/hal+json` response.
To disable this behavior set `spring.hateoas.use-hal-as-default-json-media-type` to `false` and define a [`HypermediaMappingInformation`](https://docs.spring.io/spring-hateoas/docs/3.1.x/api/org/springframework/hateoas/config/HypermediaMappingInformation.html) or [`HalConfiguration`](https://docs.spring.io/spring-hateoas/docs/3.1.x/api/org/springframework/hateoas/mediatype/hal/HalConfiguration.html) to configure Spring HATEOAS to meet the needs of your application and its clients.