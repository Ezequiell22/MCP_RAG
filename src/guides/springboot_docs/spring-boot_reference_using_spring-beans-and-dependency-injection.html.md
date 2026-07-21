Search

# Spring Beans and Dependency Injection

You are free to use any of the standard Spring Framework techniques to define your beans and their injected dependencies.
We generally recommend using constructor injection to wire up dependencies and [`@ComponentScan`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/ComponentScan.html) to find beans.

If you structure your code as suggested above (locating your application class in a top package), you can add [`@ComponentScan`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/context/annotation/ComponentScan.html) without any arguments or use the [`@SpringBootApplication`](https://docs.spring.io/spring-boot/4.1.0/api/java/org/springframework/boot/autoconfigure/SpringBootApplication.html) annotation which implicitly includes it.
All of your application components ([`@Component`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Component.html), [`@Service`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Service.html), [`@Repository`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Repository.html), [`@Controller`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Controller.html), and others) are automatically registered as Spring Beans.

The following example shows a [`@Service`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/stereotype/Service.html) Bean that uses constructor injection to obtain a required `RiskAssessor` bean:

* Java
* Kotlin

```
import org.springframework.stereotype.Service;

@Service
public class MyAccountService implements AccountService {

	private final RiskAssessor riskAssessor;

	public MyAccountService(RiskAssessor riskAssessor) {
		this.riskAssessor = riskAssessor;
	}

	// ...

}
```

```
import org.springframework.stereotype.Service

@Service
class MyAccountService(private val riskAssessor: RiskAssessor) : AccountService
```

If a bean has more than one constructor, you will need to mark the one you want Spring to use with [`@Autowired`](https://docs.spring.io/spring-framework/docs/7.0.x/javadoc-api/org/springframework/beans/factory/annotation/Autowired.html):

* Java
* Kotlin

```
import java.io.PrintStream;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class MyAccountService implements AccountService {

	private final RiskAssessor riskAssessor;

	private final PrintStream out;

	@Autowired
	public MyAccountService(RiskAssessor riskAssessor) {
		this.riskAssessor = riskAssessor;
		this.out = System.out;
	}

	public MyAccountService(RiskAssessor riskAssessor, PrintStream out) {
		this.riskAssessor = riskAssessor;
		this.out = out;
	}

	// ...

}
```

```
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.stereotype.Service
import java.io.PrintStream

@Service
class MyAccountService : AccountService {

	private val riskAssessor: RiskAssessor

	private val out: PrintStream

	@Autowired
	constructor(riskAssessor: RiskAssessor) {
		this.riskAssessor = riskAssessor
		out = System.out
	}

	constructor(riskAssessor: RiskAssessor, out: PrintStream) {
		this.riskAssessor = riskAssessor
		this.out = out
	}

	// ...

}
```

|  |  |
| --- | --- |
|  | Notice how using constructor injection lets the `riskAssessor` field be marked as `final`, indicating that it cannot be subsequently changed. |