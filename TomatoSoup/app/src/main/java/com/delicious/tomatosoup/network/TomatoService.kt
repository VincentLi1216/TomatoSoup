package com.delicious.tomatosoup.network

import retrofit2.http.GET

interface TomatoService {
    @GET("static")
    suspend fun getDates(): String
}