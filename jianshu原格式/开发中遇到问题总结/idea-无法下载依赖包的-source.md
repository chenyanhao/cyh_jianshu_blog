好像是 idea 的 maven 插件的问题，用 maven 命令就好了。解决方法如下。

下载所有POM里的依赖包的source
mvn dependency:resolve -Dclassifier=sources

下载POM文件依赖的包的source
mvn dependency:sources

下载POM文件依赖的包的javadoc
mvn dependency:resolve -Dclassifier=javadoc

下载指定依赖包（artifactId）的source
mvn dependency:sources -DincludeArtifactIds=guava
