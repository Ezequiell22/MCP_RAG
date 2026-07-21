Search

# Caching

The Spring Framework provides support for transparently adding caching to an application.
At its core, the abstraction applies caching to methods, thus reducing the number of executions based on the information available in the cache.
The caching logic is applied transparently, without any interference to the invoker.
For more details, check the [relevant section](https://docs.spring.io/spring-framework/reference/7.0/integration/cache.html) of the Spring Framework reference documentation.

Spring Boot auto-configures the cache infrastructure as long as caching support is enabled by using the [`@EnableCaching`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/annotation/EnableCaching.html) annotation.

|  |  |
| --- | --- |
|  | Avoid adding [`@EnableCaching`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/annotation/EnableCaching.html) to the main method’s application class. Doing so makes caching a mandatory feature, including [when running a test suite](#io.caching.testing). |

To add caching to an operation of your service add the relevant annotation to its method, as shown in the following example:

* Java
* Kotlin

```
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Component;

@Component
public class MyMathService {

	@Cacheable("piDecimals")
	public int computePiDecimal(int precision) {
		...
	}

}
```

```
import org.springframework.cache.annotation.Cacheable
import org.springframework.stereotype.Component

@Component
class MyMathService {

	@Cacheable("piDecimals")
	fun computePiDecimal(precision: Int): Int {
		...
	}

}
```

This example demonstrates the use of caching on a potentially costly operation.
Before invoking `computePiDecimal`, the abstraction looks for an entry in the `piDecimals` cache that matches the `precision` argument.
If an entry is found, the content in the cache is immediately returned to the caller, and the method is not invoked.
Otherwise, the method is invoked, and the cache is updated before returning the value.

|  |  |
| --- | --- |
|  | You can also use the standard JSR-107 (JCache) annotations (such as [`@CacheResult`](https://javadoc.io/doc/javax.cache/cache-api/1.1.1/javax/cache/annotation/CacheResult.html)) transparently. However, we strongly advise you to not mix and match the Spring Cache and JCache annotations. |

If you do not add any specific cache library, Spring Boot auto-configures a [simple provider](#io.caching.provider.simple) that uses concurrent maps in memory.
When a cache is required (such as `piDecimals` in the preceding example), this provider creates it for you.
The simple provider is not really recommended for production usage, but it is great for getting started and making sure that you understand the features.
When you have made up your mind about the cache provider to use, please make sure to read its documentation to figure out how to configure the caches that your application uses.
Nearly all providers require you to explicitly configure every cache that you use in the application.
Some offer a way to customize the default caches defined by the `spring.cache.cache-names` property.

|  |  |
| --- | --- |
|  | It is also possible to transparently [update](https://docs.spring.io/spring-framework/reference/7.0/integration/cache/annotations.html#cache-annotations-put) or [evict](https://docs.spring.io/spring-framework/reference/7.0/integration/cache/annotations.html#cache-annotations-evict) data from the cache. |

## Supported Cache Providers

The cache abstraction does not provide an actual store and relies on abstraction materialized by the [`Cache`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/Cache.html) and [`CacheManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/CacheManager.html) interfaces.

If you have not defined a bean of type [`CacheManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/CacheManager.html) or a [`CacheResolver`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/interceptor/CacheResolver.html) named `cacheResolver` (see [`CachingConfigurer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/annotation/CachingConfigurer.html)), Spring Boot tries to detect the following providers (in the indicated order):

1. [Generic](#io.caching.provider.generic)
2. [JCache (JSR-107)](#io.caching.provider.jcache) (EhCache 3, Hazelcast, Infinispan, and others)
3. [Hazelcast](#io.caching.provider.hazelcast)
4. [Infinispan](#io.caching.provider.infinispan)
5. [Couchbase](#io.caching.provider.couchbase)
6. [Redis](#io.caching.provider.redis)
7. [Caffeine](#io.caching.provider.caffeine)
8. [Cache2k](#io.caching.provider.cache2k)
9. [Simple](#io.caching.provider.simple)

|  |  |
| --- | --- |
|  | If the [`CacheManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/CacheManager.html) is auto-configured by Spring Boot, it is possible to *force* a particular cache provider by setting the `spring.cache.type` property. |

|  |  |
| --- | --- |
|  | Use the `spring-boot-starter-cache` starter to quickly add basic caching dependencies. The starter brings in `spring-context-support`. If you add dependencies manually, you must include `spring-context-support` in order to use the JCache or Caffeine support. |

If the [`CacheManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/CacheManager.html) is auto-configured by Spring Boot, you can further tune its configuration before it is fully initialized by exposing a bean that implements the [`CacheManagerCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/cache/autoconfigure/CacheManagerCustomizer.html) interface.
The following example sets a flag to say that `null` values should not be passed down to the underlying map:

* Java
* Kotlin

```
import org.springframework.boot.cache.autoconfigure.CacheManagerCustomizer;
import org.springframework.cache.concurrent.ConcurrentMapCacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration(proxyBeanMethods = false)
public class MyCacheManagerConfiguration {

	@Bean
	public CacheManagerCustomizer<ConcurrentMapCacheManager> cacheManagerCustomizer() {
		return (cacheManager) -> cacheManager.setAllowNullValues(false);
	}

}
```

```
import org.springframework.boot.cache.autoconfigure.CacheManagerCustomizer
import org.springframework.cache.concurrent.ConcurrentMapCacheManager
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration

@Configuration(proxyBeanMethods = false)
class MyCacheManagerConfiguration {

	@Bean
	fun cacheManagerCustomizer(): CacheManagerCustomizer<ConcurrentMapCacheManager> {
		return CacheManagerCustomizer { cacheManager ->
			cacheManager.isAllowNullValues = false
		}
	}

}
```

|  |  |
| --- | --- |
|  | In the preceding example, an auto-configured [`ConcurrentMapCacheManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/concurrent/ConcurrentMapCacheManager.html) is expected. If that is not the case (either you provided your own config or a different cache provider was auto-configured), the customizer is not invoked at all. You can have as many customizers as you want, and you can also order them by using [`@Order`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/annotation/Order.html) or [`Ordered`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/Ordered.html). |

### Generic

Generic caching is used if the context defines *at least* one [`Cache`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/Cache.html) bean.
A [`CacheManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/CacheManager.html) wrapping all beans of that type is created.

### JCache (JSR-107)

[JCache](https://jcp.org/en/jsr/detail?id=107) is bootstrapped through the presence of a [`CachingProvider`](https://javadoc.io/doc/javax.cache/cache-api/1.1.1/javax/cache/spi/CachingProvider.html) on the classpath (that is, a JSR-107 compliant caching library exists on the classpath), and the [`JCacheCacheManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/jcache/JCacheCacheManager.html) is provided by the `spring-boot-starter-cache` starter.
Various compliant libraries are available, and Spring Boot provides dependency management for Ehcache 3, Hazelcast, and Infinispan.
Any other compliant library can be added as well.

It might happen that more than one provider is present, in which case the provider must be explicitly specified.
Even if the JSR-107 standard does not enforce a standardized way to define the location of the configuration file, Spring Boot does its best to accommodate setting a cache with implementation details, as shown in the following example:

* Properties
* YAML

```
spring.cache.jcache.provider=com.example.MyCachingProvider
spring.cache.jcache.config=classpath:example.xml
```

```
# Only necessary if more than one provider is present
spring:
  cache:
    jcache:
      provider: "com.example.MyCachingProvider"
      config: "classpath:example.xml"
```

|  |  |
| --- | --- |
|  | When a cache library offers both a native implementation and JSR-107 support, Spring Boot prefers the JSR-107 support, so that the same features are available if you switch to a different JSR-107 implementation. |

|  |  |
| --- | --- |
|  | Spring Boot has [general support for Hazelcast](hazelcast.html). If a single [`HazelcastInstance`](https://docs.hazelcast.org/docs/5.5.0/javadoc/com/hazelcast/core/HazelcastInstance.html) is available, it is automatically reused for the [`CacheManager`](https://javadoc.io/doc/javax.cache/cache-api/1.1.1/javax/cache/CacheManager.html) as well, unless the `spring.cache.jcache.config` property is specified. |

There are two ways to customize the underlying [`CacheManager`](https://javadoc.io/doc/javax.cache/cache-api/1.1.1/javax/cache/CacheManager.html):

* Caches can be created on startup by setting the `spring.cache.cache-names` property.
  If a custom [`Configuration`](https://javadoc.io/doc/javax.cache/cache-api/1.1.1/javax/cache/configuration/Configuration.html) bean is defined, it is used to customize them.
* [`CacheManagerCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/cache/autoconfigure/CacheManagerCustomizer.html) beans are invoked with the reference of the [`CacheManager`](https://javadoc.io/doc/javax.cache/cache-api/1.1.1/javax/cache/CacheManager.html) for full customization.

|  |  |
| --- | --- |
|  | If a standard [`CacheManager`](https://javadoc.io/doc/javax.cache/cache-api/1.1.1/javax/cache/CacheManager.html) bean is defined, it is wrapped automatically in an [`CacheManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/CacheManager.html) implementation that the abstraction expects. No further customization is applied to it. |

### Hazelcast

Spring Boot has [general support for Hazelcast](hazelcast.html).
If a [`HazelcastInstance`](https://docs.hazelcast.org/docs/5.5.0/javadoc/com/hazelcast/core/HazelcastInstance.html) has been auto-configured and `com.hazelcast:hazelcast-spring` is on the classpath, it is automatically wrapped in a [`CacheManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/CacheManager.html).

|  |  |
| --- | --- |
|  | Hazelcast can be used as a JCache compliant cache or as a Spring [`CacheManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/CacheManager.html) compliant cache. When setting `spring.cache.type` to `hazelcast`, Spring Boot will use the [`CacheManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/CacheManager.html) based implementation. If you want to use Hazelcast as a JCache compliant cache, set `spring.cache.type` to `jcache`. If you have multiple JCache compliant cache providers and want to force the use of Hazelcast, you have to [explicitly set the JCache provider](#io.caching.provider.jcache). |

### Infinispan

[Infinispan](https://infinispan.org/) has no default configuration file location, so it must be specified explicitly.
Otherwise, the default bootstrap is used.

* Properties
* YAML

```
spring.cache.infinispan.config=infinispan.xml
```

```
spring:
  cache:
    infinispan:
      config: "infinispan.xml"
```

Caches can be created on startup by setting the `spring.cache.cache-names` property.
If a custom [`ConfigurationBuilder`](https://docs.jboss.org/infinispan/16.1/apidocs/org/infinispan/configuration/cache/ConfigurationBuilder.html) bean is defined, it is used to customize the caches.

For more details, see [the documentation](https://infinispan.org/docs/stable/titles/spring/spring.html).

### Couchbase

If Spring Data Couchbase is available and Couchbase is [configured](../data/nosql.html#data.nosql.couchbase), a [`CouchbaseCacheManager`](https://docs.spring.io/spring-data/couchbase/docs/6.1.x/api/org/springframework/data/couchbase/cache/CouchbaseCacheManager.html) is auto-configured.
It is possible to create additional caches on startup by setting the `spring.cache.cache-names` property and cache defaults can be configured by using `spring.cache.couchbase.*` properties.
For instance, the following configuration creates `cache1` and `cache2` caches with an entry *expiration* of 10 minutes:

* Properties
* YAML

```
spring.cache.cache-names=cache1,cache2
spring.cache.couchbase.expiration=10m
```

```
spring:
  cache:
    cache-names: "cache1,cache2"
    couchbase:
      expiration: "10m"
```

If you need more control over the configuration, consider registering a [`CouchbaseCacheManagerBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/cache/autoconfigure/CouchbaseCacheManagerBuilderCustomizer.html) bean.
The following example shows a customizer that configures a specific entry expiration for `cache1` and `cache2`:

* Java
* Kotlin

```
import java.time.Duration;

import org.springframework.boot.cache.autoconfigure.CouchbaseCacheManagerBuilderCustomizer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.couchbase.cache.CouchbaseCacheConfiguration;

@Configuration(proxyBeanMethods = false)
public class MyCouchbaseCacheManagerConfiguration {

	@Bean
	public CouchbaseCacheManagerBuilderCustomizer myCouchbaseCacheManagerBuilderCustomizer() {
		return (builder) -> builder
				.withCacheConfiguration("cache1", CouchbaseCacheConfiguration
						.defaultCacheConfig().entryExpiry(Duration.ofSeconds(10)))
				.withCacheConfiguration("cache2", CouchbaseCacheConfiguration
						.defaultCacheConfig().entryExpiry(Duration.ofMinutes(1)));

	}

}
```

```
import org.springframework.boot.cache.autoconfigure.CouchbaseCacheManagerBuilderCustomizer
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.data.couchbase.cache.CouchbaseCacheConfiguration
import java.time.Duration

@Configuration(proxyBeanMethods = false)
class MyCouchbaseCacheManagerConfiguration {

	@Bean
	fun myCouchbaseCacheManagerBuilderCustomizer(): CouchbaseCacheManagerBuilderCustomizer {
		return CouchbaseCacheManagerBuilderCustomizer { builder ->
			builder
				.withCacheConfiguration(
					"cache1", CouchbaseCacheConfiguration
						.defaultCacheConfig().entryExpiry(Duration.ofSeconds(10))
				)
				.withCacheConfiguration(
					"cache2", CouchbaseCacheConfiguration
						.defaultCacheConfig().entryExpiry(Duration.ofMinutes(1))
				)
		}
	}

}
```

### Redis

If [Redis](https://redis.io/) is available and configured, a [`RedisCacheManager`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/cache/RedisCacheManager.html) is auto-configured.
It is possible to create additional caches on startup by setting the `spring.cache.cache-names` property and cache defaults can be configured by using `spring.cache.redis.*` properties.
For instance, the following configuration creates `cache1` and `cache2` caches with a *time to live* of 10 minutes:

* Properties
* YAML

```
spring.cache.cache-names=cache1,cache2
spring.cache.redis.time-to-live=10m
```

```
spring:
  cache:
    cache-names: "cache1,cache2"
    redis:
      time-to-live: "10m"
```

|  |  |
| --- | --- |
|  | By default, a key prefix is added so that, if two separate caches use the same key, Redis does not have overlapping keys and cannot return invalid values. We strongly recommend keeping this setting enabled if you create your own [`RedisCacheManager`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/cache/RedisCacheManager.html). |

|  |  |
| --- | --- |
|  | You can take full control of the default configuration by adding a [`RedisCacheConfiguration`](https://docs.spring.io/spring-data/redis/docs/4.1.x/api/org/springframework/data/redis/cache/RedisCacheConfiguration.html) [`@Bean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Bean.html) of your own. This can be useful if you need to customize the default serialization strategy. |

If you need more control over the configuration, consider registering a [`RedisCacheManagerBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/cache/autoconfigure/RedisCacheManagerBuilderCustomizer.html) bean.
The following example shows a customizer that configures a specific time to live for `cache1` and `cache2`:

* Java
* Kotlin

```
import java.time.Duration;

import org.springframework.boot.cache.autoconfigure.RedisCacheManagerBuilderCustomizer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.cache.RedisCacheConfiguration;

@Configuration(proxyBeanMethods = false)
public class MyRedisCacheManagerConfiguration {

	@Bean
	public RedisCacheManagerBuilderCustomizer myRedisCacheManagerBuilderCustomizer() {
		return (builder) -> builder
				.withCacheConfiguration("cache1", RedisCacheConfiguration
						.defaultCacheConfig().entryTtl(Duration.ofSeconds(10)))
				.withCacheConfiguration("cache2", RedisCacheConfiguration
						.defaultCacheConfig().entryTtl(Duration.ofMinutes(1)));

	}

}
```

```
import org.springframework.boot.cache.autoconfigure.RedisCacheManagerBuilderCustomizer
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.data.redis.cache.RedisCacheConfiguration
import java.time.Duration

@Configuration(proxyBeanMethods = false)
class MyRedisCacheManagerConfiguration {

	@Bean
	fun myRedisCacheManagerBuilderCustomizer(): RedisCacheManagerBuilderCustomizer {
		return RedisCacheManagerBuilderCustomizer { builder ->
			builder
				.withCacheConfiguration(
					"cache1", RedisCacheConfiguration
						.defaultCacheConfig().entryTtl(Duration.ofSeconds(10))
				)
				.withCacheConfiguration(
					"cache2", RedisCacheConfiguration
						.defaultCacheConfig().entryTtl(Duration.ofMinutes(1))
				)
		}
	}

}
```

### Caffeine

[Caffeine](https://github.com/ben-manes/caffeine) is a Java 8 rewrite of Guava’s cache that supersedes support for Guava.
If Caffeine is present, a [`CaffeineCacheManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/caffeine/CaffeineCacheManager.html) (provided by the `spring-boot-starter-cache` starter) is auto-configured.
Caches can be created on startup by setting the `spring.cache.cache-names` property and can be customized by one of the following (in the indicated order):

1. A cache spec defined by `spring.cache.caffeine.spec`
2. A [`CaffeineSpec`](https://javadoc.io/doc/com.github.ben-manes.caffeine/caffeine/3.2.4/com/github/benmanes/caffeine/cache/CaffeineSpec.html) bean is defined
3. A [`Caffeine`](https://javadoc.io/doc/com.github.ben-manes.caffeine/caffeine/3.2.4/com/github/benmanes/caffeine/cache/Caffeine.html) bean is defined

For instance, the following configuration creates `cache1` and `cache2` caches with a maximum size of 500 and a *time to live* of 10 minutes

* Properties
* YAML

```
spring.cache.cache-names=cache1,cache2
spring.cache.caffeine.spec=maximumSize=500,expireAfterAccess=600s
```

```
spring:
  cache:
    cache-names: "cache1,cache2"
    caffeine:
      spec: "maximumSize=500,expireAfterAccess=600s"
```

If a [`CacheLoader`](https://javadoc.io/doc/com.github.ben-manes.caffeine/caffeine/3.2.4/com/github/benmanes/caffeine/cache/CacheLoader.html) bean is defined, it is automatically associated to the [`CaffeineCacheManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/caffeine/CaffeineCacheManager.html).
Since the [`CacheLoader`](https://javadoc.io/doc/com.github.ben-manes.caffeine/caffeine/3.2.4/com/github/benmanes/caffeine/cache/CacheLoader.html) is going to be associated with *all* caches managed by the cache manager, it must be defined as `CacheLoader<Object, Object>`.
The auto-configuration ignores any other generic type.

### Cache2k

[Cache2k](https://cache2k.org/) is an in-memory cache.
If the Cache2k spring integration is present, a `SpringCache2kCacheManager` is auto-configured.

Caches can be created on startup by setting the `spring.cache.cache-names` property.
Cache defaults can be customized using a [`Cache2kBuilderCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/cache/autoconfigure/Cache2kBuilderCustomizer.html) bean.
The following example shows a customizer that configures the capacity of the cache to 200 entries, with an expiration of 5 minutes:

* Java
* Kotlin

```
import java.util.concurrent.TimeUnit;

import org.springframework.boot.cache.autoconfigure.Cache2kBuilderCustomizer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration(proxyBeanMethods = false)
public class MyCache2kDefaultsConfiguration {

	@Bean
	public Cache2kBuilderCustomizer myCache2kDefaultsCustomizer() {
		return (builder) -> builder.entryCapacity(200)
				.expireAfterWrite(5, TimeUnit.MINUTES);
	}

}
```

```
import org.springframework.boot.cache.autoconfigure.Cache2kBuilderCustomizer
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import java.util.concurrent.TimeUnit

@Configuration(proxyBeanMethods = false)
class MyCache2kDefaultsConfiguration {

	@Bean
	fun myCache2kDefaultsCustomizer(): Cache2kBuilderCustomizer {
		return Cache2kBuilderCustomizer { builder ->
			builder.entryCapacity(200)
				.expireAfterWrite(5, TimeUnit.MINUTES)
		}
	}
}
```

### Simple

If none of the other providers can be found, a simple implementation using a [`ConcurrentHashMap`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/ConcurrentHashMap.html) as the cache store is configured.
This is the default if no caching library is present in your application.
By default, caches are created as needed, but you can restrict the list of available caches by setting the `cache-names` property.
For instance, if you want only `cache1` and `cache2` caches, set the `cache-names` property as follows:

* Properties
* YAML

```
spring.cache.cache-names=cache1,cache2
```

```
spring:
  cache:
    cache-names: "cache1,cache2"
```

If you do so and your application uses a cache not listed, then it fails at runtime when the cache is needed, but not on startup.
This is similar to the way the "real" cache providers behave if you use an undeclared cache.

### None

If you need to use a no-op cache rather than the auto-configured cache manager in a certain environment, set the cache type to `none`, as shown in the following example:

* Properties
* YAML

```
spring.cache.type=none
```

```
spring:
  cache:
    type: "none"
```

## Testing

It is generally useful to use a no-op implementation when running a test suite.
This section lists a number of strategies that are useful for tests.

When a custom [`CacheManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/CacheManager.html) is defined, the best option is to make sure that caching configuration is defined in an isolated [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) class.
Doing so makes sure that caching is not required by slice tests.
For tests that enable a full context, such as [`@SpringBootTest`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/context/SpringBootTest.html), an explicit configuration overriding the regular configuration is required.

If caching is auto-configured, more options are available.
Tests can be annotated with [`@AutoConfigureCache`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/test/autoconfigure/core/AutoConfigureCache.html) to replace the auto-configured [`CacheManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/CacheManager.html) by a no-op implementation.

* Java
* Kotlin

```
import org.springframework.boot.cache.test.autoconfigure.AutoConfigureCache;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
@AutoConfigureCache
public class MyIntegrationTests {

	// Tests use a no-op cache manager

}
```

```
import org.springframework.boot.cache.test.autoconfigure.AutoConfigureCache
import org.springframework.boot.test.context.SpringBootTest

@SpringBootTest
@AutoConfigureCache
class MyIntegrationTests {

	// Tests use a no-op cache manager

}
```

Another option is to force a no-op implementation for the auto-configured [`CacheManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/cache/CacheManager.html):

* Properties
* YAML

```
spring.cache.type=none
```

```
spring:
  cache:
    type: "none"
```