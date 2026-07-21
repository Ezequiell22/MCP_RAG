Search

# Test Scope Dependencies

The `spring-boot-starter-test` starter (in the `test` `scope`) contains the following provided libraries:

* [JUnit](https://junit.org): The de-facto standard for unit testing Java applications.
* [Spring Test](https://docs.spring.io/spring-framework/reference/7.0/testing/integration.html) & Spring Boot Test: Utilities and integration test support for Spring Boot applications.
* [AssertJ](https://assertj.github.io/doc/): A fluent assertion library.
* [Hamcrest](https://github.com/hamcrest/JavaHamcrest): A library of matcher objects (also known as constraints or predicates).
* [Mockito](https://site.mockito.org/): A Java mocking framework.
* [JSONassert](https://github.com/skyscreamer/JSONassert): An assertion library for JSON.
* [JsonPath](https://github.com/jayway/JsonPath): XPath for JSON.
* [Awaitility](https://github.com/awaitility/awaitility): A library for testing asynchronous systems.

We generally find these common libraries to be useful when writing tests.
If these libraries do not suit your needs, you can add additional test dependencies of your own.