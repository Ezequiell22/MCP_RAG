Search

# Working with NoSQL Technologies

Spring Data provides additional projects that help you access a variety of NoSQL technologies, including:

* [Cassandra](https://spring.io/projects/spring-data-cassandra)
* [Couchbase](https://spring.io/projects/spring-data-couchbase)
* [Elasticsearch](https://spring.io/projects/spring-data-elasticsearch)
* [Geode](https://spring.io/projects/spring-data-geode)
* [LDAP](https://spring.io/projects/spring-data-ldap)
* [MongoDB](https://spring.io/projects/spring-data-mongodb)
* [Neo4J](https://spring.io/projects/spring-data-neo4j)
* [Redis](https://spring.io/projects/spring-data-redis)

Of these, Spring Boot provides auto-configuration for Cassandra, Couchbase, Elasticsearch, LDAP, MongoDB, Neo4J and Redis.
Additionally, [Spring Boot for Apache Geode](https://github.com/spring-projects/spring-boot-data-geode) provides [auto-configuration for Apache Geode](https://docs.spring.io/spring-boot-data-geode-build/2.0.x/reference/html5#geode-repositories).
You can make use of the other projects, but you must configure them yourself.
See the appropriate reference documentation at [spring.io/projects/spring-data](https://spring.io/projects/spring-data).

Spring Boot also provides auto-configuration for the InfluxDB client but it is deprecated in favor of [the new InfluxDB Java client](https://github.com/influxdata/influxdb-client-java) that provides its own Spring Boot integration.

## Redis

[Redis](https://redis.io/) is a cache, message broker, and richly-featured key-value store.
Spring Boot offers basic auto-configuration for the [Lettuce](https://github.com/redis/lettuce/) and [Jedis](https://github.com/redis/jedis/) client libraries and the abstractions on top of them provided by [Spring Data Redis](https://github.com/spring-projects/spring-data-redis).

There is a `spring-boot-starter-data-redis` starter for collecting the dependencies in a convenient way.
By default, it uses [Lettuce](https://github.com/redis/lettuce/).
That starter handles both traditional and reactive applications.

|  |  |
| --- | --- |
|  | We also provide a `spring-boot-starter-data-redis-reactive` starter for consistency with the other stores with reactive support. |

### Connecting to Redis

You can inject an auto-configured [`RedisConnectionFactory`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/connection/RedisConnectionFactory.html), [`StringRedisTemplate`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/core/StringRedisTemplate.html), or vanilla [`RedisTemplate`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/core/RedisTemplate.html) instance as you would any other Spring Bean.
The following listing shows an example of such a bean:

* Java
* Kotlin

```
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Component;

@Component
public class MyBean {

	private final StringRedisTemplate template;

	public MyBean(StringRedisTemplate template) {
		this.template = template;
	}

	// ...

	public Boolean someMethod() {
		return this.template.hasKey("spring");
	}

}
```

```
import org.springframework.data.redis.core.StringRedisTemplate
import org.springframework.stereotype.Component

@Component
class MyBean(private val template: StringRedisTemplate) {

	// ...

	fun someMethod(): Boolean {
		return template.hasKey("spring")
	}

}
```

By default, the instance tries to connect to a Redis server at `localhost:6379`.
You can specify custom connection details using `spring.data.redis.*` properties, as shown in the following example:

* Properties
* YAML

```
spring.data.redis.host=localhost
spring.data.redis.port=6379
spring.data.redis.database=0
spring.data.redis.username=user
spring.data.redis.password=secret
```

```
spring:
  data:
    redis:
      host: "localhost"
      port: 6379
      database: 0
      username: "user"
      password: "secret"
```

You can also specify the url of the Redis server directly.
When setting the url, the host, port, username and password properties are ignored.
This is shown in the following example:

* Properties
* YAML

```
spring.data.redis.url=redis://user:secret@localhost:6379
spring.data.redis.database=0
```

```
spring:
  data:
    redis:
      url: "redis://user:secret@localhost:6379"
      database: 0
```

|  |  |
| --- | --- |
|  | You can also register an arbitrary number of beans that implement [`LettuceClientConfigurationBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/redis/autoconfigure/LettuceClientConfigurationBuilderCustomizer.html) for more advanced customizations. [`ClientResources`](https://javadoc.io/doc/io.lettuce/lettuce-core/7.5.2.RELEASE/io/lettuce/core/resource/ClientResources.html) can also be customized using [`ClientResourcesBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/redis/autoconfigure/ClientResourcesBuilderCustomizer.html). If you use Jedis, [`JedisClientConfigurationBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/redis/autoconfigure/JedisClientConfigurationBuilderCustomizer.html) is also available. |

Alternatively, you can register a bean of type [`RedisStandaloneConfiguration`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/connection/RedisStandaloneConfiguration.html), [`RedisSentinelConfiguration`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/connection/RedisSentinelConfiguration.html), [`RedisClusterConfiguration`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/connection/RedisClusterConfiguration.html), or [`RedisStaticMasterReplicaConfiguration`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/connection/RedisStaticMasterReplicaConfiguration.html) to take full control over the configuration.

|  |  |
| --- | --- |
|  | master/replica is not supported by Jedis. |

If you add your own [`@Bean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Bean.html) of any of the auto-configured types, it replaces the default (except in the case of [`RedisTemplate`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/core/RedisTemplate.html), when the exclusion is based on the bean name, `redisTemplate`, not its type).

By default, a pooled connection factory is auto-configured if `commons-pool2` is on the classpath.

The auto-configured [`RedisConnectionFactory`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/connection/RedisConnectionFactory.html) can be configured to use SSL for communication with the server by setting the properties as shown in this example:

* Properties
* YAML

```
spring.data.redis.ssl.enabled=true
```

```
spring:
  data:
    redis:
      ssl:
        enabled: true
```

Custom SSL trust material can be configured in an [SSL bundle](../features/ssl.html) and applied to the [`RedisConnectionFactory`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/connection/RedisConnectionFactory.html) as shown in this example:

* Properties
* YAML

```
spring.data.redis.ssl.bundle=example
```

```
spring:
  data:
    redis:
      ssl:
        bundle: "example"
```

### Receiving a Message

When the Redis infrastructure is present, any bean can be annotated with [`@RedisListener`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/annotation/RedisListener.html) to create a listener endpoint.
If no [`RedisMessageListenerContainer`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/listener/RedisMessageListenerContainer.html) has been defined, a default one is configured automatically.

The following component creates a listener endpoint on the `someChannel` channel:

* Java
* Kotlin

```
import org.springframework.data.redis.annotation.RedisListener;
import org.springframework.stereotype.Component;

@Component
public class MyBean {

	@RedisListener("someChannel")
	public void processMessage(String content) {
		// ...
	}

}
```

```
import org.springframework.data.redis.annotation.RedisListener
import org.springframework.stereotype.Component

@Component
class MyBean {

	@RedisListener("someChannel")
	fun processMessage(content: String) {
		// ...
	}

}
```

|  |  |
| --- | --- |
|  | See the [`@EnableRedisListeners`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/annotation/EnableRedisListeners.html) API documentation for more details. |

If you need to create more [`RedisMessageListenerContainer`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/listener/RedisMessageListenerContainer.html) instances or if you want to override the default, Spring Boot provides a [`RedisMessageListenerContainerConfigurer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/data/redis/autoconfigure/RedisMessageListenerContainerConfigurer.html) that you can use to initialize a [`RedisMessageListenerContainer`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/listener/RedisMessageListenerContainer.html) with the same settings as the one that is auto-configured.

For instance, the following example exposes another container that uses a specific [`RedisConnectionFactory`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/connection/RedisConnectionFactory.html):

* Java
* Kotlin

```
import org.springframework.boot.data.redis.autoconfigure.RedisMessageListenerContainerConfigurer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.listener.RedisMessageListenerContainer;

@Configuration(proxyBeanMethods = false)
public class MyRedisConfiguration {

	@Bean
	public RedisMessageListenerContainer myRedisMessageListenerContainer(
			RedisMessageListenerContainerConfigurer configurer, RedisConnectionFactory connectionFactory) {
		RedisMessageListenerContainer container = new RedisMessageListenerContainer();
		configurer.configure(container, connectionFactory);
		// ... custom configuration
		return container;
	}

}
```

```
import org.springframework.boot.data.redis.autoconfigure.RedisMessageListenerContainerConfigurer
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.data.redis.connection.RedisConnectionFactory
import org.springframework.data.redis.listener.RedisMessageListenerContainer

@Configuration(proxyBeanMethods = false)
class MyRedisConfiguration {

	@Bean
	fun myRedisMessageListenerContainer(
		configurer: RedisMessageListenerContainerConfigurer,
		connectionFactory: RedisConnectionFactory
	): RedisMessageListenerContainer {
		val container = RedisMessageListenerContainer()
		configurer.configure(container, connectionFactory)
		// ... custom configuration
		return container
	}

}
```

Then you can use the container in any [`@RedisListener`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/annotation/RedisListener.html)-annotated method as follows:

* Java
* Kotlin

```
import org.springframework.data.redis.annotation.RedisListener;
import org.springframework.stereotype.Component;

@Component
public class MyBean {

	@RedisListener(topic = "someChannel", container = "myRedisMessageListenerContainer")
	public void processMessage(String content) {
		// ...
	}

}
```

```
import org.springframework.data.redis.annotation.RedisListener
import org.springframework.stereotype.Component

@Component
class MyBean {

	@RedisListener(topic = "someChannel", container = "myRedisMessageListenerContainer")
	fun processMessage(content: String) {
		// ...
	}

}
```

## MongoDB

[MongoDB](https://www.mongodb.com/) is an open-source NoSQL document database that uses a JSON-like schema instead of traditional table-based relational data.
Spring Boot offers several conveniences for working with MongoDB, including the `spring-boot-starter-data-mongodb` and `spring-boot-starter-data-mongodb-reactive` starters.

### Connecting to a MongoDB Database

To access MongoDB databases, you can inject an auto-configured [`MongoDatabaseFactory`](https://docs.spring.io/spring-data/mongodb/docs/5.1.x/api/org/springframework/data/mongodb/MongoDatabaseFactory.html).
By default, the instance tries to connect to a MongoDB server at `mongodb://localhost/test`.
The following example shows how to connect to a MongoDB database:

* Java
* Kotlin

```
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;

import org.springframework.data.mongodb.MongoDatabaseFactory;
import org.springframework.stereotype.Component;

@Component
public class MyBean {

	private final MongoDatabaseFactory mongo;

	public MyBean(MongoDatabaseFactory mongo) {
		this.mongo = mongo;
	}

	// ...

	public MongoCollection<Document> someMethod() {
		MongoDatabase db = this.mongo.getMongoDatabase();
		return db.getCollection("users");
	}

}
```

```
import com.mongodb.client.MongoCollection
import org.bson.Document
import org.springframework.data.mongodb.MongoDatabaseFactory
import org.springframework.stereotype.Component

@Component
class MyBean(private val mongo: MongoDatabaseFactory) {

	// ...

	fun someMethod(): MongoCollection<Document> {
		val db = mongo.mongoDatabase
		return db.getCollection("users")
	}

}
```

If you have defined your own [`MongoClient`](https://mongodb.github.io/mongo-java-driver/5.8/apidocs/mongodb-driver-sync/com/mongodb/client/MongoClient.html), it will be used to auto-configure a suitable [`MongoDatabaseFactory`](https://docs.spring.io/spring-data/mongodb/docs/5.1.x/api/org/springframework/data/mongodb/MongoDatabaseFactory.html).

The auto-configured [`MongoClient`](https://mongodb.github.io/mongo-java-driver/5.8/apidocs/mongodb-driver-sync/com/mongodb/client/MongoClient.html) is created using a [`MongoClientSettings`](https://mongodb.github.io/mongo-java-driver/5.8/apidocs/mongodb-driver-core/com/mongodb/MongoClientSettings.html) bean.
If you have defined your own [`MongoClientSettings`](https://mongodb.github.io/mongo-java-driver/5.8/apidocs/mongodb-driver-core/com/mongodb/MongoClientSettings.html), it will be used without modification and the `spring.data.mongodb` properties will be ignored.
Otherwise a [`MongoClientSettings`](https://mongodb.github.io/mongo-java-driver/5.8/apidocs/mongodb-driver-core/com/mongodb/MongoClientSettings.html) will be auto-configured and will have the `spring.data.mongodb` properties applied to it.
In either case, you can declare one or more [`MongoClientSettingsBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/mongodb/autoconfigure/MongoClientSettingsBuilderCustomizer.html) beans to fine-tune the [`MongoClientSettings`](https://mongodb.github.io/mongo-java-driver/5.8/apidocs/mongodb-driver-core/com/mongodb/MongoClientSettings.html) configuration.
Each will be called in order with the [`MongoClientSettings.Builder`](https://mongodb.github.io/mongo-java-driver/5.8/apidocs/mongodb-driver-core/com/mongodb/MongoClientSettings.Builder.html) that is used to build the [`MongoClientSettings`](https://mongodb.github.io/mongo-java-driver/5.8/apidocs/mongodb-driver-core/com/mongodb/MongoClientSettings.html).

You can set the `spring.mongodb.uri` property to change the URL and configure additional settings such as the *replica set*, as shown in the following example:

* Properties
* YAML

```
spring.mongodb.uri=mongodb://user:[email protected]:27017,mongoserver2.example.com:23456/test
```

```
spring:
  mongodb:
    uri: "mongodb://user:[email protected]:27017,mongoserver2.example.com:23456/test"
```

Alternatively, you can specify connection details using discrete properties.
For example, you might declare the following settings in your `application.properties`:

* Properties
* YAML

```
spring.mongodb.host=mongoserver1.example.com
spring.mongodb.port=27017
spring.mongodb.additional-hosts[0]=mongoserver2.example.com:23456
spring.mongodb.database=test
spring.mongodb.username=user
spring.mongodb.password=secret
```

```
spring:
  mongodb:
    host: "mongoserver1.example.com"
    port: 27017
    additional-hosts:
    - "mongoserver2.example.com:23456"
    database: "test"
    username: "user"
    password: "secret"
```

The auto-configured [`MongoClient`](https://mongodb.github.io/mongo-java-driver/5.8/apidocs/mongodb-driver-sync/com/mongodb/client/MongoClient.html) can be configured to use SSL for communication with the server by setting the properties as shown in this example:

* Properties
* YAML

```
spring.mongodb.uri=mongodb://user:[email protected]:27017,mongoserver2.example.com:23456/test
spring.mongodb.ssl.enabled=true
```

```
spring:
  mongodb:
    uri: "mongodb://user:[email protected]:27017,mongoserver2.example.com:23456/test"
    ssl:
      enabled: true
```

Custom SSL trust material can be configured in an [SSL bundle](../features/ssl.html) and applied to the [`MongoClient`](https://mongodb.github.io/mongo-java-driver/5.8/apidocs/mongodb-driver-sync/com/mongodb/client/MongoClient.html) as shown in this example:

* Properties
* YAML

```
spring.mongodb.uri=mongodb://user:[email protected]:27017,mongoserver2.example.com:23456/test
spring.mongodb.ssl.bundle=example
```

```
spring:
  mongodb:
    uri: "mongodb://user:[email protected]:27017,mongoserver2.example.com:23456/test"
    ssl:
      bundle: "example"
```

|  |  |
| --- | --- |
|  | If `spring.mongodb.port` is not specified, the default of `27017` is used. You could delete this line from the example shown earlier.  You can also specify the port as part of the host address by using the `host:port` syntax. This format should be used if you need to change the port of an `additional-hosts` entry. |

|  |  |
| --- | --- |
|  | If you do not use Spring Data MongoDB, you can inject a [`MongoClient`](https://mongodb.github.io/mongo-java-driver/5.8/apidocs/mongodb-driver-sync/com/mongodb/client/MongoClient.html) bean instead of using [`MongoDatabaseFactory`](https://docs.spring.io/spring-data/mongodb/docs/5.1.x/api/org/springframework/data/mongodb/MongoDatabaseFactory.html). If you want to take complete control of establishing the MongoDB connection, you can also declare your own [`MongoDatabaseFactory`](https://docs.spring.io/spring-data/mongodb/docs/5.1.x/api/org/springframework/data/mongodb/MongoDatabaseFactory.html) or [`MongoClient`](https://mongodb.github.io/mongo-java-driver/5.8/apidocs/mongodb-driver-sync/com/mongodb/client/MongoClient.html) bean. |

|  |  |
| --- | --- |
|  | If you are using the reactive driver, Netty is required for SSL. The auto-configuration configures this factory automatically if Netty is available and the factory to use has not been customized already. |

### MongoTemplate

[Spring Data MongoDB](https://spring.io/projects/spring-data-mongodb) provides a [`MongoTemplate`](https://docs.spring.io/spring-data/mongodb/docs/5.1.x/api/org/springframework/data/mongodb/core/MongoTemplate.html) class that is very similar in its design to Spring’s [`JdbcTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jdbc/core/JdbcTemplate.html).
As with [`JdbcTemplate`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/jdbc/core/JdbcTemplate.html), Spring Boot auto-configures a bean for you to inject the template, as follows:

* Java
* Kotlin

```
import com.mongodb.client.MongoCollection;
import org.bson.Document;

import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Component;

@Component
public class MyBean {

	private final MongoTemplate mongoTemplate;

	public MyBean(MongoTemplate mongoTemplate) {
		this.mongoTemplate = mongoTemplate;
	}

	// ...

	public MongoCollection<Document> someMethod() {
		return this.mongoTemplate.getCollection("users");
	}

}
```

```
import com.mongodb.client.MongoCollection
import org.bson.Document
import org.springframework.data.mongodb.core.MongoTemplate
import org.springframework.stereotype.Component

@Component
class MyBean(private val mongoTemplate: MongoTemplate) {

	// ...

	fun someMethod(): MongoCollection<Document> {
		return mongoTemplate.getCollection("users")
	}

}
```

See the [`MongoOperations`](https://docs.spring.io/spring-data/mongodb/docs/5.1.x/api/org/springframework/data/mongodb/core/MongoOperations.html) API documentation for complete details.

### Spring Data MongoDB Repositories

Spring Data includes repository support for MongoDB.
As with the JPA repositories discussed earlier, the basic principle is that queries are constructed automatically, based on method names.

In fact, both Spring Data JPA and Spring Data MongoDB share the same common infrastructure.
You could take the JPA example from earlier and, assuming that `City` is now a MongoDB data class rather than a JPA [`@Entity`](https://jakarta.ee/specifications/persistence/3.2/apidocs/jakarta.persistence/jakarta/persistence/Entity.html), it works in the same way, as shown in the following example:

* Java
* Kotlin

```
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.repository.Repository;

public interface CityRepository extends Repository<City, Long> {

	Page<City> findAll(Pageable pageable);

	City findByNameAndStateAllIgnoringCase(String name, String state);

}
```

```
import org.springframework.data.domain.Page
import org.springframework.data.domain.Pageable
import org.springframework.data.repository.Repository

interface CityRepository :
	Repository<City, Long> {
	fun findAll(pageable: Pageable?): Page<City>
	fun findByNameAndStateAllIgnoringCase(name: String, state: String): City?
}
```

Repositories and documents are found through scanning.
By default, the [auto-configuration packages](../using/auto-configuration.html#using.auto-configuration.packages) are scanned.
You can customize the locations to look for repositories and documents by using [`@EnableMongoRepositories`](https://docs.spring.io/spring-data/mongodb/docs/5.1.x/api/org/springframework/data/mongodb/repository/config/EnableMongoRepositories.html) and [`@EntityScan`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/persistence/autoconfigure/EntityScan.html) respectively.

|  |  |
| --- | --- |
|  | For complete details of Spring Data MongoDB, including its rich object mapping technologies, see its [reference documentation](https://docs.spring.io/spring-data/mongodb/reference/5.1). |

## Neo4j

[Neo4j](https://neo4j.com/) is an open-source NoSQL graph database that uses a rich data model of nodes connected by first class relationships, which is better suited for connected big data than traditional RDBMS approaches.
Spring Boot offers several conveniences for working with Neo4j, including the `spring-boot-starter-data-neo4j` starter.

### Connecting to a Neo4j Database

To access a Neo4j server, you can inject an auto-configured [`Driver`](https://javadoc.io/doc/org.neo4j.driver/neo4j-java-driver/6.1.0/org/neo4j/driver/Driver.html).
By default, the instance tries to connect to a Neo4j server at `localhost:7687` using the Bolt protocol.
The following example shows how to inject a Neo4j [`Driver`](https://javadoc.io/doc/org.neo4j.driver/neo4j-java-driver/6.1.0/org/neo4j/driver/Driver.html) that gives you access, amongst other things, to a [`Session`](https://javadoc.io/doc/org.neo4j.driver/neo4j-java-driver/6.1.0/org/neo4j/driver/Session.html):

* Java
* Kotlin

```
import org.neo4j.driver.Driver;
import org.neo4j.driver.Session;
import org.neo4j.driver.Values;

import org.springframework.stereotype.Component;

@Component
public class MyBean {

	private final Driver driver;

	public MyBean(Driver driver) {
		this.driver = driver;
	}

	// ...

	public String someMethod(String message) {
		try (Session session = this.driver.session()) {
			return session.executeWrite(
					(transaction) -> transaction
						.run("CREATE (a:Greeting) SET a.message = $message RETURN a.message + ', from node ' + id(a)",
								Values.parameters("message", message))
						.single()
						.get(0)
						.asString());
		}
	}

}
```

```
import org.neo4j.driver.Driver
import org.neo4j.driver.TransactionContext
import org.neo4j.driver.Values
import org.springframework.stereotype.Component

@Component
class MyBean(private val driver: Driver) {
	// ...
	fun someMethod(message: String?): String {
		driver.session().use { session ->
			return@someMethod session.executeWrite { transaction: TransactionContext ->
				transaction
					.run(
						"CREATE (a:Greeting) SET a.message = \$message RETURN a.message + ', from node ' + id(a)",
						Values.parameters("message", message)
					)
					.single()[0].asString()
			}
		}
	}
}
```

You can configure various aspects of the driver using `spring.neo4j.*` properties.
The following example shows how to configure the uri and credentials to use:

* Properties
* YAML

```
spring.neo4j.uri=bolt://my-server:7687
spring.neo4j.authentication.username=neo4j
spring.neo4j.authentication.password=secret
```

```
spring:
  neo4j:
    uri: "bolt://my-server:7687"
    authentication:
      username: "neo4j"
      password: "secret"
```

The auto-configured [`Driver`](https://javadoc.io/doc/org.neo4j.driver/neo4j-java-driver/6.1.0/org/neo4j/driver/Driver.html) is created using `org.neo4j.driver.Config$ConfigBuilder`.
To fine-tune its configuration, declare one or more [`ConfigBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/neo4j/autoconfigure/ConfigBuilderCustomizer.html) beans.
Each will be called in order with the `org.neo4j.driver.Config$ConfigBuilder` that is used to build the [`Driver`](https://javadoc.io/doc/org.neo4j.driver/neo4j-java-driver/6.1.0/org/neo4j/driver/Driver.html).

### Spring Data Neo4j Repositories

Spring Data includes repository support for Neo4j.
For complete details of Spring Data Neo4j, see the [reference documentation](https://docs.spring.io/spring-data/neo4j/reference/8.1).

Spring Data Neo4j shares the common infrastructure with Spring Data JPA as many other Spring Data modules do.
You could take the JPA example from earlier and define `City` as Spring Data Neo4j [`@Node`](https://docs.spring.io/spring-data/neo4j/docs/8.1.x/api/org/springframework/data/neo4j/core/schema/Node.html) rather than JPA [`@Entity`](https://jakarta.ee/specifications/persistence/3.2/apidocs/jakarta.persistence/jakarta/persistence/Entity.html) and the repository abstraction works in the same way, as shown in the following example:

* Java
* Kotlin

```
import org.springframework.data.neo4j.repository.Neo4jRepository;

public interface CityRepository extends Neo4jRepository<City, Long> {

	City findOneByNameAndState(String name, String state);

}
```

```
import org.springframework.data.neo4j.repository.Neo4jRepository

interface CityRepository : Neo4jRepository<City, Long> {

	fun findOneByNameAndState(name: String?, state: String?): City?

}
```

The `spring-boot-starter-data-neo4j` starter enables the repository support as well as transaction management.
Spring Boot supports both classic and reactive Neo4j repositories, using the [`Neo4jTemplate`](https://docs.spring.io/spring-data/neo4j/docs/8.1.x/api/org/springframework/data/neo4j/core/Neo4jTemplate.html) or [`ReactiveNeo4jTemplate`](https://docs.spring.io/spring-data/neo4j/docs/8.1.x/api/org/springframework/data/neo4j/core/ReactiveNeo4jTemplate.html) beans.
When Project Reactor is available on the classpath, the reactive style is also auto-configured.

Repositories and entities are found through scanning.
By default, the [auto-configuration packages](../using/auto-configuration.html#using.auto-configuration.packages) are scanned.
You can customize the locations to look for repositories and entities by using [`@EnableNeo4jRepositories`](https://docs.spring.io/spring-data/neo4j/docs/8.1.x/api/org/springframework/data/neo4j/repository/config/EnableNeo4jRepositories.html) and [`@EntityScan`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/persistence/autoconfigure/EntityScan.html) respectively.

|  |  |
| --- | --- |
|  | In an application using the reactive style, a [`ReactiveTransactionManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/transaction/ReactiveTransactionManager.html) is not auto-configured. To enable transaction management, the following bean must be defined in your configuration:  * Java * Kotlin  ``` import org.neo4j.driver.Driver;  import org.springframework.context.annotation.Bean; import org.springframework.context.annotation.Configuration; import org.springframework.data.neo4j.core.ReactiveDatabaseSelectionProvider; import org.springframework.data.neo4j.core.transaction.ReactiveNeo4jTransactionManager;  @Configuration(proxyBeanMethods = false) public class MyNeo4jConfiguration {  	@Bean 	public ReactiveNeo4jTransactionManager reactiveTransactionManager(Driver driver, 			ReactiveDatabaseSelectionProvider databaseNameProvider) { 		return new ReactiveNeo4jTransactionManager(driver, databaseNameProvider); 	}  } ```  ``` import org.neo4j.driver.Driver import org.springframework.context.annotation.Bean import org.springframework.context.annotation.Configuration import org.springframework.data.neo4j.core.ReactiveDatabaseSelectionProvider import org.springframework.data.neo4j.core.transaction.ReactiveNeo4jTransactionManager  @Configuration(proxyBeanMethods = false) class MyNeo4jConfiguration {  	@Bean 	fun reactiveTransactionManager(driver: Driver, 			databaseNameProvider: ReactiveDatabaseSelectionProvider): ReactiveNeo4jTransactionManager { 		return ReactiveNeo4jTransactionManager(driver, databaseNameProvider) 	} } ``` |

## Elasticsearch

[Elasticsearch](https://www.elastic.co/products/elasticsearch) is an open source, distributed, RESTful search and analytics engine.
Spring Boot offers basic auto-configuration for Elasticsearch clients.

Spring Boot supports several clients:

* The official low-level REST client
* The official Java API client
* The [`ReactiveElasticsearchClient`](https://docs.spring.io/spring-data/elasticsearch/docs/6.1.x/api/org/springframework/data/elasticsearch/client/elc/ReactiveElasticsearchClient.html) provided by Spring Data Elasticsearch

Spring Boot provides a dedicated starter, `spring-boot-starter-data-elasticsearch`.

### Connecting to Elasticsearch Using REST clients

Elasticsearch ships two different REST clients that you can use to query a cluster: the [low-level client](https://www.elastic.co/docs/reference/elasticsearch/clients/java/transport/rest5-client/) and the [Java API client](https://www.elastic.co/docs/reference/elasticsearch/clients/java).
The Java API client is provided by the `co.elastic.clients:elasticsearch-java` module and
the low-level client is provided by the `co.elastic.clients:elasticsearch-rest5-client` module.
Additionally, Spring Boot provides support for a reactive client from the `org.springframework.data:spring-data-elasticsearch` module.
By default, the clients will target `localhost:9200`.
You can use `spring.elasticsearch.*` properties to further tune how the clients are configured, as shown in the following example:

* Properties
* YAML

```
spring.elasticsearch.uris=https://search.example.com:9200
spring.elasticsearch.socket-timeout=10s
spring.elasticsearch.username=user
spring.elasticsearch.password=secret
```

```
spring:
  elasticsearch:
    uris: "https://search.example.com:9200"
    socket-timeout: "10s"
    username: "user"
    password: "secret"
```

#### Connecting to Elasticsearch Using Rest5Client

If you have `co.elastic.clients:elasticsearch-rest5-client` on the classpath, Spring Boot will auto-configure and register a [`Rest5Client`](https://javadoc.io/doc/co.elastic.clients/elasticsearch-java/9.4.2/index.html/co/elastic/clients/transport/rest5_client/low_level/Rest5Client.html) bean.
In addition to the properties described previously, to fine-tune the [`Rest5Client`](https://javadoc.io/doc/co.elastic.clients/elasticsearch-java/9.4.2/index.html/co/elastic/clients/transport/rest5_client/low_level/Rest5Client.html) you can register an arbitrary number of beans that implement [`Rest5ClientBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/elasticsearch/autoconfigure/Rest5ClientBuilderCustomizer.html) for more advanced customizations.
To take full control over the client’s configuration, define a [`Rest5ClientBuilder`](https://javadoc.io/doc/co.elastic.clients/elasticsearch-java/9.4.2/index.html/co/elastic/clients/transport/rest5_client/low_level/Rest5ClientBuilder.html) bean.

Additionally, a [`Sniffer`](https://javadoc.io/doc/co.elastic.clients/elasticsearch-java/9.4.2/index.html/co/elastic/clients/transport/rest5_client/low_level/sniffer/Sniffer.html) can be auto-configured to automatically discover nodes from a running Elasticsearch cluster and set them on the [`Rest5Client`](https://javadoc.io/doc/co.elastic.clients/elasticsearch-java/9.4.2/index.html/co/elastic/clients/transport/rest5_client/low_level/Rest5Client.html) bean.
You can further tune how [`Sniffer`](https://javadoc.io/doc/co.elastic.clients/elasticsearch-java/9.4.2/index.html/co/elastic/clients/transport/rest5_client/low_level/sniffer/Sniffer.html) is configured, as shown in the following example:

* Properties
* YAML

```
spring.elasticsearch.restclient.sniffer.enabled=true
spring.elasticsearch.restclient.sniffer.interval=10m
spring.elasticsearch.restclient.sniffer.delay-after-failure=30s
```

```
spring:
  elasticsearch:
    restclient:
      sniffer:
        enabled: true
        interval: "10m"
        delay-after-failure: "30s"
```

#### Connecting to Elasticsearch Using ElasticsearchClient

If you use the `spring-boot-starter-elasticsearch` or have added `co.elastic.clients:elasticsearch-java` to the classpath, Spring Boot will auto-configure and register an [`ElasticsearchClient`](https://javadoc.io/doc/co.elastic.clients/elasticsearch-java/9.4.2/index.html/co/elastic/clients/elasticsearch/ElasticsearchClient.html) bean.

The [`ElasticsearchClient`](https://javadoc.io/doc/co.elastic.clients/elasticsearch-java/9.4.2/index.html/co/elastic/clients/elasticsearch/ElasticsearchClient.html) uses a transport that depends upon the previously described [`Rest5Client`](https://javadoc.io/doc/co.elastic.clients/elasticsearch-java/9.4.2/index.html/co/elastic/clients/transport/rest5_client/low_level/Rest5Client.html).
Therefore, the properties described previously can be used to configure the [`ElasticsearchClient`](https://javadoc.io/doc/co.elastic.clients/elasticsearch-java/9.4.2/index.html/co/elastic/clients/elasticsearch/ElasticsearchClient.html).
Furthermore, you can define a [`Rest5ClientOptions`](https://javadoc.io/doc/co.elastic.clients/elasticsearch-java/9.4.2/index.html/co/elastic/clients/transport/rest5_client/Rest5ClientOptions.html) bean to take further control of the behavior of the transport.

#### Connecting to Elasticsearch using ReactiveElasticsearchClient

[Spring Data Elasticsearch](https://spring.io/projects/spring-data-elasticsearch) ships [`ReactiveElasticsearchClient`](https://docs.spring.io/spring-data/elasticsearch/docs/6.1.x/api/org/springframework/data/elasticsearch/client/elc/ReactiveElasticsearchClient.html) for querying Elasticsearch instances in a reactive fashion.
If you have Spring Data Elasticsearch and Reactor on the classpath, Spring Boot will auto-configure and register a [`ReactiveElasticsearchClient`](https://docs.spring.io/spring-data/elasticsearch/docs/6.1.x/api/org/springframework/data/elasticsearch/client/elc/ReactiveElasticsearchClient.html).

The [`ReactiveElasticsearchClient`](https://docs.spring.io/spring-data/elasticsearch/docs/6.1.x/api/org/springframework/data/elasticsearch/client/elc/ReactiveElasticsearchClient.html) uses a transport that depends upon the previously described [`Rest5Client`](https://javadoc.io/doc/co.elastic.clients/elasticsearch-java/9.4.2/index.html/co/elastic/clients/transport/rest5_client/low_level/Rest5Client.html).
Therefore, the properties described previously can be used to configure the [`ReactiveElasticsearchClient`](https://docs.spring.io/spring-data/elasticsearch/docs/6.1.x/api/org/springframework/data/elasticsearch/client/elc/ReactiveElasticsearchClient.html).
Furthermore, you can define a [`Rest5ClientOptions`](https://javadoc.io/doc/co.elastic.clients/elasticsearch-java/9.4.2/index.html/co/elastic/clients/transport/rest5_client/Rest5ClientOptions.html) bean to take further control of the behavior of the transport.

### Connecting to Elasticsearch by Using Spring Data

To connect to Elasticsearch, an [`ElasticsearchClient`](https://javadoc.io/doc/co.elastic.clients/elasticsearch-java/9.4.2/index.html/co/elastic/clients/elasticsearch/ElasticsearchClient.html) bean must be defined,
auto-configured by Spring Boot or manually provided by the application (see previous sections).
With this configuration in place, an
[`ElasticsearchTemplate`](https://docs.spring.io/spring-data/elasticsearch/docs/6.1.x/api/org/springframework/data/elasticsearch/client/elc/ElasticsearchTemplate.html) can be injected like any other Spring bean,
as shown in the following example:

* Java
* Kotlin

```
import org.springframework.data.elasticsearch.client.elc.ElasticsearchTemplate;
import org.springframework.stereotype.Component;

@Component
public class MyBean {

	private final ElasticsearchTemplate template;

	public MyBean(ElasticsearchTemplate template) {
		this.template = template;
	}

	// ...

	public boolean someMethod(String id) {
		return this.template.exists(id, User.class);
	}

}
```

```
import org.springframework.stereotype.Component

@Component
class MyBean(private val template: org.springframework.data.elasticsearch.client.elc.ElasticsearchTemplate ) {

	// ...

	fun someMethod(id: String): Boolean {
		return template.exists(id, User::class.java)
	}

}
```

In the presence of `spring-data-elasticsearch` and Reactor, Spring Boot can also auto-configure a [`ReactiveElasticsearchClient`](#data.nosql.elasticsearch.connecting-using-rest.reactiveclient) and a [`ReactiveElasticsearchTemplate`](https://docs.spring.io/spring-data/elasticsearch/docs/6.1.x/api/org/springframework/data/elasticsearch/client/elc/ReactiveElasticsearchTemplate.html) as beans.
They are the reactive equivalent of the other REST clients.

### Spring Data Elasticsearch Repositories

Spring Data includes repository support for Elasticsearch.
As with the JPA repositories discussed earlier, the basic principle is that queries are constructed for you automatically based on method names.

In fact, both Spring Data JPA and Spring Data Elasticsearch share the same common infrastructure.
You could take the JPA example from earlier and, assuming that `City` is now an Elasticsearch [`@Document`](https://docs.spring.io/spring-data/elasticsearch/docs/6.1.x/api/org/springframework/data/elasticsearch/annotations/Document.html) class rather than a JPA [`@Entity`](https://jakarta.ee/specifications/persistence/3.2/apidocs/jakarta.persistence/jakarta/persistence/Entity.html), it works in the same way.

Repositories and documents are found through scanning.
By default, the [auto-configuration packages](../using/auto-configuration.html#using.auto-configuration.packages) are scanned.
You can customize the locations to look for repositories and documents by using [`@EnableElasticsearchRepositories`](https://docs.spring.io/spring-data/elasticsearch/docs/6.1.x/api/org/springframework/data/elasticsearch/repository/config/EnableElasticsearchRepositories.html) and [`@EntityScan`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/persistence/autoconfigure/EntityScan.html) respectively.

|  |  |
| --- | --- |
|  | For complete details of Spring Data Elasticsearch, see the [reference documentation](https://docs.spring.io/spring-data/elasticsearch/reference/6.1). |

Spring Boot supports both classic and reactive Elasticsearch repositories, using the [`ElasticsearchTemplate`](https://docs.spring.io/spring-data/elasticsearch/docs/6.1.x/api/org/springframework/data/elasticsearch/client/elc/ElasticsearchTemplate.html) or [`ReactiveElasticsearchTemplate`](https://docs.spring.io/spring-data/elasticsearch/docs/6.1.x/api/org/springframework/data/elasticsearch/client/elc/ReactiveElasticsearchTemplate.html) beans.
Most likely those beans are auto-configured by Spring Boot given the required dependencies are present.

If you wish to use your own template for backing the Elasticsearch repositories, you can add your own [`ElasticsearchTemplate`](https://docs.spring.io/spring-data/elasticsearch/docs/6.1.x/api/org/springframework/data/elasticsearch/client/elc/ElasticsearchTemplate.html) or [`ElasticsearchOperations`](https://docs.spring.io/spring-data/elasticsearch/docs/6.1.x/api/org/springframework/data/elasticsearch/core/ElasticsearchOperations.html) [`@Bean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Bean.html), as long as it is named `"elasticsearchTemplate"`.
Same applies to [`ReactiveElasticsearchTemplate`](https://docs.spring.io/spring-data/elasticsearch/docs/6.1.x/api/org/springframework/data/elasticsearch/client/elc/ReactiveElasticsearchTemplate.html) and [`ReactiveElasticsearchOperations`](https://docs.spring.io/spring-data/elasticsearch/docs/6.1.x/api/org/springframework/data/elasticsearch/core/ReactiveElasticsearchOperations.html), with the bean name `"reactiveElasticsearchTemplate"`.

You can choose to disable the repositories support with the following property:

* Properties
* YAML

```
spring.data.elasticsearch.repositories.enabled=false
```

```
spring:
  data:
    elasticsearch:
      repositories:
        enabled: false
```

## Cassandra

[Cassandra](https://cassandra.apache.org/) is an open source, distributed database management system designed to handle large amounts of data across many commodity servers.
Spring Boot offers auto-configuration for Cassandra and the abstractions on top of it provided by [Spring Data Cassandra](https://spring.io/projects/spring-data-cassandra).
There is a `spring-boot-starter-data-cassandra` starter for collecting the dependencies in a convenient way.

### Connecting to Cassandra

You can inject an auto-configured [`CqlTemplate`](https://docs.spring.io/spring-data/cassandra/docs/5.1.x/api/org/springframework/data/cassandra/core/cql/CqlTemplate.html), [`CassandraTemplate`](https://docs.spring.io/spring-data/cassandra/docs/5.1.x/api/org/springframework/data/cassandra/core/CassandraTemplate.html), or a Cassandra `CqlSession` instance as you would with any other Spring Bean.
The `spring.cassandra.*` properties can be used to customize the connection.
Generally, you provide `keyspace-name` and `contact-points` as well the local datacenter name, as shown in the following example:

* Properties
* YAML

```
spring.cassandra.keyspace-name=mykeyspace
spring.cassandra.contact-points=cassandrahost1:9042,cassandrahost2:9042
spring.cassandra.local-datacenter=datacenter1
```

```
spring:
  cassandra:
    keyspace-name: "mykeyspace"
    contact-points: "cassandrahost1:9042,cassandrahost2:9042"
    local-datacenter: "datacenter1"
```

If the port is the same for all your contact points you can use a shortcut and only specify the host names, as shown in the following example:

* Properties
* YAML

```
spring.cassandra.keyspace-name=mykeyspace
spring.cassandra.contact-points=cassandrahost1,cassandrahost2
spring.cassandra.local-datacenter=datacenter1
```

```
spring:
  cassandra:
    keyspace-name: "mykeyspace"
    contact-points: "cassandrahost1,cassandrahost2"
    local-datacenter: "datacenter1"
```

|  |  |
| --- | --- |
|  | Those two examples are identical as the port default to `9042`. If you need to configure the port, use `spring.cassandra.port`. |

The auto-configured `CqlSession` can be configured to use SSL for communication with the server by setting the properties as shown in this example:

* Properties
* YAML

```
spring.cassandra.keyspace-name=mykeyspace
spring.cassandra.contact-points=cassandrahost1,cassandrahost2
spring.cassandra.local-datacenter=datacenter1
spring.cassandra.ssl.enabled=true
```

```
spring:
  cassandra:
    keyspace-name: "mykeyspace"
    contact-points: "cassandrahost1,cassandrahost2"
    local-datacenter: "datacenter1"
    ssl:
      enabled: true
```

Custom SSL trust material can be configured in an [SSL bundle](../features/ssl.html) and applied to the `CqlSession` as shown in this example:

* Properties
* YAML

```
spring.cassandra.keyspace-name=mykeyspace
spring.cassandra.contact-points=cassandrahost1,cassandrahost2
spring.cassandra.local-datacenter=datacenter1
spring.cassandra.ssl.bundle=example
```

```
spring:
  cassandra:
    keyspace-name: "mykeyspace"
    contact-points: "cassandrahost1,cassandrahost2"
    local-datacenter: "datacenter1"
    ssl:
      bundle: "example"
```

|  |  |
| --- | --- |
|  | The Cassandra driver has its own configuration infrastructure that loads an `application.conf` at the root of the classpath.  Spring Boot does not look for such a file by default but can load one using `spring.cassandra.config`. If a property is both present in `spring.cassandra.*` and the configuration file, the value in `spring.cassandra.*` takes precedence.  For more advanced driver customizations, you can register an arbitrary number of beans that implement [`DriverConfigLoaderBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/cassandra/autoconfigure/DriverConfigLoaderBuilderCustomizer.html). The `CqlSession` can be customized with a bean of type [`CqlSessionBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/cassandra/autoconfigure/CqlSessionBuilderCustomizer.html). |

|  |  |
| --- | --- |
|  | If you use `CqlSessionBuilder` to create multiple `CqlSession` beans, keep in mind the builder is mutable so make sure to inject a fresh copy for each session. |

The following code listing shows how to inject a Cassandra bean:

* Java
* Kotlin

```
import org.springframework.data.cassandra.core.CassandraTemplate;
import org.springframework.stereotype.Component;

@Component
public class MyBean {

	private final CassandraTemplate template;

	public MyBean(CassandraTemplate template) {
		this.template = template;
	}

	// ...

	public long someMethod() {
		return this.template.count(User.class);
	}

}
```

```
import org.springframework.data.cassandra.core.CassandraTemplate
import org.springframework.stereotype.Component

@Component
class MyBean(private val template: CassandraTemplate) {

	// ...

	fun someMethod(): Long {
		return template.count(User::class.java)
	}

}
```

If you add your own [`@Bean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Bean.html) of type [`CassandraTemplate`](https://docs.spring.io/spring-data/cassandra/docs/5.1.x/api/org/springframework/data/cassandra/core/CassandraTemplate.html), it replaces the default.

### Spring Data Cassandra Repositories

Spring Data includes basic repository support for Cassandra.
Currently, this is more limited than the JPA repositories discussed earlier and needs [`@Query`](https://docs.spring.io/spring-data/cassandra/docs/5.1.x/api/org/springframework/data/cassandra/repository/Query.html) annotated finder methods.

Repositories and entities are found through scanning.
By default, the [auto-configuration packages](../using/auto-configuration.html#using.auto-configuration.packages) are scanned.
You can customize the locations to look for repositories and entities by using [`@EnableCassandraRepositories`](https://docs.spring.io/spring-data/cassandra/docs/5.1.x/api/org/springframework/data/cassandra/repository/config/EnableCassandraRepositories.html) and [`@EntityScan`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/persistence/autoconfigure/EntityScan.html) respectively.

|  |  |
| --- | --- |
|  | For complete details of Spring Data Cassandra, see the [reference documentation](https://docs.spring.io/spring-data/cassandra/reference/5.1). |

## Couchbase

[Couchbase](https://www.couchbase.com/) is an open-source, distributed, multi-model NoSQL document-oriented database that is optimized for interactive applications.
Spring Boot offers auto-configuration for Couchbase and the abstractions on top of it provided by [Spring Data Couchbase](https://github.com/spring-projects/spring-data-couchbase).
There are `spring-boot-starter-data-couchbase` and `spring-boot-starter-data-couchbase-reactive` starters for collecting the dependencies in a convenient way.

### Connecting to Couchbase

You can get a [`Cluster`](https://javadoc.io/doc/com.couchbase.client/java-client/3.11.3/com/couchbase/client/java/Cluster.html) by adding the Couchbase SDK and some configuration.
The `spring.couchbase.*` properties can be used to customize the connection.
Generally, you provide the [connection string](https://docs.couchbase.com/dotnet-sdk/current/howtos/managing-connections.html) and credentials for authentication. Basic authentication with username and password can be configured as shown in the following example:

* Properties
* YAML

```
spring.couchbase.connection-string=couchbase://192.168.1.123
spring.couchbase.username=user
spring.couchbase.password=secret
```

```
spring:
  couchbase:
    connection-string: "couchbase://192.168.1.123"
    username: "user"
    password: "secret"
```

[Client certificates](https://docs.couchbase.com/server/current/manage/manage-security/configure-client-certificates.html) can be used for authentication instead of username and password.
The location and password for a Java KeyStore containing client certificates can be configured as shown in the following example:

* Properties
* YAML

```
spring.couchbase.connection-string=couchbase://192.168.1.123
spring.couchbase.env.ssl.enabled=true
spring.couchbase.authentication.jks.location=classpath:client.p12
spring.couchbase.authentication.jks.password=secret
```

```
spring:
  couchbase:
    connection-string: "couchbase://192.168.1.123"
    env:
      ssl:
        enabled: true
    authentication:
      jks:
        location: "classpath:client.p12"
        password: "secret"
```

PEM-encoded certificates and a private key can be configured as shown in the following example:

* Properties
* YAML

```
spring.couchbase.connection-string=couchbase://192.168.1.123
spring.couchbase.env.ssl.enabled=true
spring.couchbase.authentication.pem.certificates=classpath:client.crt
spring.couchbase.authentication.pem.private-key=classpath:client.key
```

```
spring:
  couchbase:
    connection-string: "couchbase://192.168.1.123"
    env:
      ssl:
        enabled: true
    authentication:
      pem:
        certificates: "classpath:client.crt"
        private-key: "classpath:client.key"
```

It is also possible to customize some of the [`ClusterEnvironment`](https://javadoc.io/doc/com.couchbase.client/java-client/3.11.3/com/couchbase/client/java/env/ClusterEnvironment.html) settings.
For instance, the following configuration changes the timeout to open a new [`Bucket`](https://javadoc.io/doc/com.couchbase.client/java-client/3.11.3/com/couchbase/client/java/Bucket.html) and enables SSL support with a reference to a configured [SSL bundle](../features/ssl.html):

* Properties
* YAML

```
spring.couchbase.env.timeouts.connect=3s
spring.couchbase.env.ssl.bundle=example
```

```
spring:
  couchbase:
    env:
      timeouts:
        connect: "3s"
      ssl:
        bundle: "example"
```

|  |  |
| --- | --- |
|  | Check the `spring.couchbase.env.*` properties for more details. To take more control, one or more [`ClusterEnvironmentBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/couchbase/autoconfigure/ClusterEnvironmentBuilderCustomizer.html) beans can be used. |

### Spring Data Couchbase Repositories

Spring Data includes repository support for Couchbase.

Repositories and documents are found through scanning.
By default, the [auto-configuration packages](../using/auto-configuration.html#using.auto-configuration.packages) are scanned.
You can customize the locations to look for repositories and documents by using [`@EnableCouchbaseRepositories`](https://docs.spring.io/spring-data/couchbase/docs/6.1.x/api/org/springframework/data/couchbase/repository/config/EnableCouchbaseRepositories.html) and [`@EntityScan`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/persistence/autoconfigure/EntityScan.html) respectively.

For complete details of Spring Data Couchbase, see the [reference documentation](https://docs.spring.io/spring-data/couchbase/reference/6.1).

You can inject an auto-configured [`CouchbaseTemplate`](https://docs.spring.io/spring-data/couchbase/docs/6.1.x/api/org/springframework/data/couchbase/core/CouchbaseTemplate.html) instance as you would with any other Spring Bean, provided a [`CouchbaseClientFactory`](https://docs.spring.io/spring-data/couchbase/docs/6.1.x/api/org/springframework/data/couchbase/CouchbaseClientFactory.html) bean is available.
This happens when a [`Cluster`](https://javadoc.io/doc/com.couchbase.client/java-client/3.11.3/com/couchbase/client/java/Cluster.html) is available, as described above, and a bucket name has been specified:

* Properties
* YAML

```
spring.data.couchbase.bucket-name=my-bucket
```

```
spring:
  data:
    couchbase:
      bucket-name: "my-bucket"
```

The following examples shows how to inject a [`CouchbaseTemplate`](https://docs.spring.io/spring-data/couchbase/docs/6.1.x/api/org/springframework/data/couchbase/core/CouchbaseTemplate.html) bean:

* Java
* Kotlin

```
import org.springframework.data.couchbase.core.CouchbaseTemplate;
import org.springframework.stereotype.Component;

@Component
public class MyBean {

	private final CouchbaseTemplate template;

	public MyBean(CouchbaseTemplate template) {
		this.template = template;
	}

	// ...

	public String someMethod() {
		return this.template.getBucketName();
	}

}
```

```
import org.springframework.data.couchbase.core.CouchbaseTemplate
import org.springframework.stereotype.Component

@Component
class MyBean(private val template: CouchbaseTemplate) {

	// ...

	fun someMethod(): String {
		return template.bucketName
	}

}
```

There are a few beans that you can define in your own configuration to override those provided by the auto-configuration:

* A [`CouchbaseMappingContext`](https://docs.spring.io/spring-data/couchbase/docs/6.1.x/api/org/springframework/data/couchbase/core/mapping/CouchbaseMappingContext.html) [`@Bean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Bean.html) with a name of `couchbaseMappingContext`.
* A [`CustomConversions`](https://docs.spring.io/spring-data/commons/docs/4.1.x/api/org/springframework/data/convert/CustomConversions.html) [`@Bean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Bean.html) with a name of `couchbaseCustomConversions`.
* A [`CouchbaseTemplate`](https://docs.spring.io/spring-data/couchbase/docs/6.1.x/api/org/springframework/data/couchbase/core/CouchbaseTemplate.html) [`@Bean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Bean.html) with a name of `couchbaseTemplate`.

To avoid hard-coding those names in your own config, you can reuse [`BeanNames`](https://docs.spring.io/spring-data/couchbase/docs/6.1.x/api/org/springframework/data/couchbase/config/BeanNames.html) provided by Spring Data Couchbase.
For instance, you can customize the converters to use, as follows:

* Java
* Kotlin

```
import org.assertj.core.util.Arrays;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.couchbase.config.BeanNames;
import org.springframework.data.couchbase.core.convert.CouchbaseCustomConversions;

@Configuration(proxyBeanMethods = false)
public class MyCouchbaseConfiguration {

	@Bean(BeanNames.COUCHBASE_CUSTOM_CONVERSIONS)
	public CouchbaseCustomConversions myCustomConversions() {
		return new CouchbaseCustomConversions(Arrays.asList(new MyConverter()));
	}

}
```

```
import org.assertj.core.util.Arrays
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.data.couchbase.config.BeanNames
import org.springframework.data.couchbase.core.convert.CouchbaseCustomConversions

@Configuration(proxyBeanMethods = false)
class MyCouchbaseConfiguration {

	@Bean(BeanNames.COUCHBASE_CUSTOM_CONVERSIONS)
	fun myCustomConversions(): CouchbaseCustomConversions {
		return CouchbaseCustomConversions(Arrays.asList(MyConverter()))
	}

}
```

## LDAP

[LDAP](https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol) (Lightweight Directory Access Protocol) is an open, vendor-neutral, industry standard application protocol for accessing and maintaining distributed directory information services over an IP network.
Spring Boot offers auto-configuration for any compliant LDAP server as well as support for the embedded in-memory LDAP server from [UnboundID](https://ldap.com/unboundid-ldap-sdk-for-java/).

LDAP abstractions are provided by [Spring Data LDAP](https://github.com/spring-projects/spring-data-ldap).
There is a `spring-boot-starter-data-ldap` starter for collecting the dependencies in a convenient way.

### Connecting to an LDAP Server

To connect to an LDAP server, make sure you declare a dependency on the `spring-boot-starter-data-ldap` starter or `spring-ldap-core` and then declare the URLs of your server in your application.properties, as shown in the following example:

* Properties
* YAML

```
spring.ldap.urls=ldap://myserver:1235
spring.ldap.username=admin
spring.ldap.password=secret
```

```
spring:
  ldap:
    urls: "ldap://myserver:1235"
    username: "admin"
    password: "secret"
```

If you need to customize connection settings, you can use the `spring.ldap.base` and `spring.ldap.base-environment` properties.

An [`LdapContextSource`](https://docs.spring.io/spring-ldap/docs/4.1.x/api/org/springframework/ldap/core/support/LdapContextSource.html) is auto-configured based on these settings.
If a [`DirContextAuthenticationStrategy`](https://docs.spring.io/spring-ldap/docs/4.1.x/api/org/springframework/ldap/core/support/DirContextAuthenticationStrategy.html) bean is available, it is associated to the auto-configured [`LdapContextSource`](https://docs.spring.io/spring-ldap/docs/4.1.x/api/org/springframework/ldap/core/support/LdapContextSource.html).
If you need to customize it, for instance to use a [`PooledContextSource`](https://docs.spring.io/spring-ldap/docs/4.1.x/api/org/springframework/ldap/pool2/factory/PooledContextSource.html), you can still inject the auto-configured [`LdapContextSource`](https://docs.spring.io/spring-ldap/docs/4.1.x/api/org/springframework/ldap/core/support/LdapContextSource.html).
Make sure to flag your customized [`ContextSource`](https://docs.spring.io/spring-ldap/docs/4.1.x/api/org/springframework/ldap/core/ContextSource.html) as [`@Primary`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Primary.html) so that the auto-configured [`LdapTemplate`](https://docs.spring.io/spring-ldap/docs/4.1.x/api/org/springframework/ldap/core/LdapTemplate.html) uses it.

### Spring Data LDAP Repositories

Spring Data includes repository support for LDAP.

Repositories and documents are found through scanning.
By default, the [auto-configuration packages](../using/auto-configuration.html#using.auto-configuration.packages) are scanned.
You can customize the locations to look for repositories and documents by using [`@EnableLdapRepositories`](https://docs.spring.io/spring-data/ldap/docs/4.1.x/api/org/springframework/data/ldap/repository/config/EnableLdapRepositories.html) and [`@EntityScan`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/persistence/autoconfigure/EntityScan.html) respectively.

|  |  |
| --- | --- |
|  | For complete details of Spring Data LDAP, see the [reference documentation](https://docs.spring.io/spring-data/ldap/reference/4.1). |

You can also inject an auto-configured [`LdapTemplate`](https://docs.spring.io/spring-ldap/docs/4.1.x/api/org/springframework/ldap/core/LdapTemplate.html) instance as you would with any other Spring Bean, as shown in the following example:

* Java
* Kotlin

```
import java.util.List;

import org.springframework.ldap.core.LdapTemplate;
import org.springframework.stereotype.Component;

@Component
public class MyBean {

	private final LdapTemplate template;

	public MyBean(LdapTemplate template) {
		this.template = template;
	}

	// ...

	public List<User> someMethod() {
		return this.template.findAll(User.class);
	}

}
```

```
import org.springframework.ldap.core.LdapTemplate
import org.springframework.stereotype.Component

@Component
class MyBean(private val template: LdapTemplate) {

	// ...

	fun someMethod(): List<User> {
		return template.findAll(User::class.java)
	}

}
```

### Embedded In-memory LDAP Server

For testing purposes, Spring Boot supports auto-configuration of an in-memory LDAP server from [UnboundID](https://ldap.com/unboundid-ldap-sdk-for-java/).
To configure the server, add a dependency to `com.unboundid:unboundid-ldapsdk` and declare a `spring.ldap.embedded.base-dn` property, as follows:

* Properties
* YAML

```
spring.ldap.embedded.base-dn=dc=spring,dc=io
```

```
spring:
  ldap:
    embedded:
      base-dn: "dc=spring,dc=io"
```

|  |  |
| --- | --- |
|  | It is possible to define multiple base-dn values, however, since distinguished names usually contain commas, they must be defined using the correct notation.  In yaml files, you can use the yaml list notation. In properties files, you must include the index as part of the property name:  * Properties * YAML  ``` spring.ldap.embedded.base-dn[0]=dc=spring,dc=io spring.ldap.embedded.base-dn[1]=dc=vmware,dc=com ```  ``` spring.ldap.embedded.base-dn: - "dc=spring,dc=io" - "dc=vmware,dc=com" ``` |

By default, the server starts on a random port and triggers the regular LDAP support.
There is no need to specify a `spring.ldap.urls` property.

If there is a `schema.ldif` file on your classpath, it is used to initialize the server.
If you want to load the initialization script from a different resource, you can also use the `spring.ldap.embedded.ldif` property.

By default, a standard schema is used to validate `LDIF` files.
You can turn off validation altogether by setting the `spring.ldap.embedded.validation.enabled` property.
If you have custom attributes, you can use `spring.ldap.embedded.validation.schema` to define your custom attribute types or object classes.

#### SSL

The in-memory LDAP server supports SSL (LDAPS).
To enable SSL, configure the [SSL bundle](../features/ssl.html) to use by setting the `spring.ldap.embedded.ssl.bundle` property, as shown in the following example:

* Properties
* YAML

```
spring.ldap.embedded.ssl.bundle=example
```

```
spring:
  ldap:
    embedded:
      ssl:
        bundle: "example"
```