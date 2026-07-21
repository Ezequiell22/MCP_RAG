Search

# Distributed Transactions With JTA

Spring Boot supports distributed JTA transactions across multiple XA resources by using a transaction manager retrieved from JNDI.

When a JTA environment is detected, Spring’s [`JtaTransactionManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/transaction/jta/JtaTransactionManager.html) is used to manage transactions.
Auto-configured JMS, DataSource, and JPA beans are upgraded to support XA transactions.
You can use standard Spring idioms, such as [`@Transactional`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/transaction/annotation/Transactional.html), to participate in a distributed transaction.
If you are within a JTA environment and still want to use local transactions, you can set the `spring.jta.enabled` property to `false` to disable the JTA auto-configuration.

## Using a Jakarta EE Managed Transaction Manager

If you package your Spring Boot application as a `war` or `ear` file and deploy it to a Jakarta EE application server, you can use your application server’s built-in transaction manager.
Spring Boot tries to auto-configure a transaction manager by looking at common JNDI locations (`java:comp/UserTransaction`, `java:comp/TransactionManager`, and so on).
When using a transaction service provided by your application server, you generally also want to ensure that all resources are managed by the server and exposed over JNDI.
Spring Boot tries to auto-configure JMS by looking for a [`ConnectionFactory`](https://jakarta.ee/specifications/messaging/3.1/apidocs/jakarta.messaging/jakarta/jms/ConnectionFactory.html) at the JNDI path (`java:/JmsXA` or `java:/XAConnectionFactory`), and you can use the [`spring.datasource.jndi-name` property](../data/sql.html#data.sql.datasource.jndi) to configure your [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html).

## Mixing XA and Non-XA JMS Connections

When using JTA, the primary JMS [`ConnectionFactory`](https://jakarta.ee/specifications/messaging/3.1/apidocs/jakarta.messaging/jakarta/jms/ConnectionFactory.html) bean is XA-aware and participates in distributed transactions.
You can inject into your bean without needing to use any [`@Qualifier`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/beans/factory/annotation/Qualifier.html):

* Java
* Kotlin

```
import jakarta.jms.ConnectionFactory;

public class MyBean {

	public MyBean(ConnectionFactory connectionFactory) {
		// ...
	}

}
```

```
import jakarta.jms.ConnectionFactory

class MyBean(connectionFactory: ConnectionFactory?)
```

In some situations, you might want to process certain JMS messages by using a non-XA [`ConnectionFactory`](https://jakarta.ee/specifications/messaging/3.1/apidocs/jakarta.messaging/jakarta/jms/ConnectionFactory.html).
For example, your JMS processing logic might take longer than the XA timeout.

If you want to use a non-XA [`ConnectionFactory`](https://jakarta.ee/specifications/messaging/3.1/apidocs/jakarta.messaging/jakarta/jms/ConnectionFactory.html), you can the `nonXaJmsConnectionFactory` bean:

* Java
* Kotlin

```
import jakarta.jms.ConnectionFactory;

import org.springframework.beans.factory.annotation.Qualifier;

public class MyBean {

	public MyBean(@Qualifier("nonXaJmsConnectionFactory") ConnectionFactory connectionFactory) {
		// ...
	}

}
```

```
import jakarta.jms.ConnectionFactory
import org.springframework.beans.factory.annotation.Qualifier

class MyBean(@Qualifier("nonXaJmsConnectionFactory") connectionFactory: ConnectionFactory?)
```

For consistency, the `jmsConnectionFactory` bean is also provided by using the bean alias `xaJmsConnectionFactory`:

* Java
* Kotlin

```
import jakarta.jms.ConnectionFactory;

import org.springframework.beans.factory.annotation.Qualifier;

public class MyBean {

	public MyBean(@Qualifier("xaJmsConnectionFactory") ConnectionFactory connectionFactory) {
		// ...
	}

}
```

```
import jakarta.jms.ConnectionFactory
import org.springframework.beans.factory.annotation.Qualifier

class MyBean(@Qualifier("xaJmsConnectionFactory") connectionFactory: ConnectionFactory?)
```

## Supporting an Embedded Transaction Manager

The [`XAConnectionFactoryWrapper`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jms/XAConnectionFactoryWrapper.html) and [`XADataSourceWrapper`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/jdbc/XADataSourceWrapper.html) interfaces can be used to support embedded transaction managers.
The interfaces are responsible for wrapping [`XAConnectionFactory`](https://jakarta.ee/specifications/messaging/3.1/apidocs/jakarta.messaging/jakarta/jms/XAConnectionFactory.html) and [`XADataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/XADataSource.html) beans and exposing them as regular [`ConnectionFactory`](https://jakarta.ee/specifications/messaging/3.1/apidocs/jakarta.messaging/jakarta/jms/ConnectionFactory.html) and [`DataSource`](https://docs.oracle.com/en/java/javase/17/docs/api/java.sql/javax/sql/DataSource.html) beans, which transparently enroll in the distributed transaction.
DataSource and JMS auto-configuration use JTA variants, provided you have a [`JtaTransactionManager`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/transaction/jta/JtaTransactionManager.html) bean and appropriate XA wrapper beans registered within your [`ApplicationContext`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/ApplicationContext.html).