Search

# Recording HTTP Exchanges

You can enable recording of HTTP exchanges by providing a bean of type [`HttpExchangeRepository`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/web/exchanges/HttpExchangeRepository.html) in your application’s configuration.
For convenience, Spring Boot offers [`InMemoryHttpExchangeRepository`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/web/exchanges/InMemoryHttpExchangeRepository.html), which, by default, stores the last 100 request-response exchanges.
[`InMemoryHttpExchangeRepository`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/web/exchanges/InMemoryHttpExchangeRepository.html) is limited compared to tracing solutions, and we recommend using it only for development environments.
For production environments, we recommend using a production-ready tracing or observability solution, such as Zipkin or OpenTelemetry.
Alternatively, you can create your own [`HttpExchangeRepository`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/web/exchanges/HttpExchangeRepository.html).

You can use the `httpexchanges` endpoint to obtain information about the request-response exchanges that are stored in the [`HttpExchangeRepository`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/web/exchanges/HttpExchangeRepository.html).

## Custom HTTP Exchange Recording

To customize the items that are included in each recorded exchange, use the `management.httpexchanges.recording.include` configuration property.

To disable recording entirely, set `management.httpexchanges.recording.enabled` to `false`.