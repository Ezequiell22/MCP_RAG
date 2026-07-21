Search

# Quartz Scheduler

Spring Boot offers several conveniences for working with the [Quartz scheduler](https://www.quartz-scheduler.org/), including the `spring-boot-starter-quartz` starter.
If Quartz is available, a [`Scheduler`](https://javadoc.io/doc/org.quartz-scheduler/quartz/2.5.2/org/quartz/Scheduler.html) is auto-configured (through the [`SchedulerFactoryBean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/quartz/SchedulerFactoryBean.html) abstraction).

Beans of the following types are automatically picked up and associated with the [`Scheduler`](https://javadoc.io/doc/org.quartz-scheduler/quartz/2.5.2/org/quartz/Scheduler.html):

* [`JobDetail`](https://javadoc.io/doc/org.quartz-scheduler/quartz/2.5.2/org/quartz/JobDetail.html): defines a particular Job.
  [`JobDetail`](https://javadoc.io/doc/org.quartz-scheduler/quartz/2.5.2/org/quartz/JobDetail.html) instances can be built with the [`JobBuilder`](https://javadoc.io/doc/org.quartz-scheduler/quartz/2.5.2/org/quartz/JobBuilder.html) API.
* [`Calendar`](https://javadoc.io/doc/org.quartz-scheduler/quartz/2.5.2/org/quartz/Calendar.html).
* [`Trigger`](https://javadoc.io/doc/org.quartz-scheduler/quartz/2.5.2/org/quartz/Trigger.html): defines when a particular job is triggered.

By default, an in-memory [`JobStore`](https://javadoc.io/doc/org.quartz-scheduler/quartz/2.5.2/org/quartz/spi/JobStore.html) is used.
However, it is possible to configure a JDBC-based store if a [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html) bean is available in your application and if the `spring.quartz.job-store-type` property is configured accordingly, as shown in the following example:

* Properties
* YAML

```
spring.quartz.job-store-type=jdbc
```

```
spring:
  quartz:
    job-store-type: "jdbc"
```

When the JDBC store is used, the schema can be initialized on startup, as shown in the following example:

* Properties
* YAML

```
spring.quartz.jdbc.initialize-schema=always
```

```
spring:
  quartz:
    jdbc:
      initialize-schema: "always"
```

|  |  |
| --- | --- |
|  | By default, the database is detected and initialized by using the standard scripts provided with the Quartz library. These scripts drop existing tables, deleting all triggers on every restart. To use a custom script, set the `spring.quartz.jdbc.schema` property. Some of the standard scripts â such as those for SQL Server, Azure SQL, and Sybase â cannot be used without modification. In these cases, make a copy of the script and edit it as directed in the script’s comments then set `spring.quartz.jdbc.schema` to use your customized script. |

To have Quartz use a [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html) other than the application’s main [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html), declare a [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html) bean, annotating its [`@Bean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Bean.html) method with [`@QuartzDataSource`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/quartz/autoconfigure/QuartzDataSource.html).
Doing so ensures that the Quartz-specific [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html) is used by both the [`SchedulerFactoryBean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/quartz/SchedulerFactoryBean.html) and for schema initialization.
Similarly, to have Quartz use a [`TransactionManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/transaction/TransactionManager.html) other than the application’s main [`TransactionManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/transaction/TransactionManager.html) declare a [`TransactionManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/transaction/TransactionManager.html) bean, annotating its [`@Bean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Bean.html) method with [`@QuartzTransactionManager`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/quartz/autoconfigure/QuartzTransactionManager.html).

By default, jobs created by configuration will not overwrite already registered jobs that have been read from a persistent job store.
To enable overwriting existing job definitions set the `spring.quartz.overwrite-existing-jobs` property.

Quartz Scheduler configuration can be customized using `spring.quartz` properties and [`SchedulerFactoryBeanCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/quartz/autoconfigure/SchedulerFactoryBeanCustomizer.html) beans, which allow programmatic [`SchedulerFactoryBean`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/scheduling/quartz/SchedulerFactoryBean.html) customization.
Advanced Quartz configuration properties can be customized using `spring.quartz.properties.*`.

|  |  |
| --- | --- |
|  | In particular, an [`Executor`](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/Executor.html) bean is not associated with the scheduler as Quartz offers a way to configure the scheduler through `spring.quartz.properties`. If you need to customize the task executor, consider implementing [`SchedulerFactoryBeanCustomizer`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/quartz/autoconfigure/SchedulerFactoryBeanCustomizer.html). |

Jobs can define setters to inject data map properties.
Regular beans can also be injected in a similar manner, as shown in the following example:

* Java
* Kotlin

```
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;

import org.springframework.scheduling.quartz.QuartzJobBean;

public class MySampleJob extends QuartzJobBean {

	// fields ...

	private MyService myService;

	private String name;

	// Inject "MyService" bean
	public void setMyService(MyService myService) {
		this.myService = myService;
	}

	// Inject the "name" job data property
	public void setName(String name) {
		this.name = name;
	}

	@Override
	protected void executeInternal(JobExecutionContext context) throws JobExecutionException {
		this.myService.someMethod(context.getFireTime(), this.name);
	}

}
```

```
import org.quartz.JobExecutionContext
import org.springframework.scheduling.quartz.QuartzJobBean

class MySampleJob : QuartzJobBean() {

	// fields ...

	private var myService: MyService? = null

	private var name: String? = null

	// Inject "MyService" bean
	fun setMyService(myService: MyService?) {
		this.myService = myService
	}

	// Inject the "name" job data property
	fun setName(name: String?) {
		this.name = name
	}

	override fun executeInternal(context: JobExecutionContext) {
		myService!!.someMethod(context.fireTime, name)
	}

}
```