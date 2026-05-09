#!/bin/sh
# Gradle wrapper for Termux/CI
GRADLE_VERSION="8.5"
GRADLE_HOME="$HOME/.gradle/wrapper/dists/gradle-${GRADLE_VERSION}-bin"

if [ ! -d "$GRADLE_HOME" ]; then
    echo "Downloading Gradle ${GRADLE_VERSION}..."
    wget -q "https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip"
    unzip -q "gradle-${GRADLE_VERSION}-bin.zip" -d "$HOME/.gradle/wrapper/"
    rm "gradle-${GRADLE_VERSION}-bin.zip"
fi

exec "$GRADLE_HOME/gradle-${GRADLE_VERSION}/bin/gradle" "$@"
