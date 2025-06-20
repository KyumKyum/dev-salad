package com.devtrends

import kotlinx.coroutines.runBlocking

fun main() = runBlocking {
    val bot = Scraper();
    val results = bot.fetch();

    results.forEach { result ->
        println("====================")
        println(result.title)
        println(result.desc)
        println(result.src)
        println(result.url)
        println(result.scrapedAt)
    }
}