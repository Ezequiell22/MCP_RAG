Search

# Task Execution and Scheduling

In the absence of an [`Executor`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/Executor.html) bean in the context, Spring Boot auto-configures an [`AsyncTaskExecutor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/task/AsyncTaskExecutor.html).
When virtual threads are enabled (using Java 21+ and `spring.threads.virtual.enabled` set to `true`) this will be a [`SimpleAsyncTaskExecutor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/task/SimpleAsyncTaskExecutor.html) that uses virtual threads.
Otherwise, it will be a [`ThreadPoolTaskExecutor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/concurrent/ThreadPoolTaskExecutor.html) with sensible defaults.

The auto-configured [`AsyncTaskExecutor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/task/AsyncTaskExecutor.html) is used for the following integrations unless a custom [`Executor`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/Executor.html) bean is defined:

* Execution of asynchronous tasks using [`@EnableAsync`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/annotation/EnableAsync.html), unless a bean of type [`AsyncConfigurer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/annotation/AsyncConfigurer.html) is defined.
* Asynchronous handling of [`Callable`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/Callable.html) return values from controller methods in Spring for GraphQL.
* Asynchronous request handling in Spring MVC.
* Support for blocking execution in Spring WebFlux.
* Utilized for inbound and outbound message channels in Spring WebSocket.
* Bootstrap executor for JPA, based on the bootstrap mode of JPA repositories.
* Bootstrap executor for [background initialization](https://docs.spring.io/spring-framework/reference/7.0/core/beans/java/composing-configuration-classes.html#beans-java-startup-background) of beans in the `ApplicationContext`.

While this approach works in most scenarios, Spring Boot allows you to override the auto-configured [`AsyncTaskExecutor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/task/AsyncTaskExecutor.html).
By default, when a custom [`Executor`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/Executor.html) bean is registered, the auto-configured [`AsyncTaskExecutor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/task/AsyncTaskExecutor.html) backs off, and the custom [`Executor`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/Executor.html) is used for regular task execution (via [`@EnableAsync`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/annotation/EnableAsync.html)).

However, Spring MVC, Spring WebFlux, and Spring GraphQL all require a bean named `applicationTaskExecutor`.
For Spring MVC and Spring WebFlux, this bean must be of type [`AsyncTaskExecutor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/task/AsyncTaskExecutor.html), whereas Spring GraphQL does not enforce this type requirement.

Spring WebSocket and JPA will use [`AsyncTaskExecutor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/task/AsyncTaskExecutor.html) if either a single bean of this type is available or a bean named `applicationTaskExecutor` is defined.

Finally, the boostrap executor of the `ApplicationContext` uses a bean named `applicationTaskExecutor` unless a bean named `bootstrapExecutor` is defined.

The following code snippet demonstrates how to register a custom [`AsyncTaskExecutor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/task/AsyncTaskExecutor.html) to be used with Spring MVC, Spring WebFlux, Spring GraphQL, Spring WebSocket, JPA, and background initialization of beans.

* Java
* Kotlin

```
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.task.SimpleAsyncTaskExecutor;

@Configuration(proxyBeanMethods = false)
public class MyTaskExecutorConfiguration {

	@Bean("applicationTaskExecutor")
	SimpleAsyncTaskExecutor applicationTaskExecutor() {
		return new SimpleAsyncTaskExecutor("app-");
	}

}
```

```
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.core.task.SimpleAsyncTaskExecutor

@Configuration(proxyBeanMethods = false)
class MyTaskExecutorConfiguration {

	@Bean("applicationTaskExecutor")
	fun applicationTaskExecutor(): SimpleAsyncTaskExecutor {
		return SimpleAsyncTaskExecutor("app-")
	}

}
```

