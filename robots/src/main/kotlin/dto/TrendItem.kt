package com.devtrends.dto

import java.util.Date

data class TrendItem (
    val src: String,
    val title: String,
    val url: String,
    val desc: String,
    val scrapedAt: Date
)