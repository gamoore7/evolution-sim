use std::env;

use actix_web::{HttpServer, HttpRequest, App, get, post, Responder};

#[post("/load")]
async fn load() -> impl Responder {
    "Broker load route."
}

#[get("/run")]
async fn run() -> impl Responder {
    "Broker run route."
}

#[get("/")]
async fn index(req: HttpRequest) -> impl Responder {
    println!("{:?}", req);
    "Broker index route."
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let port = env::var("PORT")
        .expect("Required: Broker server port.")
        .parse::<u16>()
        .expect("Required: Broker server port must be u16.");

    HttpServer::new(|| {
        App::new()
            .service(index)
            .service(run)
            .service(load)
    })
    .bind(("0.0.0.0", port))?
    .run()
    .await
}
