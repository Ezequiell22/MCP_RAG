Search

# Aspect-Oriented Programming

Spring Boot provides auto-configuration for aspect-oriented programming (AOP).
You can learn more about AOP with Spring in the [Spring Framework reference documentation](https://docs.spring.io/spring-framework/reference/7.0/core/aop-api.html).

By default, Spring Boot’s auto-configuration configures Spring AOP to use CGLib proxies.
To use JDK proxies instead, set `spring.aop.proxy-target-class` to `false`.

If AspectJ is on the classpath, Spring Boot’s auto-configuration will automatically enable AspectJ auto proxy such that [`@EnableAspectJAutoProxy`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/EnableAspectJAutoProxy.html) is not required.