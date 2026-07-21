Search

# Profiles

Spring Profiles provide a way to segregate parts of your application configuration and make it be available only in certain environments.
Any [`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html), [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) or [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) can be marked with [`@Profile`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Profile.html) to limit when it is loaded, as shown in the following example:

* Java
* Kotlin

```
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

@Configuration(proxyBeanMethods = false)
@Profile("production")
public class ProductionConfiguration {

	// ...

}
```

```
import org.springframework.context.annotation.Configuration
import org.springframework.context.annotation.Profile

@Configuration(proxyBeanMethods = false)
@Profile("production")
class ProductionConfiguration {

	// ...

}
```

|  |  |
| --- | --- |
|  | If [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) beans are registered through [`@EnableConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/EnableConfigurationProperties.html) instead of automatic scanning, the [`@Profile`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Profile.html) annotation needs to be specified on the [`@Configuration`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Configuration.html) class that has the [`@EnableConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/EnableConfigurationProperties.html) annotation. In the case where [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) are scanned, [`@Profile`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/Profile.html) can be specified on the [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) class itself. |

You can use a `spring.profiles.active` [`Environment`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/env/Environment.html) property to specify which profiles are active.
You can specify the property in any of the ways described earlier in this chapter.
For example, you could include it in your `application.properties`, as shown in the following example:

* Properties
* YAML

```
spring.profiles.active=dev,hsqldb
```

```
spring:
  profiles:
    active: "dev,hsqldb"
```

You could also specify it on the command line by using the following switch: `--spring.profiles.active=dev,hsqldb`.

If no profile is active, a default profile is enabled.
The name of the default profile is `default` and it can be tuned using the `spring.profiles.default` [`Environment`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/env/Environment.html) property, as shown in the following example:

* Properties
* YAML

```
spring.profiles.default=none
```

```
spring:
  profiles:
    default: "none"
```

`spring.profiles.active` and `spring.profiles.default` can only be used in non-profile-specific documents.
This means they cannot be included in [profile specific files](external-config.html#features.external-config.files.profile-specific) or [documents activated](external-config.html#features.external-config.files.activation-properties) by `spring.config.activate.on-profile`.

For example, the second document configuration is invalid:

* Properties
* YAML

```
spring.profiles.active=prod
#---
spring.config.activate.on-profile=prod
spring.profiles.active=metrics
```

```
# this document is valid
spring:
  profiles:
    active: "prod"
---
# this document is invalid
spring:
  config:
    activate:
      on-profile: "prod"
  profiles:
    active: "metrics"
```

The `spring.profiles.active` property follows the same ordering rules as other properties.
The highest [`PropertySource`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/env/PropertySource.html) wins.
This means that you can specify active profiles in `application.properties` and then **replace** them by using the command line switch.

|  |  |
| --- | --- |
|  | See [the “Externalized Configuration”](external-config.html#features.external-config.order) for more details on the order in which property sources are considered. |

|  |  |
| --- | --- |
|  | By default, profile names in Spring Boot may contain letters, numbers, or permitted characters (`-`, `_`, `.`, `+`, `@`). In addition, they can only start and end with a letter or number.  This restriction helps to prevent common parsing issues. if, however, you prefer more flexible profile names you can set `spring.profiles.validate` to `false` in your `application.properties` or `application.yaml` file:  * Properties * YAML  ``` spring.profiles.validate=false ```  ``` spring:   profiles:     validate: false ``` |

## Adding Active Profiles

Sometimes, it is useful to have properties that **add** to the active profiles rather than replace them.
The `spring.profiles.include` property can be used to add active profiles on top of those activated by the `spring.profiles.active` property.
The [`SpringApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/SpringApplication.html) entry point also has a Java API for setting additional profiles.
See the `setAdditionalProfiles()` method in [`SpringApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/SpringApplication.html).

For example, when an application with the following properties is run, the common and local profiles will be activated even when it runs using the `--spring.profiles.active` switch:

* Properties
* YAML

```
spring.profiles.include[0]=common
spring.profiles.include[1]=local
```

```
spring:
  profiles:
    include:
      - "common"
      - "local"
```

|  |  |
| --- | --- |
|  | Included profiles are added before any `spring.profiles.active` profiles. |

|  |  |
| --- | --- |
|  | The `spring.profiles.include` property is processed for each property source, as such the usual [complex type merging rules](external-config.html#features.external-config.typesafe-configuration-properties.merging-complex-types) for lists do not apply. |

|  |  |
| --- | --- |
|  | Similar to `spring.profiles.active`, `spring.profiles.include` can only be used in non-profile-specific documents. This means it cannot be included in [profile specific files](external-config.html#features.external-config.files.profile-specific) or [documents activated](external-config.html#features.external-config.files.activation-properties) by `spring.config.activate.on-profile`. |

Profile groups, which are described in the [next section](#features.profiles.groups) can also be used to add active profiles if a given profile is active.

## Profile Groups

Occasionally the profiles that you define and use in your application are too fine-grained and become cumbersome to use.
For example, you might have `proddb` and `prodmq` profiles that you use to enable database and messaging features independently.

To help with this, Spring Boot lets you define profile groups.
A profile group allows you to define a logical name for a related group of profiles.

For example, we can create a `production` group that consists of our `proddb` and `prodmq` profiles.

* Properties
* YAML

```
spring.profiles.group.production[0]=proddb
spring.profiles.group.production[1]=prodmq
```

```
spring:
  profiles:
    group:
      production:
      - "proddb"
      - "prodmq"
```

Our application can now be started using `--spring.profiles.active=production` to activate the `production`, `proddb` and `prodmq` profiles in one hit.

|  |  |
| --- | --- |
|  | Similar to `spring.profiles.active` and `spring.profiles.include`, `spring.profiles.group` can only be used in non-profile-specific documents. This means it cannot be included in [profile specific files](external-config.html#features.external-config.files.profile-specific) or [documents activated](external-config.html#features.external-config.files.activation-properties) by `spring.config.activate.on-profile`. |

## Programmatically Setting Profiles

You can programmatically set active profiles by calling `SpringApplication.setAdditionalProfiles(…​)` before your application runs.
It is also possible to activate profiles by using Spring’s [`ConfigurableEnvironment`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/core/env/ConfigurableEnvironment.html) interface.

## Profile-specific Configuration Files

Profile-specific variants of both `application.properties` (or `application.yaml`) and files referenced through [`@ConfigurationProperties`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/context/properties/ConfigurationProperties.html) are considered as files and loaded.
See [Profile Specific Files](external-config.html#features.external-config.files.profile-specific) for details.