|  |  |
| --- | --- |
|  | The `applicationTaskExecutor` bean will also be used for regular task execution if there is no [`@Primary`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Primary.html) bean or a bean named `taskExecutor` of type [`Executor`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/Executor.html) or [`AsyncConfigurer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/annotation/AsyncConfigurer.html) present in the application context. |

|  |  |
| --- | --- |
|  | If neither the auto-configured `AsyncTaskExecutor` nor the `applicationTaskExecutor` bean is defined, the application defaults to a bean named `taskExecutor` for regular task execution ([`@EnableAsync`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/annotation/EnableAsync.html)), following Spring Framework’s behavior. However, this bean will not be used for Spring MVC, Spring WebFlux, Spring GraphQL. It could, however, be used for Spring WebSocket or JPA if the bean’s type is [`AsyncTaskExecutor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/task/AsyncTaskExecutor.html). |

If your application needs multiple `Executor` beans for different integrations, such as one for regular task execution with [`@EnableAsync`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/annotation/EnableAsync.html) and other for Spring MVC, Spring WebFlux, Spring WebSocket and JPA, you can configure them as follows.

* Java
* Kotlin

```
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.task.SimpleAsyncTaskExecutor;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@Configuration(proxyBeanMethods = false)
public class MyTaskExecutorConfiguration {

	@Bean("applicationTaskExecutor")
	SimpleAsyncTaskExecutor applicationTaskExecutor() {
		return new SimpleAsyncTaskExecutor("app-");
	}

	@Bean("taskExecutor")
	ThreadPoolTaskExecutor taskExecutor() {
		ThreadPoolTaskExecutor threadPoolTaskExecutor = new ThreadPoolTaskExecutor();
		threadPoolTaskExecutor.setThreadNamePrefix("async-");
		return threadPoolTaskExecutor;
	}

}
```

```
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.core.task.SimpleAsyncTaskExecutor
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor

@Configuration(proxyBeanMethods = false)
class MyTaskExecutorConfiguration {

	@Bean("applicationTaskExecutor")
	fun applicationTaskExecutor(): SimpleAsyncTaskExecutor {
		return SimpleAsyncTaskExecutor("app-")
	}

	@Bean("taskExecutor")
	fun taskExecutor(): ThreadPoolTaskExecutor {
		val threadPoolTaskExecutor = ThreadPoolTaskExecutor()
		threadPoolTaskExecutor.setThreadNamePrefix("async-")
		return threadPoolTaskExecutor
	}

}
```

|  |  |
| --- | --- |
|  | The auto-configured [`ThreadPoolTaskExecutorBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/task/ThreadPoolTaskExecutorBuilder.html) or [`SimpleAsyncTaskExecutorBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/task/SimpleAsyncTaskExecutorBuilder.html) allow you to easily create instances of type [`AsyncTaskExecutor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/task/AsyncTaskExecutor.html) that replicate the default behavior of auto-configuration.  * Java * Kotlin  ``` import org.springframework.boot.task.SimpleAsyncTaskExecutorBuilder; import org.springframework.context.annotation.Bean; import org.springframework.context.annotation.Configuration; import org.springframework.core.task.SimpleAsyncTaskExecutor;  @Configuration(proxyBeanMethods = false) public class MyTaskExecutorConfiguration {  	@Bean 	SimpleAsyncTaskExecutor taskExecutor(SimpleAsyncTaskExecutorBuilder builder) { 		return builder.build(); 	}  } ```  ``` import org.springframework.boot.task.SimpleAsyncTaskExecutorBuilder import org.springframework.context.annotation.Bean import org.springframework.context.annotation.Configuration import org.springframework.core.task.SimpleAsyncTaskExecutor  @Configuration(proxyBeanMethods = false) class MyTaskExecutorConfiguration {  	@Bean 	fun taskExecutor(builder: SimpleAsyncTaskExecutorBuilder): SimpleAsyncTaskExecutor { 		return builder.build() 	}  } ``` |

If a `taskExecutor` named bean is not an option, you can mark your bean as [`@Primary`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Primary.html) or define an [`AsyncConfigurer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/annotation/AsyncConfigurer.html) bean to specify the `Executor` responsible for handling regular task execution with [`@EnableAsync`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/annotation/EnableAsync.html).
The following example demonstrates how to achieve this.

