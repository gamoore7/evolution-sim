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
    HttpServer::new(|| {
        App::new()
            .service(index)
            .service(run)
            .service(load)
    })
    .bind(("0.0.0.0", 8000))?
    .run()
    .await
}
