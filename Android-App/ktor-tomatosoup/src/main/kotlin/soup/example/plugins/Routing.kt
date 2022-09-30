package soup.example.plugins

import io.ktor.http.*
import io.ktor.serialization.gson.*
import io.ktor.server.application.*
import io.ktor.server.plugins.contentnegotiation.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*

fun Application.configureRouting() {
    install(ContentNegotiation) {
        gson {
        }
    }
    routing {
        get("/") {
            call.respond(mapOf("message" to "HELLO WORLD!"))
        }

    }
}
