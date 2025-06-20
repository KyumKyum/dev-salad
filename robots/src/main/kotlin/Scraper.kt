package com.devtrends

import com.devtrends.dto.TrendItem
import io.ktor.client.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import kotlinx.coroutines.*
import kotlinx.serialization.json.*
import org.jsoup.Jsoup
import org.jsoup.parser.Parser
import java.net.URLEncoder
import java.util.*


class Scraper {
    private val client = HttpClient()

    private suspend fun fetchGitHubTrending(): List<TrendItem>  = coroutineScope {
        val doc = Jsoup.connect("https://github.com/trending").get()
        doc.select("article.Box-row").map { el ->
            val href  = el.selectFirst("h2 a")!!.attr("href")
            val title = el.selectFirst("h2")!!.text().trim()
            val desc  = el.selectFirst("p")?.text()?.trim()
            TrendItem("GitHub Trending", title, "https://github.com$href", desc ?: "", Date())
        }
    }

    private suspend fun fetchReddit(): List<TrendItem> = coroutineScope {
        val subs = listOf("programming", "coding", "webdev", "frontend", "backend")

        subs.map { subreddit ->
            async {
                val url = "https://www.reddit.com/r/$subreddit/top/.json?t=day&limit=10"
                val jsonText: String = client
                    .get(url) {
                        header("User-Agent", "TrendScraperBot/1.0")
                    }
                    .bodyAsText()

                val root = Json.parseToJsonElement(jsonText).jsonObject
                val children = root["data"]!!.jsonObject["children"]!!.jsonArray


                children.map { child ->
                    val d = child.jsonObject["data"]!!.jsonObject

                    val rawDesc = d["selftext"]?.jsonPrimitive?.contentOrNull
                    val description = rawDesc
                        ?.let { Jsoup.parse(it).text() }
                        .orEmpty()

                    TrendItem(
                        "Reddit/r/$subreddit",
                        d["title"]!!.jsonPrimitive.content,
                        "https://reddit.com" + d["permalink"]!!.jsonPrimitive.content,
                        description,
                        Date()
                    )
                }
            }
        }.awaitAll().flatten()

    }

    private suspend fun fetchDevTo(): List<TrendItem> {
        val tag = "webdev"
        val encoded = withContext(Dispatchers.IO) {
            URLEncoder.encode(tag, "UTF-8")
        }
        val xml = client.get("https://dev.to/feed/tag/${encoded}")
        val doc = Jsoup.parse(xml.bodyAsText(), "", Parser.xmlParser())
        return doc.select("item").map { item ->
            val title = item.selectFirst("title")!!.text()
            val link  = item.selectFirst("link")!!.text()
            val desc  = item.selectFirst("description")?.text()

            val description = desc
                ?.let { Jsoup.parse(it).text() }
                .orEmpty()

            TrendItem("Dev.to", title, link, description, Date())
        }
    }

    private suspend fun fetchProductHunt(): List<TrendItem> = coroutineScope {
        val xml = client
            .get("https://www.producthunt.com/feed")
            .bodyAsText()

        val doc = Jsoup.parse(xml, "", Parser.xmlParser())
        doc.select("item").map { item ->
            val title       = item.selectFirst("title")?.text().orEmpty()
            val link        = item.selectFirst("link")?.text().orEmpty()
            val desc        = item.selectFirst("description")?.text()

            TrendItem(
                "Product Hunt",
                title,
                link,
                desc ?: "",
                Date()
            )
        }
    }

    private suspend fun fetchTechCrunch(): List<TrendItem> = coroutineScope {
        val xml = client
            .get("https://techcrunch.com/feed/")
            .bodyAsText()

        val doc = Jsoup.parse(xml, "", Parser.xmlParser())
        doc.select("item").map { item ->
            val title       = item.selectFirst("title")?.text().orEmpty()
            val link        = item.selectFirst("link")?.text().orEmpty()
            val desc        = item.selectFirst("description")?.text()

            TrendItem(
                "TechCrunch",
                title,
                link,
                desc ?: "",
                Date()
            )
        }
    }

    private suspend fun fetchHackerNewsTop(): List<TrendItem> = coroutineScope {
        val idsJson: String = client
            .get("https://hacker-news.firebaseio.com/v0/topstories.json")
            .bodyAsText()

        // Decode
        val ids: List<Long> = Json.decodeFromString(idsJson)

        ids.take(20).map { id ->
            async {
                val story = client.get("https://hacker-news.firebaseio.com/v0/item/$id.json").bodyAsText()
                val json  = Json.parseToJsonElement(story).jsonObject

                val rawDesc = json["text"]?.jsonPrimitive?.content ?: ""
                val description = rawDesc
                    .let { Jsoup.parse(it).text() }
                    .orEmpty()
                TrendItem(
                    "HackerNews",
                    json["title"]!!.jsonPrimitive.content,
                    json["url"]!!.jsonPrimitive.content,
                    description,
                    Date()
                )
            }
        }.awaitAll()
    }

    suspend fun fetch(): List<TrendItem> = coroutineScope {
        listOf(
            async { fetchReddit() },
            async { fetchDevTo() },
            async { fetchHackerNewsTop() },
            async { fetchGitHubTrending() },
            async { fetchProductHunt() },
            async { fetchTechCrunch() },
        ).awaitAll().flatten()
    }
}