* Java
* Kotlin

```
import java.util.concurrent.Executor;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.AsyncConfigurer;

@Configuration(proxyBeanMethods = false)
public class MyTaskExecutorConfiguration {

	@Bean
	AsyncConfigurer asyncConfigurer(ExecutorService executorService) {
		return new AsyncConfigurer() {

			@Override
			public Executor getAsyncExecutor() {
				return executorService;
			}

		};
	}

	@Bean
	ExecutorService executorService() {
		return Executors.newCachedThreadPool();
	}

}
```

```
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.scheduling.annotation.AsyncConfigurer
import java.util.concurrent.Executor
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors

@Configuration(proxyBeanMethods = false)
class MyTaskExecutorConfiguration {

	@Bean
	fun asyncConfigurer(executorService: ExecutorService): AsyncConfigurer {
		return object : AsyncConfigurer {
			override fun getAsyncExecutor(): Executor {
				return executorService
			}
		}
	}

	@Bean
	fun executorService(): ExecutorService {
		return Executors.newCachedThreadPool()
	}

}
```

To register a custom [`Executor`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/Executor.html) while keeping the auto-configured [`AsyncTaskExecutor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/task/AsyncTaskExecutor.html), you can create a custom [`Executor`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/Executor.html) bean and set the `defaultCandidate=false` attribute in its [`@Bean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Bean.html) annotation, as demonstrated in the following example:

* Java
* Kotlin

```
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration(proxyBeanMethods = false)
public class MyTaskExecutorConfiguration {

	@Bean(defaultCandidate = false)
	@Qualifier("scheduledExecutorService")
	ScheduledExecutorService scheduledExecutorService() {
		return Executors.newSingleThreadScheduledExecutor();
	}

}
```

```
import org.springframework.beans.factory.annotation.Qualifier
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import java.util.concurrent.Executors
import java.util.concurrent.ScheduledExecutorService

@Configuration(proxyBeanMethods = false)
class MyTaskExecutorConfiguration {

	@Bean(defaultCandidate = false)
	@Qualifier("scheduledExecutorService")
	fun scheduledExecutorService(): ScheduledExecutorService {
		return Executors.newSingleThreadScheduledExecutor()
	}

}
```

In that case, you will be able to autowire your custom [`Executor`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/Executor.html) into other components while retaining the auto-configured [`AsyncTaskExecutor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/task/AsyncTaskExecutor.html).
However, remember to use the [`@Qualifier`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/beans/factory/annotation/Qualifier.html) annotation alongside [`@Autowired`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/beans/factory/annotation/Autowired.html).

If this is not possible for you, you can request Spring Boot to auto-configure an [`AsyncTaskExecutor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/task/AsyncTaskExecutor.html) anyway, as follows:

* Properties
* YAML

```
spring.task.execution.mode=force
```

```
spring:
  task:
    execution:
      mode: force
```

