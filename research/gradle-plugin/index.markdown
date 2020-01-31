---
title: "Gradle Plugin Notes"
date: 2020-01-29T22:47:17-08:00
draft: false
toc: false
comments: false
categories:
- Research
tags:
- Java
- Gradle
wip: false
snippet: "How to create a sample custom Gradle plugin in Java that reads parameters the command line."
---

To add a plugin to an existing Java project we can add it under `buildSrc`. This
way we can use it in the project `build.gradle` without hassle.

* https://www.vogella.com/tutorials/Gradle/article.html#apply-the-java-gradle-plugin-plug-in


Inside the `buildSrc` directory, we will need to create a separate Java project
with all the bells and whistles. This means we have to create another
`build.gradle` inside.

{{< codecaption title="buildSrc/build.gradle" lang="java" >}}
plugins {
    id 'java-gradle-plugin'
}

gradlePlugin {
    plugins {
        thisDoesntMatter {
            id = 'mypluginid'
            implementationClass = 'myplugin.MyPlugin'
        }
    }
}

sourceSets {
    main {
        java {
            srcDir '.'
        }
    }
}

repositories {
    mavenCentral()
    // In case we want to use 3rd party packages in the plugin.
}

dependencies {
    // No need to add gradleApi() here, because it is applied by the
    // 'java-gradle-plugin' plug-in

    // Add your dependencies here.
}
{{< /codecaption >}}

We have pointed `srcDir` to `buildSrc` so we have to create our files here.
`implementationClass` is set to `myplugin.MyPlugin` meaning that we have to
create a package named `myplugin` here and a class `MyPlugin`.

{{< codecaption title="buildSrc/MyPlugin.java" lang="java" >}}
package myplugin;

import org.gradle.api.Plugin;
import org.gradle.api.Project;

public class MyPlugin implements Plugin<Project> {

    @Override
    public void apply(Project project) {
        // Create a task named "install"
        project.getTasks().create("install", Installation.class);
    }
}
{{< /codecaption >}}

Here we create a task named `install` which runs another class called
`Installation`. `Installation` is part of the same package in this
implementation. This means we need to create a file `Installation.java` to have
the task.

{{< codecaption title="buildSrc/Installation.java" lang="java" >}}
package myplugin;

import org.gradle.api.DefaultTask;
import org.gradle.api.tasks.TaskAction;
import org.gradle.api.tasks.options.Option;

public class Installation extends DefaultTask {

    String projectPath;

    @Option(option="project", description="path to the project")
    public void setPath(String path) {
        projectPath = path;
    }

    @TaskAction
    public void myTask() {
        System.out.printf("Option value: %s", projectPath);
    }
}
{{< /codecaption >}}

The interesting part of the code is the `Option`. We can use this to get
parameters/switch from the command line. In this case, we are creating an option
named `project` and we will store it in `projectPath`. Now we can do what we
want with `projectPath`.

* https://docs.gradle.org/current/userguide/custom_tasks.html#sec:declaring_and_using_command_line_options

Our plugin is now ready. Now we need to add it to the project `build.gradle`
which is inside the root directory of the project. Add this line to it:

```java
// The id here is the same as
apply plugin: 'mypluginid' in `buildSrc/build.gradle`.
```

Now we can call this task with a command line parameter from the project
directory. The command line parameter is passed a `--project=value` or
`--project value`.

```
gradlew install --project=cli-value

> Task :install
Option value: cli-value

BUILD SUCCESSFUL in 956ms
1 actionable task: 1 executed
```

Note that if we pass a parameter that is not defined, we get an error in this
setup.

```
gradlew install --param value

FAILURE: Build failed with an exception.

* What went wrong:
Problem configuring task :install from command line.
> Unknown command-line option '--param'.

* Try:
Run gradlew help --task :install to get task usage details.
Run with --stacktrace option to get the stack trace.
Run with --info or --debug option to get more log output.
Run with --scan to get full insights.

* Get more help at https://help.gradle.org
BUILD FAILED in 837ms
```

## Using Groovy in build.gradle
It's also possible to write the task in `build.gradle` instead.

### Executing Shell Commands
To execute commands per OS (Windows needs `cmd.exe /c`) we can use:

Source: https://stackoverflow.com/a/54315477

```groovy
private static Iterable<String> osAdaptiveCommand(String... commands) {
    def newCommands = []
    if (Os.isFamily(Os.FAMILY_WINDOWS)) {
        newCommands = ['cmd', '/c']
    }

    newCommands.addAll(commands)
    return newCommands
}
```

Now we can create a task like this:

```groovy
task executeCommand(type: Exec) {    
    commandLine osAdaptiveCommand('aws', 'ecr', 'get-login', '--no-include-email')
}
```

### Defining Multiple commandLines in One Task
We cannot have multiple `commandLine`s in the same task without `exec`s.

```groovy
task whatever() {

    commandLine 'cmd.exe', '/c', 'dir'

    commandLine osAdaptiveCommand('whatever.exe', '--switch')
}
```

Based on my observation, only the last one will be executed. Instead put each
one in a separate `exec`. See below.

### Defining Multiple execs in One Task
When defining multiple `commandLine`s, we need to make sure they are not
executed in the configuration phase. I am not sure how it works but if you
create a task like this, it will be executed every time any task is executed.
Meaning the task is executed in the configuration phase.

```groovy
task whatever() {
    exec {
        // optional workingDir 'path/to/workingdir`
        commandLine 'cmd.exe', '/c', 'dir'
    }
    exec {
        commandLine osAdaptiveCommand('whatever.exe', '--switch')
    }
}
```

Both of these execs will run whenever any task is executed.

The solution is to put it in `doLast`:

```groovy
task whatever() {
    doLast {
        exec {
        // optional workingDir 'path/to/workingdir`
            commandLine 'cmd.exe', '/c', 'dir'
        }
        exec {
            commandLine osAdaptiveCommand('whatever.exe', '--switch')
        }
    }
}
```

### Accessing Command Line Parameters
If the command line parameter is always provided. Access it with `$param` and
pass it to the Gradle task like this `gradle taskname -Pparam=value`.

1. Some parameters are reserved and already have values like `$path` and
   `$project`.
2. If the parameter is not provided to the task an exception occurs.
    * `Could not get unknown property 'param' for task ':whatever' of type org.gradle.api.DefaultTask.` 

```groovy
task whatever() {
    doLast {
        println "param = $param" // Note that we have to use double-quotes.
    }
}
// Run `gradle whatever -Pparam=value`
```

A better way is to use `project.hasProperty('param')` to check if the project
has such a property first.

* https://docs.gradle.org/current/javadoc/org/gradle/api/Project.html#hasProperty-java.lang.String-

```groovy
task whatever() {
    doLast {
        if (project.hasProperty('param')) {
            println "param = $param"
        } else {
            // Can also use else.
        }
    }
}
```

### Get Current Working directory

* `System.properties['user.dir']`
    * https://stackoverflow.com/a/6492287

To get the script path:

* scriptFile = getClass().protectionDomain.codeSource.location.path
    * https://stackoverflow.com/a/1169196

