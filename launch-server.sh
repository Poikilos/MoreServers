#!/bin/bash
cat > /dev/null <<END
Java flags below are generated by:
https://docs.papermc.io/misc/tools/start-script-gen
(generic one is at <https://docs.papermc.io/paper/aikars-flags>)

Requires Java 17, but recommends 21
(<https://docs.papermc.io/misc/java-install>):
sudo rpm --import https://yum.corretto.aws/corretto.key
sudo curl -Lo /etc/yum.repos.d/corretto.repo https://yum.corretto.aws/corretto.repo
sudo dnf -y install java-21-amazon-corretto-devel

Choose a version:
sudo update-alternatives --config java
- choose 21 such as /usr/lib/jvm/java-21-amazon-corretto/bin/java
- verify by running:
  `java -version`
  (Should show version 21)

<https://docs.papermc.io/paper/getting-started> says:
Paper Version   Recommended Java Version
1.8 to 1.11     Java 8
1.12 to 1.16.4  Java 11
1.16.5          Java 16
1.17.1-1.18.1+  Java 21
END
JAVA="`command -v java`"
# JAVA=/usr/lib/jvm/java-11-openjdk-amd64/bin/java
# JAVA=/usr/lib/jvm/java-21-openjdk-amd64/bin/java
amazon_java_21=/usr/lib/jvm/java-21-amazon-corretto/bin/java

if [ ! -f "$JAVA" ]; then
    >&2 printf "java is not in your environment's path..."
    if [ ! -f "$amazon_java_21" ]; then
        >&2 echo "Error: No \"$amazon_java_21\" was found either."
        exit 1
    fi
    echo "detected \"$amazon_java_21\""
    JAVA="$amazon_java_21"
else
    JAVA="`realpath $JAVA`"
    echo "using \"$JAVA\""
fi
# JAR=server.jar
# JAR=paper-1.20.1-196.jar
# JAR=paper-1.20.4-462.jar
JAR=`ls paper-1.*.jar`
if [ ! -f "$JAR" ]; then
    >&2 echo "Error: There is no $JAR in `pwd`"
    exit 1
fi
# $JAVA -Xmx6144M -Xms6144M -XX:+AlwaysPreTouch -XX:+DisableExplicitGC -XX:+ParallelRefProcEnabled -XX:+PerfDisableSharedMem -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1HeapRegionSize=8M -XX:G1HeapWastePercent=5 -XX:G1MaxNewSizePercent=40 -XX:G1MixedGCCountTarget=4 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1NewSizePercent=30 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:G1ReservePercent=20 -XX:InitiatingHeapOccupancyPercent=15 -XX:MaxGCPauseMillis=200 -XX:MaxTenuringThreshold=1 -XX:SurvivorRatio=32 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -jar $JAR --nogui
$JAVA -Xmx6144M -Xms3072M -XX:+AlwaysPreTouch -XX:+DisableExplicitGC -XX:+ParallelRefProcEnabled -XX:+PerfDisableSharedMem -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1HeapRegionSize=8M -XX:G1HeapWastePercent=5 -XX:G1MaxNewSizePercent=40 -XX:G1MixedGCCountTarget=4 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1NewSizePercent=30 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:G1ReservePercent=20 -XX:InitiatingHeapOccupancyPercent=15 -XX:MaxGCPauseMillis=200 -XX:MaxTenuringThreshold=1 -XX:SurvivorRatio=32 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -jar $JAR --nogui
read -n 1 -s -r -p "Press any key to continue"
