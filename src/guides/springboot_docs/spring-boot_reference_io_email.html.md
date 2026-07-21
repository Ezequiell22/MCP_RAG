Search

# Sending Email

The Spring Framework provides an abstraction for sending email by using the [`JavaMailSender`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/mail/javamail/JavaMailSender.html) interface, and Spring Boot provides auto-configuration for it as well as a starter module.

|  |  |
| --- | --- |
|  | See the [reference documentation](https://docs.spring.io/spring-framework/reference/7.0/integration/email.html) for a detailed explanation of how you can use [`JavaMailSender`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/mail/javamail/JavaMailSender.html). |

If `spring.mail.host` and the relevant libraries (as defined by `spring-boot-starter-mail`) are available, a default [`JavaMailSender`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/mail/javamail/JavaMailSender.html) is created if none exists.
The sender can be further customized by configuration items from the `spring.mail` namespace.
See [`MailProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/mail/autoconfigure/MailProperties.html) for more details.

In particular, certain default timeout values are infinite, and you may want to change that to avoid having a thread blocked by an unresponsive mail server, as shown in the following example:

* Properties
* YAML

```
spring.mail.properties[mail.smtp.connectiontimeout]=5000
spring.mail.properties[mail.smtp.timeout]=3000
spring.mail.properties[mail.smtp.writetimeout]=5000
```

```
spring:
  mail:
    properties:
      "[mail.smtp.connectiontimeout]": 5000
      "[mail.smtp.timeout]": 3000
      "[mail.smtp.writetimeout]": 5000
```

It is also possible to configure a [`JavaMailSender`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/mail/javamail/JavaMailSender.html) with an existing [`Session`](https://jakarta.ee/specifications/mail/2.1/apidocs/jakarta/mail/Session.html) from JNDI:

* Properties
* YAML

```
spring.mail.jndi-name=mail/Session
```

```
spring:
  mail:
    jndi-name: "mail/Session"
```

When a `jndi-name` is set, it takes precedence over all other Session-related settings.