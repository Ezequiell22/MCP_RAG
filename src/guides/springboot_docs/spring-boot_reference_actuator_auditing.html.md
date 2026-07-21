Search

# Auditing

Once Spring Security is in play, Spring Boot Actuator has a flexible audit framework that publishes events (by default, “authentication success”, “failure” and “access denied” exceptions).
This feature can be very useful for reporting and for implementing a lock-out policy based on authentication failures.

You can enable auditing by providing a bean of type [`AuditEventRepository`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/audit/AuditEventRepository.html) in your application’s configuration.
For convenience, Spring Boot offers an [`InMemoryAuditEventRepository`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/audit/InMemoryAuditEventRepository.html).
[`InMemoryAuditEventRepository`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/audit/InMemoryAuditEventRepository.html) has limited capabilities, and we recommend using it only for development environments.
For production environments, consider creating your own alternative [`AuditEventRepository`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/audit/AuditEventRepository.html) implementation.

## Custom Auditing

To customize published security events, you can provide your own implementations of [`AbstractAuthenticationAuditListener`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/security/AbstractAuthenticationAuditListener.html) and [`AbstractAuthorizationAuditListener`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/security/AbstractAuthorizationAuditListener.html).

You can also use the audit services for your own business events.
To do so, either inject the [`AuditEventRepository`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/audit/AuditEventRepository.html) bean into your own components and use that directly or publish an [`AuditApplicationEvent`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/actuate/audit/listener/AuditApplicationEvent.html) with the Spring [`ApplicationEventPublisher`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationEventPublisher.html) (by implementing [`ApplicationEventPublisherAware`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationEventPublisherAware.html)).