package com.delicious.tomatosoup.network

import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.scalars.ScalarsConverterFactory

private const val BASE_URL = "http://114.32.43.46"
class Repository {
    private val retrofit: Retrofit

    init {
        val builder = OkHttpClient.Builder()

        retrofit = Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(ScalarsConverterFactory.create())
            .client(builder.build())
            .build()
    }
    private val tomatoService = retrofit.create(TomatoService::class.java)
    suspend fun getDates() = tomatoService.getDates()
}