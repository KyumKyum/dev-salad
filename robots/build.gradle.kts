val kotlin_version: String by project
val logback_version: String by project

plugins {
    kotlin("jvm") version "2.1.10"
    id("io.ktor.plugin") version "3.2.0"
    id("org.jetbrains.kotlin.plugin.serialization") version "2.1.10"
}

group = "com.devtrends"
version = "0.0.1"

application {
    mainClass = "com.devtrends.MainKt"
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("io.ktor:ktor-client-core")
    implementation("io.ktor:ktor-serialization-kotlinx-json")
    implementation("io.ktor:ktor-client-cio")
    implementation("org.jsoup:jsoup:1.15.4")
    implementation("ch.qos.logback:logback-classic:$logback_version")
    testImplementation("org.jetbrains.kotlin:kotlin-test-junit:$kotlin_version")
}
