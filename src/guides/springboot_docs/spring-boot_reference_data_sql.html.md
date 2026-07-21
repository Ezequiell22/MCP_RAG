Search

# SQL Databases

The [Spring Framework](https://spring.io/projects/spring-framework) provides extensive support for working with SQL databases, from direct JDBC access using [`JdbcClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jdbc/core/simple/JdbcClient.html) or [`JdbcTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jdbc/core/JdbcTemplate.html) to complete “object relational mapping” technologies such as Hibernate.
[Spring Data](https://spring.io/projects/spring-data) provides an additional level of functionality: creating [`Repository`](https://docs.spring.io/spring-data/commons/docs/4.1.x/api/org/springframework/data/repository/Repository.html) implementations directly from interfaces and using conventions to generate queries from your method names.

## Configure a DataSource

Java’s [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html) interface provides a standard method of working with database connections.
Traditionally, a [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html) uses a `URL` along with some credentials to establish a database connection.

|  |  |
| --- | --- |
|  | See the [Configure a Custom DataSource](../../how-to/data-access.html#howto.data-access.configure-custom-datasource) section of the “How-to Guides” for more advanced examples, typically to take full control over the configuration of the DataSource. |

### Embedded Database Support

It is often convenient to develop applications by using an in-memory embedded database.
Obviously, in-memory databases do not provide persistent storage.
You need to populate your database when your application starts and be prepared to throw away data when your application ends.

|  |  |
| --- | --- |
|  | The “How-to Guides” section includes a [section on how to initialize a database](../../how-to/data-initialization.html). |

Spring Boot can auto-configure embedded [H2](https://www.h2database.com), [HSQL](https://hsqldb.org/), and [Derby](https://db.apache.org/derby/) (deprecated) databases.
You need not provide any connection URLs.
You need only include a build dependency to the embedded database that you want to use.
If there are multiple embedded databases on the classpath, set the `spring.datasource.embedded-database-connection` configuration property to control which one is used.
Setting the property to `none` disables auto-configuration of an embedded database.

|  |  |
| --- | --- |
|  | If you are using this feature in your tests, you may notice that the same database is reused by your whole test suite regardless of the number of application contexts that you use. If you want to make sure that each context has a separate embedded database, you should set `spring.datasource.generate-unique-name` to `true`. |

For example, the typical POM dependencies would be as follows:

```
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<dependency>
	<groupId>org.hsqldb</groupId>
	<artifactId>hsqldb</artifactId>
	<scope>runtime</scope>
</dependency>
```

|  |  |
| --- | --- |
|  | You need a dependency on `spring-jdbc` for an embedded database to be auto-configured. In this example, it is pulled in transitively through `spring-boot-starter-data-jpa`. |

|  |  |
| --- | --- |
|  | If, for whatever reason, you do configure the connection URL for an embedded database, take care to ensure that the database’s automatic shutdown is disabled. If you use H2, you should use `DB_CLOSE_ON_EXIT=FALSE` to do so. If you use HSQLDB, you should ensure that `shutdown=true` is not used. Disabling the database’s automatic shutdown lets Spring Boot control when the database is closed, thereby ensuring that it happens once access to the database is no longer needed. |

### Connection to a Production Database

Production database connections can also be auto-configured by using a pooling [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html).

### DataSource Configuration

DataSource configuration is controlled by external configuration properties in `spring.datasource.*`.
For example, you might declare the following section in `application.properties`:

* Properties
* YAML

```
spring.datasource.url=jdbc:mysql://localhost/test
spring.datasource.username=dbuser
spring.datasource.password=dbpass
```

```
spring:
  datasource:
    url: "jdbc:mysql://localhost/test"
    username: "dbuser"
    password: "dbpass"
```

|  |  |
| --- | --- |
|  | You should at least specify the URL by setting the `spring.datasource.url` property. Otherwise, Spring Boot tries to auto-configure an embedded database. |

|  |  |
| --- | --- |
|  | Spring Boot can deduce the JDBC driver class for most databases from the URL. If you need to specify a specific class, you can use the `spring.datasource.driver-class-name` property. |

|  |  |
| --- | --- |
|  | For a pooling [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html) to be created, we need to be able to verify that a valid [`Driver`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/java/sql/Driver.html) class is available, so we check for that before doing anything. In other words, if you set `spring.datasource.driver-class-name=com.mysql.jdbc.Driver`, then that class has to be loadable. |

See [`DataSourceProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jdbc/autoconfigure/DataSourceProperties.html) API documentation for more of the supported options.
These are the standard options that work regardless of [the actual implementation](#data.sql.datasource.connection-pool).
It is also possible to fine-tune implementation-specific settings by using their respective prefix (`spring.datasource.hikari.*`, `spring.datasource.tomcat.*`, `spring.datasource.dbcp2.*`, and `spring.datasource.oracleucp.*`).
See the documentation of the connection pool implementation you are using for more details.

For instance, if you use the [Tomcat connection pool](https://tomcat.apache.org/tomcat-11.0-doc/jdbc-pool.html#Common_Attributes), you could customize many additional settings, as shown in the following example:

* Properties
* YAML

```
spring.datasource.tomcat.max-wait=10000
spring.datasource.tomcat.max-active=50
spring.datasource.tomcat.test-on-borrow=true
```

```
spring:
  datasource:
    tomcat:
      max-wait: 10000
      max-active: 50
      test-on-borrow: true
```

This will set the pool to wait 10000ms before throwing an exception if no connection is available, limit the maximum number of connections to 50 and validate the connection before borrowing it from the pool.

### Supported Connection Pools

Spring Boot uses the following algorithm for choosing a specific implementation:

1. We prefer [HikariCP](https://github.com/brettwooldridge/HikariCP) for its performance and concurrency.
   If HikariCP is available, we always choose it.
2. Otherwise, if the Tomcat pooling [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html) is available, we use it.
3. Otherwise, if [Commons DBCP2](https://commons.apache.org/proper/commons-dbcp/) is available, we use it.
4. If none of HikariCP, Tomcat, and DBCP2 are available and if Oracle UCP is available, we use it.

|  |  |
| --- | --- |
|  | If you use the `spring-boot-starter-jdbc` or `spring-boot-starter-data-jpa` starters, you automatically get a dependency to HikariCP. |

You can bypass that algorithm completely and specify the connection pool to use by setting the `spring.datasource.type` property.
This is especially important if you run your application in a Tomcat container, as `tomcat-jdbc` is provided by default.

Additional connection pools can always be configured manually, using [`DataSourceBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jdbc/DataSourceBuilder.html).
If you define your own [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html) bean, auto-configuration does not occur.
The following connection pools are supported by [`DataSourceBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jdbc/DataSourceBuilder.html):

* HikariCP
* Tomcat pooling [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html)
* Commons DBCP2
* Oracle UCP & `OracleDataSource`
* Spring Framework’s [`SimpleDriverDataSource`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jdbc/datasource/SimpleDriverDataSource.html)
* H2 [`JdbcDataSource`](https://www.h2database.com/javadoc/org/h2/jdbcx/JdbcDataSource.html)
* PostgreSQL [`PGSimpleDataSource`](https://jdbc.postgresql.org/documentation/publicapi/org/postgresql/ds/PGSimpleDataSource.html)
* C3P0
* Vibur

### Connection to a JNDI DataSource

If you deploy your Spring Boot application to an Application Server, you might want to configure and manage your DataSource by using your Application Server’s built-in features and access it by using JNDI.

The `spring.datasource.jndi-name` property can be used as an alternative to the `spring.datasource.url`, `spring.datasource.username`, and `spring.datasource.password` properties to access the [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html) from a specific JNDI location.
For example, the following section in `application.properties` shows how you can access a JBoss AS defined [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html):

* Properties
* YAML

```
spring.datasource.jndi-name=java:jboss/datasources/customers
```

```
spring:
  datasource:
    jndi-name: "java:jboss/datasources/customers"
```

### Lazy Connection Proxy

When a pooled `DataSource` is auto-configured, it can be wrapped in a proxy that fetches JDBC connections as late as possible by setting `spring.datasource.connection-fetch` to `lazy`, as shown in the following example:

* Properties
* YAML

```
spring.datasource.connection-fetch=lazy
```

```
spring:
  datasource:
    connection-fetch: "lazy"
```

With this feature enabled, JDBC Connections are only fetched from the pool when actually necessary.
JDBC transaction control can happen without fetching a Connection from the pool or communicating with the database; this will be done lazily on the first creation of a JDBC Statement.
To get access to the target auto-configured `DataSource`, use `DataSource.unwrap`.

|  |  |
| --- | --- |
|  | If you are wrapping the target `DataSource` in a `TransactionAwareDataSourceProxy`, make sure to do so with a `BeanPostProcessor` that has a positive order. |

See [`LazyConnectionDataSourceProxy`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jdbc/datasource/LazyConnectionDataSourceProxy.html) for more details.

## Using JdbcTemplate

Spring’s [`JdbcTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jdbc/core/JdbcTemplate.html) and [`NamedParameterJdbcTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jdbc/core/namedparam/NamedParameterJdbcTemplate.html) classes are auto-configured, and you can autowire them directly into your own beans, as shown in the following example:

* Java
* Kotlin

```
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

@Component
public class MyBean {

	private final JdbcTemplate jdbcTemplate;

	public MyBean(JdbcTemplate jdbcTemplate) {
		this.jdbcTemplate = jdbcTemplate;
	}

	public void doSomething() {
		this.jdbcTemplate ...
	}

}
```

```
import org.springframework.jdbc.core.JdbcTemplate
import org.springframework.stereotype.Component

@Component
class MyBean(private val jdbcTemplate: JdbcTemplate) {

	fun doSomething() {
		jdbcTemplate.execute("delete from customer")
	}

}
```

You can customize some properties of the template by using the `spring.jdbc.template.*` properties, as shown in the following example:

* Properties
* YAML

```
spring.jdbc.template.max-rows=500
```

```
spring:
  jdbc:
    template:
      max-rows: 500
```

If tuning of SQL exceptions is required, you can define your own `SQLExceptionTranslator` bean so that it is associated with the auto-configured `JdbcTemplate`.

|  |  |
| --- | --- |
|  | The [`NamedParameterJdbcTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jdbc/core/namedparam/NamedParameterJdbcTemplate.html) reuses the same [`JdbcTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jdbc/core/JdbcTemplate.html) instance behind the scenes. If more than one [`JdbcTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jdbc/core/JdbcTemplate.html) is defined and no primary candidate exists, the [`NamedParameterJdbcTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jdbc/core/namedparam/NamedParameterJdbcTemplate.html) is not auto-configured. |

## Using JdbcClient

Spring’s [`JdbcClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jdbc/core/simple/JdbcClient.html) is auto-configured based on the presence of a [`NamedParameterJdbcTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jdbc/core/namedparam/NamedParameterJdbcTemplate.html).
You can inject it directly in your own beans as well, as shown in the following example:

* Java
* Kotlin

```
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Component;

@Component
public class MyBean {

	private final JdbcClient jdbcClient;

	public MyBean(JdbcClient jdbcClient) {
		this.jdbcClient = jdbcClient;
	}

	public void doSomething() {
		this.jdbcClient ...
	}

}
```

```
import org.springframework.jdbc.core.simple.JdbcClient
import org.springframework.stereotype.Component

@Component
class MyBean(private val jdbcClient: JdbcClient) {

	fun doSomething() {
		jdbcClient.sql("delete from customer").update()
	}

}
```

If you rely on auto-configuration to create the underlying [`JdbcTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jdbc/core/JdbcTemplate.html), any customization using `spring.jdbc.template.*` properties is taken into account in the client as well.

## JPA and Spring Data JPA

The Java Persistence API is a standard technology that lets you “map” objects to relational databases.
The `spring-boot-starter-data-jpa` POM provides a quick way to get started.
It provides the following key dependencies:

* Hibernate: One of the most popular JPA implementations.
* Spring Data JPA: Helps you to implement JPA-based repositories.
* Spring ORM: Core ORM support from the Spring Framework.

|  |  |
| --- | --- |
|  | We do not go into too many details of JPA or [Spring Data](https://spring.io/projects/spring-data) here. You can follow the [Accessing Data with JPA](https://spring.io/guides/gs/accessing-data-jpa/) guide from [spring.io](https://spring.io) and read the [Spring Data JPA](https://spring.io/projects/spring-data-jpa) and [Hibernate](https://hibernate.org/orm/documentation/) reference documentation. |

### Entity Classes

Traditionally, JPA “Entity” classes are specified in a `persistence.xml` file.
With Spring Boot, this file is not necessary and “Entity Scanning” is used instead.
By default the [auto-configuration packages](../using/auto-configuration.html#using.auto-configuration.packages) are scanned.

Any classes annotated with [`@Entity`](https://jakarta.ee/specifications/persistence/3.2/apidocs/jakarta.persistence/jakarta/persistence/Entity.html), [`@Embeddable`](https://jakarta.ee/specifications/persistence/3.2/apidocs/jakarta.persistence/jakarta/persistence/Embeddable.html), or [`@MappedSuperclass`](https://jakarta.ee/specifications/persistence/3.2/apidocs/jakarta.persistence/jakarta/persistence/MappedSuperclass.html) are considered.
A typical entity class resembles the following example:

* Java
* Kotlin

```
import java.io.Serializable;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;

@Entity
public class City implements Serializable {

	@Id
	@GeneratedValue
	private Long id;

	@Column(nullable = false)
	private String name;

	@Column(nullable = false)
	private String state;

	// ... additional members, often include @OneToMany mappings

	protected City() {
		// no-args constructor required by JPA spec
		// this one is protected since it should not be used directly
	}

	public City(String name, String state) {
		this.name = name;
		this.state = state;
	}

	public String getName() {
		return this.name;
	}

	public String getState() {
		return this.state;
	}

	// ... etc

}
```

```
import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.GeneratedValue
import jakarta.persistence.Id
import java.io.Serializable

@Entity
class City : Serializable {

	@Id
	@GeneratedValue
	private val id: Long? = null

	@Column(nullable = false)
	var name: String? = null
		private set

	// ... etc
	@Column(nullable = false)
	var state: String? = null
		private set

	// ... additional members, often include @OneToMany mappings

	protected constructor() {
		// no-args constructor required by JPA spec
		// this one is protected since it should not be used directly
	}

	constructor(name: String?, state: String?) {
		this.name = name
		this.state = state
	}

}
```

|  |  |
| --- | --- |
|  | You can customize entity scanning locations by using the [`@EntityScan`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/persistence/autoconfigure/EntityScan.html) annotation. See the [Separate @Entity Definitions from Spring Configuration](../../how-to/data-access.html#howto.data-access.separate-entity-definitions-from-spring-configuration) section of the “How-to Guides”. |

### Spring Data JPA Repositories

[Spring Data JPA](https://spring.io/projects/spring-data-jpa) repositories are interfaces that you can define to access data.
JPA queries are created automatically from your method names.
For example, a `CityRepository` interface might declare a `findAllByState(String state)` method to find all the cities in a given state.

For more complex queries, you can annotate your method with Spring Data’s [`Query`](https://docs.spring.io/spring-data/jpa/docs/4.1.x/api/org/springframework/data/jpa/repository/Query.html) annotation.

Spring Data repositories usually extend from the [`Repository`](https://docs.spring.io/spring-data/commons/docs/4.1.x/api/org/springframework/data/repository/Repository.html) or [`CrudRepository`](https://docs.spring.io/spring-data/commons/docs/4.1.x/api/org/springframework/data/repository/CrudRepository.html) interfaces.
If you use auto-configuration, the [auto-configuration packages](../using/auto-configuration.html#using.auto-configuration.packages) are searched for repositories.

|  |  |
| --- | --- |
|  | You can customize the locations to look for repositories using [`@EnableJpaRepositories`](https://docs.spring.io/spring-data/jpa/docs/4.1.x/api/org/springframework/data/jpa/repository/config/EnableJpaRepositories.html). |

The following example shows a typical Spring Data repository interface definition:

* Java
* Kotlin

```
import org.springframework.boot.docs.data.sql.jpaandspringdata.entityclasses.City;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.repository.Repository;

public interface CityRepository extends Repository<City, Long> {

	Page<City> findAll(Pageable pageable);

	City findByNameAndStateAllIgnoringCase(String name, String state);

}
```

```
import org.springframework.boot.docs.data.sql.jpaandspringdata.entityclasses.City
import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.data.repository.Repository

interface CityRepository : Repository<City, Long> {

	fun findAll(pageable: Pageable?): Page<City>?

	fun findByNameAndStateAllIgnoringCase(name: String?, state: String?): City?

}
```

Spring Data JPA repositories support three different modes of bootstrapping: default, deferred, and lazy.
To enable deferred or lazy bootstrapping, set the `spring.data.jpa.repositories.bootstrap-mode` property to `deferred` or `lazy` respectively.
When using deferred or lazy bootstrapping, the auto-configured [`EntityManagerFactoryBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jpa/EntityManagerFactoryBuilder.html) will use the context’s [`AsyncTaskExecutor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/task/AsyncTaskExecutor.html), if any, as the bootstrap executor.
If more than one exists, the one named `applicationTaskExecutor` will be used.

|  |  |
| --- | --- |
|  | When using deferred or lazy bootstrapping, make sure to defer any access to the JPA infrastructure after the application context bootstrap phase. You can use [`SmartInitializingSingleton`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/beans/factory/SmartInitializingSingleton.html) to invoke any initialization that requires the JPA infrastructure. For JPA components (such as converters) that are created as Spring beans, use [`ObjectProvider`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/beans/factory/ObjectProvider.html) to delay the resolution of dependencies, if any. |

|  |  |
| --- | --- |
|  | We have barely scratched the surface of Spring Data JPA. For complete details, see the [Spring Data JPA reference documentation](https://docs.spring.io/spring-data/jpa/reference/4.1). |

### Spring Data Envers Repositories

If [Spring Data Envers](https://spring.io/projects/spring-data-envers) is available, JPA repositories are auto-configured to support typical Envers queries.

To use Spring Data Envers, make sure your repository extends from [`RevisionRepository`](https://docs.spring.io/spring-data/commons/docs/4.1.x/api/org/springframework/data/repository/history/RevisionRepository.html) as shown in the following example:

* Java
* Kotlin

```
import org.springframework.boot.docs.data.sql.jpaandspringdata.entityclasses.Country;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.repository.Repository;
import org.springframework.data.repository.history.RevisionRepository;

public interface CountryRepository extends RevisionRepository<Country, Long, Integer>, Repository<Country, Long> {

	Page<Country> findAll(Pageable pageable);

}
```

```
import org.springframework.boot.docs.data.sql.jpaandspringdata.entityclasses.Country
import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.data.repository.Repository
import org.springframework.data.repository.history.RevisionRepository

interface CountryRepository :
		RevisionRepository<Country, Long, Int>,
		Repository<Country, Long> {

	fun findAll(pageable: Pageable?): Page<Country>?

}
```

|  |  |
| --- | --- |
|  | For more details, check the [Spring Data Envers reference documentation](https://docs.spring.io/spring-data/jpa/reference/4.1/envers.html). |

### Creating and Dropping JPA Databases

By default, JPA databases are automatically created **only** if you use an embedded database, that is H2, HSQL, or Derby (deprecated).
You can explicitly configure JPA settings by using `spring.jpa.*` properties.
For example, to create and drop tables you can add the following line to your `application.properties`:

* Properties
* YAML

```
spring.jpa.hibernate.ddl-auto=create-drop
```

```
spring:
  jpa:
    hibernate.ddl-auto: "create-drop"
```

|  |  |
| --- | --- |
|  | Hibernate’s own internal property name for this (if you happen to remember it better) is `hibernate.hbm2ddl.auto`. You can set it, along with other Hibernate native properties, by using `spring.jpa.properties.*` (the prefix is stripped before adding them to the entity manager). The following line shows an example of setting JPA properties for Hibernate: |

* Properties
* YAML

```
spring.jpa.properties.hibernate.globally_quoted_identifiers=true
```

```
spring:
  jpa:
    properties:
      hibernate:
        "globally_quoted_identifiers": "true"
```

The line in the preceding example passes a value of `true` for the `hibernate.globally_quoted_identifiers` property to the Hibernate entity manager.

By default, the DDL execution (or validation) is deferred until the [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html) has started.

### Open EntityManager in View

If you are running a web application, Spring Boot by default registers [`OpenEntityManagerInViewInterceptor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/orm/jpa/support/OpenEntityManagerInViewInterceptor.html) to apply the “Open EntityManager in View” pattern, to allow for lazy loading in web views.
If you do not want this behavior, you should set `spring.jpa.open-in-view` to `false` in your `application.properties`.

## Spring Data JDBC

Spring Data includes repository support for JDBC and will automatically generate SQL for the methods on [`CrudRepository`](https://docs.spring.io/spring-data/commons/docs/4.1.x/api/org/springframework/data/repository/CrudRepository.html).
For more advanced queries, a [`@Query`](https://docs.spring.io/spring-data/jdbc/docs/4.1.x/api/org/springframework/data/jdbc/repository/query/Query.html) annotation is provided.

Spring Boot will auto-configure Spring Data’s JDBC repositories when the necessary dependencies are on the classpath.
They can be added to your project with a single dependency on `spring-boot-starter-data-jdbc`.
If necessary, you can take control of Spring Data JDBC’s configuration by adding the [`@EnableJdbcRepositories`](https://docs.spring.io/spring-data/jdbc/docs/4.1.x/api/org/springframework/data/jdbc/repository/config/EnableJdbcRepositories.html) annotation or an [`AbstractJdbcConfiguration`](https://docs.spring.io/spring-data/jdbc/docs/4.1.x/api/org/springframework/data/jdbc/repository/config/AbstractJdbcConfiguration.html) subclass to your application.

If you’re using Spring Data JDBC with [ahead-of-time processing](../packaging/aot.html) (targeting either the JVM or a native image), some additional configuration is recommended.
To prevent the need for a DB connection during AOT processing, define a `JdbcDialect` bean that’s appropriate for your application’s database.
For example, if you’re using Postgres, define a `JdbcPostgresDialect` bean.

|  |  |
| --- | --- |
|  | For complete details of Spring Data JDBC, see the [reference documentation](https://docs.spring.io/spring-data/relational/reference/4.1). |

## Using H2’s Web Console

The [H2 database](https://www.h2database.com) provides a [browser-based console](https://www.h2database.com/html/quickstart.html#h2_console) that Spring Boot can auto-configure for you.
The console is auto-configured when the following conditions are met:

* You are developing a servlet-based web application.
* `org.springframework.boot:spring-boot-h2console` is on the classpath.
* You are using [Spring Boot’s developer tools](../using/devtools.html).

|  |  |
| --- | --- |
|  | If you are not using Spring Boot’s developer tools but would still like to make use of H2’s console, you can configure the `spring.h2.console.enabled` property with a value of `true`. |

|  |  |
| --- | --- |
|  | The H2 console is only intended for use during development, so you should take care to ensure that `spring.h2.console.enabled` is not set to `true` in production. |

### Changing the H2 Console’s Path

By default, the console is available at `/h2-console`.
You can customize the console’s path by using the `spring.h2.console.path` property.

### Accessing the H2 Console in a Secured Application

H2 Console uses frames and, as it is intended for development only, does not implement CSRF protection measures.
If your application uses Spring Security, you need to configure it to

* disable CSRF protection for requests against the console,
* set the header `X-Frame-Options` to `SAMEORIGIN` on responses from the console.

More information on [CSRF](https://docs.spring.io/spring-security/reference/7.1/features/exploits/csrf.html) and the header [X-Frame-Options](https://docs.spring.io/spring-security/reference/7.1/features/exploits/headers.html#headers-frame-options) can be found in the Spring Security Reference Guide.

In simple setups, a [`SecurityFilterChain`](https://docs.spring.io/spring-security/reference/7.1/api/java/org/springframework/security/web/SecurityFilterChain.html) like the following can be used:

* Java
* Kotlin

```
import org.springframework.boot.security.autoconfigure.web.servlet.PathRequest;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.CsrfConfigurer;
import org.springframework.security.config.annotation.web.configurers.HeadersConfigurer.FrameOptionsConfig;
import org.springframework.security.web.SecurityFilterChain;

@Profile("dev")
@Configuration(proxyBeanMethods = false)
public class DevProfileSecurityConfiguration {

	@Bean
	@Order(Ordered.HIGHEST_PRECEDENCE)
	SecurityFilterChain h2ConsoleSecurityFilterChain(HttpSecurity http) {
		http.securityMatcher(PathRequest.toH2Console());
		http.authorizeHttpRequests(yourCustomAuthorization());
		http.csrf(CsrfConfigurer::disable);
		http.headers((headers) -> headers.frameOptions(FrameOptionsConfig::sameOrigin));
		return http.build();
	}

}
```

```
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.context.annotation.Profile
import org.springframework.core.Ordered
import org.springframework.core.annotation.Order
import org.springframework.security.config.Customizer
import org.springframework.security.config.annotation.web.builders.HttpSecurity
import org.springframework.security.web.SecurityFilterChain

@Profile("dev")
@Configuration(proxyBeanMethods = false)
class DevProfileSecurityConfiguration {

	@Bean
	@Order(Ordered.HIGHEST_PRECEDENCE)
	fun h2ConsoleSecurityFilterChain(http: HttpSecurity): SecurityFilterChain {
		return http.authorizeHttpRequests(yourCustomAuthorization())
			.csrf { csrf -> csrf.disable() }
			.headers { headers -> headers.frameOptions { frameOptions -> frameOptions.sameOrigin() } }
			.build()
	}

}
```

|  |  |
| --- | --- |
|  | The H2 console is only intended for use during development. In production, disabling CSRF protection or allowing frames for a website may create severe security risks. |

|  |  |
| --- | --- |
|  | `PathRequest.toH2Console()` returns the correct request matcher also when the console’s path has been customized. |

## Using jOOQ

jOOQ Object Oriented Querying ([jOOQ](https://www.jooq.org/)) is a popular product from [Data Geekery](https://www.datageekery.com/) which generates Java code from your database and lets you build type-safe SQL queries through its fluent API.
Both the commercial and open source editions can be used with Spring Boot.
jOOQ requires Java 21 or later.

### Code Generation

In order to use jOOQ type-safe queries, you need to generate Java classes from your database schema.
You can follow the instructions in the [jOOQ user manual](https://www.jooq.org/doc/3.21.5/manual-single-page/#jooq-in-7-steps-step3).
If you use the `jooq-codegen-maven` plugin and you also use the `spring-boot-starter-parent` “parent POM”, you can safely omit the plugin’s `<version>` tag.
You can also use Spring Boot-defined version variables (such as `h2.version`) to declare the plugin’s database dependency.
The following listing shows an example:

```
<plugin>
	<groupId>org.jooq</groupId>
	<artifactId>jooq-codegen-maven</artifactId>
	<executions>
		...
	</executions>
	<dependencies>
		<dependency>
			<groupId>com.h2database</groupId>
			<artifactId>h2</artifactId>
			<version>${h2.version}</version>
		</dependency>
	</dependencies>
	<configuration>
		<jdbc>
			<driver>org.h2.Driver</driver>
			<url>jdbc:h2:~/yourdatabase</url>
		</jdbc>
		<generator>
			...
		</generator>
	</configuration>
</plugin>
```

### Using DSLContext

The fluent API offered by jOOQ is initiated through the [`DSLContext`](https://www.jooq.org/javadoc/3.21.5/org/jooq/DSLContext.html) interface.
Spring Boot auto-configures a [`DSLContext`](https://www.jooq.org/javadoc/3.21.5/org/jooq/DSLContext.html) as a Spring Bean and connects it to your application [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html).
To use the [`DSLContext`](https://www.jooq.org/javadoc/3.21.5/org/jooq/DSLContext.html), you can inject it, as shown in the following example:

* Java
* Kotlin

```
import java.util.GregorianCalendar;
import java.util.List;

import org.jooq.DSLContext;

import org.springframework.stereotype.Component;

import static org.springframework.boot.docs.data.sql.jooq.dslcontext.Tables.AUTHOR;

@Component
public class MyBean {

	private final DSLContext create;

	public MyBean(DSLContext dslContext) {
		this.create = dslContext;
	}

}
```

```
import org.jooq.DSLContext
import org.springframework.stereotype.Component
import java.util.GregorianCalendar

@Component
class MyBean(private val create: DSLContext) {

}
```

|  |  |
| --- | --- |
|  | The jOOQ manual tends to use a variable named `create` to hold the [`DSLContext`](https://www.jooq.org/javadoc/3.21.5/org/jooq/DSLContext.html). |

You can then use the [`DSLContext`](https://www.jooq.org/javadoc/3.21.5/org/jooq/DSLContext.html) to construct your queries, as shown in the following example:

* Java
* Kotlin

```
	public List<GregorianCalendar> authorsBornAfter1980() {
		return this.create.selectFrom(AUTHOR)
			.where(AUTHOR.DATE_OF_BIRTH.greaterThan(new GregorianCalendar(1980, 0, 1)))
			.fetch(AUTHOR.DATE_OF_BIRTH);
```

```
	fun authorsBornAfter1980(): List<GregorianCalendar> {
		return create.selectFrom<Tables.TAuthorRecord>(Tables.AUTHOR)
			.where(Tables.AUTHOR?.DATE_OF_BIRTH?.greaterThan(GregorianCalendar(1980, 0, 1)))
			.fetch(Tables.AUTHOR?.DATE_OF_BIRTH)
	}
```

### jOOQ SQL Dialect

Unless the `spring.jooq.sql-dialect` property has been configured, Spring Boot determines the SQL dialect to use for your datasource.
If Spring Boot could not detect the dialect, it uses `DEFAULT`.

|  |  |
| --- | --- |
|  | Spring Boot can only auto-configure dialects supported by the open source version of jOOQ. |

### Customizing jOOQ

More advanced customizations can be achieved by defining your own [`DefaultConfigurationCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jooq/autoconfigure/DefaultConfigurationCustomizer.html) bean that will be invoked prior to creating the [`Configuration`](https://www.jooq.org/javadoc/3.21.5/org/jooq/Configuration.html) [`@Bean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Bean.html).
This takes precedence to anything that is applied by the auto-configuration.

You can also create your own [`Configuration`](https://www.jooq.org/javadoc/3.21.5/org/jooq/Configuration.html) [`@Bean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Bean.html) if you want to take complete control of the jOOQ configuration.

## Using R2DBC

The Reactive Relational Database Connectivity ([R2DBC](https://r2dbc.io)) project brings reactive programming APIs to relational databases.
R2DBC’s [`Connection`](https://r2dbc.io/spec/1.0.0.RELEASE/api/io/r2dbc/spi/Connection.html) provides a standard method of working with non-blocking database connections.
Connections are provided by using a [`ConnectionFactory`](https://r2dbc.io/spec/1.0.0.RELEASE/api/io/r2dbc/spi/ConnectionFactory.html), similar to a [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html) with jdbc.

[`ConnectionFactory`](https://r2dbc.io/spec/1.0.0.RELEASE/api/io/r2dbc/spi/ConnectionFactory.html) configuration is controlled by external configuration properties in `spring.r2dbc.*`.
For example, you might declare the following section in `application.properties`:

* Properties
* YAML

```
spring.r2dbc.url=r2dbc:postgresql://localhost/test
spring.r2dbc.username=dbuser
spring.r2dbc.password=dbpass
```

```
spring:
  r2dbc:
    url: "r2dbc:postgresql://localhost/test"
    username: "dbuser"
    password: "dbpass"
```

|  |  |
| --- | --- |
|  | You do not need to specify a driver class name, since Spring Boot obtains the driver from R2DBC’s Connection Factory discovery. |

|  |  |
| --- | --- |
|  | At least the url should be provided. Information specified in the URL takes precedence over individual properties, that is `name`, `username`, `password` and pooling options. |

|  |  |
| --- | --- |
|  | The “How-to Guides” section includes a [section on how to initialize a database](../../how-to/data-initialization.html#howto.data-initialization.using-basic-sql-scripts). |

To customize the connections created by a [`ConnectionFactory`](https://r2dbc.io/spec/1.0.0.RELEASE/api/io/r2dbc/spi/ConnectionFactory.html), that is, set specific parameters that you do not want (or cannot) configure in your central database configuration, you can use a [`ConnectionFactoryOptionsBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/r2dbc/autoconfigure/ConnectionFactoryOptionsBuilderCustomizer.html) [`@Bean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Bean.html).
The following example shows how to manually override the database port while the rest of the options are taken from the application configuration:

* Java
* Kotlin

```
import io.r2dbc.spi.ConnectionFactoryOptions;

import org.springframework.boot.r2dbc.autoconfigure.ConnectionFactoryOptionsBuilderCustomizer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration(proxyBeanMethods = false)
public class MyR2dbcConfiguration {

	@Bean
	public ConnectionFactoryOptionsBuilderCustomizer connectionFactoryPortCustomizer() {
		return (builder) -> builder.option(ConnectionFactoryOptions.PORT, 5432);
	}

}
```

```
import io.r2dbc.spi.ConnectionFactoryOptions
import org.springframework.boot.r2dbc.autoconfigure.ConnectionFactoryOptionsBuilderCustomizer
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration

@Configuration(proxyBeanMethods = false)
class MyR2dbcConfiguration {

	@Bean
	fun connectionFactoryPortCustomizer(): ConnectionFactoryOptionsBuilderCustomizer {
		return ConnectionFactoryOptionsBuilderCustomizer { builder ->
			builder.option(ConnectionFactoryOptions.PORT, 5432)
		}
	}

}
```

The following examples show how to set some PostgreSQL connection options:

* Java
* Kotlin

```
import java.util.HashMap;
import java.util.Map;

import io.r2dbc.postgresql.PostgresqlConnectionFactoryProvider;

import org.springframework.boot.r2dbc.autoconfigure.ConnectionFactoryOptionsBuilderCustomizer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration(proxyBeanMethods = false)
public class MyPostgresR2dbcConfiguration {

	@Bean
	public ConnectionFactoryOptionsBuilderCustomizer postgresCustomizer() {
		Map<String, String> options = new HashMap<>();
		options.put("lock_timeout", "30s");
		options.put("statement_timeout", "60s");
		return (builder) -> builder.option(PostgresqlConnectionFactoryProvider.OPTIONS, options);
	}

}
```

```
import io.r2dbc.postgresql.PostgresqlConnectionFactoryProvider
import org.springframework.boot.r2dbc.autoconfigure.ConnectionFactoryOptionsBuilderCustomizer
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration

@Configuration(proxyBeanMethods = false)
class MyPostgresR2dbcConfiguration {

	@Bean
	fun postgresCustomizer(): ConnectionFactoryOptionsBuilderCustomizer {
		val options: MutableMap<String, String> = HashMap()
		options["lock_timeout"] = "30s"
		options["statement_timeout"] = "60s"
		return ConnectionFactoryOptionsBuilderCustomizer { builder ->
			builder.option(PostgresqlConnectionFactoryProvider.OPTIONS, options)
		}
	}

}
```

When a [`ConnectionFactory`](https://r2dbc.io/spec/1.0.0.RELEASE/api/io/r2dbc/spi/ConnectionFactory.html) bean is available, the regular JDBC [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html) auto-configuration backs off.
If you want to retain the JDBC [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html) auto-configuration, and are comfortable with the risk of using the blocking JDBC API in a reactive application, add `@Import(DataSourceAutoConfiguration.class)` on a [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) class in your application to re-enable it.

### Embedded Database Support

Similarly to [the JDBC support](#data.sql.datasource.embedded), Spring Boot can automatically configure an embedded database for reactive usage.
You need not provide any connection URLs.
You need only include a build dependency to the embedded database that you want to use, as shown in the following example:

```
<dependency>
	<groupId>io.r2dbc</groupId>
	<artifactId>r2dbc-h2</artifactId>
	<scope>runtime</scope>
</dependency>
```

|  |  |
| --- | --- |
|  | If you are using this feature in your tests, you may notice that the same database is reused by your whole test suite regardless of the number of application contexts that you use. If you want to make sure that each context has a separate embedded database, you should set `spring.r2dbc.generate-unique-name` to `true`. |

### Using DatabaseClient

A [`DatabaseClient`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/r2dbc/core/DatabaseClient.html) bean is auto-configured, and you can autowire it directly into your own beans, as shown in the following example:

* Java
* Kotlin

```
import java.util.Map;

import reactor.core.publisher.Flux;

import org.springframework.r2dbc.core.DatabaseClient;
import org.springframework.stereotype.Component;

@Component
public class MyBean {

	private final DatabaseClient databaseClient;

	public MyBean(DatabaseClient databaseClient) {
		this.databaseClient = databaseClient;
	}

	// ...

	public Flux<Map<String, Object>> someMethod() {
		return this.databaseClient.sql("select * from user").fetch().all();
	}

}
```

```
import org.springframework.r2dbc.core.DatabaseClient
import org.springframework.stereotype.Component
import reactor.core.publisher.Flux

@Component
class MyBean(private val databaseClient: DatabaseClient) {

	// ...

	fun someMethod(): Flux<Map<String, Any>> {
		return databaseClient.sql("select * from user").fetch().all()
	}

}
```

### Spring Data R2DBC Repositories

[Spring Data R2DBC](https://spring.io/projects/spring-data-r2dbc) repositories are interfaces that you can define to access data.
Queries are created automatically from your method names.
For example, a `CityRepository` interface might declare a `findAllByState(String state)` method to find all the cities in a given state.

For more complex queries, you can annotate your method with Spring Data’s [`@Query`](https://docs.spring.io/spring-data/r2dbc/docs/4.1.x/api/org/springframework/data/r2dbc/repository/Query.html) annotation.

Spring Data repositories usually extend from the [`Repository`](https://docs.spring.io/spring-data/commons/docs/4.1.x/api/org/springframework/data/repository/Repository.html) or [`CrudRepository`](https://docs.spring.io/spring-data/commons/docs/4.1.x/api/org/springframework/data/repository/CrudRepository.html) interfaces.
If you use auto-configuration, the [auto-configuration packages](../using/auto-configuration.html#using.auto-configuration.packages) are searched for repositories.

The following example shows a typical Spring Data repository interface definition:

* Java
* Kotlin

```
import reactor.core.publisher.Mono;

import org.springframework.data.repository.Repository;

public interface CityRepository extends Repository<City, Long> {

	Mono<City> findByNameAndStateAllIgnoringCase(String name, String state);

}
```

```
import org.springframework.data.repository.Repository
import reactor.core.publisher.Mono

interface CityRepository : Repository<City, Long> {

	fun findByNameAndStateAllIgnoringCase(name: String, state: String): Mono<City>

}
```

|  |  |
| --- | --- |
|  | We have barely scratched the surface of Spring Data R2DBC. For complete details, see the [Spring Data R2DBC reference documentation](https://docs.spring.io/spring-data/relational/reference/4.1). |