The auto-configured [`AsyncTaskExecutor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/task/AsyncTaskExecutor.html) will be used automatically for all integrations, even if a custom [`Executor`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/Executor.html) bean is registered, including those marked as [`@Primary`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Primary.html).
These integrations include:

* Asynchronous task execution ([`@EnableAsync`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/annotation/EnableAsync.html)), unless an [`AsyncConfigurer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/annotation/AsyncConfigurer.html) bean is present.
* Spring for GraphQL’s asynchronous handling of [`Callable`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/Callable.html) return values from controller methods.
* Spring MVC’s asynchronous request processing.
* Spring WebFlux’s blocking execution support.
* Utilized for inbound and outbound message channels in Spring WebSocket.
* Bootstrap executor for JPA, based on the bootstrap mode of JPA repositories.
* Bootstrap executor for [background initialization](https://docs.spring.io/spring-framework/reference/7.0/core/beans/java/composing-configuration-classes.html#beans-java-startup-background) of beans in the `ApplicationContext`, unless a bean named `bootstrapExecutor` is defined.

|  |  |
| --- | --- |
|  | Depending on your target arrangement, you could set `spring.task.execution.mode` to `force` to auto-configure an `applicationTaskExecutor`, change your [`Executor`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/Executor.html) into an [`AsyncTaskExecutor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/task/AsyncTaskExecutor.html) or define both an [`AsyncTaskExecutor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/task/AsyncTaskExecutor.html) and an [`AsyncConfigurer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/annotation/AsyncConfigurer.html) wrapping your custom [`Executor`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/Executor.html). |

|  |  |
| --- | --- |
|  | When `force` mode is enabled, `applicationTaskExecutor` will also be configured for regular task execution with [`@EnableAsync`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/annotation/EnableAsync.html), even if a [`@Primary`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Primary.html) bean or a bean named `taskExecutor` of type [`Executor`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/Executor.html) is present. The only way to override the `Executor` for regular tasks is by registering an [`AsyncConfigurer`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/annotation/AsyncConfigurer.html) bean. |

When a [`ThreadPoolTaskExecutor`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/concurrent/ThreadPoolTaskExecutor.html) is auto-configured, the thread pool uses 8 core threads that can grow and shrink according to the load.
Those default settings can be fine-tuned using the `spring.task.execution` namespace, as shown in the following example:

* Properties
* YAML

```
spring.task.execution.pool.max-size=16
spring.task.execution.pool.queue-capacity=100
spring.task.execution.pool.keep-alive=10s
```

```
spring:
  task:
    execution:
      pool:
        max-size: 16
        queue-capacity: 100
        keep-alive: "10s"
```

This changes the thread pool to use a bounded queue so that when the queue is full (100 tasks), the thread pool increases to maximum 16 threads.
Shrinking of the pool is more aggressive as threads are reclaimed when they are idle for 10 seconds (rather than 60 seconds by default).

A scheduler can also be auto-configured if it needs to be associated with scheduled task execution (using [`@EnableScheduling`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/annotation/EnableScheduling.html) for instance).

If virtual threads are enabled (using Java 21+ and `spring.threads.virtual.enabled` set to `true`) this will be a [`SimpleAsyncTaskScheduler`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/concurrent/SimpleAsyncTaskScheduler.html) that uses virtual threads.
This [`SimpleAsyncTaskScheduler`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/concurrent/SimpleAsyncTaskScheduler.html) will ignore any pooling related properties.

If virtual threads are not enabled, it will be a [`ThreadPoolTaskScheduler`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/concurrent/ThreadPoolTaskScheduler.html) with sensible defaults.
The [`ThreadPoolTaskScheduler`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/concurrent/ThreadPoolTaskScheduler.html) uses one thread by default and its settings can be fine-tuned using the `spring.task.scheduling` namespace, as shown in the following example:

* Properties
* YAML

```
spring.task.scheduling.thread-name-prefix=scheduling-
spring.task.scheduling.pool.size=2
```

```
spring:
  task:
    scheduling:
      thread-name-prefix: "scheduling-"
      pool:
        size: 2
```

A [`ThreadPoolTaskExecutorBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/task/ThreadPoolTaskExecutorBuilder.html) bean, a [`SimpleAsyncTaskExecutorBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/task/SimpleAsyncTaskExecutorBuilder.html) bean, a [`ThreadPoolTaskSchedulerBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/task/ThreadPoolTaskSchedulerBuilder.html) bean and a [`SimpleAsyncTaskSchedulerBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/task/SimpleAsyncTaskSchedulerBuilder.html) are made available in the context if a custom executor or scheduler needs to be created.
The [`SimpleAsyncTaskExecutorBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/task/SimpleAsyncTaskExecutorBuilder.html) and [`SimpleAsyncTaskSchedulerBuilder`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/task/SimpleAsyncTaskSchedulerBuilder.html) beans are auto-configured to use virtual threads if they are enabled (using Java 21+ and `spring.threads.virtual.enabled` set to `true`).