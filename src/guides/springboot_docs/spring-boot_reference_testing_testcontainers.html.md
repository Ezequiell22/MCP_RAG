Search

# Testcontainers

The [Testcontainers](https://www.testcontainers.org/) library provides a way to manage services running inside Docker containers.
It integrates with JUnit, allowing you to write a test class that can start up a container before any of the tests run.
Testcontainers is especially useful for writing integration tests that talk to a real backend service such as MySQL, MongoDB, Cassandra and others.

In following sections we will describe some of the methods you can use to integrate Testcontainers with your tests.

## Using Spring Beans

The containers provided by Testcontainers can be managed by Spring Boot as beans.

To declare a container as a bean, add a [`@Bean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Bean.html) method to your test configuration:

* Java
* Kotlin

```
import org.testcontainers.mongodb.MongoDBContainer;
import org.testcontainers.utility.DockerImageName;

import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;

@TestConfiguration(proxyBeanMethods = false)
class MyTestConfiguration {

	@Bean
	MongoDBContainer mongoDbContainer() {
		return new MongoDBContainer(DockerImageName.parse("mongo:5.0"));
	}

}
```

```
import org.springframework.boot.test.context.TestConfiguration
import org.springframework.context.annotation.Bean
import org.testcontainers.mongodb.MongoDBContainer
import org.testcontainers.utility.DockerImageName

@TestConfiguration(proxyBeanMethods = false)
class MyTestConfiguration {

	@Bean
	fun mongoDbContainer(): MongoDBContainer {
		return MongoDBContainer(DockerImageName.parse("mongo:5.0"))
	}

}
```

You can then inject and use the container by importing the configuration class in the test class:

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;
import org.testcontainers.mongodb.MongoDBContainer;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Import;

@SpringBootTest
@Import(MyTestConfiguration.class)
class MyIntegrationTests {

	@Autowired
	private MongoDBContainer mongo;

	@Test
	void myTest() {
		...
	}

}
```

```
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.context.annotation.Import
import org.testcontainers.mongodb.MongoDBContainer

@SpringBootTest
@Import(MyTestConfiguration::class)
class MyIntegrationTests {

	@Autowired
	private val mongo: MongoDBContainer? = null

	@Test
	fun myTest() {
		...
	}

}
```

|  |  |
| --- | --- |
|  | This method of managing containers is often used in combination with [service connection annotations](#testing.testcontainers.service-connections). |

## Using the JUnit Extension

Testcontainers provides a JUnit extension which can be used to manage containers in your tests.
The extension is activated by applying the [`@Testcontainers`](https://javadoc.io/doc/org.testcontainers/junit-jupiter/2.0.5/org/testcontainers/junit/jupiter/Testcontainers.html) annotation from Testcontainers to your test class.

You can then use the [`@Container`](https://javadoc.io/doc/org.testcontainers/junit-jupiter/2.0.5/org/testcontainers/junit/jupiter/Container.html) annotation on static container fields.

The [`@Testcontainers`](https://javadoc.io/doc/org.testcontainers/junit-jupiter/2.0.5/org/testcontainers/junit/jupiter/Testcontainers.html) annotation can be used on vanilla JUnit tests, or in combination with [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html):

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.neo4j.Neo4jContainer;

import org.springframework.boot.test.context.SpringBootTest;

@Testcontainers
@SpringBootTest
class MyIntegrationTests {

	@Container
	static Neo4jContainer neo4j = new Neo4jContainer("neo4j:5");

	@Test
	void myTest() {
		...
	}

}
```

```
import org.junit.jupiter.api.Test;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.neo4j.Neo4jContainer;

import org.springframework.boot.test.context.SpringBootTest;

@Testcontainers
@SpringBootTest
class MyIntegrationTests {

	@Test
	fun myTest() {
		...
	}

	companion object {

		@Container
		@JvmStatic
		val neo4j = Neo4jContainer("neo4j:5");

	}
}
```

The example above will start up a Neo4j container before any of the tests are run.
The lifecycle of the container instance is managed by Testcontainers, as described in [their official documentation](https://java.testcontainers.org/test_framework_integration/junit_5/#extension).

When using the JUnit extension, container instances are stopped after the test class has run (for static fields) or after each test method (for non-static fields).
This can cause issues when used with Spring Boot tests, as Spring’s TestContext Framework may cache the [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html) beyond that point and reuse it for another test class or method with the same configuration.
If the cached application context contains beans that depend on a container that has already been stopped, later tests or bean destruction callbacks may fail.
For this reason, you should prefer [managing containers as Spring beans](#testing.testcontainers.spring-beans) or [importing container declarations](#testing.testcontainers.importing-configuration-interfaces) when the application context should remain usable for as long as it is cached.

|  |  |
| --- | --- |
|  | In most cases, you will additionally need to configure the application to connect to the service running in the container. |

## Importing Container Configuration Interfaces

A common pattern with Testcontainers is to declare the container instances as static fields in an interface.

For example, the following interface declares two containers, one named `mongo` of type [`MongoDBContainer`](https://javadoc.io/doc/org.testcontainers/mongodb/2.0.5/org/testcontainers/mongodb/MongoDBContainer.html) and another named `neo4j` of type [`Neo4jContainer`](https://javadoc.io/doc/org.testcontainers/neo4j/2.0.5/org/testcontainers/neo4j/Neo4jContainer.html):

* Java
* Kotlin

```
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.mongodb.MongoDBContainer;
import org.testcontainers.neo4j.Neo4jContainer;

interface MyContainers {

	@Container
	MongoDBContainer mongoContainer = new MongoDBContainer("mongo:5.0");

	@Container
	Neo4jContainer neo4jContainer = new Neo4jContainer("neo4j:5");

}
```

```
import org.testcontainers.junit.jupiter.Container
import org.testcontainers.mongodb.MongoDBContainer
import org.testcontainers.neo4j.Neo4jContainer

interface MyContainers {

	companion object {

		@Container
		val mongoContainer: MongoDBContainer = MongoDBContainer("mongo:5.0")

		@Container
		val neo4jContainer: Neo4jContainer = Neo4jContainer("neo4j:5")

	}

}
```

When you have containers declared in this way, you can reuse their configuration in multiple tests by having the test classes implement the interface.

It’s also possible to use the same interface configuration in your Spring Boot tests.
To do so, add [`@ImportTestcontainers`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/testcontainers/context/ImportTestcontainers.html) to your test configuration class:

* Java
* Kotlin

```
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.boot.testcontainers.context.ImportTestcontainers;

@TestConfiguration(proxyBeanMethods = false)
@ImportTestcontainers(MyContainers.class)
class MyTestConfiguration {

}
```

```
import org.springframework.boot.test.context.TestConfiguration
import org.springframework.boot.testcontainers.context.ImportTestcontainers

@TestConfiguration(proxyBeanMethods = false)
@ImportTestcontainers(MyContainers::class)
class MyTestConfiguration {

}
```

## Lifecycle of Managed Containers

If you have used the annotations and extensions provided by Testcontainers, then the lifecycle of container instances is managed entirely by Testcontainers.
Please refer to the [official Testcontainers documentation](https://java.testcontainers.org) for the information.

When the containers are managed by Spring as beans, then their lifecycle is managed by Spring:

* Container beans are created and started before all other beans.
* Container beans are stopped after the destruction of all other beans.

This process ensures that any beans, which rely on functionality provided by the containers, can use those functionalities.
It also ensures that they are cleaned up whilst the container is still available.

|  |  |
| --- | --- |
|  | When your application beans rely on functionality of containers, prefer configuring the containers as Spring beans to ensure the correct lifecycle behavior. |

|  |  |
| --- | --- |
|  | Having containers managed by Testcontainers instead of as Spring beans provides no guarantee of the order in which beans and containers will shutdown. It can happen that containers are shutdown before the beans relying on container functionality are cleaned up. This can lead to exceptions being thrown by client beans, for example, due to loss of connection. When the application context should remain usable for as long as it is cached, prefer managing containers as Spring beans or importing container declarations with [`@ImportTestcontainers`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/testcontainers/context/ImportTestcontainers.html). |

Container beans are created and started once per application context managed by Spring’s TestContext Framework.
For details about how the TestContext Framework manages the underlying application contexts and beans therein, please refer to the [Spring Framework documentation](https://docs.spring.io/spring-framework/reference/7.0).

Container beans are stopped as part of the TestContext Framework’s standard application context shutdown process.
When the application context gets shutdown, the containers are shutdown as well.
This usually happens after all tests using that specific cached application context have finished executing.
It may also happen earlier, depending on the caching behavior configured in the TestContext Framework.

|  |  |
| --- | --- |
|  | A single test container instance can, and often is, retained across execution of tests from multiple test classes. |

## Service Connections

A service connection is a connection to any remote service.
Spring Boot’s auto-configuration can consume the details of a service connection and use them to establish a connection to a remote service.
When doing so, the connection details take precedence over any connection-related configuration properties.

When using Testcontainers, connection details can be automatically created for a service running in a container by annotating the container field in the test class.

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.neo4j.Neo4jContainer;

import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;

@Testcontainers
@SpringBootTest
class MyIntegrationTests {

	@Container
	@ServiceConnection
	static Neo4jContainer neo4j = new Neo4jContainer("neo4j:5");

	@Test
	void myTest() {
		...
	}

}
```

```
import org.junit.jupiter.api.Test;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.neo4j.Neo4jContainer;

import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;

@Testcontainers
@SpringBootTest
class MyIntegrationTests {

	@Test
	fun myTest() {
		...
	}

	companion object {

		@Container
		@ServiceConnection
		@JvmStatic
		val neo4j = Neo4jContainer("neo4j:5");

	}

}
```

Thanks to [`@ServiceConnection`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/testcontainers/service/connection/ServiceConnection.html), the above configuration allows Neo4j-related beans in the application to communicate with Neo4j running inside the Testcontainers-managed Docker container.
This is done by automatically defining a [`Neo4jConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/neo4j/autoconfigure/Neo4jConnectionDetails.html) bean which is then used by the Neo4j auto-configuration, overriding any connection-related configuration properties.

|  |  |
| --- | --- |
|  | You’ll need to add the `spring-boot-testcontainers` module as a test dependency in order to use service connections with Testcontainers. |

Service connection annotations are processed by [`ContainerConnectionDetailsFactory`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/testcontainers/service/connection/ContainerConnectionDetailsFactory.html) classes registered with `spring.factories`.
A [`ContainerConnectionDetailsFactory`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/testcontainers/service/connection/ContainerConnectionDetailsFactory.html) can create a [`ConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/service/connection/ConnectionDetails.html) bean based on a specific [`Container`](https://javadoc.io/doc/org.testcontainers/testcontainers/2.0.5/org/testcontainers/containers/Container.html) subclass, or the Docker image name.

The following service connection factories are provided in the `spring-boot-testcontainers` jar:

| Connection Details | Matched on |
| --- | --- |
| [`ActiveMQConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/activemq/autoconfigure/ActiveMQConnectionDetails.html) | Containers named "symptoma/activemq" or [`ActiveMQContainer`](https://javadoc.io/doc/org.testcontainers/activemq/2.0.5/org/testcontainers/activemq/ActiveMQContainer.html) |
| [`ArtemisConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/artemis/autoconfigure/ArtemisConnectionDetails.html) | Containers of type [`ArtemisContainer`](https://javadoc.io/doc/org.testcontainers/activemq/2.0.5/org/testcontainers/activemq/ArtemisContainer.html) |
| [`CassandraConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/cassandra/autoconfigure/CassandraConnectionDetails.html) | Containers of type [`CassandraContainer`](https://javadoc.io/doc/org.testcontainers/testcontainers/2.0.5/org/testcontainers/cassandra/CassandraContainer.html) |
| [`CouchbaseConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/couchbase/autoconfigure/CouchbaseConnectionDetails.html) | Containers of type [`CouchbaseContainer`](https://javadoc.io/doc/org.testcontainers/couchbase/2.0.5/org/testcontainers/couchbase/CouchbaseContainer.html) |
| [`ElasticsearchConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/elasticsearch/autoconfigure/ElasticsearchConnectionDetails.html) | Containers of type [`ElasticsearchContainer`](https://javadoc.io/doc/org.testcontainers/elasticsearch/2.0.5/org/testcontainers/elasticsearch/ElasticsearchContainer.html) |
| [`FlywayConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/flyway/autoconfigure/FlywayConnectionDetails.html) | Containers of type [`JdbcDatabaseContainer`](https://javadoc.io/doc/org.testcontainers/jdbc/2.0.5/org/testcontainers/containers/JdbcDatabaseContainer.html) |
| [`JdbcConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jdbc/autoconfigure/JdbcConnectionDetails.html) | Containers of type [`JdbcDatabaseContainer`](https://javadoc.io/doc/org.testcontainers/jdbc/2.0.5/org/testcontainers/containers/JdbcDatabaseContainer.html) |
| [`KafkaConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/kafka/autoconfigure/KafkaConnectionDetails.html) | Containers of type [`KafkaContainer`](https://javadoc.io/doc/org.testcontainers/kafka/2.0.5/org/testcontainers/kafka/KafkaContainer.html), [`ConfluentKafkaContainer`](https://javadoc.io/doc/org.testcontainers/kafka/2.0.5/org/testcontainers/kafka/ConfluentKafkaContainer.html) or [`RedpandaContainer`](https://javadoc.io/doc/org.testcontainers/redpanda/2.0.5/org/testcontainers/redpanda/RedpandaContainer.html) |
| [`LdapConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/ldap/autoconfigure/LdapConnectionDetails.html) | Containers named "osixia/openldap" or of type [`LLdapContainer`](https://javadoc.io/doc/org.testcontainers/testcontainers/2.0.5/org/testcontainers/ldap/LLdapContainer.html) |
| [`LiquibaseConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/liquibase/autoconfigure/LiquibaseConnectionDetails.html) | Containers of type [`JdbcDatabaseContainer`](https://javadoc.io/doc/org.testcontainers/jdbc/2.0.5/org/testcontainers/containers/JdbcDatabaseContainer.html) |
| [`MongoConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/mongodb/autoconfigure/MongoConnectionDetails.html) | Containers of type [`MongoDBContainer`](https://javadoc.io/doc/org.testcontainers/mongodb/2.0.5/org/testcontainers/mongodb/MongoDBContainer.html) or [`MongoDBAtlasLocalContainer`](https://javadoc.io/doc/org.testcontainers/mongodb/2.0.5/org/testcontainers/mongodb/MongoDBAtlasLocalContainer.html) |
| [`Neo4jConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/neo4j/autoconfigure/Neo4jConnectionDetails.html) | Containers of type [`Neo4jContainer`](https://javadoc.io/doc/org.testcontainers/neo4j/2.0.5/org/testcontainers/neo4j/Neo4jContainer.html) |
| [`OtlpLoggingConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/opentelemetry/autoconfigure/logging/otlp/OtlpLoggingConnectionDetails.html) | Containers named "otel/opentelemetry-collector-contrib" or of type [`LgtmStackContainer`](https://javadoc.io/doc/org.testcontainers/grafana/2.0.5/org/testcontainers/grafana/LgtmStackContainer.html) |
| [`OtlpMetricsConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/micrometer/metrics/autoconfigure/export/otlp/OtlpMetricsConnectionDetails.html) | Containers named "otel/opentelemetry-collector-contrib" or of type [`LgtmStackContainer`](https://javadoc.io/doc/org.testcontainers/grafana/2.0.5/org/testcontainers/grafana/LgtmStackContainer.html) |
| [`OtlpTracingConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/micrometer/tracing/opentelemetry/autoconfigure/otlp/OtlpTracingConnectionDetails.html) | Containers named "otel/opentelemetry-collector-contrib" or of type [`LgtmStackContainer`](https://javadoc.io/doc/org.testcontainers/grafana/2.0.5/org/testcontainers/grafana/LgtmStackContainer.html) |
| [`PulsarConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/pulsar/autoconfigure/PulsarConnectionDetails.html) | Containers of type [`PulsarContainer`](https://javadoc.io/doc/org.testcontainers/pulsar/2.0.5/org/testcontainers/pulsar/PulsarContainer.html) |
| [`R2dbcConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/r2dbc/autoconfigure/R2dbcConnectionDetails.html) | Containers of type [`ClickHouseContainer`](https://javadoc.io/doc/org.testcontainers/clickhouse/2.0.5/org/testcontainers/clickhouse/ClickHouseContainer.html), [`MariaDBContainer`](https://javadoc.io/doc/org.testcontainers/mariadb/2.0.5/org/testcontainers/mariadb/MariaDBContainer.html), [`MSSQLServerContainer`](https://javadoc.io/doc/org.testcontainers/mssqlserver/2.0.5/org/testcontainers/mssqlserver/MSSQLServerContainer.html), [`MySQLContainer`](https://javadoc.io/doc/org.testcontainers/mysql/2.0.5/org/testcontainers/mysql/MySQLContainer.html), [OracleContainer (free)](https://javadoc.io/doc/org.testcontainers/oracle-free/2.0.5/org/testcontainers/oracle/OracleContainer.html), [OracleContainer (XE)](https://javadoc.io/doc/org.testcontainers/oracle-xe/2.0.5/org/testcontainers/containers/OracleContainer.html) or [`PostgreSQLContainer`](https://javadoc.io/doc/org.testcontainers/postgresql/2.0.5/org/testcontainers/postgresql/PostgreSQLContainer.html) |
| [`RabbitConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/amqp/autoconfigure/RabbitConnectionDetails.html) | Containers of type [`RabbitMQContainer`](https://javadoc.io/doc/org.testcontainers/rabbitmq/2.0.5/org/testcontainers/rabbitmq/RabbitMQContainer.html) |
| [`RabbitStreamConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/amqp/autoconfigure/RabbitStreamConnectionDetails.html) | Containers of type [`RabbitMQContainer`](https://javadoc.io/doc/org.testcontainers/rabbitmq/2.0.5/org/testcontainers/rabbitmq/RabbitMQContainer.html) when the `@ServiceConnection` `type` attribute includes [`RabbitStreamConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/amqp/autoconfigure/RabbitStreamConnectionDetails.html) |
| [`DataRedisConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/redis/autoconfigure/DataRedisConnectionDetails.html) | Containers of type [`RedisContainer`](https://javadoc.io/doc/com.redis/testcontainers-redis/2.2.4/com/redis/testcontainers/RedisContainer.html) or [`RedisStackContainer`](https://javadoc.io/doc/com.redis/testcontainers-redis/2.2.4/com/redis/testcontainers/RedisStackContainer.html), or containers named "redis", "redis/redis-stack" or "redis/redis-stack-server" |
| [`ZipkinConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/zipkin/autoconfigure/ZipkinConnectionDetails.html) | Containers named "openzipkin/zipkin" |

|  |  |
| --- | --- |
|  | By default, with the exception of [`RabbitStreamConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/amqp/autoconfigure/RabbitStreamConnectionDetails.html), all applicable connection details beans will be created for a given [`Container`](https://javadoc.io/doc/org.testcontainers/testcontainers/2.0.5/org/testcontainers/containers/Container.html). For example, a [`PostgreSQLContainer`](https://javadoc.io/doc/org.testcontainers/postgresql/2.0.5/org/testcontainers/postgresql/PostgreSQLContainer.html) will create both [`JdbcConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jdbc/autoconfigure/JdbcConnectionDetails.html) and [`R2dbcConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/r2dbc/autoconfigure/R2dbcConnectionDetails.html).  If you want to create only a subset of the applicable types, you can use the `type` attribute of [`@ServiceConnection`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/testcontainers/service/connection/ServiceConnection.html).  To create a [`RabbitStreamConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/amqp/autoconfigure/RabbitStreamConnectionDetails.html) bean from a [`RabbitMQContainer`](https://javadoc.io/doc/org.testcontainers/rabbitmq/2.0.5/org/testcontainers/rabbitmq/RabbitMQContainer.html), you must opt in using the `type` attribute of [`@ServiceConnection`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/testcontainers/service/connection/ServiceConnection.html). The container must also expose port 5552, the RabbitMQ streams port. |

By default `Container.getDockerImageName().getRepository()` is used to obtain the name used to find connection details.
The repository portion of the Docker image name ignores any registry and the version.
This works as long as Spring Boot is able to get the instance of the [`Container`](https://javadoc.io/doc/org.testcontainers/testcontainers/2.0.5/org/testcontainers/containers/Container.html), which is the case when using a `static` field like in the example above.

If you’re using a [`@Bean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Bean.html) method, Spring Boot won’t call the bean method to get the Docker image name, because this would cause eager initialization issues.
Instead, the return type of the bean method is used to find out which connection detail should be used.
This works as long as you’re using typed containers such as [`Neo4jContainer`](https://javadoc.io/doc/org.testcontainers/neo4j/2.0.5/org/testcontainers/neo4j/Neo4jContainer.html) or [`RabbitMQContainer`](https://javadoc.io/doc/org.testcontainers/rabbitmq/2.0.5/org/testcontainers/rabbitmq/RabbitMQContainer.html).
This stops working if you’re using [`GenericContainer`](https://javadoc.io/doc/org.testcontainers/testcontainers/2.0.5/org/testcontainers/containers/GenericContainer.html), for example with Redis as shown in the following example:

* Java
* Kotlin

```
import org.testcontainers.containers.GenericContainer;

import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.springframework.context.annotation.Bean;

@TestConfiguration(proxyBeanMethods = false)
public class MyRedisConfiguration {

	@Bean
	@ServiceConnection(name = "redis")
	public GenericContainer<?> redisContainer() {
		return new GenericContainer<>("redis:7");
	}

}
```

```
import org.springframework.boot.test.context.TestConfiguration
import org.springframework.boot.testcontainers.service.connection.ServiceConnection
import org.springframework.context.annotation.Bean
import org.testcontainers.containers.GenericContainer

@TestConfiguration(proxyBeanMethods = false)
class MyRedisConfiguration {

	@Bean
	@ServiceConnection(name = "redis")
	fun redisContainer(): GenericContainer<*> {
		return GenericContainer("redis:7")
	}

}
```

Spring Boot can’t tell from [`GenericContainer`](https://javadoc.io/doc/org.testcontainers/testcontainers/2.0.5/org/testcontainers/containers/GenericContainer.html) which container image is used, so the `name` attribute from [`@ServiceConnection`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/testcontainers/service/connection/ServiceConnection.html) must be used to provide that hint.

You can also use the `name` attribute of [`@ServiceConnection`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/testcontainers/service/connection/ServiceConnection.html) to override which connection detail will be used, for example when using custom images.
If you are using the Docker image `registry.mycompany.com/mirror/myredis`, you’d use `@ServiceConnection(name="redis")` to ensure [`DataRedisConnectionDetails`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/redis/autoconfigure/DataRedisConnectionDetails.html) are created.

### SSL with Service Connections

You can use the [`@Ssl`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/testcontainers/service/connection/Ssl.html), [`@JksKeyStore`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/testcontainers/service/connection/JksKeyStore.html), [`@JksTrustStore`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/testcontainers/service/connection/JksTrustStore.html), [`@PemKeyStore`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/testcontainers/service/connection/PemKeyStore.html) and [`@PemTrustStore`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/testcontainers/service/connection/PemTrustStore.html) annotations on a supported container to enable SSL support for that service connection.
Please note that you still have to enable SSL on the service which is running inside the Testcontainer yourself, the annotations only configure SSL on the client side in your application.

```
import com.redis.testcontainers.RedisContainer;
import org.junit.jupiter.api.Test;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.testcontainers.service.connection.PemKeyStore;
import org.springframework.boot.testcontainers.service.connection.PemTrustStore;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.springframework.data.redis.core.RedisOperations;

@Testcontainers
@SpringBootTest
class MyRedisWithSslIntegrationTests {

	@Container
	@ServiceConnection
	@PemKeyStore(certificate = "classpath:client.crt", privateKey = "classpath:client.key")
	@PemTrustStore("classpath:ca.crt")
	static RedisContainer redis = new SecureRedisContainer("redis:latest");

	@Autowired
	private RedisOperations<Object, Object> operations;

	@Test
	void testRedis() {
		// ...
	}

}
```

The above code uses the [`@PemKeyStore`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/testcontainers/service/connection/PemKeyStore.html) annotation to load the client certificate and key into the keystore and the and [`@PemTrustStore`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/testcontainers/service/connection/PemTrustStore.html) annotation to load the CA certificate into the truststore.
This will authenticate the client against the server, and the CA certificate in the truststore makes sure that the server certificate is valid and trusted.

The `SecureRedisContainer` in this example is a custom subclass of `RedisContainer` which copies certificates to the correct places and invokes `redis-server` with commandline parameters enabling SSL.

The SSL annotations are supported for the following service connections:

* Cassandra
* Couchbase
* Elasticsearch
* Kafka
* MongoDB
* RabbitMQ
* RabbitMQ Streams
* Redis

The `ElasticsearchContainer` additionally supports automatic detection of server side SSL.
To use this feature, annotate the container with [`@Ssl`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/testcontainers/service/connection/Ssl.html), as seen in the following example, and Spring Boot takes care of the client side SSL configuration for you:

```
import org.junit.jupiter.api.Test;
import org.testcontainers.elasticsearch.ElasticsearchContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.elasticsearch.test.autoconfigure.DataElasticsearchTest;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.springframework.boot.testcontainers.service.connection.Ssl;
import org.springframework.data.elasticsearch.client.elc.ElasticsearchTemplate;

@Testcontainers
@DataElasticsearchTest
class MyElasticsearchWithSslIntegrationTests {

	@Ssl
	@Container
	@ServiceConnection
	static ElasticsearchContainer elasticsearch = new ElasticsearchContainer(
			"docker.elastic.co/elasticsearch/elasticsearch:8.17.2");

	@Autowired
	private ElasticsearchTemplate elasticsearchTemplate;

	@Test
	void testElasticsearch() {
		// ...
	}

}
```

## Dynamic Properties

A slightly more verbose but also more flexible alternative to service connections is [`@DynamicPropertySource`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/context/DynamicPropertySource.html).
A static [`@DynamicPropertySource`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/test/context/DynamicPropertySource.html) method allows adding dynamic property values to the Spring Environment.

* Java
* Kotlin

```
import org.junit.jupiter.api.Test;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.neo4j.Neo4jContainer;

import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;

@Testcontainers
@SpringBootTest
class MyIntegrationTests {

	@Container
	static Neo4jContainer neo4j = new Neo4jContainer("neo4j:5");

	@Test
	void myTest() {
		// ...
	}

	@DynamicPropertySource
	static void neo4jProperties(DynamicPropertyRegistry registry) {
		registry.add("spring.neo4j.uri", neo4j::getBoltUrl);
	}

}
```

```
import org.junit.jupiter.api.Test
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.test.context.DynamicPropertyRegistry
import org.springframework.test.context.DynamicPropertySource
import org.testcontainers.junit.jupiter.Container
import org.testcontainers.junit.jupiter.Testcontainers
import org.testcontainers.neo4j.Neo4jContainer

@Testcontainers
@SpringBootTest
class MyIntegrationTests {

	@Test
	fun myTest() {
		...
	}

	companion object {
		@Container
		@JvmStatic
		val neo4j = Neo4jContainer("neo4j:5");

		@DynamicPropertySource
		@JvmStatic
		fun neo4jProperties(registry: DynamicPropertyRegistry) {
			registry.add("spring.neo4j.uri") { neo4j.boltUrl }
		}
	}
}
```

The above configuration allows Neo4j-related beans in the application to communicate with Neo4j running inside the Testcontainers-managed Docker container.