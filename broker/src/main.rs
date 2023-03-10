use std::env;

use serde::Deserialize;
use actix_web::{HttpServer, HttpResponse, App, get, post, web, Responder, Result};
use deadpool_redis::{redis::cmd, Config, Runtime, CreatePoolError};

#[derive(Deserialize)]
struct SimArgs {
    name: String,
}

fn redis_new() -> Result<deadpool_redis::Pool, CreatePoolError> {
    let url = env::var("REDIS").expect("Required: Broker redis url");
    let cfg = Config::from_url(url);
    let runtime = Some(Runtime::Tokio1);

    cfg.create_pool(runtime)
}

#[post("/load")]
async fn load() -> impl Responder {
    "Broker load route."
}

#[post("/run")]
async fn run(pool: web::Data<deadpool_redis::Pool>, json: web::Json<SimArgs>) -> impl Responder {
    println!("{}", json.name);
    let mut conn = pool.get().await.unwrap();

    match cmd("SET")
        .arg(&["test-key", &json.name])
        .query_async::<_, ()>(&mut conn)
        .await {
            Ok(_) => HttpResponse::Ok(),
            Err(_) => HttpResponse::BadRequest(),
        }
}

#[get("/")]
async fn index() -> impl Responder {
    "Broker index route."
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    
    let host = env::var("HOST")
        .expect("Required: Broker server host.");

    let port = env::var("PORT")
        .expect("Required: Broker server port.")
        .parse::<u16>()
        .expect("Required: Broker server port must be u16.");

    // TODO: Actix middleware logging.
    env::set_var("RUST_LOG", "debug");
    env_logger::init();

    let pool = web::Data::new(redis_new().unwrap());
    HttpServer::new(move || {
        App::new()
            .app_data(pool.clone())
            .service(index)
            .service(run)
            .service(load)
    })
    .bind((host, port))?
    .run()
    .await
}
