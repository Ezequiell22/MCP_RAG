Search

# Spring Batch

Spring Boot offers several conveniences for working with [Spring Batch](https://spring.io/projects/spring-batch), including running a Job on startup.

When building a batch application, the following stores can be auto-configured:

* In-memory
* JDBC
* MongoDB

Each store has specific additional settings.
For instance, it is possible to customize the tables prefix for the JDBC store, as shown in the following example:

* Properties
* YAML

```
spring.batch.jdbc.table-prefix=CUSTOM_
```

```
spring:
  batch:
    jdbc:
      table-prefix: "CUSTOM_"
```

When using the MongoDB store, you can enable initialization of the Spring Batch job repository schema (collections and indexes):

* Properties
* YAML

```
spring.batch.data.mongodb.schema.initialize=true
```

```
spring:
  batch:
    data:
      mongodb:
        schema:
          initialize: true
```

To disable Spring Boot’s auto-configuration and take complete control of Spring Batch’s configuration, add [`@EnableBatchProcessing`](https://docs.spring.io/spring-batch/docs/6.0.x/api/org/springframework/batch/core/configuration/annotation/EnableBatchProcessing.html) to one of your [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) classes or extend [`DefaultBatchConfiguration`](https://docs.spring.io/spring-batch/docs/6.0.x/api/org/springframework/batch/core/configuration/support/DefaultBatchConfiguration.html).
This will cause the auto-configuration to back off, including initialization of Spring Batch’s database schema (JDBC or MongoDB).
Spring Batch can then be configured using the `@Enable*JobRepository` annotation’s attributes rather than the previously described configuration properties.

To learn more about manually configuring Spring Batch, see the API documentation of:

* [`DefaultBatchConfiguration`](https://docs.spring.io/spring-batch/docs/6.0.x/api/org/springframework/batch/core/configuration/support/DefaultBatchConfiguration.html)
* [`@EnableBatchProcessing`](https://docs.spring.io/spring-batch/docs/6.0.x/api/org/springframework/batch/core/configuration/annotation/EnableBatchProcessing.html)
* [`@EnableJdbcJobRepository`](https://docs.spring.io/spring-batch/docs/6.0.x/api/org/springframework/batch/core/configuration/annotation/EnableJdbcJobRepository.html)
* [`@EnableMongoJobRepository`](https://docs.spring.io/spring-batch/docs/6.0.x/api/org/springframework/batch/core/configuration/annotation/EnableMongoJobRepository.html)

For more information about Spring Batch, see the [Spring Batch project page](https://spring.io/projects/spring-batch).

## Running Spring Batch Jobs on Startup

When Spring Boot auto-configures Spring Batch, and if a single [`Job`](https://docs.spring.io/spring-batch/docs/6.0.x/api/org/springframework/batch/core/job/Job.html) bean is found in the application context, it is executed on startup (see [`JobLauncherApplicationRunner`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/batch/autoconfigure/JobLauncherApplicationRunner.html) for details).
If multiple [`Job`](https://docs.spring.io/spring-batch/docs/6.0.x/api/org/springframework/batch/core/job/Job.html) beans are found, the job that should be executed must be specified using `spring.batch.job.name`.

You can disable running a [`Job`](https://docs.spring.io/spring-batch/docs/6.0.x/api/org/springframework/batch/core/job/Job.html) found in the application context, as shown in the following example:

* Properties
* YAML

```
spring.batch.job.enabled=false
```

```
spring:
  batch:
    job:
      enabled: false
```

See [`BatchAutoConfiguration`](https://github.com/spring-projects/spring-boot/tree/v4.1.0/module/spring-boot-batch/src/main/java/org/springframework/boot/batch/autoconfigure/BatchAutoConfiguration.java), [`BatchJdbcAutoConfiguration`](https://github.com/spring-projects/spring-boot/tree/v4.1.0/module/spring-boot-batch-jdbc/src/main/java/org/springframework/boot/batch/jdbc/autoconfigure/BatchJdbcAutoConfiguration.java), and [`BatchDataMongoAutoConfiguration`](https://github.com/spring-projects/spring-boot/tree/v4.1.0/module/spring-boot-batch-data-mongodb/src/main/java/org/springframework/boot/batch/mongodb/autoconfigure/BatchDataMongoAutoConfiguration.java) for more details.