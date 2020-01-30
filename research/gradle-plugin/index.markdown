---
title: "Gradle Plugin Sample"
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

